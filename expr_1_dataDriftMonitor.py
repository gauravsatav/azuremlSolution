'''     CHECKLIST
    Dataset monitors depend on the following Azureservices.
    * Dataset
    * Azureml pipeline and compute
    * Application Insights
    * Azure Blob Storage

'''
from azureml.core import Workspace

from azureml.datadrift import DataDriftDetector,AlertConfiguration
import datetime as dt
import pandas as pd


from azureml.core import Datastore, Dataset



# ============================== (1). FETCH WORKSPACE ==============================
ws = Workspace.from_config()
print('Ready to work with', ws.name)


# ============================== (2). PROVISION BASELINE DATASET ==============================
default_ds = ws.get_default_datastore()
default_ds.upload_files(files=['data/diabetes.csv','data/diabetes2.csv'],
                       target_path='diabetes-baseline',
                       overwrite=True,
                       show_progress=True)

# Create and register the baseline dataset
print('Registering baseline dataset...')
baseline_data_set = Dataset.Tabular.from_delimited_files(path=(default_ds, 'diabetes-baseline/*.csv'))
baseline_data_set = baseline_data_set.register(workspace=ws,
                           name='diabetes baseline',
                           description='diabetes baseline data',
                           tags = {'format':'CSV'},
                           create_new_version=True)

print('Baseline dataset registered!')

# ============================== (3). PROVISION TARGET DATASET ==============================

'''             (3.0) SIMULATING TARGET DATA CODE
    print('Generating simulated data...')

    # Load the smaller of the two data files
    data = pd.read_csv('data/diabetes2.csv')

    # We'll generate data for the past 6 weeks
    weeknos = reversed(range(6))

    file_paths = []
    for weekno in weeknos:

        # Get the date X weeks ago
        data_date = dt.date.today() - dt.timedelta(weeks=weekno)

        # Modify data to ceate some drift
        data['Pregnancies'] = data['Pregnancies'] + 1
        data['Age'] = round(data['Age'] * 1.2).astype(int)
        data['BMI'] = data['BMI'] * 1.1

        # Save the file with the date encoded in the filename
        file_path = 'data/diabetes_{}.csv'.format(data_date.strftime("%Y-%m-%d"))
        data.to_csv(file_path)
        file_paths.append(file_path)

    # Upload the files
    path_on_datastore = 'diabetes-target/beforeTransition/'
    default_ds.upload_files(files=file_paths[0:3],
                        target_path=path_on_datastore,
                        overwrite=True,
                        show_progress=True)


    path_on_datastore = 'diabetes-target/afterTransition/'
    default_ds.upload_files(files=file_paths[3:6],
                        target_path=path_on_datastore,
                        overwrite=True,
                        show_progress=True)

'''


'''             (3.1) USE FOLDER PARTITIONING FORMAT TO DEFINE DATASET WITH A TIMESTAMP COLUMN

    (3.1.1) Datastore repo structure is like:

        'carManufacturer/2020/01/01/data.csv',
        'carManufacturer/2020/01/02/data.csv', etc
    
        When the folder structure is the above format, then its better to have a date column (by any name, lets say 'fooDate') added to the individual data.csv file itself.
        This way when we use the method 
        
        partition _format =  path_on_datastore + '/carManufacturer/*/*/*/data.csv'
        target_data_set = target_data_set.with_timestamp_columns('fooDate')

        Example @ : https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/work-with-data/datadrift-tutorial/datadrift-tutorial.ipynb

    (3.1.2) Datastore repo structure is like :
        'beforeTransition/diabetes_2020-01-01.csv'
        'beforeTransition/diabetes_2020-01-02.csv'
        'afterTransition/diabetes_2020-01-03.csv'
        'afterTransition/diabetes_2020-01-04.csv'

        Then use the example provided below.

        The first * is mapped to {transitionState} the second * is mapped to {itWasWindyToday:yyyy-MM-dd}
        
                    code  : myPath = [(default_ds,path_on_datastore+'/*/*.csv')]                                                                

        
        The {transitionState} will create a column called 'transitionState' in new dataset and the values will be the different
        unique values that the first wild character * will match in the myPath list. In this case the first * represents unique
        folder names within the path_on_datastore directory of datastore.
        Similarly the {itWasWindyToday} will create a column called  'itWasWindyToday' and the unique values will be defined by 
        the "yyyy-MM-dd" part.

        
                    code : partition_format = path_on_datastore + '/{transitionState}/diabetes_{itWasWindyToday:yyyy-MM-dd}.csv'               
        

        Note : It is NOT NECESSARY to use 'itWasWindyToday' to represent as the timestamp column. We can choose to map it to another
        column in the dataset which contain datetime.
        
                    code : target_data_set = target_data_set.with_timestamp_columns('itWasWindyToday')                                        
        
'''



path_on_datastore = 'diabetes-target'
myPath = [(default_ds,path_on_datastore+'/*/*.csv')]                                                                # The first * is mapped to {transitionState} the second * is mapped to {itWasWindyToday:yyyy-MM-dd}

partition_format = path_on_datastore + '/{transitionState}/diabetes_{itWasWindyToday:yyyy-MM-dd}.csv'               # The {transitionState} will create a column called 'transitionState' in new dataset and the values will be the different unique values that the first wild character * will match in the myPath list. In this case the first * represents unique folder names within the path_on_datastore directory of datastore
target_data_set = Dataset.Tabular.from_delimited_files(path=myPath,                                                 # Similarly the {itWasWindyToday} will create a column called  'itWasWindyToday' and the unique values will be defined by the "yyyy-MM-dd" part.
                                                       partition_format=partition_format)

# Register the target dataset
print('Registering target dataset...')
target_data_set = target_data_set.with_timestamp_columns('itWasWindyToday')                                         # Note : It is NOT NECESSARY to use 'itWasWindyToday' to represent as the timestamp column. We can choose to map it to another column in the dataset which contain datetime.
target_data_set = target_data_set.register(workspace=ws,
                        name='diabetes target',
                        description='diabetes target data',
                        tags = {'format':'CSV'},
                        create_new_version=True)

print('Target dataset registered!')

# ============================== (4). PROVISION COMPUTE ==============================





# ============================== (4). SETUP DATA DRIFT MONITOR ==============================
features = ['Pregnancies', 'Age', 'BMI']

alertConf = AlertConfiguration(['gausatav@in.ibm.com'])
                                                                                            # set up feature list
monitor = DataDriftDetector.create_from_datasets(ws, 'mslearn-diabates-drift', baseline_data_set, target_data_set,                  # set up data drift detector
                                                      compute_target=cluster_name,
                                                      frequency='Week',
                                                      feature_list=features,
                                                      drift_threshold=.3,
                                                      latency=24,
                                                      alert_config=alertConf)


# ============================== (5). BACKFILL DATA DRIFT MONITOR ==============================
backfillDurationWeeks = 6

startTime = dt.datetime.now() - dt.timedelta(weeks=backfillDurationWeeks)
stopTime = dt.datetime.now()

backfill = monitor.backfill(startTime, stopTime)



# ============================== (6). ANALYZE DATA DRIFT MONITOR ==============================
drift_metrics = backfill.get_metrics()
for metric in drift_metrics:
    print(metric, drift_metrics[metric])
