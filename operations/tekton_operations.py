from kubernetes import client, config

config.load_kube_config()

kubeclient= client.CoreV1Api()
CustomObjectClient=client.CustomObjectsApi()

# get all custom resource definitions
def get_all_crds():
    try:
        crds = CustomObjectClient.get_cluster_custom_object(
            name="customresourcedefinitions",
            group="apiextensions.k8s.io",
            version="v1",
            plural="customresourcedefinitions"
        )
         # Extracting the names of the CRDs
         # Assuming crds.items is a list of CRD objects
         # and each object has a metadata field with a name attribute
         # Adjust according to your actual CRD structure
        return [crd.metadata.name for crd in crds.items]
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_all_namespaces():
    try:
        namespaces = kubeclient.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    

# get all pods in a specific namespace
def get_pods_in_namespace(namespace):
    try:
        pods = kubeclient.list_namespaced_pod(namespace)
        return pods.items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
namespaces = get_all_namespaces()
for ns in namespaces:
    print(f"Namespace: {ns}")

# pods=get_pods_in_namespace("tekton-pipelines")
# for pod in pods:
    # print(f"Pod Name: {pod.metadata.name}, Status: {pod.status.phase}")

crds= get_all_crds()
for crd in crds:
    print(f"CRD Name: {crd}")
