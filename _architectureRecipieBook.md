## Project Definition

### Purpose

### Benefitting Personas and benefit walk through for each persona

### Scale and Scope

* How many users and at what rate will they be growing per month

* Scale of data required 

* Compute required (How fast, how frequent)


### Cost constrains
More Info : https://docs.microsoft.com/en-gb/azure/machine-learning/concept-plan-manage-cost





## Authentication Roles and Security
### How to connect to workspace
* Interactive: Person authenticating via browser, it checks its credentials in Azure Active Directory

* Service Principle: For script trying to connect. Some Automation Process etc.

* Managed Identity: Adding Trusted Machines, like specific VM's

### Roles Azure RBAC

### Network Security

### Data Protection


## MLOps
[More Info](https://docs.microsoft.com/en-gb/azure/machine-learning/concept-model-management-and-deployment)
Machine Learning Operations (MLOps) is based on DevOps principles and practices that increase the efficiency of workflows. For example, continuous integration, delivery, and deployment. MLOps applies these principles to the machine learning process, with the goal of:
* Faster experimentation and development of models
* Faster deployment of models into production
* Quality assurance

### Create reproducible ML pipelines. 
Machine Learning pipelines allow you to define repeatable and reusable steps for your data preparation, training, and scoring processes.

### Create reusable software environments for training and deploying models.

### Register, package, and deploy models from anywhere. 
You can also track associated metadata required to use the model.

* Register and track ML models : Model registration allows you to store and version your models in the Azure cloud, in your workspace. The model registry makes it easy to organize and keep track of your trained models.

* Profile models : when you deploy your model, profiling tests the service that runs your model and returns information such as the CPU usage, memory usage, and response latency. It also provides a CPU and memory recommendation based on the resource usage.

* Package and debug models : Before deploying a model into production, it is packaged into a Docker image. In most cases, image creation happens automatically in the background during deployment. You can manually specify the image.

* Convert and optimize models : Converting your model to Open Neural Network Exchange (ONNX) may improve performance. On average, converting to ONNX can yield a 2x performance increase.

* Use models : Trained machine learning models are deployed as web services in the cloud or locally or on IOT Edge devices.
    * Batch Scoring : Batch scoring is supported through ML pipelines.
    * Real-time web services : Deploy on ACI, AKS, Locally
    * Controlled Rollouts : (Only in AKS) Perform A/B Testing, etc
    * IOT Edge Devices : You can use models with IoT devices through Azure IoT Edge modules. IoT Edge modules are deployed to a hardware device, which enables  inference, or model scoring, on the device.
    * Analytics : Integrate with Power BI

### Capture the governance data for the end-to-end ML lifecycle.
The logged information can include who is publishing models, why changes were made, and when models were deployed or used in production.
Azure ML gives you the capability to track the end-to-end audit trail of all of your ML assets by using metadata.

* Integrates with git
* Datasets help track,profile and version.
* Interpretability
* Run history
* Azure ML Model Registry captures all of the metadata associated with your model
* Integration with Azure allows you to act on events in the ML lifecycle. For example, model registration, deployment, data drift, and training (run) events.


### Notify and alert on events in the ML lifecycle.
* Azure ML publishes key events to Azure EventGrid, which can be used to notify and automate on events in the ML lifecycle.

### Monitor ML applications for operational and ML-related issues.
* Compare model inputs between training and inference, explore model-specific metrics, and provide monitoring and alerts on your ML infrastructure.
* For example, experiment completion, model registration, model deployment, and data drift detection.
* Monitor for operational & ML issues : Enable Data collection from models deployed as service.
* Retrain your model on new data : Based on data drift
* There is no universal answer to "How do I know if I should retrain?" but Azure ML event and monitoring tools previously discussed are good starting points for automation. Once you have decided to retrain, you should:    
    * Preprocess your data using a repeatable, automated process
    * Train your new model
    * Compare the outputs of your new model to those of your old model
    * Use predefined criteria to choose whether to replace your old model 
* A theme of the above steps is that your retraining should be automated, not ad hoc. Use Pipelines for this.

### Automate the end-to-end ML lifecycle with Azure Machine Learning and Azure Pipelines.
* Using pipelines allows you to frequently update models, test new models, and continuously roll out new ML models alongside your other applications and services.
* You can use GitHub and Azure Pipelines to create a continuous integration process that trains a model.
    * A Data Scientist checks a change into the Git repo for a project
    * The Azure Pipeline will start a training run. 
    * The results of the run can then be inspected to see the performance characteristics of the trained model.
    * You can also create a pipeline that deploys the model as a web service.

## Data 

### Purpose or requirements

* Labelling and annotation

* Differential Privacy

* Training :

* Deploying Services
    * Batch Processing
    * Streaming
    * Collect data from deployed model service in production using `data collect`
        Check _deploymentChecklist.md document for more info.
        More Info : https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-enable-data-collection
        
        The output is saved in Blob storage at the following path
        * ```/modeldata/<subscriptionid>/<resourcegroup>/<workspace>/<webservice>/<model>/<version>/<designation>/<year>/<month>/<day>/data.csv```
        * example: 
        ```/modeldata/1a2b3c4d-5e6f-7g8h-9i10-j11k12l13m14/myresourcegrp/myWorkspace/aks-w-collv9/best_model/10/inputs/2018/12/31/data.csv```

* Monitor Data Drift.
    * Baseline Dataset
    * Target Dataset


### Data Solutions


Azure Storage Services ----> Datastore ----> Dataset


[Azure Storage Services](https://docs.microsoft.com/en-gb/azure/storage/common/storage-account-create?tabs=azure-portal)

Supported cloud-based storage services in Azure that can be registered as datastores:

* Azure Blob Container
* Azure File Share
* Azure Data Lake
* Azure Data Lake Gen2
* Azure SQL Database
* Azure Database for PostgreSQL
* Databricks File System
* Azure Database for MySQL

[Datastore](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.datastore.datastore?view=azure-ml-py): (Its a virtual entity which stores connection information to selected files saved on your Azure Storage Service)

* Represents a storage abstraction over an Azure Machine Learning storage account.

* Datastores are attached to workspaces and are used to store connection information to Azure storage services so you can refer to them by name and don't need to remember the connection information and secret used to connect to the storage services.


[Dataset](https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.dataset(class)?view=azure-ml-py)
* Datasets provide functions that load tabular data into a pandas or Spark DataFrame. 
* Datasets also provide the ability to download or mount files of any format from Azure Blob storage, Azure Files, Azure Data Lake Storage Gen1, Azure Data Lake Storage Gen2, Azure SQL Database, and Azure Database for PostgreSQL.

## Compute


### Purpose or requirements
In a typical model development lifecycle, you might:

* Start by developing and experimenting on a small amount of data. At this stage, use your local environment, such as a local computer or cloud-based virtual machine (VM), as your compute target.

* Scale up to larger data, or do distributed training by using one of these training compute targets.

* After your model is ready, deploy it to a web hosting environment or IoT device with one of these deployment compute targets.

More Info : https://docs.microsoft.com/en-us/azure/machine-learning/concept-compute-target

#### Training Compute Target - TCT

[How to choose compute target for training](https://docs.microsoft.com/en-gb/azure/machine-learning/concept-compute-target#train)

Training Constrains:

* Do you want Automated Machine Learning (Check list above to see which one is supported)
* Pipelines (ALl support it apart from local compute)
* Azure Machine Learning Designer (It is only supported by AzureML compute cluster)

#### Deployment or Inference Compute Targets - DICT

[How to choose a compute target](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-deploy-and-where?tabs=azcli#choose-a-compute-target)

Deployment Constrains:

* Throughput vs Latency (Batch Processing vs Real Time Service)

* Cost vs Availability (ACI vs AKS)

### Compute Solutions

A compute target is a designated compute resource or environment where you run your training script or host your service deployment.
"Compute Target" is the logical name given to a physical computing resource.
[What is a compute target?](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-compute-targets#whats-a-compute-target)
[How to attach compute targets](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-attach-compute-targets)


Only Specific Compute Resources can support the purposes/requirements mentioned above.
More Info : https://docs.microsoft.com/en-us/azure/machine-learning/concept-compute-target


-----LOCAL----- (TCT,DICT)

While Training : Your local computer : While configuring ScriptRunConfig(compute_target = 'local'). This will execute the runs locally.
During Deployment : When you use your local computer for inference, you must have Docker installed.
                    To perform the deployment, use LocalWebservice.deploy_configuration() to define the port that the web service will use. Then use the normal deployment process as described in Deploy models with Azure Machine Learning.
----CLOUD-----
There are 2 types of cloud compute which you can use as compute targets.

* Independent Offerings, not a part of Azure ML and will need to be managed seperately by you.

* For Training:
    * Remote virtual machines - (TCT) -  The VM must be an Azure Data Science Virtual Machine (DSVM).
    
    * Azure HDInsight - (TCT) - 
    
    * Azure Batch - (TCT) - 
    
    * Azure Databricks - (TCT) - 
    
    * Azure Data Lake Analytics - (TCT) - 

* For Deployment:
    
    * Azure Container Instance - (DICT) - `Choose this when prioritizing low latency over high throughput at a lower price and at cost of high availability` - Container instances are suitable only for small models less than 1 GB in size.

    * Azure App Service - (DICT) - This is currently in preview

    * Azure Functions - (DICT) - This is currently in preview

    * Azure Cognitive Search - (DICT) - This is currently in preview

    * Custom Docker Image - (DICT) - This is currently in preview

    * IOT Edge - (DICT) - This is currently in preview

    * FPGA Inference - (DICT) - This is currently in preview

* Managed by AzureMl -  A managed compute resource is created and managed by Azure Machine Learning.
                        This compute is optimized for machine learning workloads. Azure Machine Learning compute
                        clusters and compute instances are the only managed computes.
    
    * [Azure Machine Learning compute instance](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-create-manage-compute-instance?tabs=python) - (TCT, DICT) - This is a VM configured by AzureML with essential data science packages and tools. Although it can be used for deployment (this would be the same as deploying locally, see above for local deloyment) it is not recommended.

    * [Azure Machine Learning compute cluster](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-create-attach-compute-cluster?tabs=python#what-is-a-compute-cluster) - (TCT, DICT) - `Prioritizing throughput over low latency.`

    * Azure Kubernetes Service cluster - (DICT) - You can deploy it with different base images depending on performance.
        * `Low Latency and high throughput then choose NVIDIA GPS's`
        * `Low Latency and high availability but low throughput then choose Azure Kubernets CPU`



















## Environment

### Purpose or requirements

Decide on the python package, os, or custom apps and databases (like neo4j, django, node, etc) required during each step.

* Training 

* Inferencing : This should generally contain python packages like sklearn as the basic job of inferencing is to use its  `predict` method. This configuration is stored in a `*.yml` file and is saved in the folder for the service along with the scoring script.


### Environment Decisions

* Local Environment managed by creating a python virtual environment. Read more docs

* Decide on who'll manage the dependencies

* If not user managed, then you can choose either `Anaconda` to manage or choose one of the `curated environments` provided by AzureML

* Decide if you want to enable a docker version of it. If you do decide to enable it you can add a lot more dependecies and control
the environment even more finely, like choosing the os to run, etc. 
Also you get the option of choose from a host of `base images` offered by AzureMl and also available on docker hub.

### Container Registery
Once you decide to register the environment, it will be saved to the Azure Container Registery associated with the workspace.
This can be expensive.

## Experiments 

### Check ONNX Models
* Get ONNX models
    * Train a new ONNX model in Azure Machine Learning (see examples at the bottom of this article) or by using automated Machine Learning capabilities
    * Convert existing model from another format to ONNX (see the tutorials)
    * Get a pre-trained ONNX model from the ONNX Model Zoo
    * Generate a customized ONNX model from Azure Custom Vision service

* Deploy ONNX models in Azure
    * Install and use ONNX Runtime with Python
    * 



### AutoMl


### Simple Experiment


### Hyperparameter Tuning Experiment


## Pipelines
### Publish Pipeline

* Standalone Experiment
* Pipeline Type:
    * Custom Model Pipeline
        * Simple Experiment Pipeline
        * Hyperparameter Pipeline
    * AutoML Pipeline
    * Data Drift Monitor Pipeline


### Fairness




## Deployment

### Purpose or requirements

* Real Time Service

* Monitor Model Service, Application Insight Service

* Batch Service

### WebService Solutions

## Security

### Azure Security Baseline
[Full Info](https://docs.microsoft.com/en-gb/security/benchmark/azure/baselines/machine-learning-security-baseline?context=/azure/machine-learning/context/ml-context)
* Network Security
    * 1.1: Protect Azure resources within virtual networks
    * 1.2: Monitor and log the configuration and traffic of virtual networks, subnets, and NICs
    * 1.3: Protect critical web applications
    * 1.4: Deny communications with known malicious IP addresses
    * 1.5: Record network packets
    * 1.6: Deploy network-based intrusion detection/intrusion prevention systems (IDS/IPS)
    * 1.8: Minimize complexity and administrative overhead of network security rules
    * 1.9: Maintain standard security configurations for network devices
    * 1.10: Document traffic configuration rules

* Logging and Monitoring

* Identity and Access Control

* Data Protection

* Vulnerability Management

* Inventory and Asset Management

* Secure Configuration

* Malware Defense

* Data Recovery

* Incident Response

* Penetration Tests and Red Team Exercises


### Restrict access to resources and operations by user account or groups
Azure Active Directory (Azure AD) is the identity service provider for Azure Machine Learning.


### Restrict incoming and outgoing network communications
* To restrict network access to Azure Machine Learning resources, you can use Azure Virtual Network (VNet).

### Encrypt data in transit and at rest
* Encryption at rest
    * Azure Blob storage
    * Azure Cosmos DB
    * Azure Container Registry
    * Azure Container Instance
    * Azure Kubernetes Service
    * Machine Learning Compute
    * Azure Databricks

* Encryption in transit
    * Azure Machine Learning uses TLS to secure internal communication between various Azure Machine Learning microservices. All Azure Storage access also occurs over a secure channel.

* Data collection and handling: 
    Microsoft collected data. Microsoft may collect non-user identifying information like resource names (for example the dataset name, or the machine learning experiment name), or job environment variables for diagnostic purposes.

* Using Azure Key Vault : Azure Machine Learning uses the Azure Key Vault instance associated with the workspace to store credentials of various kinds
    * The associated storage account connection string
    * Passwords to Azure Container Repository instances
    * Connection strings to data stores

SSH passwords and keys to compute targets like Azure HDInsight and VMs are stored in a separate key vault that's associated with the Microsoft subscription. Azure Machine Learning doesn't store any passwords or keys provided by users. Instead, it generates, authorizes, and stores its own SSH keys to connect to VMs and HDInsight to run the experiments.

Each workspace has an associated system-assigned managed identity that has the same name as the workspace.

### Scan for vulnerabilities
* Azure Security Center : Provides unified security management and advanced threat protection across hybrid cloud workloads.

* For Azure machine learning, you should enable scanning of your Azure Container Registry resource and Azure Kubernetes Service resources.

### Apply and audit configuration policies
* Azure Policy is a governance tool that allows you to ensure that Azure resources are compliant with your policies.
