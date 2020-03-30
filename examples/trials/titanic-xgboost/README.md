# Titanic-xgboost example
This example shows how to use Dr.Opt to optimize a XGBoost model
trained on [Kaggle Titanic dataset](https://www.kaggle.com/c/titanic).



## Components
```
.
├── config.json         // project configuration
├── titanic_xgb.py      // model Python code
└── requirements.txt    // required Python packages (xgboost, etc.)
```



## Hyperparameters
* max\_depth
* gamma
* subsample
* colsample\_bytree
* alpha
* eta (learning rate)

As for the detail of hyper-parameters, please see
[XGBoost document](https://xgboost.readthedocs.io/en/latest/parameter.html).
