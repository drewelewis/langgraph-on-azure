from kubernetes import client, config
from openshift.dynamic import DynamicClient
 
from openshift.dynamic.resource import ResourceInstance

config.load_kube_config()

k8s_client = config.new_client_from_config()
dyn_client = DynamicClient(k8s_client)
# https://github.com/openshift/openshift-restclient-python
# install teckton tasks https://hub.tekton.dev/tekton/task/git-clone

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
    
# get all pods
def get_pods(namespace: str = None) -> list[ResourceInstance]:
    try:
        pods = dyn_client.resources.get(api_version='v1', kind='Pod')
        if namespace:
            return pods.get(namespace=namespace).items
        else:
            return pods.get().items
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

# get deployments
def get_deployments(namespace: str = None) -> list[ResourceInstance]:
    try:
        deployments = dyn_client.resources.get(api_version='apps/v1', kind='Deployment')
        if namespace:
            return deployments.get(namespace=namespace).items
        else:
            return deployments.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

# get services
def get_services(namespace: str = None) -> list[ResourceInstance]:
    try:
        services = dyn_client.resources.get(api_version='v1', kind='Service')
        if namespace:
            return services.get(namespace=namespace).items
        else:
            return services.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_configmaps(namespace: str = None) -> list[ResourceInstance]:
    try:
        configmaps = dyn_client.resources.get(api_version='v1', kind='ConfigMap')
        if namespace:
            return configmaps.get(namespace=namespace).items
        else:
            return configmaps.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_secrets(namespace: str = None) -> list[ResourceInstance]:
    try:
        secrets = dyn_client.resources.get(api_version='v1', kind='Secret')
        if namespace:
            return secrets.get(namespace=namespace).items
        else:
            return secrets.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_cronjobs(namespace: str = None) -> list[ResourceInstance]:
    try:
        cronjobs = dyn_client.resources.get(api_version='batch/v1', kind='CronJob')
        if namespace:
            return cronjobs.get(namespace=namespace).items
        else:
            return cronjobs.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_statefulsets(namespace: str = None) -> list[ResourceInstance]:
    try:
        statefulsets = dyn_client.resources.get(api_version='apps/v1', kind='StatefulSet')
        if namespace:
            return statefulsets.get(namespace=namespace).items
        else:
            return statefulsets.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_daemonsets(namespace: str = None) -> list[ResourceInstance]:
    try:
        daemonsets = dyn_client.resources.get(api_version='apps/v1', kind='DaemonSet')
        if namespace:
            return daemonsets.get(namespace=namespace).items
        else:
            return daemonsets.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_ingresses(namespace: str = None) -> list[ResourceInstance]:
    try:
        ingresses = dyn_client.resources.get(api_version='networking.k8s.io/v1', kind='Ingress')
        if namespace:
            return ingresses.get(namespace=namespace).items
        else:
            return ingresses.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_persistentvolumeclaims(namespace: str = None) -> list[ResourceInstance]:
    try:
        pvc = dyn_client.resources.get(api_version='v1', kind='PersistentVolumeClaim')
        if namespace:
            return pvc.get(namespace=namespace).items
        else:
            return pvc.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_persistentvolumes() -> list[ResourceInstance]:
    try:
        pv = dyn_client.resources.get(api_version='v1', kind='PersistentVolume')
        return pv.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_horizontalpodautoscalers(namespace: str = None) -> list[ResourceInstance]:
    try:
        hpa = dyn_client.resources.get(api_version='autoscaling/v2', kind='HorizontalPodAutoscaler')
        if namespace:
            return hpa.get(namespace=namespace).items
        else:
            return hpa.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_networkpolicies(namespace: str = None) -> list[ResourceInstance]:
    try:
        networkpolicies = dyn_client.resources.get(api_version='networking.k8s.io/v1', kind='NetworkPolicy')
        if namespace:
            return networkpolicies.get(namespace=namespace).items
        else:
            return networkpolicies.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_roles(namespace: str = None) -> list[ResourceInstance]:
    try:
        roles = dyn_client.resources.get(api_version='rbac.authorization.k8s.io/v1', kind='Role')
        if namespace:
            return roles.get(namespace=namespace).items
        else:
            return roles.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_rolebindings(namespace: str = None) -> list[ResourceInstance]:
    try:
        rolebindings = dyn_client.resources.get(api_version='rbac.authorization.k8s.io/v1', kind='RoleBinding')
        if namespace:
            return rolebindings.get(namespace=namespace).items
        else:
            return rolebindings.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []   
    
def get_clusterroles() -> list[ResourceInstance]:
    try:
        clusterroles = dyn_client.resources.get(api_version='rbac.authorization.k8s.io/v1', kind='ClusterRole')
        return clusterroles.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_clusterrolebindings() -> list[ResourceInstance]:
    try:
        clusterrolebindings = dyn_client.resources.get(api_version='rbac.authorization.k8s.io/v1', kind='ClusterRoleBinding')
        return clusterrolebindings.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_events(namespace: str = None) -> list[ResourceInstance]:
    try:
        events = dyn_client.resources.get(api_version='v1', kind='Event')
        if namespace:
            return events.get(namespace=namespace).items
        else:
            return events.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_ingressclasses() -> list[ResourceInstance]:
    try:
        ingressclasses = dyn_client.resources.get(api_version='networking.k8s.io/v1', kind='IngressClass')
        return ingressclasses.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_storageclasses() -> list[ResourceInstance]:
    try:
        storageclasses = dyn_client.resources.get(api_version='storage.k8s.io/v1', kind='StorageClass')
        return storageclasses.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_resource_quota(namespace: str = None) -> list[ResourceInstance]:
    try:
        resource_quota = dyn_client.resources.get(api_version='v1', kind='ResourceQuota')
        if namespace:
            return resource_quota.get(namespace=namespace).items
        else:
            return resource_quota.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_limit_ranges(namespace: str = None) -> list[ResourceInstance]:
    try:
        limit_ranges = dyn_client.resources.get(api_version='v1', kind='LimitRange')
        if namespace:
            return limit_ranges.get(namespace=namespace).items
        else:
            return limit_ranges.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_serviceaccounts(namespace: str = None) -> list[ResourceInstance]:
    try:
        serviceaccounts = dyn_client.resources.get(api_version='v1', kind='ServiceAccount')
        if namespace:
            return serviceaccounts.get(namespace=namespace).items
        else:
            return serviceaccounts.get().items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_resource_by_name(resource_type: str, name: str, namespace: str = None) -> ResourceInstance:
    try:
        resource = dyn_client.resources.get(api_version='v1', kind=resource_type)
        if namespace:
            return resource.get(name=name, namespace=namespace)
        else:
            return resource.get(name=name)
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return None
    
def get_resource_by_label(resource_type: str, label_selector: str, namespace: str = None) -> list[ResourceInstance]:
    try:
        resource = dyn_client.resources.get(api_version='v1', kind=resource_type)
        if namespace:
            return resource.get(label_selector=label_selector, namespace=namespace).items
        else:
            return resource.get(label_selector=label_selector).items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []
    
def get_resource_by_field(resource_type: str, field_selector: str, namespace: str = None) -> list[ResourceInstance]:
    try:
        resource = dyn_client.resources.get(api_version='v1', kind=resource_type)
        if namespace:
            return resource.get(field_selector=field_selector, namespace=namespace).items
        else:
            return resource.get(field_selector=field_selector).items
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return []

def get_resource_by_name_and_namespace(resource_type: str, name: str, namespace: str) -> ResourceInstance:
    try:
        resource = dyn_client.resources.get(api_version='v1', kind=resource_type)
        return resource.get(name=name, namespace=namespace)
    except client.exceptions.ApiException as e:
        print(f"An error occurred: {e}")
        return None
    

