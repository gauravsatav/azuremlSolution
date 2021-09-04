# Implement security and access control in Azure Machine Learning

### Exam Syllabus
Implement security and access control in Azure Machine Learning
 determine access requirements and map requirements to built-in roles
 create custom roles
 manage role membership
 manage credentials by using Azure Key Vault

* determine access requirements and map requirements to built-in roles


* create custom roles


* manage role membership


* manage credentials by using Azure Key Vault

### How to connect to workspace - Authentication Workflows
All the authentication workflows for your workspace rely on Azure Active Directory.

* Interactive: Person authenticating via browser, it checks its credentials in Azure Active Directory

* Service Principle: For script trying to connect. Some Automation Process etc.

* Managed Identity: Adding Trusted Machines, like specific VM's. 
    * Managed identity is only supported when using the Azure Machine Learning SDK from an Azure Virtual Machine or with an Azure Machine Learning compute cluster.
    * While creating VM just choose to keep managed identity `ON`

### Roles Azure RBAC
* Once you're able to access, what you can use within the workspace is controlled by Azure Rule Based Access Control

* For each entity in Azure Active Directory you'll have to assign a role.

* Azure Machine Learning relies on other services like Storage Account, AKS while deployment, ACR. Each of these will have their own Azure RBAC config

* Default roles
    * Reader
    * Contributor
    * Owner
    * Custom Roles : Create a `.json` file in specified [format](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-assign-roles#create-custom-role)

```shell
az role definition create --role-definition data_scientist_role.json
```

* After deployment, this role becomes available in the specified workspace. Now you can add and assign this role in the Azure portal. Or, you can assign this role to a user by using the az ml workspace share CLI command:

```shell
az ml workspace share -w my_workspace -g my_resource_group --role "Data Scientist" --user jdoe@contoson.com
```
* To update role
```shell
az role definition update --role-definition update_def.json --subscription <sub-id>
```

* [RBAC provided to Managed Roles for ACR and Storage](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-use-managed-identities?tabs=python)
    * If we don't bring our own ACR, Azure ML will create one for us.
    * While creating ACR don't enable `admin` role.

* The Azure AD Pod Identity project allows applications to access cloud resources securely with Azure AD by using a Managed Identity and Kubernetes primitives. This allows your web service to securely access your Azure resources without having to embed credentials or manage tokens directly inside your score.py script. 

### [Network Security](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-network-security-overview)

*  Secure the workspace and associated resources.
    * Create a private link : Azure Private Link lets you connect to your workspace using a private endpoint.
        * Create a workspace that uses a private endpoint : This will create a new `vnet`
        * Add private endpoint to this workspace
        * You can enable public access later, the private rules will still remain intact.
    * Secure Azure storage accounts with either a service endpoints or a private endpoint.
        * Service Endpoint: Proceed to the network setting page of storage account and allow access from selected networks and add the existing `vnet` link which was created above also Allow trusted Microsoft services to access this storage account
        * Private Endpoints: If the storage account uses private endpoints, you must configure two private endpoints for your default storage account:
            * A private endpoint with a blob target subresource.
            * A private endpoint with a file target subresource (fileshare).

    * Secure datastores and datasets
        * Disable data validation : If the data is behind a virtual network, Azure Machine Learning can't complete these checks. To bypass this check, you must create datastores and datasets that skip validation. While creating both datasets and datastores set `skip_validation=True`

    * Secure Azure Key Vault: 
        * Azure Machine Learning uses an associated Key Vault instance to store the following credentials:
            * The associated storage account connection string
            * Passwords to Azure Container Repository instances
            * Connection strings to data stores
        * Similar to storage account add the `vnet` to Key vault

    * Enable Azure Container Registry (ACR)
        * Pre-requisites:
            * Must be premium version
            * Must be in same `vnet` as storage and key-vault
            * Azure ml must contain a compute cluster
        * Similar to storage account add the `vnet` to Key vault
    
*  [Secure the training environment](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-network-security-overview#secure-the-training-environment)
    * Create an Azure Machine Learning compute instance and computer cluster in the virtual network to run the training job.

    * Allow inbound communication from Azure Batch Service so that Batch Service can submit jobs to your compute resources.
        * Inbound TCP traffic on ports 29876 and 29877 from a Service Tag of BatchNodeManagement. Traffic over these ports is encrypted and is used by Azure Batch for scheduler/node communication.
        
    * Limitations : Azure Compute Instance and Azure Compute Clusters must be in the same VNet, region, and subscription as the workspace and its associated resources.

*  Secure the inferencing environment.
    * You have two options for AKS clusters in a virtual network:
        
        * Deploy or attach a default AKS cluster to your VNet: have a control plane with public IP addresses. You can add a default AKS cluster to your VNet during the deployment or attach a cluster after it's created.
        
        * Attach a private AKS cluster to your VNet: have a control plane, which can only be accessed through private IPs. Private AKS clusters must be attached after the cluster is created.
    
    * Limitations : Azure Compute Instance and Azure Compute Clusters must be in the same VNet, region, and subscription as the workspace and its associated resources.

*  Optionally: enable studio functionality.
    * Just enable public access, your private endpoints will remain intact

*  Configure firewall settings.

*  Configure DNS name resolution.

### Data Protection
