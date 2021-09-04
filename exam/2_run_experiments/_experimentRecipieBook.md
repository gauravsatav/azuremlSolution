# What happens when you submit an experiment (training):
[original](https://docs.microsoft.com/en-gb/azure/machine-learning/concept-train-machine-learning-model#understand-what-happens-when-you-submit-a-training-job)

The Azure training lifecycle consists of:

1. Zipping the files in your project folder, ignoring those specified in .amlignore or .gitignore
2. Scaling up your compute cluster
3. Building or downloading the dockerfileto thecompute node
    * The system calculates a hash of:
            * The baseimage
            * Custom docker steps (see Deploy a model using a custom Docker baseimage)
            * The conda definition YAML (see Create & usesoftwareenvironments in Azure Machine Learning)
    * The system uses this hash as the key in a lookup of the workspace Azure Container Registry (ACR)
    * If it is not found, it looks for a match in the global ACR
    * If it is not found, thesystem builds a new image(which will becached and registered with the workspace ACR)
4. Downloading your zipped project file to temporary storage on thecompute node
5. Unzipping the project file
6. The compute node executing python <entry script> <arguments>
7. Saving logs, model files,and other files written to ./outputs to the storage account associated with the workspace
8. Scaling down compute, including removing temporary storage
    

If you choose to train on your local machine("configureas local run"),you do not need to use Docker. You may
use Docker locally if you choose(seethesection Configure ML pipelinefor an example).







# [DISTRIBUTED TRAINING](https://docs.microsoft.com/en-gb/azure/machine-learning/concept-distributed-training):

## Types
There are two main types of distributed training: data parallelism and model parallelism. 

## While configuring the environment:
Horovod is an open-source, all reduce framework for distributed training developed by Uber. It offers an easy path to writing distributed PyTorch code for training.
If you are using a PyTorch curated environment, horovod is already included as one of the dependencies. If you are using your own environment, make sure the horovod dependency is included.

## [How to configure ScriptRunConfig for distributed computing jobs](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-train-pytorch#distributed-training):

In order to execute a distributed job using MPI/Horovod on Azure ML, you must specify an MpiConfiguration (Message Passing Interface) to the distributed_job_config parameter of the ScriptRunConfig constructor. 

# RUN

The environment, compute target and training script together form the run configuration: the full specification of a training run.

A run represents a single trial of an experiment. A Run object is used to monitor the asynchronous execution of a trial, log metrics and store output of the trial, and to analyze results and access artifacts generated by the trial.
Run is used inside of your experimentation code to log metrics and artifacts to the Run History service.
Run is used outside of your experiments to monitor progress and to query and analyze the metrics and results that were generated.

* The functionality of Run includes:
    * Storing and retrieving metrics and data
    * Uploading and downloading files
    * Using tags as well as the child hierarchy for easy lookup of past runs
    * Registering stored model files as a model that can be operationalized
    * Storing, modifying, and retrieving properties of a run
    * Loading the current run from a remote environment with the get_context method
    * Efficiently snapshotting a file or directory for reproducibility

* This class works with the Experiment in these scenarios:
    * Creating a run by executing code using submit
    * Creating a run interactively in a notebook using start_logging
    * Logging metrics and uploading artifacts in your experiment, such as when using log
    * Reading metrics and downloading artifacts when analyzing experimental results, such as when using get_metrics

* To submit a run, create a configuration object that describes how the experiment is run. Here are examples of the different configuration objects you can use:
* The environment, compute target and training script together form the run configuration: the full specification of a training run.
    * ScriptRunConfig
    * AutoMLConfig
    * HyperDriveConfig
    * Pipeline
    * PublishedPipeline
    * PipelineEndpoint

* The Details tab contains the general properties of the experiment run.
    * The Metrics tab enables you to select logged metrics and view them as tables or charts.
    * The Images tab enables you to select and view any images or plots that were logged in the experiment (in this case, the Label Distribution plot)
    * The Child Runs tab lists any child runs (in this experiment there are none).
    * The Outputs + Logs tab shows the output or log files generated by the experiment.
    * The Snapshot tab contains all files in the folder where the experiment code was run (in this case, everything in the same folder as this notebook).
    * The Explanations tab is used to show model explanations generated by the experiment (in this case, there are none).
    * The Fairness tab is used to visualize predictive performance disparities that help you evaluate the fairness of machine learning models (in this case, there are none).

    * Special Folders Two folders, outputs and logs, receive special treatment by Azure Machine Learning. During training, when you write files to folders named outputs and logs that are relative to the root directory (./outputs and ./logs, respectively), the files will automatically upload to your run history so that you have access to them once your run is finished.


# General Experiment Steps
* Provision Workspace

* Provision/Fetch Data

* Provision/Fetch Compute

* Provision/Fetch Environent

* Create run configuration

* Create and submit experiment

* Create Train Script
    * Fetch Run Context
    
    * Unload passed parameters
        * Data
            * Define X and Y in 3 categories Train, Test and Sensitive Features
            * while training you can choose to add sensitive features or remove them.
        * additional parameters

    * Fit data to model
    
    * Log metrics, images, outputs
    
    * Upload a file to the run record. using `run.upload_file()`
    
    * Retrive best model and save it as pkl file

    * Register best model

    * [Add Interpretability](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-interpretability-aml)
        * Retrive registered model
        * Create explainer
        * get global explainations for x_test
        * create an instance of `Explaination Client` by passing the `run` context and upload the above explainations

    * [Add Fairness](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-fairness-aml)
        * Retrive the registered model
        * Precompute Fairness Metric: You'll require
            * sf = { 'Race': A_test.race, 'Sex': A_test.sex}
            * ys_pred = { lr_reg_id:lr_predictor.predict(X_test) }
            * ```python from fairlearn.metrics._group_metric_set import _create_group_metric_set

              dash_dict = _create_group_metric_set(y_true=y_test,
                                                predictions=ys_pred,
                                                sensitive_features=sf,
                                                prediction_type='binary_classification')
                                                ```
        * Upload the Precomputed Dashboard : fetch `from azureml.contrib.fairness import upload_dashboard_dictionary`
            * run
            * precomputed dashboard (dash_dict)
            * upload using `upload_dashboard_dictionary` method


    * Add Mitigation Fairness?

    * Complete Run

# Types of Experiments

## AutoMl

### Run config
```python
automl_config = AutoMLConfig(name='Automated ML Experiment',
                                    task='classification',
                                    compute_target=training_cluster,
                                    training_data = train_ds,
                                    validation_data = test_ds,
                                    label_column_name='Diabetic',
                                    iterations=4,
                                    primary_metric = 'AUC_weighted',
                                    max_concurrent_iterations=2,
                                    featurization='auto'
                                    )
```
## Simple Experiment

### Run config
```python
script_config = ScriptRunConfig(source_directory, 
                                        script=None, 
                                        arguments=None, 
                                        run_config=None, 
                                        _telemetry_values=None, 
                                        compute_target=None, 
                                        environment=None, 
                                        distributed_job_config=None, 
                                        resume_from=None, 
                                        max_run_duration_seconds=2592000, 
                                        command=None, 
                                        docker_runtime_config=None)
```

## Hyperparameter Tuning Experiment

### Run Config
Before defining a hyperdrive config, Define a scriptRunConfig for the experiment and create a parameters dict along with its sampling method.    

```python
hyperdrive = HyperDriveConfig(run_config=script_config, 
                        hyperparameter_sampling=params, 
                        policy=None, # No early stopping policy
                        primary_metric_name='AUC', # Find the highest AUC metric
                        primary_metric_goal=PrimaryMetricGoal.MAXIMIZE, 
                        max_total_runs=6, # Restict the experiment to 6 iterations
                        max_concurrent_runs=2)

```
## Pipelines

### Run Config
```python
pipeline_steps = [prep_step, train_step]
                Other Types of steps are : PythonScriptStep
                                        HyperdriveStepRun and HyperdriveStep
                                        AutoMLStepRun and AutoMLStep
                                        ParallelRunConfig and ParallelRunStep

pipeline = Pipeline(workspace=ws, steps=pipeline_steps)
```