# Table of content
- [Environment](#environment)
  * [What is Environment](#what-is-environment)
  * [How does Environment fit in with compute and training script to create run config architecture](#how-does-environment-fit-in-with-compute-and-training-script-to-create-run-config-architecture)
    + [Stepwise fit in experiment run](#stepwise-fit-in-experiment-run)
  * [Types of python environments based on who maintains em](#types-of-python-environments-based-on-who-maintains-em)
  * [Brief word on docker image and containers](#brief-word-on-docker-image-and-containers)
  * [Summary](#summary)
  * [Sample Environment json file](#sample-environment-json-file)



## Exam
Set up an Azure Machine Learning development environment
 create compute instances
 share compute instances
 access Azure Machine Learning workspaces from other development environments

## Environment
More Info : https://docs.microsoft.com/en-gb/azure/machine-learning/concept-environments


## What is Environment

Environment is isolating dependencies. In Azure ML these dependencies can be classified into 2 general categories.
1. Python dependencies
2. Non-Python dependencies (Environment Variables, Spark, Docker)

These dependencies are defined using `Environment` Class. The Environment Class has 4 sections

* python                        # NOT OPTIONAL (Not really, but you'll at least have to have one python package)
    * conda                     # Most popularly used. 
    * user defined              # Don't forget to include azureml-defaults package

* environment variables         # OPTIONAL
* docker                        # SET `**your-env-name**.docker.enabled = True`. Define additional dependencies, like os, etc.
* spark



## How does Environment fit in with compute and training script to create run config architecture

An environment is registered for a workspace and is registered independently from the compute. This means you can mix and match different environments, compute and script to create a runConfiguration for different purposes

The environment, compute target and training script together form the run configuration, inference configuration and deployment configuration : the full specification of a run.

When you register an environment it is saved in Container Registery associated with the workspace. (Service is called Azure Container Registery or ACR)
* If you've enabled docker, then it is saved as a docker image.
* If docker is disabled then the environment (conda/user managed) is created directly in the compute target.

Workspace ---> linked to independent service ----> Container Registery (Storing Environments in the form of containers)
          ---> linked to independent service ----> Storage Account (Datastores,Datasets,Experiment Run Output Files and logs,
                                                     Individual Pipeline Step output (intermediate and output files) and logs,
                                                     batch inferencing, capture data made to deployed model services, data drift)
          ---> linked to independent service ----> Key Vault
          ---> linked to independent service ----> Application Insight (Model Monitoring)
          ---> linked to independent service ----> 


### Stepwise fit in experiment run

* When you first define `RunConfiguration()` and submit a remote run using an environment, the Azure Machine Learning service invokes an ACR Build Task on the Azure Container Registry (ACR) associated with the Workspace. 

* The built Docker image is then cached on the Workspace ACR. 

* Curated environments are backed by Docker images that are cached in Global ACR. 

* At the start of the run execution, the image is retrieved by the compute target from the relevant ACR.

* For local runs, a Docker or Conda environment is created based on the environment definition. The scripts are then executed on the target compute - a local runtime environment or local Docker engine.

## Types of python environments based on who maintains em

* Curated : Pre-packaged environments provided and maintained by AzureML. 
    * AzureML-Pytorch1.7-Cuda11-OpenMpi4.1.0-py36
    * AzureML-Scikit-learn0.20.4-Cuda11-OpenMpi4.1.0-py36
    * AzureML-TensorFlow2.4-Cuda11-OpenMpi4.1.0-py36
    * Full list : https://docs.microsoft.com/en-gb/azure/machine-learning/resource-curated-environments

* User Managed
    * Remember to mention azureml-defaults with version >= 1.0.45 as pip dependency.

* System Managed
    * Managed by conda. These dependencies can be defined using steps
        * Set `**your-env-name**.python.user_managed_dependencies=False`.
        * Define Conda dependencies in 2 parts `CondaDependencies.create(conda_packages=['pip'],pip_packages=[]`
        * Add these to `**your-env-name**.python.conda_dependencies`
        * Define conda dependency in yml file. [More Info](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#sharing-an-environment)


## Where to save input files
* AML takes the snapshot of your source directory
* Add files to `.gitignore` or `.amlignore` if you don't want your file to get uploaded to experiment
* The file size of the source directory should not be more than 300MB and/or 2000 files
* Mostly try to use datasets and datastore

## Where to write output files
* Writing to `./outputs` and `./logs` folder
    * These 2 folder receive special treatment

* Write to cloud storage by mounting the remote storage using [`OutputFileDatasetConfig`](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-save-write-experiment-files#where-to-write-files) object.
    * once this output config is created pass this config to `ScriptRunConfig` at run time and make use of the location in the `training.py` script.

## Brief word on docker image and containers

A docker is a program like the hypervisor (but not really) that isolates an application from which os/hardware/environment it is running on.

It acts like a translator between the application and the host os such that we can swap one host os with another without having to
change our application code.

Docker Image is immutable (cannot be changed) package. Following components are added to construct this image. These components are 
available on [docker hub](https://hub.docker.com/)

* `base image` : A base image can be os like linux,ubuntu,alpine(smallest in size linux distr)
               There are also a lot of custom images developed by folks like NVIDIA called `cuda` and lot more
               available [here](https://github.com/Azure/AzureML-Containers)

* To this base image you add any additional dependencies like in our case conda env, python env (These can be called software dependencies)

* Even more dependencies can be added by specifying them in the `Dockerfile` file.

* Then you run a docker command to build this image. 
The image will be built step by step as defined in `Dockerfile`, eg step 1 will be loading the base image, step 2: installing conda and so on and so forth adding one step, checkpointing, adding next step, deleting previous step 1, checkpointing step 2 and so on with step 3,4,5.

* Once the image is built (it can range from few MB in size to few GB) you can now distribute this image to others.

* For them to run the image (the created environment is then run on the selected compute target either while training or while inferencing), they'll have to run another docker command this will run the image in a `container`

* [Youtube Video 1](https://www.youtube.com/watch?v=i7ABlHngi1Q)

* [Youtube Video 2](https://www.youtube.com/watch?v=hnxI-K10auY)

## Summary

* Environment specify the Python packages, environment variables, and software settings around your training and scoring scripts.

* They also specify run times (Python, Spark, or Docker). Check the json file below to see all the different parameters which we can specify

* The environments are managed and versioned entities within your Machine Learning workspace 

* They enable reproducible, auditable, and portable machine learning workflows across a variety of compute targets.

You can use an Environment object on your local compute to:

Develop your training script.
Reuse the same environment on Azure Machine Learning Compute for model training at scale.
Deploy your model with that same environment.
Revisit the environment in which an existing model was trained.

* With versioning, you can see changes to your environments over time, which ensures reproducibility.

* You can build Docker images automatically from your environments.


More information on how to configure local environment:
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-configure-environment


## Sample Environment json file

<details>
<summary> Sample json file </summary>

```json
{
    "name": "azureEntropy",
    "version": "1",
    "python": {
        "interpreterPath": "python",
        "userManagedDependencies": false,
        "condaDependencies": {
            "channels": [
                "anaconda",
                "conda-forge"
            ],
            "dependencies": [
                "python=3.6.2",
                {
                    "pip": [
                        "azureml-defaults~=1.27.0",
                        "pyarrow",
                        "azureml-dataprep[fuse]",
                        "azureml-interpret~=1.27.0"
                    ]
                },
                "scikit-learn",
                "ipykernel",
                "matplotlib",
                "pandas",
                "pip"
            ],
            "name": "azureml_4a1a93529aaa38bbaad0e5d6ae5a859a"
        },
        "baseCondaEnvironment": null
    },
    "environmentVariables": {
        "EXAMPLE_ENV_VAR": "EXAMPLE_VALUE"
    },
    "docker": {
        "baseImage": "mcr.microsoft.com/azureml/intelmpi2018.3-ubuntu16.04:20210301.v1",
        "platform": {
            "os": "Linux",
            "architecture": "amd64"
        },
        "baseDockerfile": null,
        "baseImageRegistry": {
            "address": null,
            "username": null,
            "password": null
        },
        "enabled": true,
        "arguments": []
    },
    "spark": {
        "repositories": [],
        "packages": [],
        "precachePackages": true
    },
    "inferencingStackVersion": null
}
```
</details>