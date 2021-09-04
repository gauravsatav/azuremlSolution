# Define ScriptRunConfig for single Experiment

# Define HyperDriveConfig with following parameters
The defined hyperparameter search space
Your early termination policy
The primary metric
Resource allocation settings
ScriptRunConfig script_run_config

# Find the best run
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-tune-hyperparameters#find-the-best-model

# Define search space
* Discrete: Need to add the `choice` keyword before the range/dictionary
    * qnormal
    * quniform
    * qloguniform
    * qlognormal
* Continueous Remove the 'q' from above methods: No need to add `choice` keyword

# Choose Sampling Method
* GridSearch
    * Only discrete search space
    * Supports early termination
    * Can only be used with `choice` parameter

* RandomSampling
    * Both discrete/continueous search space
    * Supports early termination policy
    * 

* BaysianSampling
    * selects next sample based on how the previous one was
    * set max run limit >= 20*(number of hyperparameters being tuned)
    * supports choice,uniform,quniform search space
    * No support for early termination policy.

# Specify primary metric and primary metric goal

# Early termination policy

Pass this as the `policy` parameter to `HyperDriveConfig` class

## Decide when to apply. This needs to be supplied with every type of early termination policy. Both are optional

* `evalutaion_interval` : set to 1 by default, which means evalute after every run.

* `delay_evaluation` : delay first few evaluations

## Policy types:
* Bandit policy : Determine slack 
    * slack factor : Abandon a training run if : 
        currentBestRunInInterval <= (previousBestRunInInterval)/(1+slack_factor)
    * slack_amount: same as before, but instead of ratio its by an amount.

    ```python
    from azureml.train.hyperdrive import BanditPolicy
    early_termination_policy = BanditPolicy(slack_factor = 0.1, evaluation_interval=1, delay_evaluation=5)
    ```

* Median Stopping
    * Stops runs whose primary metric is < median of previous runs
    
    ```python
    from azureml.train.hyperdrive import MedianStoppingPolicy
    early_termination_policy = MedianStoppingPolicy(evaluation_interval=1, delay_evaluation=5)
    ```

* Truncation selection:
    * cancels a percentage of lowest performing runs at each evaluation interval. Runs are compared using the primary metric.
    * you have to define the percentage between 1 and 99
    * A run terminates at interval 5 if its performance at interval 5 is in the lowest 20% of performance of all runs at interval 5.

* No Termination Policy
    
# Other paramters
* max total runs
* max duration run
* max concurrent runs    

# Warm Start
Sampling is handeled differently
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-tune-hyperparameters#warm-start-hyperparameter-tuning-optional


