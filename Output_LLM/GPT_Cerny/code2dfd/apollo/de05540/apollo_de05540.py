from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "apollo_de05540"
apollo_assembly = CClass(service, "apollo-assembly", stereotype_instances = [internal, local_logging])
apollo_core = CClass(service, "apollo-core", stereotype_instances = [internal, local_logging])
apollo_demo = CClass(service, "apollo-demo", stereotype_instances = [internal, local_logging])
apollo_biz = CClass(service, "apollo-biz", stereotype_instances = [basic_authentication, internal, local_logging])
apollo_buildtools = CClass(service, "apollo-buildtools", stereotype_instances = [internal])
apollo_mockserver = CClass(service, "apollo-mockserver", stereotype_instances = [internal, local_logging])
apollo_client = CClass(service, "apollo-client", stereotype_instances = [internal, local_logging])
apollo_configservice = CClass(service, "apollo-configservice", stereotype_instances = [service_discovery, local_logging, infrastructural], tagged_values = {'Endpoints': "['/services/admin', '/services/meta', '/configfiles/{appId}/{clusterName}/{namespace:.+}', '/configs/{appId}/{clusterName}/{namespace:.+}', '/configfiles/json/{appId}/{clusterName}/{namespace:.+}', '/notifications/v2', '/configfiles', '/services/config', '/configs', '/services', '/notifications']", 'Port': 8080, 'Service Discovery': 'Eureka'})
apollo_adminservice = CClass(service, "apollo-adminservice", stereotype_instances = [internal, local_logging], tagged_values = {'Endpoints': "['/instances', '/instances/by-namespace/count', '/', '/instances/by-namespace', '/instances/by-release', '/instances/by-namespace-and-releases-not-in']", 'Port': 8090})
apollo_portal = CClass(service, "apollo-portal", stereotype_instances = [internal, pre_authorized_endpoints, local_logging, csrf_disabled, encryption, basic_authentication], tagged_values = {'Pre-authorized Endpoints': "['/apps/{appId}/envs/{env}/clusters/{clusterName}/namespaces/{namespaceName}/items/export']", 'Port': 8070, 'Endpoints': "['/apps/by-owner', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/items', '/apps/envs/{env}', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/items/{key:.+}', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/branches/{branchName}', '/system-info/health', '/openapi/v1/envs/{env}apps/{appId}/clusters/{clusterName:.+}', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/branches/{branchName}/releases', '/apps/{appId}/miss_envs', '/openapi/v1/apps', '/openapi/v1/envs/{env}apps/{appId}/clusters', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/branches/{branchName}/gray-del-releases', '/openapi/v1/envs/{env}', '/envs', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/releases/latest', '/openapi/v1/envs/{env}/releases/{releaseId}/rollback', '/apps', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/branches', '/organizations', '/system-info', '/apps/search/by-appid-or-name', '/sso_heartbeat', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/branches/{branchName}/merge', '/openapi/v1', '/apps/{appId:.+}', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/branches/{branchName}/rules', '/apps/{appId}/navtree', '/openapi/v1/envs/{env}/apps/{appId}/clusters/{clusterName}/namespaces/{namespaceName}/releases', '/openapi/v1/apps/{appId}/envclusters']"})
apollo_openapi = CClass(service, "apollo-openapi", stereotype_instances = [internal])
apollo_common = CClass(service, "apollo-common", stereotype_instances = [internal, local_logging], tagged_values = {'Endpoints': "['/apollo']"})
apollo_db = CClass(service, "apollo-db", stereotype_instances = [internal], tagged_values = {'Port': 13306})
add_links({apollo_quick_start: apollo_db}, stereotype_instances = [restful_http])
add_links({apollo_biz: apollo_configservice}, stereotype_instances = [restful_http])
add_links({apollo_assembly: apollo_configservice}, stereotype_instances = [restful_http])
add_links({apollo_adminservice: apollo_configservice}, stereotype_instances = [restful_http])
model = CBundle(model_name, elements = apollo_db.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()