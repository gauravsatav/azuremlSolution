https://docs.microsoft.com/en-us/azure/machine-learning/how-to-track-monitor-analyze-runs?tabs=python

* run.get_status()
    * Common values returned include "Running", "Completed", and "Failed".

* run.get_details()
    * run ID, execution time, and other details about the run


* run.add_properties({"author":"azureml-user"}
    * run.get_properties() properties are immutable, tags can be changed

* run.tag("quality", "great run")
    * run.get_tags()

* To log metrics
https://docs.microsoft.com/en-us/azure/machine-learning/how-to-log-view-metrics
    * run.log('AUC', np.float(auc))
    * run.log_list()
    * run.log_row()
    * run.log_image()


* Child Runs
    * mychildRun = run.child_run() to create child run
        * mychildRun.log()
        * As they move out of scope, child runs are automatically marked as completed.
    * get_children() to get child runs


* Pipelines
    * for run in pipeline_run.get_children():

* run.get_metrics()
    * 

* IN Auto ML
    * best_run_customized, fitted_model_customized = remote_run.get_output()
    * for run in automl_run.get_children()
    * run.get_metrics()

* Hyperdrive
    * best_run = run.get_best_run_by_primary_metric()
    * for child_run in run.get_children_sorted_by_primary_metric()
    * best_run_metrics = best_run.get_metrics()
        * print(' -AUC:', best_run_metrics['AUC'])
    * script_arguments = best_run.get_details() ['runDefinition']['arguments']

* Batch Inferencing Pipeline
    * prediction_run = next(pipeline_run.get_children())
    * prediction_output = prediction_run.get_output_data('inferences')
    * prediction_output.download(local_path='diabetes-results')

* run.get_details_with_logs()
    * Used to get last run info with log files

* summaryTable = automl_run.get_summary()
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

* 
    * 

