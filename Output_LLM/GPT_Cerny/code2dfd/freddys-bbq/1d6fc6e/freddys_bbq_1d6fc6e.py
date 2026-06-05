from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "freddys-bbq_1d6fc6e"
menu_service = CClass(service, "menu-service", stereotype_instances = [internal, resource_server], tagged_values = {'Port': 8083})
microsec_uaa = CClass(service, "microsec-uaa", stereotype_instances = [internal])
admin_portal = CClass(service, "admin-portal", stereotype_instances = [internal, circuit_breaker, load_balancer], tagged_values = {'Port': 8084, 'Endpoints': "['/menuItems', '/menuItems/{id}/delete', '/orders', '/orders/{id}/delete', '/', '/menuItems/new', '/menuItems/{id}']", 'Load Balancer': 'Spring Cloud'})
microsec_common = CClass(service, "microsec-common", stereotype_instances = [internal], tagged_values = {'Endpoints': "['/dump_token']"})
order_service = CClass(service, "order-service", stereotype_instances = [internal, pre_authorized_endpoints, resource_server, load_balancer], tagged_values = {'Pre-authorized Endpoints': "['/myorders']", 'Port': 8085, 'Load Balancer': 'Spring Cloud', 'Endpoints': "['/myorders']"})
microsec_hystrix_dashboard = CClass(service, "microsec-hystrix-dashboard", stereotype_instances = [infrastructural, monitoring_dashboard], tagged_values = {'Monitoring Dashboard': 'Hystrix', 'Port': 9999})
microsec_eureka_server = CClass(service, "microsec-eureka-server", stereotype_instances = [infrastructural, service_discovery], tagged_values = {'Service Discovery': 'Eureka', 'Port': 8761})
microsec_custom_registry = CClass(service, "microsec-custom-registry", stereotype_instances = [infrastructural, authorization_server, csrf_disabled], tagged_values = {'Endpoints': "['/', '/login']", 'Authorization Server': 'Spring OAuth2'})
customer_portal = CClass(service, "customer-portal", stereotype_instances = [internal, circuit_breaker, load_balancer], tagged_values = {'Endpoints': "['/', '/menu', '/myorders']", 'Load Balancer': 'Spring Cloud', 'Port': 8082})
microsec_test = CClass(service, "microsec-test", stereotype_instances = [internal])
add_links({menu_service: microsec_eureka_server}, stereotype_instances = [restful_http])
add_links({order_service: microsec_eureka_server}, stereotype_instances = [restful_http, load_balanced_link], tagged_values = {'Load Balancer': 'Spring Cloud'})
add_links({customer_portal: microsec_eureka_server}, stereotype_instances = [restful_http, load_balanced_link, circuit_breaker_link], tagged_values = {'Load Balancer': 'Spring Cloud'})
add_links({admin_portal: microsec_eureka_server}, stereotype_instances = [restful_http, load_balanced_link, circuit_breaker_link], tagged_values = {'Load Balancer': 'Spring Cloud'})
model = CBundle(model_name, elements = microsec_test.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()