import azureml.core
from azureml.core import Workspace

from azureml.core import Model

from azureml.pipeline.steps import ParallelRunConfig, ParallelRunStep
from azureml.pipeline.core import PipelineData


from azureml.core import Experiment
from azureml.pipeline.core import Pipeline
import pandas as pd
import shutil
import os

from azureml.core.conda_dependencies import CondaDependencies

from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig
import requests
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.pipeline.core.run import PipelineRun


import json





import provision
# ============================== (1). GET WORKSPACE CONTEXT ==============================
ws = Workspace.from_config()
print('Ready to use Azure ML {} to work with {}'.format(azureml.core.VERSION, ws.name))

# ============================== (2). PROVISION/FETCH DATA SOLUTION ==============================

datastoreToUse = 'default'
# datastoreToUse = 'workspacefilestore'
subFolderNameInDatastore = 'batch-data/'
pathToLocalFolderToUpload = './data/incomingBatchData'

registerDatasetByName = 'batchInferencingDataset'
registeredDatasetDescription = 'This dataset batch files to be inferenced by model service.'
sourceFolderPathInDatastore = 'batch-data/'                                 # Subfolder Name in Datastore + Files names.

batchDataDatastore = provision.data.checkCreateUploadDatastore(myDatastoreName = datastoreToUse,
                                                        currentWorkspace=ws,
                                                        uploadFolderPath=pathToLocalFolderToUpload,
                                                        pathToTargetFolderInDatastore=subFolderNameInDatastore,
                                                        uploadFiles=False,
                                                        uploadFolder=True,
                                                        listCurrentDatastores=True,
                                                        createNewIfNotFound=True
                                                        )

tupleOfDatastoreAndFiles = (batchDataDatastore,sourceFolderPathInDatastore)

batchDataDataset = provision.data.checkCreateRegisterDataset(myRegisteredDatasetName = registerDatasetByName,
                                                            tulpleDatastoreNameAndFilePath = tupleOfDatastoreAndFiles,
                                                            myRegisteredDatasetDescription = registeredDatasetDescription,
                                                            currentWorkspace=ws,
                                                            createNewIfNotFound=True,
                                                            registerDataset = True,
                                                            listRegisteredDatasets = True,
                                                            typeFile=True
                                                            )

# ============================== (3). PROVISION/FETCH COMPUTE SOLUTION(S) ==============================
computeClusterName = "D11-v2-2"                                                                             # My recommendation to name cluster is to use the compute configuration as name.
                                                                                                            # Example : standard_ds11_v2_2nodes
                                                                                                            # More information on sizes at https://docs.microsoft.com/en-us/azure/virtual-machines/sizes
vmSize = 'STANDARD_DS11_V2'
minNodes = 0
maxNodes = 4
vmPriorityType = 'dedicated'

computeForBatchInferencing = provision.compute.checkCreateComputeCluster(currentWorkspace = ws,
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

    'azureml-dataprep[fuse]','azureml-core' ---> Batch Inferencing Service
    'azureml-interpret' ---> Interpret Models Module.
'''
pythonEnvironmentName = 'batchInferenceEnv'
condaPackagesList = ['scikit-learn','pandas','pip']
pipPackagesList = ['azureml-defaults','azureml-dataprep[fuse]','azureml-core']


batchInfEnv = provision.pythonEnv.checkCreateRegisterEnvironment(currentWorkspace=ws,
                                                                        environmentName=pythonEnvironmentName,
                                                                        listOfCondaPackages=condaPackagesList,
                                                                        listOfPipPackages=pipPackagesList,
                                                                        registerNewEnvironment=True,
                                                                        batchEnv=True
                                                                        )

# ============================== (5). CREATE/FETCH SCRIPTS OF THE ML EXPERIMENT ALL IN ONE FOLDER   ==============================

experimentFolderPath = 'expr_1_batchService'
batchScriptName = "batch_diabetes.py"
# ============================== (6). DEFINE PIPELINE STEPS AND LOAD INTO PIPELINE OBJECT ==============================


output_dir = PipelineData(name='inferences',
                          pipeline_output_name='output of inferences',
                          datastore=batchDataDatastore,
                          output_path_on_compute='diabetes/results')

parallel_run_config = ParallelRunConfig(
    source_directory=experimentFolderPath,
    entry_script=batchScriptName,
    mini_batch_size="5",
    error_threshold=10,
    output_action="append_row",
    environment=batchInfEnv,
    compute_target=computeForBatchInferencing,
    node_count=2)

parallelrun_step = ParallelRunStep(
    name='batch-score-diabetes',
    parallel_run_config=parallel_run_config,
    inputs=[batchDataDataset.as_named_input('diabetes_batch')],
    output=output_dir,
    arguments=[],
    allow_reuse=True
)

print('Steps defined')
batchPipeline = Pipeline(workspace=ws, steps=[parallelrun_step])


# ============================== (4). CREATE AND RUN PIPELINE AS EXPERIMENT ==============================
experinementName = 'batchInferencingPipelineExperiment'
experiment = Experiment(workspace=ws, name = experinementName)
batchPipelineRun = experiment.submit(batchPipeline, regenerate_outputs=True)
print("Pipeline submitted for execution.")
batchPipelineRun.wait_for_completion(show_output=True)



# ============================== (4). DOWNLOAD BATCH PREDICTIONS LOCALLY ==============================

downloadResultsFolderPath = './data/predictedBatchData'
downloadedFileName = 'batchResults.csv'

shutil.rmtree(downloadResultsFolderPath, ignore_errors=True)                                                # Remove the local results folder if left over from a previous run


prediction_run = next(batchPipelineRun.get_children())                                                      # Get the run for the first step and download its output
prediction_output = prediction_run.get_output_data('inferences')
prediction_output.download(local_path=downloadResultsFolderPath)


for root, dirs, files in os.walk(downloadResultsFolderPath):                                                 # Traverse the folder hierarchy and find the results file
    for file in files:
        if file.endswith('parallel_run_step.txt'):
            result_file = os.path.join(root,file)


df = pd.read_csv(result_file, delimiter=":", header=None)                                                       # cleanup output format
df.columns = ["File", "Prediction"]


downloadFilePath = os.path.join(downloadResultsFolderPath,downloadedFileName)
df.to_csv(downloadFilePath)




# ============================== (4). PUBLISH PIPELINE AS REST SERVICE ==============================
publishedBatchPipeline = batchPipelineRun.publish_pipeline(
    name='diabetes-batch-pipeline', description='Batch scoring of diabetes data', version='1.0')

batchPipelineRestEndpoint = publishedBatchPipeline.endpoint
print(batchPipelineRestEndpoint)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                       EXAMPLE HOW TO CALL THE PIPELINE                                                
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ============================== (4). CALL PIPELINE REST SERVICE ENDPOINT ==============================

experiment_name = 'Published_Batch_Pipeline_Execution'

            # GET AUTH PARAMETERS
interactive_auth = InteractiveLoginAuthentication()
auth_header = interactive_auth.get_authentication_header()
print("Authentication header ready.")


            # GET PIPELINE REST ENDPOINT
rest_endpoint = publishedBatchPipeline.endpoint
response = requests.post(rest_endpoint,
                         headers=auth_header,
                         json={"ExperimentName": experiment_name})
run_id = response.json()["Id"]
run_id


            # START PIPELINE EXECUTION
published_pipeline_run = PipelineRun(ws.experiments[experiment_name], run_id)
published_pipeline_run.wait_for_completion(show_output=True)


# ============================== (4). AS BEFORE, DOWNLOAD RESULTS FROM FIRST PIPELINE STEP ==============================

downloadResultsFolderPath = './data/predictedBatchData'
downloadedFileName = 'batchResults.csv'
whichPipelineRun = published_pipeline_run


shutil.rmtree(downloadResultsFolderPath, ignore_errors=True)                                                # Remove the local results folder if left over from a previous run


prediction_run = next(whichPipelineRun.get_children())                                                      # Get the run for the first step and download its output
prediction_output = prediction_run.get_output_data('inferences')
prediction_output.download(local_path=downloadResultsFolderPath)


for root, dirs, files in os.walk(downloadResultsFolderPath):                                                 # Traverse the folder hierarchy and find the results file
    for file in files:
        if file.endswith('parallel_run_step.txt'):
            result_file = os.path.join(root,file)


df = pd.read_csv(result_file, delimiter=":", header=None)                                                       # cleanup output format
df.columns = ["File", "Prediction"]


downloadFilePath = os.path.join(downloadResultsFolderPath,downloadedFileName)
df.to_csv(downloadFilePath)
