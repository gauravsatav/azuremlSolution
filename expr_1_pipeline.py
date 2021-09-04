import azureml.core                                                                                         # Section 1
from azureml.core import Workspace                                                                                         # Section 1


from azureml.pipeline.core import Pipeline,PipelineData                                                                                         # Section 1
from azureml.pipeline.steps import PythonScriptStep                                                                                         # Section 1

from azureml.core import Experiment
from azureml.core.runconfig import RunConfiguration

# For executing published pipeline
import requests
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.pipeline.core.run import PipelineRun


# For scheduling a pipeline.
from azureml.pipeline.core import ScheduleRecurrence, Schedule



# Local Imports.
import provision

# ============================== (1). LOAD WORKSPACE FROM CONF FILE ==============================
ws = Workspace.from_config()
print('Ready to use Azure ML {} to work with {}'.format(azureml.core.VERSION, ws.name))


# ============================== (2). PROVISION/FETCH DATA SOLUTION ==============================

datastoreToUse = 'default'
# datastoreToUse = 'workspacefilestore'
subFolderNameInDatastore = 'diabetes-data/'
pathToLocalDataInList = ['./data/diabetes.csv']

registerDatasetByName = 'diabetes dataset'
registeredDatasetDescription = 'This dataset contains 2 csv file to train diabetes model.'
tabularDatasetFilePathInDatastore = 'diabetes-data/*.csv'

diabetesDatastore = provision.data.checkCreateUploadDatastore(myDatastoreName = datastoreToUse,
                                                        currentWorkspace=ws,
                                                        uploadFilesPath=pathToLocalDataInList,
                                                        pathToTargetFolderInDatastore=subFolderNameInDatastore,
                                                        uploadFiles=False,
                                                        uploadFolder=False,
                                                        listCurrentDatastores=True,
                                                        createNewIfNotFound=False
                                                        )

tupleOfDatastoreAndFiles = (diabetesDatastore,tabularDatasetFilePathInDatastore)

diabetesDataset = provision.data.checkCreateRegisterDataset(myRegisteredDatasetName = registerDatasetByName,
                                                            tulpleDatastoreNameAndFilePath = tupleOfDatastoreAndFiles,
                                                            myRegisteredDatasetDescription = registeredDatasetDescription,
                                                            currentWorkspace=ws,
                                                            createNewIfNotFound=True,
                                                            registerDataset = True,
                                                            listRegisteredDatasets = False,
                                                            typeTabular=True
                                                            )

# ============================== (3). PROVISION/FETCH COMPUTE SOLUTION(S) ==============================
computeClusterName = "D11-v2-2"                                                                             # My recommendation to name cluster is to use the compute configuration as name.
                                                                                                            # Example : standard_ds11_v2_2nodes
                                                                                                            # More information on sizes at https://docs.microsoft.com/en-us/azure/virtual-machines/sizes
vmSize = 'STANDARD_DS11_V2'
minNodes = 0
maxNodes = 4
vmPriorityType = 'dedicated'

computeForTraining = provision.compute.checkCreateComputeCluster(currentWorkspace = ws,
                                                                    myClusterName=computeClusterName,
                                                                    myVmSizeConfig = vmSize,
                                                                    minNodeConfig = minNodes,
                                                                    maxNodeConfig = maxNodes,
                                                                    vmPriorityConfig = vmPriorityType
                                                                    )


# ============================== (4). PROVISION/FETCH PYTHON ENVIRONMENT ==============================
'''
    Install Dependencies on each compute
    The compute will require a Python environment with the necessary package dependencies installed, so you'll need to create a run configuration.

    'azureml-dataprep[fuse]' ---> Batch Inferencing Service
    'azureml-interpret' ---> Interpret Models Module.
'''
pythonEnvironmentName = 'azureEntropy'
condaPackagesList = ['scikit-learn','ipykernel','matplotlib','pandas','pip']
pipPackagesList = ['azureml-defaults','azureml-dataprep[pandas]','pyarrow','azureml-dataprep[fuse]','azureml-interpret']


pipelineEnvironment = provision.pythonEnv.checkCreateRegisterEnvironment(currentWorkspace=ws,
                                                                        environmentName=pythonEnvironmentName,
                                                                        listOfCondaPackages=condaPackagesList,
                                                                        listOfPipPackages=pipPackagesList,
                                                                        registerNewEnvironment=True
                                                                        )


# ============================== (5). CREATE PIPELINE RUN CONFIGURATION   ==============================
pipelineRunConfiguration = RunConfiguration()                                               # Create a new runconfig object for the pipeline
pipelineRunConfiguration.target = computeForTraining                                               # Use the compute you created above.
pipelineRunConfiguration.environment = pipelineEnvironment                                               # Assign the environment to the run configuration

# ============================== (5). CREATE/FETCH SCRIPTS OF THE ML EXPERIMENT ALL IN ONE FOLDER   ==============================

experimentFolderPath = 'expr_1_decisionTreeClassifier'


'''   !!! IMPORTANT !!!
    define argument variables expected, especially.

    inputFile/trainingData/rawDatafile ---> How is this referenced in the script. The same name needs to be passed to the pipeline step while calling it.
    in our case in the script training data is read as follows:
        trainingData = run.get_input_datasets['raw_data'] , and the same name ('raw_data') is passed as argument to the PythonScriptStep.



    outputFileName --> Need to work on this, create an argument which decides the name of file in which post script execution output will be stored. eg 'output.csv' or in current case its stored by the name 'data.csv'
    This is important again as the file of this name will be read by the next step. In currnt senario, in the training script, the file is read as file_path = os.path.join(training_folder,'data.csv')
'''

step1_preprocessingScript = "expr_1_preprocess.py"
step2_trainingScript = "expr_1_train_decisionTreeClassifier.py"
step3_registerModelScript = 'expr_1_registerModel.py'





# ============================== (5). TEST EXPERIMENT   ==============================
'''
    testExperiment = 'testExperiment.py'
    # Create a script config
    script_config = ScriptRunConfig(source_directory=experimentFolderPath,
                                    script=testExperiment,
                                    arguments = ['--regularization', 0.1, # Regularizaton rate parameter
                                                '--input-data', diabetesDataset.as_named_input('training_data')], # Reference to dataset
                                    environment=pipelineEnvironment,
                                    compute_target=computeForTraining
                                    )


    # submit the experiment
    experiment_name = 'testExperiment'
    experiment = Experiment(workspace=ws, name=experiment_name)
    run = experiment.submit(config=script_config)
    # RunDetails(run).show()
    run.wait_for_completion()
'''



# ============================== (6). DEFINE PIPELINE STEPS AND LOAD INTO PIPELINE OBJECT ==============================

decionTreePreprocessedData = PipelineData(name = "preprocessingPipelineDataname",
                                          datastore = diabetesDatastore,
                                          pipeline_output_name='processed data to training'
                                          )                                                              # Create a PipelineData (temporary Data Reference) for the model folder


pipelinePreprocessingStep = PythonScriptStep(name = "Prepare Data",                                                                                 # Step 1, Run the data prep script
                                source_directory = experimentFolderPath,
                                script_name = step1_preprocessingScript,
                                arguments = ['--input-data', diabetesDataset.as_named_input('raw_data'),
                                             '--prepped-data', decionTreePreprocessedData],
                                outputs=[decionTreePreprocessedData],
                                compute_target = computeForTraining,
                                runconfig = pipelineRunConfiguration,
                                allow_reuse = True)


pipelineTrainAndRegisterStep = PythonScriptStep(name = "Train and Register Model",                                                                  # Step 2, run the training script
                                source_directory = experimentFolderPath,
                                script_name = step2_trainingScript,
                                arguments = ['--training-folder', decionTreePreprocessedData
                                            ],
                                inputs=[decionTreePreprocessedData],
                                compute_target = computeForTraining,
                                runconfig = pipelineRunConfiguration,
                                allow_reuse = True)

print("Pipeline steps defined")

pipelineCompleteSteps = [pipelinePreprocessingStep, pipelineTrainAndRegisterStep]                                                                   # Construct the pipeline
decisionTreePipeline = Pipeline(workspace=ws, steps=pipelineCompleteSteps)
print("Pipeline is built.")


# ============================== (4). CREATE AND RUN PIPELINE AS EXPERIMENT ==============================

experinementName = 'decisionTreePipelineExperiment'
experiment = Experiment(workspace=ws, name = experinementName)
decisionTreePipelineRun = experiment.submit(decisionTreePipeline, regenerate_outputs=True)
print("Pipeline submitted for execution.")
# RunDetails(decisionTreePipelineRun).show()
decisionTreePipelineRun.wait_for_completion(show_output=True)


# ============================== (4). PUBLISH PIPELINE AS REST SERVICE ==============================

# Publish the pipeline from the run
publishedDecisionTreePipeline = decisionTreePipelineRun.publish_pipeline(name="diabetes-training-pipeline",
                                                                         description="Trains diabetes model",
                                                                         version="1.0")



decisionTreePipelineRestEndpoint = publishedDecisionTreePipeline.endpoint
print(decisionTreePipelineRestEndpoint)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                       EXAMPLE HOW TO CALL THE PIPELINE                                                
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ============================== (4). CALL PIPELINE REST SERVICE ENDPOINT ==============================

experiment_name = 'Published_Pipeline_Execution'

            # GET AUTH PARAMETERS
interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()
print("Authentication header ready.")


            # GET PIPELINE REST ENDPOINT
rest_endpoint = publishedDecisionTreePipeline.endpoint
response = requests.post(rest_endpoint,
                         headers=auth_header,
                         json={"ExperimentName": experiment_name})
run_id = response.json()["Id"]
run_id


            # START PIPELINE EXECUTION
published_pipeline_run = PipelineRun(ws.experiments[experiment_name], run_id)
published_pipeline_run.wait_for_completion(show_output=True)

# ============================== (4). SCHEDULE PIPELINE ==============================


# Submit the Pipeline every Monday at 00:00 UTC
recurrence = ScheduleRecurrence(frequency="Week", interval=1, week_days=["Monday"], time_of_day="00:00")

weekly_schedule = Schedule.create(ws, name="weekly-diabetes-training",
                                  description="Based on time",
                                  pipeline_id=publishedDecisionTreePipeline.id,
                                  experiment_name=experiment_name,
                                  recurrence=recurrence)

print('Pipeline scheduled.')


schedules = Schedule.list(ws)           # List of all scheduled experiments (even in the form of pipelines.)


pipeline_experiment = ws.experiments.get(experiment_name)               # Get details of the latest run of experiment by the name experiment_name
latest_run = list(pipeline_experiment.get_runs())[0]
latest_run.get_details()
