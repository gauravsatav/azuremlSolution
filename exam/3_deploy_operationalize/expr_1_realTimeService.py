import azureml.core
from azureml.core import Workspace

from azureml.core import Model

import os

from azureml.core.conda_dependencies import CondaDependencies

from azureml.core.webservice import AciWebservice
from azureml.core.model import InferenceConfig

import json


# ============================== (1). GET WORKSPACE CONTEXT ==============================
ws = Workspace.from_config()
print('Ready to use Azure ML {} to work with {}'.format(azureml.core.VERSION, ws.name))

# ============================== (2). FETCH THE MODEL TO BE PUBLISH FROM LIST OF MODELS REGISTERED IN THE WORKSPACE ==============================
for model in Model.list(ws):
    print(model.name, 'version:', model.version)
    for tag_name in model.tags:
        tag = model.tags[tag_name]
        print ('\t',tag_name, ':', tag)
    for prop_name in model.properties:
        prop = model.properties[prop_name]
        print ('\t',prop_name, ':', prop)
    print('\n')

myModelName = 'diabetes_model'
model = ws.models[myModelName]
print(model.name, 'version', model.version)

# ============================== (3). SETUP SCORING FOLDER AND SCRIPT ==============================
experimentFolder = 'expr_1_Service'
scoringScriptName = 'expr_1_score.py'
scorintScriptPath = os.path.join(experimentFolder,scoringScriptName)

# ============================== (4). CREATE ENV CONFIG FILE ==============================
configEnv = CondaDependencies()                                                                   # Add the dependencies for our model (AzureML defaults is already included)
configEnv.add_conda_package('scikit-learn')


envConfigFileName = 'expr_1_serviceEnvConfig.yml'
envConfigFileNamePath = os.path.join(experimentFolder,envConfigFileName)
with open(envConfigFileNamePath,"w") as f:                                                       # Save the environment config as a .yml file
    f.write(configEnv.serialize_to_string())

print("Saved dependency info in", envConfigFileNamePath)

# ============================== (5). CONFIGURE INFERENCE/SCORING ENV. AND PASS IT AS A PARAMETER TO DEPLOY MODEL AS A SERVICE  ==============================
service_name = "diabetes-service"
numberOfCores = 1
gbOfMemory = 1

inference_config = InferenceConfig(runtime= "python",                                                   # Configure the scoring environment
                                   entry_script=scorintScriptPath,
                                   conda_file=envConfigFileNamePath)

deployment_config = AciWebservice.deploy_configuration(cpu_cores = numberOfCores, memory_gb = gbOfMemory,auth_enabled=False)

# If you want to collect back the data then deployig using AKS
# While defining the config : aks_config = AksWebservice.deploy_configuration(collect_model_data=True)
# Additionally you can turn on application insight : aks_config = AksWebservice.deploy_configuration(collect_model_data=True, enable_app_insights=True)
# To Stop data collection use : <service_name>.update(collect_model_data=False)

service = Model.deploy(ws, service_name, [model], inference_config, deployment_config)
service.wait_for_deployment(True)
print(service.state)
print(service.get_logs())


# ============================== (4). ENABLE MODEL MONITORING ==============================
''' WILL COST MONEY, AS THIS IS A SEPERATE OFFERING
 The offering is called "Azure Application Insights"
'''

service.update(enable_app_insights=True)            # Enable AppInsights 
print('AppInsights enabled!')



# ============================== (4). MANAGE OLD-VERSIONS OF WEB SERVICE ==============================
for webservice_name in ws.webservices:
    print(webservice_name)


# If you need to make a change and redeploy, you may need to delete unhealthy service using the following code:
    # from azureml.core.webservice import Webservice
    # service = Webservice(workspace=ws,name='diabetes-service')
    # service.delete()

# ============================== (4). EXAMPLE 1 OF HOW TO MAKE CALLS TO THE WEB SERVICE ==============================

'''             TO FETCH A SERVICE BY NAME

    # List of all Webservices in a ws:
    ws.webservices

    myWebserviceName = 'diabetes-service'
    from azureml.core.webservice import Webservice
    service = Webservice(workspace=ws,name=myWebserviceName)
'''
x_new = [[2,180,74,24,21,23.9091702,1.488172308,22]]
print ('Patient: {}'.format(x_new[0]))

input_json = json.dumps({"data": x_new})                                                                        # Convert the array to a serializable list in a JSON document
predictions = service.run(input_data = input_json)                                                              # Call the web service, passing the input data (the web service will also accept the data in binary format)
predicted_classes = json.loads(predictions)                                                                     # Get the predicted class - it'll be the first (and only) one.
print(predicted_classes[0])

endpoint = service.scoring_uri
print(endpoint)

# ============================== (4). EXAMPLE 2 OF HOW TO MAKE CALLS TO THE WEB SERVICE ==============================
x_new = [[2,180,74,24,21,23.9091702,1.488172308,22],                                                            # This time our input is an array of two feature arrays
         [0,148,58,11,179,39.19207553,0.160829008,45]]


input_json = json.dumps({"data": x_new})                                                                        # Convert the array or arrays to a serializable list in a JSON document
predictions = service.run(input_data = input_json)                                                              # Call the web service, passing the input data
predicted_classes = json.loads(predictions)                                                                     # Get the predicted classes.

for i in range(len(x_new)):
    print ("Patient {}".format(x_new[i]), predicted_classes[i] )


# ============================== (4). DELETE SERVICE ==============================
service.delete()
print ('Service deleted.')