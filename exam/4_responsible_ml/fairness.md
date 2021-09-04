# Fairness
The Fairlearn open-source package has two components:

Assessment Dashboard: A Jupyter notebook widget for assessing how a model's predictions affect different groups. It also enables comparing multiple models by using fairness and performance metrics.

Mitigation Algorithms: A set of algorithms to mitigate unfairness in binary classification and regression.

## General Concept

* Fairness works at group level. These groups are defined by the sensitive features.

* Fairness is quantified through disparity metrics calculated for each of the subgroups.
    * Disparity in model performance (accuracy vs Precision vs Recall vs F1 etc)
    * Disparity in selection rate

* Mitigating unfairness
    * Pairity constraints: Parity constraints require some aspects of the predictor behavior to be comparable across the groups that sensitive features define (e.g., different races).
    * Types of Pairity
        * Demographic parity: Proportion of each segment of a protected class (e.g. gender) should receive the positive outcome at equal rates. Positive Rate (PR). PR(Group A) = PR (Group B). Same number should be present.
        * Equalized odds : TRP-A = TRP-B and FPR-A = FPR-B
        * Equal opportunity : TPR-A = TRP-B where TRP = True Positive Rate
        * Bounded group loss : 
    * Mitigation Algorithms:
        * Reduction
            * ExponentiatedGradient 
            * GridSearch
            * GridSerach 
            * ThresholdOptimizer

## How to use in experiment

Check the experiment [template](../../expr_1_decisionTreeClassifier/template_experiment.py)

https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-fairness-aml
