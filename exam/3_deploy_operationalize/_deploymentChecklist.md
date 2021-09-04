# Model webservice
Your webservice is the name given to your deployment. An endpoint is the address from where this service (deployment) can then be interacted with.
See the steps necessary to be defined for your deployment below.



# [What are endpoints and deployments](https://docs.microsoft.com/en-gb/azure/machine-learning/concept-endpoints):

## Endpoint
An Endpoint is an HTTPS endpoint that clients can call to receive the inferencing (scoring) output of a trained model. It provides:
* Authentication using 'key & token' based auth
* SSL termination
* Traffic allocation between deployments
* A stable scoring URI (endpoint-name.region.inference.ml.azure.com)
* 2 Types of endpoints: [comparison](https://docs.microsoft.com/en-gb/azure/machine-learning/concept-endpoints#managed-online-endpoints-vs-aks-online-endpoints-preview)
    * Online Endpoints (used for real-time)
        * Managed Online.
            * Compute_type: Managed AmlCompute, For: More control on deployment. Infra management is done by azure.
        * AKS Online Endpoint.
            * Compute_type: AKS, For: Who prefers AKS and can manage Infra

    * Batch Endpoints:
        * Batch endpoints receive pointers to data and run jobs asynchronously to process the data in parallel on compute clusters. Batch endpoints store outputs to a data store for further analysis.
        
A single endpoint can contain multiple deployments. Endpoints and deployments are independent ARM (Azure Resource Manager) resources that will appear in the Azure portal. Azure Machine Learning uses the concept of endpoints and deployments to implement different types of endpoints: online endpoints and batch endpoints.

## Deployment
A Deployment is a set of compute resources hosting the model that performs the actual inferencing. It contains:

* Model details (code, model, environment)
* Compute resource and scale settings
* Advanced settings (like request and probe settings)

# Deployment Lifecycle Management
[Native blue/green deployment](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-safely-rollout-managed-endpoints)

A single endpoint can have multiple deployments. The online endpoint can perform load balancing to allocate any percentage of traffic to each deployment.
* Deploy a new online endpoint called "blue" that serves version 1 of the model
* Scale this deployment so that it can handle more requests
* Deploy version 2 of the model to an endpoint called "green" that accepts no live traffic
* Test the green deployment in isolation
* Send 10% of live traffic to the green deployment
* Fully cut-over all live traffic to the green deployment
* Delete the now-unused v1 blue deployment

# Online or real time endpoints

## Deploy Managed Online and AKS Endpoints using CLI
Managed online endpoints (preview) provide you the ability to deploy your model without your having to create and manage the underlying infrastructure.

### Prerequisites
* Subscription
* Latest CLI
* `Contributor` access rights
* If deploying locally, then installed `Docker engine`.

### Define the endpoint/deployment configuration

* There are 2 options to define your deployment configuration
    * Managed Online Endpoints
    * AKS

* Depending on the type selected above choose the compute_target and the respective `yml` file.

* The inputs needed to deploy a model on an online endpoint are:
    * Model files (or the name and version of a model already registered in your workspace). In the example, we have a scikit-learn model that does regression. You can create and register an explainability model.
    * Code that is needed to score the model. In this case, we have a score.py file.
    * An environment in which your model is run (as you'll see, the environment may be a Docker image with conda dependencies or may be a Dockerfile).
    * Settings to specify the instance type and scaling capacity.

* These have to be saved into a `yml` file it must contain information about
    * Model : Register model and environment seperately
    * Conda dependencies : 
    * Environmet : name,version,path,docker_image
    * Compute Instance Type : 
    * Scale Settings : 
    * [Example configuration](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-deploy-managed-online-endpoints#define-the-endpoint-configuration)


### Scoring script
* Structure:
    * `init()` function:
        * Called when container is initialized.
        * This initialization typically occurs shortly after the deployment is created or updated.
        * Write logic here to do global initialization operations like caching the model in memory.
        * You can import following models
            * Original Prediction Model
            * Explainability Model
    * `run()` function:
        * Called for every invocation of the endpoint and should do the actual scoring/prediction. 

* [Interpretability at time of inference](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-interpretability-aml#interpretability-at-inference-time)


### Deploy and debug locally using local endpoints
* Local endpoints do not support traffic rules, authentication, scale settings, or probe settings.

* Local endpoints only support one deployment per endpoint. That is, in a local deployment you cannot use a reference to a model or environment registered in your Azure machine learning workspace.

* There's a cli command to do the following. Each of this is preceeded by the `--local` parameter
    * Deploy locally using command

    * Check if the local deployment succeeded

    * Invoke the local endpoint to score data with your model

    * Review the logs for output from the invoke operation

### Deploy your managed online endpoint to Azure

* A similart set of commands exist to deploy on azure, only this time use the `$ENDPOINT_NAME` instead of `--local` option. where $ENDPOINT_NAME is the name you have to define before.

* Use `invoke` command or REST Client of choice to invoke an endpoint and score new data.

* `get-logs` to see previous invocations


* Using REST you'll requie both
    * `show` command to get scoring_uri
    * `get-credentials` to get auth information

### Update deployment
To scale up or change deployment

* Update the `yml` file

* run the `az ml endpoint update` command.

* You can only modify one aspect (traffic, scale settings, code, model, or environment) in a single update command.

### Delete the endpoint and deployment
Use following command to delete the endpoint

* az ml endpoint delete -n $ENDPOINT_NAME --yes --no-wait

## Other Notes

More Info : https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-deploy-and-where?tabs=azcli


The workflow is similar no matter where you deploy your model:

* Register the model

* Prepare an entry script

* Prepare an inference configuration (Describes the docker image, conda dependencies etc. Basically this is the environment you saved in ACR. Save this in a .yml file containing the entry script above. While building up the env on the compute as defined in deployment configuration, it will check if an environment of the same configuration exist in ACR. if yes then it will use it if no then it'll create a new env.)

* [Create a Deployment Configuration](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-deploy-and-where?tabs=python#define-a-deployment-configuration)
    * Choose a compute target
        * Local
        * Deploy the model locally to ensure everything works
    * The options available for a deployment configuration differ depending on the compute target you choose.
    * 

```python
service = Model.deploy(
    ws,
    "myservice",
    [model],
    dummy_inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)
```


Re-deploy the model to the cloud

Test the resulting web service



### Deploy Model Locally

* Local WebService : Create a local docker webservice
        More Info @ : https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.webservice.local.localwebservice?view=azure-ml-py#deploy-configuration-port-none-



### Do you want to collect data back from the deployed model service in production

[scriptHere](C:\Users\GauravSatav\Desktop\Certifications and Courses\Azure\azuremlSolution\expr_1_realTimeService.py)

This has to be enabled:

* Make changes to the scoring file and adding lines of code. Read the article below.
* Set data collection to TRUE when deploying using AKSWebservice.deploy_configuration()
* Add the 'Azure-Monitoring' pip package to the conda-dependencies of the web service environment

More Info : https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-enable-data-collection

The output is saved in Blob storage at the following path
* /modeldata/<subscriptionid>/<resourcegroup>/<workspace>/<webservice>/<model>/<version>/<designation>/<year>/<month>/<day>/data.csv

example: /modeldata/1a2b3c4d-5e6f-7g8h-9i10-j11k12l13m14/myresourcegrp/myWorkspace/aks-w-collv9/best_model/10/inputs/2018/12/31/data.csv



### Consume and test an Azure Machine Learning model deployed as a web service
More Info : https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-consume-web-service?tabs=python

The general workflow for creating a client that uses a machine learning web service is:

Use the SDK to get the connection information.
Determine the type of request data used by the model.
Create an application that calls the web service.

# Batch Endpoints

* Define the following before deployment:
    * Model files (or specify a registered model in your workspace)
    * Compute target
    * Scoring script - code needed to perform scoring/inferencing (no need to define in case deployment is from mlflow)
    * Environment - a Docker image with Conda dependencies (no need to define in case deployment is from mlflow)

## Prerequisites
* Subscription
* Azure CLI version >=2.15.0

## Create a compute target
* Batch scoring runs only on cloud computing resources, not locally.
* Create a general purpose AmlCompute target.
* To reduce cost, while creating deployments (see next step) in the yml file define scaling to be `auto scaling` and other settings can be over-ridden (see ways to start a batch scoring job below) using mini-batch and other parameters.

## Create a batch endpoint
* This is where you define your deployment.
* If you're using an MLflow model, you can use no-code batch endpoint creation. You'll need to create an yml file.
```shell
az ml endpoint create --type batch --file cli/endpoints/batch/create-batch-endpoint.yml
```
* 

## Check batch endpoint details
* After a batch endpoint is created, you can use show to check the details. Use the --query parameter to get only specific attributes from the returned data.

## Start a batch scoring job using CLI
There are 2 ways to stat a scoring job:
* CLI
* REST
### CLI
* A batch scoring workload runs as an offline job.
* Define input locations:
    * Registered data (File Dataset) : Use parameter `--input-data`
    * Data in cloud storage, but not registered (Datastore). : Use parameter `--input-datastore`
    * Data on public website : Use parameter `--input-path`
    * Local : Use parameter `--input-local-path`
* Some settings can be overwritten when you start a batch scoring job to make best use of the compute resource and to improve performance:
    * Use --mini-batch-size to overwrite mini_batch_size if different size of input data is used.
    * Use --instance-count to overwrite instance_count if different compute resource is needed for this job.
    * Use --set to overwrite other settings including max_retries, timeout, and error_threshold.

### REST
* Get Scoring URI
* Get Access Token
* Use the scoring_uri, the access token, and JSON data to POST a request and start a batch scoring job

## Check batch scoring job execution progress
* invoke : get job name (the value returned is `interactionEndpoints.Studio.endpoint`)
* job show : check details and status
* job stream : to stream job

## Check batch scoring results
* Batch Scoring output can be access from the `./outputs` folder as a `predictions.txt` file
* The `./outputs` folder can be saved locally or on the blob storage, where its name will be under the parent folder having number `interactionEndpoints.Studio.endpoint`

## Add a deployment to the batch endpoint
* One batch endpoint can have multiple deployments. Each deployment hosts one model for batch scoring.
* Create a new yml file for the new deployment and then run the following command.
```shell
az ml endpoint update --name mybatchedp --type batch --deployment-file cli/endpoints/batch/add-deployment.yml
```
* Activate the new deployment.
    * Select the amount of traffic to be sent (This will always be 100% in case of batch deployment)
    * ```shell az ml endpoint update --name mybatchedp --type batch --traffic mnist-deployment:100```

## Security
* Authentication: Azure Active Directory Tokens
* SSL by default for endpoint invocation




## Azure Kubernet Service Cluster

[Microservices and Kubernetes](https://www.youtube.com/watch?v=1xo-0gCVhTU)
