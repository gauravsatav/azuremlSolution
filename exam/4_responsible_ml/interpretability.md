# Interpretability Techniques
https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-interpretability#supported-interpretability-techniques

MimicExplainer - Creates a new surrogate model to explain the results. We can use one of the 4 models as a surrogate model.

LGBMExplainableModel
LinearExplainableModel
SGDExplainableModel
DecisionTreeExplainableModel


PFIExplainer does not support local explanations.


# [Steps](https://docs.microsoft.com/en-gb/azure/machine-learning/how-to-machine-learning-interpretability-aml#generate-feature-importance-value-on-your-personal-machine)

## 1 Choose an explainer
```python
from interpret.ext.blackbox import TabularExplainer

# "features" and "classes" fields are optional
explainer = TabularExplainer(model, 
                             x_train, 
                             features=breast_cancer_data.feature_names, 
                             classes=classes)
```

## 2 Get global or local explainations

* Global
    PFIExplainer does not support local explanations.

    *  global_explanation = explainer.explain_global(x_test)
    
    *  global_explanation.get_ranked_global_values()
    *  global_explanation.get_ranked_global_names()
    *  global_explanation.get_feature_importance_dict()

* Local

    *  local_explanation = explainer.explain_local(x_test[0:5])
    *  sorted_local_importance_names = local_explanation.get_ranked_local_names()
    *  sorted_local_importance_values = local_explanation.get_ranked_local_values()

### Raw untransformed features

If you have created transformed features through a pre-processing pipline earlier,
You can choose to only pass the raw untransformed features by passing this pipline info to your transformer.

## Remote runs
Create a `train.py` script for the explaination and submit as experiment on amlCompute

## Visualization
To load the explanations dashboard widget in your Jupyter Notebook, use the following code:
```python
from interpret_community.widget import ExplanationDashboard

ExplanationDashboard(global_explanation, model, datasetX=x_test)
```

## Troubleshooting

* Sparse data not supported
* Forecasting models not supported with model explanations
* Local explanation for data index
* What-if/ICE plots not supported in studio: