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
params = {'booster': 'gbtree',
          'verbosity': 0,
          'base_score': 0.5,
          'colsample_bylevel': 1,
          'n_estimators': 50,
          'objective': "binary:logistic",
          'max_depth': 5,
          'gamma': 0.2,
          'subsample': 0.8,
          'colsample-bytree': 0.8,
          'lambda': 1,
          'alpha': 0.25,
          'eta': 0.01,
          'min_child_weight': 1.0}
                  

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
    '''Model loader'''
    model = XGBClassifier(**params)

    return model


def run(args):
    '''Evaluate performance of the model with the given parameters'''
    X, y = data_loader()
    params.update(args)
    model = model_loader(params)
    kf = model_selection.KFold(n_splits=5, shuffle=False)
    scores = model_selection.cross_val_score(model, X, y, cv=kf)
    score = scores.mean()
    logger.debug(f'score: {score:10.6f}')
    return score


def params_loader():
    '''Get parameters'''
    parser = ArgumentParser(description='Titanic XGBoost Example')
    parser.add_argument('--booster', type=str)
    parser.add_argument('--verbosity', type=int)
    parser.add_argument('--base_score', type=float)
    parser.add_argument('--colsample-bylevel', type=float)
    parser.add_argument('--n_estimators', type=int)
    parser.add_argument('--objective', type=str)
    parser.add_argument('--max-depth', type=int)
    parser.add_argument('--gamma', type=float)
    parser.add_argument('--subsample', type=float)
    parser.add_argument('--colsample-bytree', type=float)
    parser.add_argument('--alpha', type=float)
    parser.add_argument('--learning-rate', type=float)
    parser.add_argument('--min-child-weight', type=float)

    args, _ = parser.parse_known_args()
    params = {k: v for k, v in vars(args).items() if v is not None}
    return params


if __name__ == '__main__':
    params.update(params_loader())
    logger.debug(f'parameters = {params}')
    print(run(params))
