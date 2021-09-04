# # ============================== (5). HYPER PARAMETER EXPERIMENT   ==============================

# script_config = ScriptRunConfig(source_directory=experimentFolderPath,                                              # Create a script config
#                                 script=step2_trainingScript,
#                                 # Add non-hyperparameter arguments -in this case, the training dataset
#                                 arguments = ['--training-folder', decionTreePreprocessedData
#                                             ],
#                                 environment=pipelineRunConfiguration,
#                                 compute_target = computeForTraining)

# # Sample a range of parameter values
# params = GridParameterSampling(
#     {
#         # Hyperdrive will try 6 combinations, adding these as script arguments
#         '--learning_rate': choice(0.01, 0.1, 1.0),
#         '--n_estimators' : choice(10, 100)
#     }
# )

# # Configure hyperdrive settings
# hyperdriveConfiguration = HyperDriveConfig(run_config=script_config,
#                           hyperparameter_sampling=params,
#                           policy=None, # No early stopping policy
#                           primary_metric_name='AUC', # Find the highest AUC metric
#                           primary_metric_goal=PrimaryMetricGoal.MAXIMIZE,
#                           max_total_runs=2, # Restict the experiment to 6 iterations
#                           max_concurrent_runs=2) # Run up to 2 iterations in parallel


# import azureml.core                                                                                         # Section 1
# from azureml.core import Workspace                                                                                         # Section 1

# from azureml.pipeline.core import PipelineData, TrainingOutput                                                                                         # Section 1
# from azureml.pipeline.steps import PythonScriptStep,HyperDriveStep                                                                                         # Section 1

# from azureml.core import Experiment, ScriptRunConfig
# from azureml.pipeline.core import Pipeline
# from azureml.widgets import RunDetails
# from azureml.core.runconfig import RunConfiguration




# from azureml.train.hyperdrive import GridParameterSampling, HyperDriveConfig, PrimaryMetricGoal, choice



# metrics_data = PipelineData(name='decisionTreeClassifierMetricData', datastore=diabetesDatastore,
#                             pipeline_output_name='metrics_output',
#                             training_output=TrainingOutput(type='Metrics'))

# saved_model = PipelineData(name='decisionTreeClassifierModelFile',
#                             datastore=diabetesDatastore,
#                             pipeline_output_name='model output',
#                             training_output=TrainingOutput(type='Model'))

# hd_step_name='hd_step01'
# hd_step = HyperDriveStep(
#     name=hd_step_name,
#     hyperdrive_config=hyperdriveConfiguration,
#     inputs=[decionTreePreprocessedData],
#     outputs=[metrics_data, saved_model])

# '''
#     pipelineRegisterStep = PythonScriptStep(script_name='register_model.py',
#     #                                        name="register_model_step01",
#     #                                        inputs=[saved_model],
#     #                                        compute_target=cpu_cluster,
#     #                                        arguments=["--saved-model", saved_model],
#     #                                        allow_reuse=True,
#     #                                        runconfig=rcfg)
# '''