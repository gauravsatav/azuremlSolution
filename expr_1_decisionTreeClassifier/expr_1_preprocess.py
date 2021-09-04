# Import libraries
import os
import argparse
import pandas as pd
from azureml.core import Run
from sklearn.preprocessing import MinMaxScaler

# Get parameters
parser = argparse.ArgumentParser()
parser.add_argument("--input-data", type=str, dest='raw_dataset_id', help='raw dataset')
parser.add_argument('--prepped-data', type=str, dest='prepped_data', default='prepped_data', help='Folder for results')
args = parser.parse_args()
save_folder = args.prepped_data

# Get the experiment run context
run = Run.get_context()


'''
    We are not reading the data as a passed argument here.
    What happens is while passing the training dataset as argument, we actually run a command called dataset.as_named_input('raw_data').

    This command creates a dataset within the run context by the name 'raw_data'. This dataset within the run context is then accessed using the command given below.
    which is
    run.input_datasets['raw_data'].
    The dest called 'raw_dataset_id' is un-utilized to read the dataset. We could have chosen to pass the dataset as an argument and then read
    datasetId = args.raw_dataset_id
    diabetes = ws.getdatasetbyid(datasetId)     !!!  This is not an actual command. See how to get fetch dataset from its id from azureml docs.
'''
print("Loading Data...")                                        # load the data (passed as an input dataset). READ THE COMMENT SECTION ABOVE.
diabetes = run.input_datasets['raw_data'].to_pandas_dataframe()

# Log raw row count
row_count = (len(diabetes))
run.log('raw_rows', row_count)

# remove nulls
diabetes = diabetes.dropna()


''' ADDING DIFFERENTIAL PRIVACY USING SMARTNOISE SDK 

    Differential privacy is a technique that is designed to preserve the privacy of individual data points by adding "noise" to the data.
    The goal is to ensure that enough noise is added to provide privacy for individual values while ensuring that the overall statistical makeup of the data remains consistent, and aggregations produce statistically similar results as when used with the original raw data.

    import opendp.smartnoise.core as sn
    
    !! READ ME !!
    Smartnoise is added for the purposes of Data Analysis not for the purpose of Machine Learning.
    Therefore, if you choose to use this technique, store the csv data file in a seperate location, with the name "dataForDashboarding.csv"

    This data can then be used to create dashboards and perform other data analysis.
'''


# Normalize the numeric columns
scaler = MinMaxScaler()
num_cols = ['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness','SerumInsulin','BMI','DiabetesPedigree']
diabetes[num_cols] = scaler.fit_transform(diabetes[num_cols])

# Log processed rows
row_count = (len(diabetes))
run.log('processed_rows', row_count)

# Save the prepped data
print("Saving Data...")
os.makedirs(save_folder, exist_ok=True)
save_path = os.path.join(save_folder,'data.csv')
diabetes.to_csv(save_path, index=False, header=True)

# End the run
run.complete()