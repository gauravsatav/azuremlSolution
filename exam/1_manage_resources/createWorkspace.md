# Exam


Create an Azure Machine Learning workspace
 create an Azure Machine Learning workspace
 configure workspace settings
 manage a workspace by using Azure Machine Learning studio


# [Create workspace and Manage workspace](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace?view=azure-ml-py&tabs=python)

## CLI
* Create resource group
az group create --name {} --location {}

* Create a workspace
    * If there are no existing resources
        az ml workspace create -w {} -g {}
        * -g is the resource group name


    * If there are existing resources
        az ml workspace create -w {} -g {} 
        * --acr {service-id}
        * --application-insights <service-id>
        * --keyvault {service-id}
        * --storage-account {service-id}

* get information
az ml workspace show -w {} -g {}

* update 
az ml workspace update

* share
az ml workspace share -w {} -g {} --user {} --role {}

* sync-keys
az ml workspace sync-keys 

## Python SDK

* [Create Workspace and manage workspace](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace?view=azure-ml-py&tabs=python)
```python

# Create New
from azureml.core import Workspace

ws = Workspace.create(name='',
                subscription_id='',
                resouce_group='',
                create_resource_group = ''
                location = ''
                )

# Multiple tenet
from azureml.core.authentication import InteractiveLoginAuthentication
interactiveAuth = InteractiveLoginAuthentication("tenent-id") #pass this to the ws.create() command

# Use existing resources
from azureml.core.authenticaiton import ServicePrincipalAuthentication

servicePrincipal = ServicePrincipalAuthentication(      #Pass this to the auth along with resources names.
    tenant_id="<tenant-id>",
    username="<application-id>",
    password=service_principal_password)
```
* Connect to workspace
```python
from azureml.core import Workspace

ws = Workspace.from_config()
```

## Portal

## REST

curl -X POST https://login.microsoftonline.com/{your-tenant-id}/oauth2/token \
-d "grant_type=client_credentials&resource=https%3A%2F%2Fmanagement.azure.com%2F&client_id={your-client-id}&client_secret={your-client-secret}" \
* Parameters 
    * tenant-id
    * client-id
    * client-secret
    
* Step 1:Retrieve a service principal authentication token
    * The response should provide an access token good for one hour:
    * Make note of the token, as you'll use it to authenticate all subsequent administrative requests. 
* Get a list of resource groups associated with your subscription
    * curl https://management.azure.com/subscriptions/{your-subscription-id}/resourceGroups?api-version=2019-11-01 -H "Authorization:Bearer {your-access-token}"

* Drill down into workspaces and their resources

* Create and modify resources using PUT and POST requests

* Use REST to score a deployed model

* Create a workspace using REST
