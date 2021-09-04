import azureml.core
from azureml.core import Workspace


# ============================== LOAD WORKSPACE FROM CONF FILE ==============================
ws = Workspace.from_config()
print('Ready to use Azure ML {} to work with {}'.format(azureml.core.VERSION, ws.name))



# ============================== DATA ==============================

#            # ------ LIST EXISTING DATASTORES AND GETTING DEFAULT ------

default_ds = ws.get_default_datastore()     # Get the default datastore. Use ws.set_default_datastore() to set default DataStore.
for ds_name in ws.datastores:               # Enumerate all datastores, indicating which is the default
    print(ds_name, "- Default =", ds_name == default_ds.name)



'''
#            # ------ CREATE DATASTORE (BLOB CONTAINER) ------

# To create a blob container you'll have to use azure sdk which is outside the scope of azureml sdk.

#            # ------ REGISTER EXISTING DATA STORE (BLOB CONTAINER) ------
# from azureml.core import Datastore
# blob_ds = Datastore.register_azure_blob_container(workspace=ws, 
#                                                   datastore_name='blob_data', 
#                                                   container_name='data_container',
#                                                   account_name='myworkspstorage7c2fcbb23',
#                                                   account_key='123456abcde789…')


'''


myDatastoreName = 'default'
targetDatastorePath = 'diabetes-data/'

myRegisteredTabularDatasetName = 'diabetes dataset'
myRegisteredTabularDatasetDescription = 'diabetes data for training.'
tabularDatasetFilePathInDatastore = 'diabetes-data/*.csv'

listWithPathsToLocalData = ['./data/diabetes.csv']



if myDatastoreName != 'default':
    fetchedDatastore = ws.datastores.get(myDatastoreName)
else:
    fetchedDatastore = ws.get_default_datastore()

if myRegisteredTabularDatasetName not in ws.datasets():

    #            # ------ UPLOAD DATA TO DEFAULT DATASTORE ------
    fetchedDatastore.upload_files(files=listWithPathsToLocalData, # Upload the diabetes csv files in /data
                        target_path=targetDatastorePath, # Put it in a folder path in the datastore
                        overwrite=True, # Replace existing files of the same name
                        show_progress=True)


    #            # ------ CREATE AND REGISTER TABULAR DATASET ------
    from azureml.core import Dataset
    tab_data_set = Dataset.Tabular.from_delimited_files(path=(fetchedDatastore, tabularDatasetFilePathInDatastore))       #Create a tabular dataset from the path on the datastore (this may take a short while)
    # createdDataset= tab_data_set.take(20).to_pandas_dataframe()                                         # Display the first 20 rows as a Pandas dataframe


    try:                                                                                                # Register the tabular dataset
        tab_data_set = tab_data_set.register(workspace=ws, 
                                            name = myRegisteredTabularDatasetName,
                                            description=myRegisteredTabularDatasetDescription,
                                            tags = {'format':'CSV'},
                                            create_new_version=True)
    except Exception as ex:                                                                             # Handel expection.
        print(ex)

    # print("\nDatasets:")
    # for dataset_name in list(ws.datasets.keys()):                                                       # Get all datasets by name and version registered in the workspace.
    #     dataset = Dataset.get_by_name(ws, dataset_name)
    #     print("\t", dataset.name, 'version', dataset.version)
    
    print('Dataset registered.')
else:
    print(f'A Dataset with name {myRegisteredTabularDatasetName} is already registered in the workspace : {ws.name}.')



# ============================== COMPUTE ==============================


#            # ------ LIST EXISTING COMPUTE TARGETS ------
existingComputeTargets = ws.compute_targets
if len(existingComputeTargets)==0:
    print(f"\n There are no compute targets found within the workspace : {ws.name} ")

else:
    for compute_name in existingComputeTargets:
        compute = ws.compute_targets[compute_name]
        print(compute.name, ":", compute.type)

#            # ------ COMPUTE CLUSTER NAME ------
cluster_name = "D11-v2-2"                                                                           # My recommendation to name cluster is to use the compute configuration as name.
                                                                                                    # Example : standard_ds11_v2_2nodes
                                                                                                    # More information on sizes at https://docs.microsoft.com/en-us/azure/virtual-machines/sizes


#            # ------ CREATE CLUSTER IF CLUSTER NAME DOES NOT EXIST------
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException


try:                                                                                                 # Check for existing compute target.
    training_cluster = ComputeTarget(workspace=ws, name=cluster_name)
    print('Found existing cluster, use it.')
except ComputeTargetException:                                                                       # If it doesn't already exist, create it
    print(f'\nDid not find compute cluster with name {cluster_name}')                                
    try:
        compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS11_V2',           # Define compute configuration
                                                                min_nodes=0, max_nodes=2,
                                                                vm_priority='dedicated'
                                                               )
        training_cluster = ComputeTarget.create(ws, cluster_name, compute_config)                    # Create Compute Target in given Workspace with given name and configuration.
        training_cluster.wait_for_completion(show_output=True)                                       # Wait for Completion.
    except Exception as ex:
        print(ex)

print(f'There are {len(ws.compute_targets)} compute targets available within {ws.name}')




# ============================== REGISTER PYTHON ENV : ISOLATING DEPENDENCIES BY CREATING A PYTHON ENVIRONMENT ==============================
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies

#            # ------ FETCH ALL ENVIRONMENTS------
envs = Environment.list(workspace=ws)                                                                       # Returns list of registered environments as list.
                                                                                                            # All curated environments have names that begin AzureML- (you can't use this prefix for your own environments).

#            # ------ CREATE NEW ENVIRONMENT------
sklearn_env = Environment(name = "sklearn-env")                                                             # Create a Python environment for the experiment
sklearn_env.python.user_managed_dependencies = False                                                        # Let Azure ML manage dependencies.
sklearn_env.docker.enabled = True                                                                           # Use a docker container.

packages = CondaDependencies.create(conda_packages=['scikit-learn','pip'],
                                    pip_packages=['azureml-defaults','azureml-dataprep[pandas]'])
sklearn_env.python.conda_dependencies = packages                                                            # Ensure the required packages are installed (we need scikit-learn, Azure ML defaults, and Azure ML dataprep)
print(f"\n Created Python environment with name : {sklearn_env.name}")

#            # ------ REGISTER NEW ENVIRONMENT------
sklearn_env.register(workspace=ws)