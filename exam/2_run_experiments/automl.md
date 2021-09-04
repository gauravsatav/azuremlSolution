*  Select your experiment type/task
    * classification, regression, and forecasting

*  Data source and format
    * Data must be in tabular form.
    * The value to predict, target column, must be in the data.

*  Training, validation, and test data
    * If you do not explicitly specify a validation_data or n_cross_validation parameter, automated ML applies default techniques to determine how validation is performed.
    * Default
        * training count > 20,000 rows :	take 10% of the initial training data set
        * 1000 < training count < 20,000 rows : 3 fold Cross-validation approach is applied.
        * training count < 1000 rows : 10 fold CV

*  Compute to run experiment only on:
    * Local
    * Databricks
    * Azure ML Compute (Instance/cluster)

*  Configure your experiment settings
    * Create `AutoMLConfig` object
        * Choose model depending on task (classification/regression/forecasting) 
        
        * Choose `primary_metric` based on task 
            * https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-configure-auto-train#primary-metrics-for-classification-scenarios
            * Classification :
                * `AUC_weighted`  : datasets which are small, have very large class skew
            * Regression:
                * `r2_score` and `spearman_correlation` : the scale of the value-to-predict covers many orders of magnitude
                * `normalized_mean_absolute_error` and `normalized_root_mean_squared_error` :  are useful when the values to predict are in a similar scale.
        * Data Featurization:
            * auto
            * off
            * [custom](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-configure-auto-features#customize-featurization) :
                * featurization_config = FeaturizationConfig()
        * Ensemble configuration : Set as `True` if choosing to switch em on.
            * VotingEnsemble : soft-voting, which uses weighted averages.
            * StackEnsemble : 2 layers : Turn off if you want to use ONNX
        * Stopping Criteria 
            * No criteria
            * after length of time
            * a score has been reached

*  Run experiment
    * To get a featurization summary and understand what features were added to a particular model, see Featurization transparency.

*  Explore models and metrics
    * use `best_run, fitted_model = run.get_output()` to get best model 

*  Monitor automated machine learning runs


*  Register and deploy models
    ```python
    best_run, fitted_model = run.get_output()
    print(fitted_model.steps)

    model_name = best_run.properties['model_name']
    description = 'AutoML forecast example'
    tags = None

    model = remote_run.register_model(model_name = model_name, 
                                    description = description, 
                                    tags = tags)
    ```                                  

*  Model interpretability