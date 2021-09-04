from azureml.core import Workspace

from azureml.core import  Datastore
from azureml.core import Dataset


def fetchWorkspace(myWorkspaceName = 'default'):
    if myWorkspaceName!='default':
        print("\n In here")
        fetchedWorkspace = Workspace.get(myWorkspaceName)
    else:
        print('\nOut There')
        fetchedWorkspace = Workspace.from_config("../config.json")
        print(fetchedWorkspace.get_default_datastore())
    return fetchedWorkspace


def checkCreateUploadDatastore(myDatastoreName='default',
                                currentWorkspace = 'default',
                                uploadFilesPath=[],
                                uploadFolderPath='',
                                pathToTargetFolderInDatastore='uploadedData',
                                uploadFiles=False,
                                uploadFolder=False,
                                listCurrentDatastores=False,
                                createNewIfNotFound = False
                                ):

    ws = currentWorkspace

    fetchedDatastore = ws.get_default_datastore()

    if listCurrentDatastores:
        default_ds = fetchedDatastore     # Get the default datastore. Use ws.set_default_datastore() to set default DataStore.
        for ds_name in ws.datastores:               # Enumerate all datastores, indicating which is the default
            print(ds_name, "- Default =", ds_name == default_ds.name)

    if myDatastoreName != 'default':                                                                        # If datastore IS NOT 'default' then get datastore by name.
        try :
            fetchedDatastore = Datastore.get(ws, datastore_name=myDatastoreName)
        except Exception as ex:                                                                                            # If datastore IS NOT FOUND then create datastore by name.
                #TODO Create a datastore with the name
                if createNewIfNotFound:
                    # blob_datastore_name='azblobsdk' # Name of the datastore to workspace
                    # container_name=os.getenv("BLOB_CONTAINER", "<my-container-name>") # Name of Azure blob container
                    # account_name=os.getenv("BLOB_ACCOUNTNAME", "<my-account-name>") # Storage account name
                    # account_key=os.getenv("BLOB_ACCOUNT_KEY", "<my-account-key>") # Storage account access key

                    # blob_datastore = Datastore.register_azure_blob_container(workspace=ws,
                    #                                                         datastore_name=blob_datastore_name,
                    #                                                         container_name=container_name,
                    #                                                         account_name=account_name,
                    #                                                         account_key=account_key)
                    print(f"Created a datastore with name {myDatastoreName}")
                else:
                    print(ex)

    if (len(uploadFilesPath)>0) and uploadFiles:
        fetchedDatastore.upload_files(files=uploadFilesPath, # Upload the diabetes csv files in /data
                            target_path=pathToTargetFolderInDatastore, # Put it in a folder path in the datastore
                            overwrite=True, # Replace existing files of the same name
                            show_progress=True)
    
    if (len(uploadFolderPath)>0) and uploadFolder:
        print(f'\nUploading folder : {uploadFolderPath} \nIn datastore : {fetchedDatastore}\nTo folder :{pathToTargetFolderInDatastore}')
        fetchedDatastore.upload(src_dir=uploadFolderPath,
                                target_path=pathToTargetFolderInDatastore,
                                overwrite=True,
                                show_progress=True)


    print(f'\nDatastore = {fetchedDatastore}\n')

    return fetchedDatastore


def checkCreateRegisterDataset(myRegisteredDatasetName,
                                    tulpleDatastoreNameAndFilePath=('default','enter Datastore File Path where data resides'),
                                    myRegisteredDatasetDescription='registered a new dataset',
                                    currentWorkspace='default',
                                    createNewIfNotFound=True,
                                    registerDataset = True,
                                    listRegisteredDatasets = False,
                                    typeTabular=False,
                                    typeFile=False,
                                    ):

    ws = currentWorkspace

    if listRegisteredDatasets:
        print("\nDatasets:")
        for dataset_name in list(ws.datasets.keys()):                                                       # Get all datasets by name and version registered in the workspace.
            dataset = Dataset.get_by_name(ws, dataset_name)
            print("\t", dataset.name, 'version', dataset.version)

    if (myRegisteredDatasetName not in ws.datasets) and createNewIfNotFound and typeTabular:
        # parentDatastore = checkCreateUploadDatastore(myDatastoreName = tulpleDatastoreNameAndFilePath[0])

        createdTabularDataset = Dataset.Tabular.from_delimited_files(path=tulpleDatastoreNameAndFilePath)       #Create a tabular dataset from the path on the datastore (this may take a short while)

        if registerDataset:
            try:                                                                                                # Register the tabular dataset
                createdTabularDataset = createdTabularDataset.register(workspace=ws,
                                                    name = myRegisteredDatasetName,
                                                    description=myRegisteredDatasetDescription,
                                                    tags = {'format':'CSV'},
                                                    create_new_version=True)
            except Exception as ex:                                                                             # Handle expection.
                print(ex)

            print(f'\nDataset with name {myRegisteredDatasetName} registered.\n')

        return createdTabularDataset

    if (myRegisteredDatasetName not in ws.datasets) and createNewIfNotFound and typeFile:
        createdFileDataset = Dataset.File.from_files(path=tulpleDatastoreNameAndFilePath,validate=False)       #Create a tabular dataset from the path on the datastore (this may take a short while)

        if registerDataset:
            try:                                                                                                # Register the tabular dataset
                createdFileDataset = createdFileDataset.register(workspace=ws,
                                                    name = myRegisteredDatasetName,
                                                    description=myRegisteredDatasetDescription,
                                                    create_new_version=True)
            except Exception as ex:                                                                             # Handle expection.
                print(ex)

            print(f'\nDataset with name {myRegisteredDatasetName} registered.\n')

        return createdFileDataset


    else:
        print(f'A Dataset with name {myRegisteredDatasetName} is already registered in the workspace : {ws.name}.')
        return ws.datasets.get(myRegisteredDatasetName)

















