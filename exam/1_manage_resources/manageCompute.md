Manage compute for experiments in Azure Machine Learning
 determine the appropriate compute specifications for a training workload 
 create compute targets for experiments and training
 configure Attached Compute resources including Azure Databricks
 monitor compute utilization

Set up an Azure Machine Learning development environment
 create compute instances
 share compute instances
 access Azure Machine Learning workspaces from other development environments

# General Points
The host OS for compute cluster and compute instance has been Ubuntu 16.04 LTS. On April 30, 2021, Ubuntu is ending support for 16.04. Starting on March 15, 2021, Microsoft will automatically update the host OS to Ubuntu 18.04 LTS. 


# Attach differnt computes, you cannot create them only attach/use them as compute targets
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-attach-compute-targets#hdinsight

* In general instead of using `AmlCompute.provisioning_configuration` we use `xyz.attach_configuration({info of where this can be accesed like workspace, port, access tokens etc})`

* Then instead of `ComputeTarget.create(ws,yourName,config)` we use `ComputeTarget.attach(ws,yourName,config)`


# Remote VM
* AML Cannot create, only acesss it
* VM must be Azure DSVM
```python
from azureml.core.compute import RemoteCompute, ComputeTarget
attach_config = RemoteCompute.attach_configuration(resource_id='<resource_id>',
                                                ssh_port=22,
                                                username='<username>',
                                                password="<password>")
compute = ComputeTarget.attach(ws, compute_target_name, attach_config)
```

# Azure HD Insight

Azure HDInsight is a popular platform for big-data analytics. The platform provides Apache Spark, which can be used to train your model.
* AzureML cannot create it, it must be present already.
* To attach you'll require

```python
from azureml.core.compute import ComputeTarget, HDInsightCompute

HDInsightCompute.attach_configuration(resource_id='<resource_id>',
                                                      ssh_port=22, 
                                                      username='<ssh-username>', 
                                                      password='<ssh-pwd>')
```
## Azure Batch
BatchCompute.attach_configuration(
        resource_group=batch_resource_group, account_name=batch_account_name)
        
## Data Bricks
```python
attach_config = DatabricksCompute.attach_configuration(resource_group=databricks_resource_group,
                                                           workspace_name=databricks_workspace_name,
                                                           access_token=databricks_access_token)
databricks_compute = ComputeTarget.attach(
ws,
databricks_compute_name,
attach_config
)

databricks_compute.wait_for_completion(True)
```

## Azure Data Lake
AdlaCompute.attach_configuration(resource_group=adla_resource_group,
                                                     account_name=adla_account_name)
