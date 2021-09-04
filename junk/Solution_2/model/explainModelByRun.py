# from azureml.interpret import ExplanationClient

# run = ''
# # Get the feature explanations
# client = ExplanationClient.from_run(run)
# engineered_explanations = client.download_model_explanation()
# feature_importances = engineered_explanations.get_feature_importance_dict()

# # Overall feature importance
# print('Feature\tImportance')
# for key, value in feature_importances.items():
#     print(key, '\t', value)