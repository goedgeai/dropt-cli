"""
Reference
---
https://www.twblogs.net/a/5c4a9fb8bd9eee6e7e068b5f
"""

import logging
import argparse
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn import model_selection


# setup logs
logger = logging.getLogger("sklearn_randomForest")

# setup path to data
DATA_PATH = '../../data/titanic'


def data_loader():
    '''Load dataset'''
    data = pd.read_csv(f'{DATA_PATH}/train.csv')

    # data imputation
    fill_values = {'Age': data['Age'].median(), 'Embarked': 'S'}
    data.fillna(fill_values, inplace=True)

    # encode values of 'Sex' and 'Embarked' by integers
    replace_values = {'Sex': {'male': 0, 'female': 1},
                      'Embarked': {'S': 0, 'C': 1, 'Q': 2}}
    data.replace(replace_values, inplace=True)

    # determine features and label
    features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
    label = 'Survived'

    X, y = data[features], data[label]
    return X, y


def get_params():
    """get parameters"""
    parser = argparse.ArgumentParser(description='Titanic XGBoost Example')
    parser.add_argument("-d", "--max_depth", type=int, default=5)
    parser.add_argument("-g", "--gamma", type=float, default=0.2)
    parser.add_argument("-s", "--subsample", type=float, default=0.8)
    parser.add_argument("-c", "--colsample", type=float, default=0.8, dest='colsample_bytree')
    parser.add_argument("-a", "--alpha", type=float, default=0.25)
    parser.add_argument("-l", "--lr", type=float, default=0.01, dest='eta')
    parser.add_argument("-w", "--min_child_weight", type=float, default=1.0)

    args, _ = parser.parse_known_args()
    return vars(args)


def get_model(params):
    model = XGBClassifier(booster="gbtree", silent=True, nthread=None,
                          random_state=None, base_score=0.5,
                          colsample_bylevel=1, n_estimators=50,
                          reg_lambda=1, objective="binary:logistic",
                          **params)

    return model


def main(X, y, model):
    """Train model and predict result"""
    kf = model_selection.KFold(n_splits=5, shuffle=False, random_state=None)
    scores = model_selection.cross_val_score(model, X, y, cv=kf)
    #print(scores)
    score = scores.mean()
    print(score)
    logger.debug(f"score: {score}")


if __name__ == "__main__":
    X, y = data_loader()
    params = get_params()
    logger.debug(params)
    model = get_model(params)
    main(X, y, model)
