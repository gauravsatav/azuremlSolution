import azureml.core
from azureml.core import Workspace

from azureml.core import Experiment, ScriptRunConfig, Environment

# ============================== LOAD WORKSPACE FROM CONF FILE, EXPERIMENT FOLDER NAME, COMPUTE CLUSTER NAME ==============================
ws = Workspace.from_config()
print('Ready to use Azure ML {} to work with {}'.format(azureml.core.VERSION, ws.name))


# ============================== SET/RETRIVE ENV. VARIABLE NAMES ==============================
registerExperimentByName = 'mslearn-train-diabetes'                                                         # Give a new name to the experiment.

fetchedExperimentFolderPath = './experiment1'                                                               # --FETCH-- Specify experiment folder.It must be created before-hand.
fetchedTrainingScriptName = 'training.py'                                                                   # --FETCH-- Specify the name of training script present within the experiment folder.

fetchedDatasetName = 'diabetes dataset'                                                                     # --FETCH-- Defined in setup.py

fetchedRegisteredEnvironmentName = 'sklearn-env'                                                            # --FETCH-- Defined in setup.py

fetchedClusterName = "D11-v2-2"                                                                             # --FETCH-- Defined in setup.py

fetchOutputModelFromPath = 'outputs/diabetes_model.pkl'                                                     # --FETCH-- Specified in fetchedTrainingScriptName
registerOutputModelByName = 'diabetes_model'                                                                # Give a new name to register model by.

# ============================== GET REGISTERED PYTHON ENVIRONMENT ==============================
sklearn_env = Environment.get(ws, fetchedRegisteredEnvironmentName)

# ============================== DATA : SPECIFY WHERE DATA IS TO BE READ ==============================
# fetchedDatasetName = 'diabetes dataset'
diabetes_ds = ws.datasets.get(fetchedDatasetName)                                                                  # Get the training dataset


# ============================== SETUP EXPERIMENT PARAMETERS ==============================
'''
    Ensure you have created an experiment folder by the some name which contains.
    1. Experiment training script.
    2. [OPTIONAL] Data folder with training and test data : If data is not being read from a dataset(created from data uploaded to a datastore, either default or specified).
    3. [AFTER EXPERIMENT IS RUN] : It will contain output folder.

    To create an experiment folder from script, use the following snippet.
    import os    
    experiment_folder = 'diabetes_training_tree'
    os.makedirs(experiment_folder, exist_ok=True)                                                           # Create a folder for the experiment files
    print(experiment_folder, 'folder created')
'''

# fetchedExperimentFolderPath = './experiment1'
# fetchedClusterName = "D11-v2-2"
# fetchedTrainingScriptName = 'training.py'



script_config = ScriptRunConfig(source_directory=fetchedExperimentFolderPath,                               # Experiment Folder Name.
                              script = fetchedTrainingScriptName,                                           # Training Script Name.
                              arguments = ['--regularization', 0.1,                                         # Argument defined in and expected by training script. Regularizaton rate parameter
                                           '--input-data', diabetes_ds.as_named_input('training_data')],    # Argument defined in and expected by training script. Reference to dataset
                              environment=sklearn_env,                                                      # Python Environment Name.
                              compute_target=fetchedClusterName
                              )                                                      


# ============================== NAME THE EXPERIMENT AND SUBMIT IT TO START EXPERIMENT EXECUTION. ==============================
# registerExperimentByName = 'mslearn-train-diabetes'
experiment = Experiment(workspace=ws, name=registerExperimentByName)
run = experiment.submit(config=script_config)

#                  # ---------- Monitor Current Experiment Parameters. ----------
# from azureml.widgets import RunDetails
# RunDetails(run).show()                                                                                    # Monitor current experiment run.

# from azureml.core.compute import ComputeTarget                                                            # Monitor current compute target.
# training_cluster = ComputeTarget(workspace=ws, name=fetchedClusterName)
# cluster_state = training_cluster.get_status()
# print(cluster_state.allocation_state, cluster_state.current_node_count)

#                  # ---------- Wait for Run(Experiment) Completion. ----------
run.wait_for_completion()


# ============================== REGISTER MODEL ==============================
from azureml.core import Model
# registerOutputModelByName = 'diabetes_model'
# fetchOutputModelFromPath = 'outputs/diabetes_model.pkl'

run.register_model(model_path = fetchOutputModelFromPath,                                                   # Output path where pkl file will be stored.
                    model_name = registerOutputModelByName,                                                 # Name of the model.
                    tags={'Training context':'Tabular dataset'},                                            # Tags / Summary of the model.
                    properties={                                                                            # Properties : This will help in comparing different model runs.
                        'AUC': run.get_metrics()['AUC'], 
                        'Accuracy': run.get_metrics()['Accuracy']
                        }
                    )

for model in Model.list(ws):                                                                                # Get all Models registered in the Workspace along with their metrics for comparison.
    print(model.name, 'version:', model.version)
    for tag_name in model.tags:
        tag = model.tags[tag_name]
        print ('\t',tag_name, ':', tag)
    for prop_name in model.properties:
        prop = model.properties[prop_name]
        print ('\t',prop_name, ':', prop)
    print('\n')