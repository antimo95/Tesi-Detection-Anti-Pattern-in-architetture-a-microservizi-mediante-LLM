from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "ftgo-application_c028190"
ftgo_order_history_service = CClass(service, "ftgo-order-history-service", stereotype_instances = [internal, local_logging])
ftgo_order_service = CClass(service, "ftgo-order-service", stereotype_instances = [internal, local_logging])
ftgo_api_gateway = CClass(service, "ftgo-api-gateway", stereotype_instances = [infrastructural, gateway], tagged_values = {'Gateway': 'Spring Cloud Gateway'})
ftgo_kitchen_service = CClass(service, "ftgo-kitchen-service", stereotype_instances = [internal])
ftgo_accounting_service = CClass(service, "ftgo-accounting-service", stereotype_instances = [internal])
ftgo_consumer_service = CClass(service, "ftgo-consumer-service", stereotype_instances = [internal])
ftgo_restaurant_service = CClass(service, "ftgo-restaurant-service", stereotype_instances = [internal])
zookeeper = CClass(service, "zookeeper", stereotype_instances = [internal], tagged_values = {'Port': 2181})
kafka = CClass(service, "kafka", stereotype_instances = [infrastructural, message_broker], tagged_values = {'Port': 9092, 'Message Broker': 'Kafka'})
zipkin = CClass(service, "zipkin", stereotype_instances = [infrastructural, tracing_server], tagged_values = {'Port': 9411, 'Tracing Server': 'Zipkin'})
mysql = CClass(service, "mysql", stereotype_instances = [internal], tagged_values = {'Port': 3306})
database_ftgo_order_service = CClass(external_component, "database-ftgo-order-service", stereotype_instances = [external_database, exitpoint, plaintext_credentials, entrypoint], tagged_values = {'Password': 'ftgo_delivery_service_password', 'Username': 'ftgo_delivery_service_user', 'Database': 'MySQL'})
database_ftgo_kitchen_service = CClass(external_component, "database-ftgo-kitchen-service", stereotype_instances = [external_database, exitpoint, plaintext_credentials, entrypoint], tagged_values = {'Database': 'MySQL', 'Username': 'ftgo_kitchen_service_user', 'Password': 'ftgo_kitchen_service_password'})
database_ftgo_accounting_service = CClass(external_component, "database-ftgo-accounting-service", stereotype_instances = [external_database, exitpoint, plaintext_credentials, entrypoint], tagged_values = {'Database': 'MySQL', 'Username': 'ftgo_accounting_service_user', 'Password': 'ftgo_accounting_service_password'})
database_ftgo_consumer_service = CClass(external_component, "database-ftgo-consumer-service", stereotype_instances = [external_database, exitpoint, plaintext_credentials, entrypoint], tagged_values = {'Database': 'MySQL', 'Password': 'ftgo_consumer_service_password', 'Username': 'ftgo_consumer_service_user'})
database_ftgo_restaurant_service = CClass(external_component, "database-ftgo-restaurant-service", stereotype_instances = [external_database, exitpoint, plaintext_credentials, entrypoint], tagged_values = {'Database': 'MySQL', 'Username': 'ftgo_restaurant_service_user', 'Password': 'ftgo_restaurant_service_password'})
user = CClass(external_component, "user", stereotype_instances = [user_stereotype, exitpoint, entrypoint])
add_links({database_ftgo_order_service: ftgo_order_service}, stereotype_instances = [jdbc, plaintext_credentials_link], tagged_values = {'Password': 'ftgo_order_service_password', 'Username': 'ftgo_order_service_user'})
add_links({database_ftgo_kitchen_service: ftgo_kitchen_service}, stereotype_instances = [jdbc, plaintext_credentials_link], tagged_values = {'Username': 'ftgo_kitchen_service_user', 'Password': 'ftgo_kitchen_service_password'})
add_links({database_ftgo_accounting_service: ftgo_accounting_service}, stereotype_instances = [jdbc, plaintext_credentials_link], tagged_values = {'Password': 'ftgo_accounting_service_password', 'Username': 'ftgo_accounting_service_user'})
add_links({database_ftgo_consumer_service: ftgo_consumer_service}, stereotype_instances = [jdbc, plaintext_credentials_link], tagged_values = {'Password': 'ftgo_consumer_service_password', 'Username': 'ftgo_consumer_service_user'})
add_links({database_ftgo_restaurant_service: ftgo_restaurant_service}, stereotype_instances = [jdbc, plaintext_credentials_link], tagged_values = {'Username': 'ftgo_restaurant_service_user', 'Password': 'ftgo_restaurant_service_password'})
add_links({user: ftgo_api_gateway}, stereotype_instances = [restful_http])
add_links({ftgo_api_gateway: user}, stereotype_instances = [restful_http])
model = CBundle(model_name, elements = mysql.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()