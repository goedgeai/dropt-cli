# Titanic-xgboost example
This example shows how to use Dr.Opt to optimize a XGBoost model
trained on [Kaggle Titanic dataset](https://www.kaggle.com/c/titanic).


## Components
```
.
├── dropt_client.py     // dropt client API example
├── config.json         // configuration file
├── xgb.py              // training program
└── requirements.txt    // requirement packages of this example (xgboost, etc.)
```


## Hyperparameters
* max\_depth
* gamma
* subsample
* colsample\_bytree
* alpha
* eta (learning rate)

As for the detailed information of each hyperparameters, please refer to
[XGBoost document](https://xgboost.readthedocs.io/en/latest/parameter.html).


## Execution
This example uses the [argparse module](https://docs.python.org/3/library/argparse.html).
You can specify the arguments via command line, as below:
```
python3 dropt_client.py -t [USER_TOKEN] -c tpe.json -i dropt-beta.nctu.me
```

Or add `USER_TOKEN`, `DROPT_IP` in [dropt_client.py](./dropt_client.py) and execute by
```
python3 dropt_client.py
```
