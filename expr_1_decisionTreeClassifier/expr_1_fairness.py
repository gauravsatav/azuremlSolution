# Import Model to be pass for mitigation in grid search.
from sklearn.tree import DecisionTreeClassifier


# For uploading dashboard.
from fairlearn.metrics._group_metric_set import _create_group_metric_set
from azureml.contrib.fairness import upload_dashboard_dictionary, download_dashboard_by_upload_id



# Libraries for mitigating unfairness
from fairlearn.reductions import GridSearch, EqualizedOdds


# For model storing Registration purposes
import joblib
import os
from azureml.core import Model


def measureFairness(myWorkspace,currentModel,modelPath,runInstance,yTest,xTest,sensitiveFeatureDict,typeOfPrediction='binary_classification'):
    
    registered_model = Model.register(model_path=modelPath,
                                  model_name='unmitigated fairness model',
                                  workspace=myWorkspace)
    model_id= registered_model.id

    yHat = { model_id:currentModel.predict(xTest) }

    dash_dict = _create_group_metric_set(y_true=yTest,
                                        predictions=yHat,
                                        sensitive_features=sensitiveFeatureDict,
                                        prediction_type=typeOfPrediction)

    try:
        dashboard_title = "Fairness insights of Diabetes Classifier"
        upload_id = upload_dashboard_dictionary(runInstance,
                                                dash_dict,
                                                dashboard_name=dashboard_title)
        print("\nUploaded to id: {0}\n".format(upload_id))

    except Exception as exp:
        print(f"There was an error uploading dashboard. Details:\n {exp}")


def mitigateUnfairness(myWorkspace,currentModel,runInstance,sensitiveFeatureDict,X_train,X_test,y_train,y_test,S_train,S_test):

    print('Finding mitigated models...')

    # Train multiple models
    sweep = GridSearch(DecisionTreeClassifier(),
                    constraints=EqualizedOdds(),
                    grid_size=20)

    sweep.fit(X_train, y_train, sensitive_features=S_train.Age)
    models = sweep.predictors_

    # Save the models and get predictions from them (plus the original unmitigated one for comparison)
    model_dir = 'mitigated_models'
    os.makedirs(model_dir, exist_ok=True)
    model_name = 'diabetes_unmitigated'
    print(model_name)
    joblib.dump(value=currentModel, filename=os.path.join(model_dir, '{0}.pkl'.format(model_name)))
    predictions = {model_name: currentModel.predict(X_test)}
    i = 0
    for model in models:
        i += 1
        model_name = 'diabetes_mitigated_{0}'.format(i)
        print(model_name)
        joblib.dump(value=model, filename=os.path.join(model_dir, '{0}.pkl'.format(model_name)))
        predictions[model_name] = model.predict(X_test)

    # Register the models
    registered_model_predictions = dict()
    for model_name, prediction_data in predictions.items():
        model_file = os.path.join(model_dir, model_name + ".pkl")
        registered_model = Model.register(model_path=model_file,
                                        model_name=model_name,
                                        workspace=myWorkspace)
        registered_model_predictions[registered_model.id] = prediction_data

    #  Create a group metric set for binary classification based on the Age feature for all of the models
    dash_dict = _create_group_metric_set(y_true=y_test,
                                        predictions=registered_model_predictions,
                                        sensitive_features=sensitiveFeatureDict,
                                        prediction_type='binary_classification')

    
    # Upload the dashboard to Azure Machine Learning
    try:
        dashboard_title = "Fairness Comparison of Diabetes Models"
        upload_id = upload_dashboard_dictionary(runInstance,
                                                dash_dict,
                                                dashboard_name=dashboard_title)
        print("\nUploaded to id: {0}\n".format(upload_id))
    except Exception as exp:
        print(f"There was an error uploading dashboard. Details:\n {exp}")
