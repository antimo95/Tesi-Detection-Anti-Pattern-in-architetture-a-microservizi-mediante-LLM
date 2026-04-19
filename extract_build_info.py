#!/usr/bin/env python3
"""
Estrae informazioni dai file di build (pom.xml e build.gradle) di un progetto microservizi. 
Genera un unico file JSON con dati grezzi aggregati per analisi LLM. 

Uso:
    python extract_build_info. py <path_progetto> [-o output. json]
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json
import argparse
import re
from datetime import datetime


def parse_pom(pom_path, project_root):
    """Estrae tutte le informazioni da un pom.xml."""
    
    try:
        tree = ET.parse(pom_path)
        root = tree.getroot()
        
        # Gestione namespace Maven
        ns = {'m': 'http://maven.apache.org/POM/4.0.0'}
        has_ns = root.tag.startswith('{')
        
        def find_text(element, path):
            if element is None:
                return None
            if has_ns:
                ns_path = '/'.join([f'm:{p}' for p in path. split('/')])
                el = element.find(ns_path, ns)
            else:
                el = element.find(path)
            return el.text. strip() if el is not None and el.text else None
        
        def find_all(element, path):
            if element is None:
                return []
            if has_ns:
                ns_path = '/'. join([f'm:{p}' for p in path.split('/')])
                return element.findall(ns_path, ns)
            return element.findall(path)
        
        info = {
            "file":  str(pom_path. relative_to(project_root)),
            "type": "maven",
            "groupId": find_text(root, "groupId"),
            "artifactId":  find_text(root, "artifactId"),
            "version": find_text(root, "version"),
            "packaging":  find_text(root, "packaging"),
            "name": find_text(root, "name"),
            "description":  find_text(root, "description")
        }
        
        # Parent
        parent_el = root.find('m:parent', ns) if has_ns else root. find('parent')
        if parent_el is not None: 
            info["parent"] = {
                "groupId": find_text(parent_el, "groupId"),
                "artifactId":  find_text(parent_el, "artifactId"),
                "version": find_text(parent_el, "version")
            }
            # Eredita groupId/version da parent se mancanti
            if not info["groupId"]:
                info["groupId"] = info["parent"]["groupId"]
            if not info["version"]: 
                info["version"] = info["parent"]["version"]
        
        # Modules
        modules = find_all(root, "modules/module")
        if modules:
            info["modules"] = [m.text for m in modules if m.text]
        
        # Properties
        props_el = root.find('m:properties', ns) if has_ns else root.find('properties')
        if props_el is not None:
            info["properties"] = {}
            for prop in props_el: 
                tag = re.sub(r'\{.*\}', '', prop.tag)
                if prop.text:
                    info["properties"][tag] = prop. text. strip()
        
        # Dependencies
        deps = find_all(root, "dependencies/dependency")
        if deps:
            info["dependencies"] = []
            for dep in deps:
                info["dependencies"].append({
                    "groupId": find_text(dep, "groupId"),
                    "artifactId":  find_text(dep, "artifactId"),
                    "version": find_text(dep, "version"),
                    "scope": find_text(dep, "scope")
                })
        
        # Dependency Management
        dep_mgmt = find_all(root, "dependencyManagement/dependencies/dependency")
        if dep_mgmt:
            info["dependencyManagement"] = []
            for dep in dep_mgmt:
                info["dependencyManagement"]. append({
                    "groupId": find_text(dep, "groupId"),
                    "artifactId": find_text(dep, "artifactId"),
                    "version": find_text(dep, "version"),
                    "type": find_text(dep, "type"),
                    "scope": find_text(dep, "scope")
                })
        
        # Plugins
        plugins = find_all(root, "build/plugins/plugin")
        if plugins: 
            info["plugins"] = []
            for plugin in plugins: 
                info["plugins"].append({
                    "groupId":  find_text(plugin, "groupId"),
                    "artifactId": find_text(plugin, "artifactId"),
                    "version":  find_text(plugin, "version")
                })
        
        # Repositories
        repos = find_all(root, "repositories/repository")
        if repos:
            info["repositories"] = []
            for repo in repos:
                info["repositories"].append({
                    "id":  find_text(repo, "id"),
                    "url": find_text(repo, "url")
                })
        
        # Profiles
        profiles = find_all(root, "profiles/profile")
        if profiles: 
            info["profiles"] = [find_text(p, "id") for p in profiles]
        
        return info
        
    except ET.ParseError as e:
        return {
            "file": str(pom_path. relative_to(project_root)),
            "type": "maven",
            "parse_error": str(e)
        }
    except Exception as e:
        return {
            "file": str(pom_path.relative_to(project_root)),
            "type": "maven",
            "error": str(e)
        }


def parse_gradle(gradle_path, project_root):
    """Estrae informazioni da un build. gradle (parsing semplificato)."""
    
    try:
        content = gradle_path. read_text(encoding='utf-8')
        
        info = {
            "file": str(gradle_path.relative_to(project_root)),
            "type": "gradle",
            "raw_content_lines": len(content.splitlines())
        }
        
        # Plugins
        plugins = re.findall(r"id\s*['\"]([^'\"]+)['\"]", content)
        plugins += re.findall(r"apply\s+plugin:\s*['\"]([^'\"]+)['\"]", content)
        if plugins:
            info["plugins"] = list(set(plugins))
        
        # Group e Version
        group_match = re. search(r"group\s*=\s*['\"]([^'\"]+)['\"]", content)
        if group_match:
            info["group"] = group_match.group(1)
            
        version_match = re. search(r"version\s*=\s*['\"]([^'\"]+)['\"]", content)
        if version_match:
            info["version"] = version_match.group(1)
        
        # Source Compatibility
        java_match = re.search(r"sourceCompatibility\s*=\s*['\"]? ([^'\"\s]+)", content)
        if java_match: 
            info["sourceCompatibility"] = java_match.group(1)
        
        # Dependencies (cattura tutte le forme comuni)
        deps = []
        
        # Formato: implementation 'group:artifact:version'
        dep_patterns = [
            r"(implementation|compile|api|runtimeOnly|compileOnly|testImplementation|testCompile)\s*['\"]([^'\"]+)['\"]",
            r"(implementation|compile|api|runtimeOnly|compileOnly|testImplementation|testCompile)\s*\(?\s*['\"]([^'\"]+)['\"]",
        ]
        
        for pattern in dep_patterns:
            matches = re.findall(pattern, content)
            for scope, dep in matches:
                deps.append({
                    "configuration": scope,
                    "coordinates": dep
                })
        
        # Formato: implementation group:  'x', name: 'y', version: 'z'
        map_deps = re.findall(
            r"(implementation|compile|api|runtimeOnly|compileOnly|testImplementation|testCompile)\s+group:\s*['\"]([^'\"]+)['\"],\s*name:\s*['\"]([^'\"]+)['\"](? : ,\s*version:\s*['\"]([^'\"]+)['\"])?",
            content
        )
        for scope, group, name, version in map_deps: 
            coord = f"{group}:{name}"
            if version: 
                coord += f":{version}"
            deps.append({
                "configuration":  scope,
                "coordinates": coord
            })
        
        if deps:
            info["dependencies"] = deps
        
        # Repositories
        repos = re.findall(r"(mavenCentral|jcenter|google|mavenLocal)\s*\(\s*\)", content)
        maven_urls = re.findall(r"maven\s*\{\s*url\s*['\"]([^'\"]+)['\"]", content)
        
        if repos or maven_urls: 
            info["repositories"] = repos + maven_urls
        
        # Spring Boot version (se presente)
        spring_boot = re.search(r"org\.springframework\.boot['\"]?\s*version\s*['\"]([^'\"]+)['\"]", content)
        if spring_boot:
            info["springBootVersion"] = spring_boot.group(1)
        
        # Subprojects/Allprojects (indica multi-module)
        if "subprojects" in content:
            info["hasSubprojects"] = True
        if "allprojects" in content:
            info["hasAllprojects"] = True
            
        return info
        
    except Exception as e:
        return {
            "file": str(gradle_path.relative_to(project_root)),
            "type": "gradle",
            "error": str(e)
        }


def parse_settings_gradle(settings_path, project_root):
    """Estrae informazioni da settings.gradle."""
    
    try: 
        content = settings_path.read_text(encoding='utf-8')
        
        info = {
            "file": str(settings_path. relative_to(project_root)),
            "type": "gradle-settings"
        }
        
        # Root project name
        root_name = re.search(r"rootProject\. name\s*=\s*['\"]([^'\"]+)['\"]", content)
        if root_name: 
            info["rootProjectName"] = root_name.group(1)
        
        # Included modules
        includes = re.findall(r"include\s*['\"]([^'\"]+)['\"]", content)
        includes += re.findall(r"include\s*\(([^)]+)\)", content)
        
        if includes: 
            # Pulisci i moduli
            modules = []
            for inc in includes:
                # Gestisce include('a', 'b', 'c')
                parts = re.findall(r"['\"]([^'\"]+)['\"]", inc)
                if parts:
                    modules.extend(parts)
                else:
                    modules.append(inc. strip())
            info["modules"] = modules
        
        return info
        
    except Exception as e: 
        return {
            "file": str(settings_path. relative_to(project_root)),
            "type": "gradle-settings",
            "error": str(e)
        }


def extract_all(project_path):
    """Estrae tutte le informazioni di build dal progetto."""
    
    root = Path(project_path).resolve()
    
    result = {
        "metadata": {
            "project_path": str(root),
            "project_name": root. name,
            "extraction_timestamp": datetime. now().isoformat(),
            "extractor_version": "1.0.0"
        },
        "build_files": [],
        "statistics": {
            "maven_files": 0,
            "gradle_files": 0,
            "total_modules": 0
        }
    }
    
    # Trova e parsa tutti i pom.xml
    for pom in root.rglob("pom.xml"):
        # Salta directory target, build, .git
        if any(part in pom.parts for part in ['target', 'build', '.git', 'node_modules']):
            continue
        info = parse_pom(pom, root)
        result["build_files"]. append(info)
        result["statistics"]["maven_files"] += 1
    
    # Trova e parsa tutti i build.gradle
    for gradle in root.rglob("build. gradle"):
        if any(part in gradle.parts for part in ['target', 'build', '.git', 'node_modules']):
            continue
        info = parse_gradle(gradle, root)
        result["build_files"].append(info)
        result["statistics"]["gradle_files"] += 1
    
    # Trova e parsa build.gradle.kts (Kotlin DSL)
    for gradle_kts in root. rglob("build.gradle.kts"):
        if any(part in gradle_kts.parts for part in ['target', 'build', '. git', 'node_modules']):
            continue
        info = parse_gradle(gradle_kts, root)
        info["type"] = "gradle-kts"
        result["build_files"].append(info)
        result["statistics"]["gradle_files"] += 1
    
    # Trova e parsa settings.gradle
    for settings in root. rglob("settings.gradle"):
        if any(part in settings.parts for part in ['target', 'build', '.git', 'node_modules']):
            continue
        info = parse_settings_gradle(settings, root)
        result["build_files"].append(info)
    
    # settings.gradle.kts
    for settings_kts in root. rglob("settings.gradle.kts"):
        if any(part in settings_kts.parts for part in ['target', 'build', '. git', 'node_modules']):
            continue
        info = parse_settings_gradle(settings_kts, root)
        info["type"] = "gradle-settings-kts"
        result["build_files"].append(info)
    
    # Ordina per path
    result["build_files"].sort(key=lambda x:  x["file"])
    
    # Conta moduli
    for bf in result["build_files"]:
        if bf. get("modules"):
            result["statistics"]["total_modules"] += len(bf["modules"])
    
    return result


def main():
    parser = argparse. ArgumentParser(
        description="Estrae informazioni dai file di build (Maven/Gradle) per analisi LLM"
    )
    parser.add_argument("path", help="Path alla root del progetto")
    parser.add_argument("-o", "--output", help="File di output JSON")
    parser.add_argument("--stdout", action="store_true", help="Output su stdout")
    
    args = parser. parse_args()
    
    project_path = Path(args.path)
    if not project_path. exists():
        print(f"Errore: '{args.path}' non esiste")
        return 1
    
    # Estrai
    result = extract_all(project_path)
    
    # Output
    output_json = json.dumps(result, indent=2, ensure_ascii=False, default=str)
    
    if args.stdout:
        print(output_json)
    else:
        output_file = Path(args.output) if args.output else Path(f"build_info_{project_path.name}. json")
        output_file.write_text(output_json, encoding='utf-8')
        print(f"Output:  {output_file}")
        print(f"Maven:  {result['statistics']['maven_files']}, Gradle: {result['statistics']['gradle_files']}")
    
    return 0


if __name__ == "__main__": 
    exit(main())