# Trial Examples
## Overview
Here we provide several examples of DrOpt projects consisting
of different types of optimization problems:
- `func-eggholder`: test function for optimization
- `func-rosenbrock`: another test function for optimization
- `titanic-xgboost`: Titanic survival prediction by XGBoost
- `mnist-pytorch`: handwritten digit recognition with PyTorch framework
- `imagenet-pytorch`: image classification with PyTorch framework



## Run a trial
- Install `dropt-cli` (see `README.md` in the root of the source code).
- Change the current working directory to a trial folder.
- __[optional]__ Install Python packages required by the trial:
  ```console
  $ pip insatll -r requirements.txt
  ```
  > Perform this step only if `requirements.txt` is presented.
- Run the trial via `droptctl`:
  ```console
  $ droptctl -t [token]
  ```
- Note that the datasets required by `titanic-xgboost` and
  `imagenet-pytorch` are not included in the package.
  One needs to download these datasets before running the trials.
  Please see the readme files corresponding to these two trials
  for details.