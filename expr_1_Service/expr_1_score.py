import json
import joblib
import numpy as np
from azureml.core.model import Model


def init():                                                                                             # Called when the service is loaded
    global model                                                                                        # Get the path to the deployed model file and load it
    model_path = Model.get_model_path('diabetes_model')
    model = joblib.load(model_path)
    # Choose to import explaination model here
    # You can choose to enable data collection here

def run(raw_data):                                                                                      # Called when a request is received
    data = np.array(json.loads(raw_data)['data'])                                                       # Get the input data as a numpy array
    predictions = model.predict(data)                                                                   # Get a prediction from the model
    classnames = ['not-diabetic', 'diabetic']                                                           # Get the corresponding classname for each prediction (0 or 1)
    predicted_classes = []
    for prediction in predictions:
        predicted_classes.append(classnames[prediction])
    return json.dumps(predicted_classes)                                                                # Return the predictions as JSON

'''
--------- FOR DATA COLLECTION -------
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-enable-data-collection

add to init() function
    from azureml.monitoring import ModelDataCollector
    global inputs_dc, prediction_dc
    inputs_dc = ModelDataCollector("best_model", designation="inputs", feature_names=["feat1", "feat2", "feat3", "feat4", "feat5", "feat6"])
    prediction_dc = ModelDataCollector("best_model", designation="predictions", feature_names=["prediction1", "prediction2"])

add to run() function
    inputs_dc.collect(data) #this call is saving our input data into Azure Blob
    prediction_dc.collect(result) #this call is saving our input data into Azure Blob


'''