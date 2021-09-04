# Types of pipelines

## Data injestions and transformation pipelines

## Preprocessing Pipelines
* Feature Engineering
    example : https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-interpretability-aml#raw-feature-transformations


## Training Pipeline


## Deployment Pipeline
* Score.py
* Selection criteria and choosing the best models

## [Upon submitting a pipeline](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-create-machine-learning-pipelines#submit-the-pipeline)
When you submit the pipeline, Azure Machine Learning checks the dependencies for each step and uploads a snapshot of the source directory you specified. If no source directory is specified, the current local directory is uploaded. The snapshot is also stored as part of the experiment in your workspace.

## Use Pipeline Parameter to pass values during pipeline run
* ```python
    from azureml.pipeline.core import PipelineParameter

    pipeline_param = PipelineParameter(name="pipeline_arg", default_value="default_val")
    train_step = PythonScriptStep(script_name="train.py",
                                arguments=["--param1", pipeline_param],
                                target=compute_target,
                                source_directory=project_folder)
    ```                            

* If you choose to use PipelineParameter objects to dynamically set variables at runtime for your pipeline steps,you must set the environment field of the RunConfiguration to an Environment object.


## Publish Pipelines

### Publish pipline
```python
published_pipeline = pipeline_run.publish_pipeline(
    name="diabetes-training-pipeline", description="Trains diabetes model", version="1.0")

published_pipeline
rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)
```

### Call endpoints
```python
from azureml.core.authentication import InteractiveLoginAuthentication

interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()
print("Authentication header ready.")
```

### Schedule
```python
rest_endpoint = published_pipeline.endpoint
print(rest_endpoint)
``` 

