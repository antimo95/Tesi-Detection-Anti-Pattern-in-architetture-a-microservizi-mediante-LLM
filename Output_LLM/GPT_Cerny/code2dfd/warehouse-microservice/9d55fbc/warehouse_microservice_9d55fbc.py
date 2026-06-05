from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "warehouse-microservice_9d55fbc"
authentacation_server = CClass(service, "authentacation-server", stereotype_instances = [csrf_disabled, authorization_server, resource_server, infrastructural], tagged_values = {'Authorization Server': 'Spring OAuth2', 'Endpoints': "['/account', '/account/userInfo']"})
product_catalog_service = CClass(service, "product-catalog-service", stereotype_instances = [circuit_breaker, basic_authentication, internal, local_logging, resource_server, pre_authorized_endpoints], tagged_values = {'Logging Technology': 'Lombok', 'Pre-authorized Endpoints': "['/{idPriceList}/goods/{idGoods}']", 'Endpoints': "['/products/{idGoods}/category-attribute', '/price-list/{idPriceList}', '/price-list/{idPriceList}/goods/{idGoods}', '/products/{idGoods}', '/price-list/{idPriceList}/goods', '/products', '/price-list']", 'Circuit Breaker': 'Hystrix'})
eureka_server = CClass(service, "eureka-server", stereotype_instances = [service_discovery, infrastructural], tagged_values = {'Port': 8761, 'Service Discovery': 'Eureka'})
order_service = CClass(service, "order-service", stereotype_instances = [circuit_breaker, internal, local_logging, ssl_enabled, load_balancer, pre_authorized_endpoints], tagged_values = {'Port': 8080, 'Logging Technology': 'Lombok', 'Load Balancer': 'Ribbon', 'Endpoints': "['/purchase-order', '/purchase-order/{orderNumber}/customer']", 'Circuit Breaker': 'Hystrix'})
account_service = CClass(service, "account-service", stereotype_instances = [circuit_breaker, local_logging, internal, pre_authorized_endpoints], tagged_values = {'Circuit Breaker': 'Hystrix', 'Endpoints': "['/account', '/account/{userName}']", 'Logging Technology': 'Lombok'})
turbine_server = CClass(service, "turbine-server", stereotype_instances = [monitoring_server, infrastructural], tagged_values = {'Monitoring Server': 'Turbine'})
api_gateway = CClass(service, "api-gateway", stereotype_instances = [load_balancer, circuit_breaker, gateway, infrastructural], tagged_values = {'Gateway': 'Zuul', 'Circuit Breaker': 'Hystrix', 'Load Balancer': 'Ribbon'})
config_server = CClass(service, "config-server", stereotype_instances = [infrastructural, configuration_server], tagged_values = {'Configuration Server': 'Spring Cloud Config', 'Port': 8888})
product_catalog_management_website = CClass(service, "product-catalog-management-website", stereotype_instances = [circuit_breaker, load_balancer, csrf_disabled, gateway, infrastructural], tagged_values = {'Gateway': 'Zuul', 'Circuit Breaker': 'Hystrix', 'Load Balancer': 'Ribbon'})
spring_boot_admin = CClass(service, "spring-boot-admin", stereotype_instances = [administration_server, infrastructural], tagged_values = {'Administration Server': 'Spring Boot Admin'})
website = CClass(service, "website", stereotype_instances = [circuit_breaker, load_balancer, csrf_disabled, gateway, infrastructural], tagged_values = {'Gateway': 'Zuul', 'Circuit Breaker': 'Hystrix', 'Load Balancer': 'Ribbon'})
zipkin_server = CClass(service, "zipkin-server", stereotype_instances = [internal])
github_repository = CClass(external_component, "github-repository", stereotype_instances = [github_repository, entrypoint], tagged_values = {'URL': 'https://github.com/HienNguyen711/warehouse-microservice'})
user = CClass(external_component, "user", stereotype_instances = [exitpoint, user_stereotype, entrypoint])
add_links({github_repository: config_server}, stereotype_instances = [restful_http])
add_links({turbine_server: eureka_server}, stereotype_instances = [restful_http])
add_links({eureka_server: product_catalog_management_website}, stereotype_instances = [restful_http])
add_links({eureka_server: website}, stereotype_instances = [restful_http])
add_links({eureka_server: api_gateway}, stereotype_instances = [restful_http])
add_links({zipkin_server: eureka_server}, stereotype_instances = [restful_http])
add_links({account_service: eureka_server}, stereotype_instances = [restful_http])
add_links({authentacation_server: eureka_server}, stereotype_instances = [restful_http])
add_links({product_catalog_service: eureka_server}, stereotype_instances = [restful_http])
add_links({config_server: eureka_server}, stereotype_instances = [restful_http])
add_links({order_service: eureka_server}, stereotype_instances = [load_balanced_link, restful_http], tagged_values = {'Load Balancer': 'Spring Cloud'})
add_links({spring_boot_admin: eureka_server}, stereotype_instances = [restful_http])
add_links({user: api_gateway}, stereotype_instances = [restful_http])
add_links({api_gateway: user}, stereotype_instances = [restful_http])
add_links({user: product_catalog_management_website}, stereotype_instances = [restful_http])
add_links({product_catalog_management_website: user}, stereotype_instances = [load_balanced_link, restful_http], tagged_values = {'Load Balancer': 'Spring Cloud'})
add_links({user: website}, stereotype_instances = [restful_http])
add_links({website: user}, stereotype_instances = [restful_http])
model = CBundle(model_name, elements = zipkin_server.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()