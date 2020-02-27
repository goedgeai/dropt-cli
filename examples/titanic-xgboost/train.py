"""
Reference
---
https://www.twblogs.net/a/5c4a9fb8bd9eee6e7e068b5f
"""

import logging

import argparse as arg
import numpy as np
import pandas as pd

from xgboost import XGBClassifier
from sklearn import model_selection


# parse arguments
parser = arg.ArgumentParser()
parser.add_argument("-d", "--max_depth", dest="max_depth", type=int, default=5)
parser.add_argument("-g", "--gamma", dest="gamma", type=float, default=0.2)
parser.add_argument("-s", "--subsample", dest="subsample", type=float, default=0.8)
parser.add_argument("-c", "--colsample", type=float, dest="colsample", default=0.8)
parser.add_argument("-a", "--alpha", dest="alpha", type=float, default=0.25)
parser.add_argument("-l", "--lr", dest="lr", type=float, default=0.01)
args = parser.parse_args()

# setup logs
LOG = logging.getLogger("sklearn_randomForest")

# setup path to data
DATA_PATH = '../../data/titanic'


def load_data():
    '''Load dataset'''
    data_train = pd.read_csv(f'{DATA_PATH}/train.csv')

    # data imputation
    fill_values = {'Age': data_train['Age'].median(), 'Embarked': 'S'}
    data_train.fillna(fill_values, inplace=True)

    # encode values of 'Sex' and 'Embarked' by integers
    replace_values = {'Sex': {'male': 0, 'female': 1},
                      'Embarked': {'S': 0, 'C': 1, 'Q' 2}}
    data_train.replace(replace_values, inplace=True)

    # determine features and label
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    label = ['Survived']

    X_train, y_train = data_train[features], data_train[label]
    return X_train, y_train


def get_default_parameters():
    """get default parameters"""
    params = {
        "max_depth": args.max_depth,
        "min_child_weight": 1,
        "gamma": args.gamma,
        "subsample": args.subsample,
        "colsample_bytree": args.colsample,
        "reg_alpha": args.alpha,
        "learning_rate": args.lr
    }
    return params


def get_model(PARAMS):
    model = XGBClassifier(booster="gbtree", silent=True, nthread=None, random_state=None, base_score=0.5,
                          colsample_bylevel=1, n_estimators=50, reg_lambda=1, objective="binary:logistic")
    model.max_depth = PARAMS.get("max_depth")
    model.min_child_weight = PARAMS.get("min_child_weight")
    model.gamma = PARAMS.get("gamma")
    model.subsample = PARAMS.get("subsample")
    model.colsample_bytree = PARAMS.get("colsample_bytree")
    model.reg_alpha = PARAMS.get("reg_alpha")
    model.learning_rate = PARAMS.get("learning_rate")

    return model


def run(X_train, y_train, model):
    """Train model and predict result"""
    kf = model_selection.KFold(n_splits=5, shuffle=False, random_state=None)
    scores = model_selection.cross_val_score(model, X_train, y_train, cv=kf)
    # print(scores)
    score = scores.mean()
    print(score)
    LOG.debug(f"score: {score}")


if __name__ == "__main__":
    X_train, y_train = load_data()
    PARAMS = get_default_parameters()
    LOG.debug(PARAMS)
    model = get_model(PARAMS)
    run(X_train, y_train.values.ravel(), model)
