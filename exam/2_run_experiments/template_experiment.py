
# ============================== (1). PREPROCESSING   ==============================
# Get Run Config

# Read Passed Arguments using Argparse
    # 2 arguments are must, input data path and processed data path (this can be created)

# Fetch Data

# Preprocesssing - before differential privacy
    # Remove Null, Fill missing, etc. Log the summary in experiment run.
    # 

# Create a differential Privacy Step to encode all incoming data (Optional)

# Preprocesssing - after differential privacy
    # Normalise data


# Save the data in datastore

# ============================== (2). EXPERIMENT   ==============================

# Import libraries


# Get Run Config

# Define what arguments to accept and read Passed Arguments using Argparse

# Fetch Data
'''
# load the diabetes dataset
print("Loading Data...")
data = pd.read_csv('data/diabetes.csv')

# Separate features and labels
features = ['Pregnancies','PlasmaGlucose','DiastolicBloodPressure','TricepsThickness','SerumInsulin','BMI','DiabetesPedigree','Age']
X, y = data[features].values, data['Diabetic'].values

'''

# Define Sensitive Features
    # Create a dataframe of only sensitive features
    # You can group them too. For example if age is sensitive feature then you can group them into 2 categories, above and below 50
    # Create x_train,y_train,x_test,y_test,s_train,s_test here 's' is the sensitive features.
'''
# Get sensitive features
S = data[['Age']].astype(int)
# Change value to represent age groups
S['Age'] = np.where(S.Age > 50, 'Over 50', '50 or younger')

# Split data into training set and test set
X_train, X_test, y_train, y_test, S_train, S_test = train_test_split(X, y, S, test_size=0.20, random_state=0, stratify=y)


'''

# Apply Differential Privacy on X-train,Y-train ?? (Optional)
# If the experiment is run without the above preprocessing step and differential privacy has not already been implemented.
# Think if it can be applied to the read data entirely or just to X-train and Y-train, because we are also performing fairness testing how will it affect that dashboard.



# Create/Import and Train Model
    # Log passed hyperparmeter values.
    # Fit model on x-train,y-train

'''
diabetes_model = DecisionTreeClassifier().fit(X_train, y_train)

'''
# What to log?
    # Log in the input passed parameter values
    # Primary Metric, Secondary metric (any list of test metrics)
    # Graphs (like the ROC Curve)

# Define and measure metric
    # yhat = model.predict(x-test)
    # accuracy/AUC/ROC/RMSE etc
    # log metrics

# Create graphs for accuracy or other (OPTIONAL)
    # Log images

# Create model output directory
    # Store Model In pkl file

# Upload the ./outputs folder to folder under the current experiment run 
    # run.upload_file(targetFolderName,sourceFolderName )
# Register Model


# Create and Upload sensitivity dashboard. Detect Fairness.
    # Fetch registered model id, sensitiveFeature and its values as dictionary (Eg. sf = { 'Age': S_test.Age}),ytest, yhat_test(prediction for x_test), and prediction type.
    # create fariness dashboard using above values
    # create a name for the dashboard and upload the dashboard as part of the current run of the experiment

'''
STEP 1 :   Create a dictionary of model(s) you want to assess for fairness 
    
    sf = { 'Race': A_test.race, 'Sex': A_test.sex}
    ys_pred = { lr_reg_id:lr_predictor.predict(X_test) }
    
    from fairlearn.metrics._group_metric_set import _create_group_metric_set

    dash_dict = _create_group_metric_set(y_true=y_test,
                                        predictions=ys_pred,
                                        sensitive_features=sf,
                                        prediction_type='binary_classification')


STEP 2 : UPLOAD
    from azureml.contrib.fairness import upload_dashboard_dictionary, download_dashboard_by_upload_id

    dashboard_title = "Fairness insights of Logistic Regression Classifier"    
    upload_id = upload_dashboard_dictionary(run,            # Set validate_model_ids parameter of upload_dashboard_dictionary to False if you have not registered your model(s)
                                            dash_dict,
                                            dashboard_name=dashboard_title)

STEP 3 :  To test the dashboard, you can download it back and ensure it contains the right information

downloaded_dict = download_dashboard_by_upload_id(run, upload_id)


'''

# Mitigate Fairness (optional)
'''

'''



# Get Explanation, Explanation Client and upload the explanation
'''
Part 1 : UPLOAD EXPLAINER (To be used inside this training script)
    from azureml.interpret import ExplanationClient
    from interpret.ext.blackbox import TabularExplainer

    explainer = TabularExplainer(model, X_train, features=features, classes=labels)
    explanation = explainer.explain_global(X_test)

    # Get an Explanation Client and upload the explanation
    explain_client = ExplanationClient.from_run(run)
    explain_client.upload_model_explanation(explanation, comment='Tabular Explanation')

Part 2 : IF DOWNLOAD EXPLAINAIONS AND GET FEATURE IMPORTANCE AT A LATER POINT FROM ANYWHERE OUTSIDE 
    client = ExplanationClient.from_run(run)
    engineered_explanations = client.download_model_explanation()
    feature_importances = engineered_explanations.get_feature_importance_dict()

    # Overall feature importance
    print('Feature\tImportance')
    for key, value in feature_importances.items():
        print(key, '\t', value)

Part 3 : VISUALISE IN JUPYTER NOTEBOOK

    from interpret_community.widget import ExplanationDashboard
    ExplanationDashboard(global_explanation, model, datasetX=x_test)

'''

# End Run using run.complete()
