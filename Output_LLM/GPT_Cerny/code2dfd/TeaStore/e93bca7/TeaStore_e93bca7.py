from codeable_models import CClass, CBundle, add_links, CStereotype, CMetaclass, CEnum, CAttribute 
from metamodels.microservice_dfds_metamodel import * 
from plant_uml_renderer import PlantUMLGenerator 
plantuml_path = "../../plantuml.jar" 
output_directory = "." 
model_name = "TeaStore_e93bca7"
tools.descartes.teastore.recommender = CClass(service, "tools.descartes.teastore.recommender", stereotype_instances = [internal, local_logging])
tools.descartes.teastore.registry = CClass(service, "tools.descartes.teastore.registry", stereotype_instances = [internal, local_logging])
tools.descartes.teastore.webui = CClass(service, "tools.descartes.teastore.webui", stereotype_instances = [internal, local_logging])
tools.descartes.teastore.image = CClass(service, "tools.descartes.teastore.image", stereotype_instances = [internal, local_logging])
tools.descartes.teastore.auth = CClass(service, "tools.descartes.teastore.auth", stereotype_instances = [internal])
tools.descartes.teastore.persistence = CClass(service, "tools.descartes.teastore.persistence", stereotype_instances = [internal, local_logging])
tools.descartes.teastore.entities = CClass(service, "tools.descartes.teastore.entities", stereotype_instances = [internal])
tools.descartes.teastore.kieker.probes = CClass(service, "tools.descartes.teastore.kieker.probes", stereotype_instances = [internal])
tools.descartes.teastore.dockerbase = CClass(service, "tools.descartes.teastore.dockerbase", stereotype_instances = [internal], tagged_values = {'Port': 8080})
dockermemoryconfigurator = CClass(service, "dockermemoryconfigurator", stereotype_instances = [internal])
kieker.rabbitmq = CClass(service, "kieker.rabbitmq", stereotype_instances = [internal], tagged_values = {'Port': 8080})
tools.descartes.teastore.registryclient = CClass(service, "tools.descartes.teastore.registryclient", stereotype_instances = [internal, local_logging])
model = CBundle(model_name, elements = tools.descartes.teastore.registryclient.class_object.get_connected_elements())
def run():
    generator = PlantUMLGenerator()
    generator.plant_uml_jar_path = plantuml_path
    generator.directory = output_directory
    generator.object_model_renderer.left_to_right = True
    generator.generate_object_models(model_name, [model, {}])
    print(f"Generated models in {generator.directory!s}/" + model_name)
if __name__ == "__main__":
    run()