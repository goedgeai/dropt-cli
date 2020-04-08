# Trial Examples
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

- Inspect the project result on DrOpt webpage
  (The default one is <https://dropt.neuralscope.org>).
