# Titanic Survival Dataset
## Overview
The dataset is from [kaggle](https://www.kaggle.com/c/titanic/data),
which has been split into two groups:
- training set (`train.csv`)
- test set (`test.csv`)

The __training set__, which contains the outcome (whether a given passenger
survived or not), is used to build your ML models.
On the other hand, the __test set__, in which the outcome is absent,
is used to see how well your model performs on unseen data.
You can submit your result to kaggle to check how good your model is.


## Data dictionary
| Variable | Definition   | Key |
| -------- | ------------ | --- |
| Survival | Survival     | 0 = No, 1 = Yes |
| Pclass   | Ticket class | 1 = 1st, 2 = 2nd, 3 = 3rd |
| Name     | Passenger name | |
| Sex      | Sex | |
| Age      | Age in years | |
| SibSp    | # of siblings / spouses aboard the Titanic | |
| Parch    | # of parents / children abroad the Titanic | |
| Ticket   | Ticket number | |
| Fare     | Passenger fare | |
| Cabin    | Cabin number | |
| Embarked | Port of embarkation | C = Cherbourg, Q = Queenstown, S  = Southampton |
