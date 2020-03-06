'''
Reference
---
https://www.twblogs.net/a/5c4a9fb8bd9eee6e7e068b5f
'''

import logging
import numpy as np
import pandas as pd
from argparse import ArgumentParser
from sklearn import model_selection
from xgboost import XGBClassifier


# setup logs
logger = logging.getLogger("sklearn_randomForest")

# setup path to data
DATA_PATH = '../../data/titanic'

# default value of parameters
params_default = {'booster': 'gbtree',
                  'verbosity': 0,
                  'base_score': 0.5,
                  'colsample_bylevel': 1,
                  'n_estimators': 50,
                  'reg_lambda': 1,
                  'objective': "binary:logistic"}
                  

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


def model_loader(params):
    '''Model loader.'''
    model = XGBClassifier(booster="gbtree", silent=True, nthread=None,
                          base_score=0.5, colsample_bylevel=1, n_estimators=50,
                          reg_lambda=1, objective="binary:logistic",
                          **params)

    return model


def run(args):
    '''Evaluate performance of model with the given parameters.'''
    X, y = data_loader()
    params = params_default.copy()
    params.update(args)
    model = model_loader(params)
    kf = model_selection.KFold(n_splits=5, shuffle=False)
    scores = model_selection.cross_val_score(model, X, y, cv=kf)
    score = scores.mean()
    logger.debug(f"score: {score}")
    return score


def params_loader():
    '''get parameters'''
    parser = ArgumentParser(description='Titanic XGBoost Example')
    parser.add_argument('--booster', type=str, default='gbtree')
    parser.add_argument('--verbosity', type=int, default=0)
    parser.add_argument('--nthread', type=str, default='none')
    parser.add_argument('--max-depth', type=int, default=5)
    parser.add_argument('--gamma', type=float, default=0.2)
    parser.add_argument('--subsample', type=float, default=0.8)
    parser.add_argument('--colsample-bytree', type=float, default=0.8)
    parser.add_argument('--alpha', type=float, default=0.25)
    parser.add_argument('--learning-rate', type=float, default=0.01)
    parser.add_argument('--min-child-weight', type=float, default=1.0)

    args, _ = parser.parse_known_args()
    return vars(args)


if __name__ == '__main__':
    params = params_loader()
    logger.debug(f'parameters = {params}')
    print(main(params))
