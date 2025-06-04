from kubernetes import client, config
from openshift.dynamic import DynamicClient
 
from openshift.dynamic.resource import ResourceInstance

config.load_kube_config()

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)
# https://github.com/openshift/openshift-restclient-python

# get all custom resource definitions
def get_custom_resources() -> list[ResourceInstance]:
    try:
        custom_resources = dyn_client.resources.get(
        api_version='apiextensions.k8s.io/v1beta1',
        kind='CustomResourceDefinition'
        )
        return custom_resources.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
# get namespaces    
def get_namespaces() -> list[ResourceInstance]:
    try:
        namespaces = dyn_client.resources.get(api_version='v1', kind='Namespace')
        return namespaces.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    

# get projects
def get_projects() -> list[ResourceInstance]:
    try:
        projects = dyn_client.resources.get(api_version='project.openshift.io/v1', kind='Project')
        return projects.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
namespaces = get_namespaces()
print("Namespaces:")
for namespace in namespaces:
    print(f"Namespace Name: {namespace.metadata.name}")

projects= get_projects()
print("Projects:")
for project in projects:
    print(f"Project Name: {project.metadata.name}, Status: {project.status.phase if hasattr(project.status, 'phase') else 'N/A'}")
