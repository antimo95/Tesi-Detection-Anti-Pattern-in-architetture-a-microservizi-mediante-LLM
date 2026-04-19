#!/usr/bin/env python3
"""
Estrae metriche di codice (LOC, classi, metodi, costruttori) per ogni microservizio.

Aggiornamenti principali:
- Rilevamento microservizi anche senza pom/build.gradle (es. client Angular con package.json)
- Conteggio LOC anche per TS/JS/HTML/CSS/SCSS/JSON (oltre a Java/Kotlin/Python/Go)
- count_loc più robusto (non perde righe con commenti inline) + supporto commenti HTML <!-- -->
- Esclusione path case-insensitive + EXCLUDE_DIRS ampliata
- Esclusione "cross-service" corretta: esclude solo file di microservizi ANNIDATI (discendenti)
"""

import re
import json
import argparse
import yaml
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Directory da escludere
EXCLUDE_DIRS = {
    # build & tooling
    "target", "build", "dist", "out", "bin", "obj", "release",
    "node_modules", ".gradle", ".mvn", "__pycache__", ".pytest_cache",
    ".venv", "venv", ".tox", ".ruff_cache", ".mypy_cache",

    # vcs/ide
    ".git", ".idea", ".vscode", ".settings",
    ".classpath", ".project",

    # docs & meta
    "doc", "docs", "documentation", "asciidoc", "site", "mkdocs", ".github",

    # reports & coverage
    "coverage", ".coverage", "jacoco", "surefire-reports", "failsafe-reports",

    # misc
    "tmp", "temp", "logs"
}

def is_excluded_path(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    return any(ex.lower() in parts for ex in EXCLUDE_DIRS)

def is_under(child: Path, parent: Path) -> bool:
    """True se child è dentro parent (discendente)."""
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except Exception:
        return False

STEREOTYPES = {
    "controller": ["@RestController", "@Controller"],
    "service": ["@Service"],
    "repository": ["@Repository"],
    "entity": ["@Entity", "@Table"],
    "component": ["@Component"],
    "configuration": ["@Configuration"],
    "feign_client": ["@FeignClient"]
}

def is_aggregator_pom(pom_path: Path) -> bool:
    try:
        c = pom_path.read_text(encoding="utf-8", errors="ignore").lower()
        return ("<modules>" in c) or ("<packaging>pom</packaging>" in c)
    except Exception:
        return False

def detect_stereotypes(content: str):
    found = []
    for stereotype, keywords in STEREOTYPES.items():
        for keyword in keywords:
            if keyword in content:
                found.append(stereotype)
                break
    return found

def extract_jpa_entities(content: str):
    tables = []
    if "@Entity" in content:
        class_match = re.search(r'class\s+(\w+)', content)
        default_name = class_match.group(1) if class_match else "unknown"
        table_match = re.search(r'@Table\s*\(\s*name\s*=\s*"([^"]+)"', content)
        table_name = table_match.group(1) if table_match else default_name
        tables.append(table_name)
    return tables

def find_hardcoded_urls_in_text(text: str):
    url_pattern = re.compile(
        r'https?://[^\s"\'<>{}()\[\]]+|'
        r'localhost:\d+|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+'
    )
    return list(set(url_pattern.findall(text)))

def find_hardcoded_urls(content: str):
    return find_hardcoded_urls_in_text(content)

def find_feign_with_url(content: str):
    return bool(re.search(r'@FeignClient\s*\([^)]*\burl\s*=', content))

def extract_datasource_url_from_yaml(content: str):
    try:
        data = yaml.safe_load(content)
        if data and isinstance(data, dict):
            return data.get("spring", {}).get("datasource", {}).get("url")
    except Exception:
        pass
    return None

# ---------------- LOC robusto con supporto HTML <!-- --> ----------------

def count_loc(content: str, syntax: str = "c"):
    """
    syntax:
      - "c":    // and /* */
      - "hash": # line comments (+ /* */ + // comunque)
      - "html": <!-- --> (+ /* */ + //)
    """
    lines = content.splitlines()
    total = len(lines)
    blank = 0
    comment_only = 0
    code = 0

    in_block_c = False      # /* */
    in_block_html = False   # <!-- -->

    for line in lines:
        s = line.rstrip("\n")
        stripped = s.strip()

        if not stripped:
            blank += 1
            continue

        i = 0
        has_code = False

        while i < len(s):
            # HTML block comment
            if in_block_html:
                end = s.find("-->", i)
                if end == -1:
                    i = len(s)
                    break
                in_block_html = False
                i = end + 3
                continue

            # C block comment
            if in_block_c:
                end = s.find("*/", i)
                if end == -1:
                    i = len(s)
                    break
                in_block_c = False
                i = end + 2
                continue

            if s[i].isspace():
                i += 1
                continue

            # start HTML comment
            if syntax == "html" and s.startswith("<!--", i):
                in_block_html = True
                i += 4
                continue

            # line comment //
            if s.startswith("//", i):
                break

            # line comment #
            if syntax in ("hash",) and s[i] == "#":
                break

            # start C block
            if s.startswith("/*", i):
                in_block_c = True
                i += 2
                continue

            # otherwise code
            has_code = True
            i += 1

        if has_code:
            code += 1
        else:
            comment_only += 1

    return {"total": total, "code": code, "blank": blank, "comment": comment_only}

# ---------------- Analyzers ----------------

def analyze_java_file(content: str):
    class_pattern = re.compile(r'\b(class|interface|enum)\s+(\w+)')
    class_matches = class_pattern.findall(content)
    classes = len(class_matches)
    class_names = {name for kind, name in class_matches if kind in ("class", "enum")}

    method_pattern = re.compile(
        r'(public|private|protected)\s+\w[\w<>\[\],\s]*\s+(\w+)\s*\('
    )
    ctor_pattern = re.compile(
        r'(public|private|protected)\s+(' + "|".join(re.escape(n) for n in class_names) + r')\s*\('
    )

    method_matches = method_pattern.findall(content)
    ctor_matches = ctor_pattern.findall(content)

    methods = 0
    for _, method_name in method_matches:
        if method_name in ("if", "while", "for", "switch", "catch", "try", "return"):
            continue
        if method_name in class_names:
            continue
        methods += 1

    return {
        "classes": classes,
        "methods": methods,
        "constructors": len(ctor_matches),
        "stereotypes": detect_stereotypes(content),
        "jpa_tables": extract_jpa_entities(content),
        "hardcoded_urls": find_hardcoded_urls(content),
        "feign_with_url": find_feign_with_url(content)
    }

def analyze_kotlin_file(content: str):
    class_pattern = re.compile(r'\bclass\s+(\w+)')
    method_pattern = re.compile(r'\bfun\s+(\w+)\s*\(')
    return {
        "classes": len(class_pattern.findall(content)),
        "methods": len(method_pattern.findall(content)),
        "constructors": 0,
        "stereotypes": [],
        "jpa_tables": [],
        "hardcoded_urls": find_hardcoded_urls(content),
        "feign_with_url": find_feign_with_url(content)
    }

def analyze_python_file(content: str):
    class_pattern = re.compile(r'^class\s+(\w+)', re.MULTILINE)
    method_pattern = re.compile(r'^\s*def\s+(\w+)\s*\(', re.MULTILINE)
    classes = len(class_pattern.findall(content))
    all_methods = method_pattern.findall(content)
    constructors = all_methods.count("__init__")
    return {
        "classes": classes,
        "methods": len(all_methods) - constructors,
        "constructors": constructors,
        "stereotypes": [],
        "jpa_tables": [],
        "hardcoded_urls": find_hardcoded_urls(content),
        "feign_with_url": False
    }

def analyze_go_file(content: str):
    struct_pattern = re.compile(r'type\s+(\w+)\s+struct\s*\{')
    func_pattern = re.compile(r'func\s+(\w+)\s*\(')
    return {
        "classes": len(struct_pattern.findall(content)),
        "methods": len(func_pattern.findall(content)),
        "constructors": 0,
        "stereotypes": [],
        "jpa_tables": [],
        "hardcoded_urls": find_hardcoded_urls(content),
        "feign_with_url": False
    }

def analyze_ts_or_js_file(content: str):
    """
    Stima leggera:
    - class: 'class X'
    - methods/functions: 'function x(' + 'x(' per arrow? (teniamola semplice)
    """
    class_pattern = re.compile(r'\bclass\s+(\w+)')
    func_pattern = re.compile(r'\bfunction\s+(\w+)\s*\(')
    arrow_pattern = re.compile(r'\b(\w+)\s*=\s*\([^)]*\)\s*=>')
    classes = len(class_pattern.findall(content))
    methods = len(func_pattern.findall(content)) + len(arrow_pattern.findall(content))
    return {
        "classes": classes,
        "methods": methods,
        "constructors": 0,
        "stereotypes": [],
        "jpa_tables": [],
        "hardcoded_urls": find_hardcoded_urls(content),
        "feign_with_url": False
    }

# ---------------- Rilevamento microservizi ----------------

def find_microservices(project_root: Path):
    services = {}

    def add_service(service_dir: Path, svc_type: str):
        if service_dir == project_root:
            return
        if is_excluded_path(service_dir):
            return
        name = service_dir.name
        services[name] = {
            "path": str(service_dir.relative_to(project_root)),
            "type": svc_type,
            "absolute_path": service_dir
        }

    # Maven services (non aggregator)
    for pom in project_root.rglob("pom.xml"):
        if is_excluded_path(pom):
            continue
        if is_aggregator_pom(pom):
            continue
        add_service(pom.parent, "maven")

    # Gradle services
    for gradle in project_root.rglob("build.gradle"):
        if is_excluded_path(gradle):
            continue
        add_service(gradle.parent, "gradle")

    # Node/Frontend services (es. client Angular/React/Vue)
    for pkg in project_root.rglob("package.json"):
        if is_excluded_path(pkg):
            continue
        # evita package.json dentro node_modules ecc. (già escluso, ma doppia sicurezza)
        if "node_modules" in {p.lower() for p in pkg.parts}:
            continue
        add_service(pkg.parent, "node")

    # Python services
    for pyproj in project_root.rglob("pyproject.toml"):
        if is_excluded_path(pyproj):
            continue
        add_service(pyproj.parent, "python")

    for setup in project_root.rglob("setup.py"):
        if is_excluded_path(setup):
            continue
        add_service(setup.parent, "python")

    # Go services
    for gomod in project_root.rglob("go.mod"):
        if is_excluded_path(gomod):
            continue
        add_service(gomod.parent, "go")

    # Dockerized services (fallback)
    for dockerfile in project_root.rglob("Dockerfile"):
        if is_excluded_path(dockerfile):
            continue
        # se non già rilevato con altri marker, aggiungilo
        add_service(dockerfile.parent, "docker")

    return services

# ---------------- Analisi microservizio ----------------

def analyze_microservice(service_path: Path, other_service_paths):
    metrics = {
        "loc": {"total": 0, "code": 0, "blank": 0, "comment": 0},
        "classes_count": 0,
        "methods_count": 0,
        "constructors_count": 0,
        "files_count": 0,
        "stereotype_instances": defaultdict(int),
        "jpa_tables": set(),
        "hardcoded_endpoints": set(),
        "feign_with_url": False,
        "datasource_url": None,
        "languages": defaultdict(int),
        "file_types": defaultdict(int),
    }

    # microservizi ANNIDATI dentro questo servizio (discendenti)
    nested_services = [
        p for p in other_service_paths
        if p != service_path and is_under(p, service_path)
    ]

    # Estensioni da contare per LOC (incluso client Angular)
    loc_syntax_by_ext = {
        ".java": "c",
        ".kt": "c",
        ".py": "hash",
        ".go": "c",
        ".ts": "c",
        ".tsx": "c",
        ".js": "c",
        ".jsx": "c",
        ".proto": "c",
    }

    # Analyzer per classi/metodi (solo alcuni)
    analyzers = {
        ".java": ("java", analyze_java_file),
        ".kt": ("kotlin", analyze_kotlin_file),
        ".py": ("python", analyze_python_file),
        ".go": ("go", analyze_go_file),
        ".ts": ("typescript", analyze_ts_or_js_file),
        ".tsx": ("typescript", analyze_ts_or_js_file),
        ".js": ("javascript", analyze_ts_or_js_file),
        ".jsx": ("javascript", analyze_ts_or_js_file),
    }

    # 1) YAML / properties: datasource + hardcoded endpoints
    for ext in (".yml", ".yaml", ".properties"):
        for cfg in service_path.rglob("*" + ext):
            if is_excluded_path(cfg):
                continue
            if any(is_under(cfg, ns) for ns in nested_services):
                continue
            try:
                content = cfg.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            metrics["hardcoded_endpoints"].update(find_hardcoded_urls_in_text(content))

            if ext in (".yml", ".yaml"):
                url = extract_datasource_url_from_yaml(content)
                if url:
                    metrics["datasource_url"] = url

    # 2) LOC: conta per tutte le estensioni in loc_syntax_by_ext
    for file_path in service_path.rglob("*"):
        if not file_path.is_file():
            continue
        if is_excluded_path(file_path):
            continue
        if any(is_under(file_path, ns) for ns in nested_services):
            continue

        ext = file_path.suffix.lower()
        if ext not in loc_syntax_by_ext:
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        metrics["files_count"] += 1
        metrics["file_types"][ext] += 1

        # linguaggio per conteggio (best effort)
        if ext in analyzers:
            lang, _ = analyzers[ext]
            metrics["languages"][lang] += 1
        else:
            metrics["languages"][ext.lstrip(".")] += 1

        loc = count_loc(content, syntax=loc_syntax_by_ext[ext])
        for k in loc:
            metrics["loc"][k] += loc[k]

        # 3) analisi classi/metodi per estensioni note
        if ext in analyzers:
            _, analyzer = analyzers[ext]
            analysis = analyzer(content)

            metrics["classes_count"] += analysis["classes"]
            metrics["methods_count"] += analysis["methods"]
            metrics["constructors_count"] += analysis["constructors"]

            for st in analysis.get("stereotypes", []):
                metrics["stereotype_instances"][st] += 1

            metrics["jpa_tables"].update(analysis.get("jpa_tables", []))
            metrics["hardcoded_endpoints"].update(analysis.get("hardcoded_urls", []))
            if analysis.get("feign_with_url"):
                metrics["feign_with_url"] = True
        else:
            # comunque prova a beccare URL hardcoded anche su altri file “loc”
            metrics["hardcoded_endpoints"].update(find_hardcoded_urls_in_text(content))

    # JSON-serializable
    metrics["stereotype_instances"] = dict(metrics["stereotype_instances"])
    metrics["jpa_tables"] = list(metrics["jpa_tables"])
    metrics["hardcoded_endpoints"] = list(metrics["hardcoded_endpoints"])
    metrics["languages"] = dict(metrics["languages"])
    metrics["file_types"] = dict(metrics["file_types"])

    return metrics

# ---------------- Main extraction ----------------

def extract_all(project_path: str):
    root = Path(project_path).resolve()
    services = find_microservices(root)
    all_service_paths = [info["absolute_path"].resolve() for info in services.values()]

    result = {
        "metadata": {
            "project_path": str(root),
            "project_name": root.name,
            "extraction_timestamp": datetime.now().isoformat(),
            "extractor_version": "2.1.0"
        },
        "microservices": [],
        "statistics": {
            "total_services": 0,
            "total_files": 0,
            "total_loc_code": 0,
            "total_classes": 0,
            "total_methods": 0,
            "total_constructors": 0
        }
    }

    for service_name, service_info in sorted(services.items()):
        service_path = service_info["absolute_path"].resolve()

        metrics = analyze_microservice(service_path, all_service_paths)

        result["microservices"].append({
            "name": service_name,
            "type": service_info["type"],
            "path": service_info["path"],
            "loc": metrics["loc"],
            "classes_count": metrics["classes_count"],
            "methods_count": metrics["methods_count"],
            "constructors_count": metrics["constructors_count"],
            "files_count": metrics["files_count"],
            "stereotype_instances": list(metrics["stereotype_instances"].keys()),
            "stereotype_counts": metrics["stereotype_instances"],
            "languages": metrics["languages"],
            "file_types": metrics["file_types"],
            "jpa_tables": metrics["jpa_tables"],
            "datasource_url": metrics["datasource_url"],
            "hardcoded_endpoints": metrics["hardcoded_endpoints"],
            "feign_with_url": metrics["feign_with_url"]
        })

        result["statistics"]["total_loc_code"] += metrics["loc"]["code"]
        result["statistics"]["total_classes"] += metrics["classes_count"]
        result["statistics"]["total_methods"] += metrics["methods_count"]
        result["statistics"]["total_constructors"] += metrics["constructors_count"]
        result["statistics"]["total_files"] += metrics["files_count"]

    result["statistics"]["total_services"] = len(result["microservices"])
    return result

def main():
    parser = argparse.ArgumentParser(description="Estrae metriche di codice per microservizio (esteso)")
    parser.add_argument("path", help="Path alla root del progetto")
    parser.add_argument("-o", "--output", help="File di output JSON")
    args = parser.parse_args()

    project_path = Path(args.path)
    if not project_path.exists():
        print("Errore: percorso non esistente")
        return 1

    result = extract_all(str(project_path))

    output_file = Path(args.output) if args.output else Path("extended_code_metrics_" + project_path.name + ".json")
    output_file.write_text(json.dumps(result, indent=2), encoding="utf-8")

    stats = result["statistics"]
    print("Output:", output_file)
    print("Microservices:", stats["total_services"])
    print("Total Files:", stats["total_files"])
    print("LOC:", stats["total_loc_code"])
    print("Classes:", stats["total_classes"])
    print("Methods:", stats["total_methods"])
    print("Constructors:", stats["total_constructors"])
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
