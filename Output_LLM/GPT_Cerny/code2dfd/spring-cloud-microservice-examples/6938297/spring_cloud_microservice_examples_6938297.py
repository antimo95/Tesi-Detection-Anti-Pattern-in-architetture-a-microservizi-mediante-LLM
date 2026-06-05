from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "spring-cloud-microservice-examples_6938297"
cloud_thrift_server = CClass(service, "cloud-thrift-server", stereotype_instances = [internal], tagged_values = {'Port': 8071})
gateway = CClass(service, "gateway", stereotype_instances = [local_logging, load_balancer, infrastructural, gateway], tagged_values = {'Load Balancer': 'Ribbon', 'Gateway': 'Zuul'})
uaa_service = CClass(service, "uaa-service", stereotype_instances = [authorization_server, infrastructural], tagged_values = {'Authorization Server': 'Spring OAuth2', 'Port': 8769})
cloud_config_server = CClass(service, "cloud-config-server", stereotype_instances = [infrastructural, configuration_server], tagged_values = {'Configuration Server': 'Spring Cloud Config', 'Port': 8888})
cloud_eureka_server = CClass(service, "cloud-eureka-server", stereotype_instances = [infrastructural, service_discovery], tagged_values = {'Service Discovery': 'Eureka', 'Port': 8761})
cloud_finagle_thrift_api = CClass(service, "cloud-finagle-thrift-api", stereotype_instances = [internal])
cloud_simple_ui = CClass(service, "cloud-simple-ui", stereotype_instances = [circuit_breaker, load_balancer, internal], tagged_values = {'Endpoints': "['/users']", 'Port': 8090, 'Load Balancer': 'Spring Cloud'})
cloud_finagle_thrift_client = CClass(service, "cloud-finagle-thrift-client", stereotype_instances = [internal])
cloud_thrift_client = CClass(service, "cloud-thrift-client", stereotype_instances = [internal], tagged_values = {'Port': 8070, 'Endpoints': "['/hello']"})
cloud_finagle_thrift_server = CClass(service, "cloud-finagle-thrift-server", stereotype_instances = [internal])
cloud_finagle_commons_thrift = CClass(service, "cloud-finagle-commons-thrift", stereotype_instances = [internal])
hystrix_dashboard = CClass(service, "hystrix-dashboard", stereotype_instances = [monitoring_dashboard, infrastructural], tagged_values = {'Port': 8022, 'Monitoring Dashboard': 'Hystrix', 'Endpoints': "['/']"})
cloud_hystrix_turbine = CClass(service, "cloud-hystrix-turbine", stereotype_instances = [infrastructural, monitoring_server], tagged_values = {'Monitoring Server': 'Turbine', 'Port': 8989})
zipkin = CClass(service, "zipkin", stereotype_instances = [internal], tagged_values = {'Port': 9411})
cloud_dummy_service = CClass(service, "cloud-dummy-service", stereotype_instances = [resource_server, internal], tagged_values = {'Endpoints': "['/']"})
cloud_simple_service = CClass(service, "cloud-simple-service", stereotype_instances = [local_logging, internal], tagged_values = {'Port': 8081, 'Endpoints': "['/user']"})
cloud_thrift_interface = CClass(service, "cloud-thrift-interface", stereotype_instances = [local_logging, internal])
cloud_simple_serviceb = CClass(service, "cloud-simple-serviceb", stereotype_instances = [internal], tagged_values = {'Endpoints': "['/user']", 'Port': 8091})
user = CClass(external_component, "user", stereotype_instances = [exitpoint, user_stereotype, entrypoint])
add_links({cloud_config_server: cloud_hystrix_turbine}, stereotype_instances = [restful_http])
add_links({hystrix: gateway}, stereotype_instances = [restful_http])
add_links({turbine: gateway}, stereotype_instances = [restful_http])
add_links({gateway: zipkin}, stereotype_instances = [restful_http])
add_links({simple_service: zipkin}, stereotype_instances = [restful_http])
add_links({simple_service2: zipkin}, stereotype_instances = [restful_http])
add_links({simple_serviceb: zipkin}, stereotype_instances = [restful_http])
add_links({simple_ui: zipkin}, stereotype_instances = [restful_http])
add_links({cloud_simple_serviceb: cloud_eureka_server}, stereotype_instances = [restful_http])
add_links({uaa_service: cloud_eureka_server}, stereotype_instances = [restful_http])
add_links({cloud_simple_ui: cloud_eureka_server}, stereotype_instances = [restful_http, circuit_breaker_link, load_balanced_link], tagged_values = {'Load Balancer': 'Spring Cloud'})
add_links({cloud_dummy_service: cloud_eureka_server}, stereotype_instances = [restful_http])
add_links({cloud_hystrix_turbine: cloud_eureka_server}, stereotype_instances = [restful_http])
add_links({cloud_config_server: cloud_eureka_server}, stereotype_instances = [restful_http])
add_links({cloud_simple_service: cloud_eureka_server}, stereotype_instances = [restful_http])
add_links({user: gateway}, stereotype_instances = [restful_http])
add_links({gateway: user}, stereotype_instances = [restful_http])
add_links({cloud_hystrix_turbine: hystrix_dashboard}, stereotype_instances = [restful_http])
model = CBundle(model_name, elements = cloud_simple_serviceb.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()