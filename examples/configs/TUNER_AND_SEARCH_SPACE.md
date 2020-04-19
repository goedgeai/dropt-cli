# Dr.Opt Tuners & Search Space README
# Tuners

Currently, Dr.Opt provides the following tuners. Below is a brief introduction to the tuner algorithms.

| Name | Information |
| -------- | -------- |
| Anneal     | Annealing algorithm begins by sampling from the prior and tends over time to sample from points closer and closer to the best ones observed.     |
| Naïve Evolution | Naïve Evolution randomly initializes a population-based on the search space, and chooses better ones and does some mutation on them to get the next generation. Naïve Evolution may require many trials to work.  [[reference]](https://arxiv.org/pdf/1703.01041.pdf)
| GP Tuner <br> **[not available now]** | GP (Gaussian Process) Tuner is a sequential model-based optimization (SMBO) approach that uses Gaussian Process as the surrogate. [[reference]](https://github.com/fmfn/BayesianOptimization) |
| Grid Search | Grid Search performs an exhaustive searching through a manually specified subset of the space defined in the search space file. |
| Random     | As the name implies, it randomly selects hyper-parameter combinations through the search space. It's worth noting that researches show that it might be surprisingly effective. [[reference]](http://www.jmlr.org/papers/volume13/bergstra12a/bergstra12a.pdf) |
| TPE | TPE (Tree-structured Parzen Estimator) is a sequential model-based optimization (SMBO) approach that used Tree Parzen Estimators as the surrogate. [[reference]](https://papers.nips.cc/paper/4443-algorithms-for-hyper-parameter-optimization.pdf) |

## Usage of each tuner

### TPE
#### Arguments
* optimize_mode
    * "maximize" or "minimize" (default: "maximize")
#### Example config
```
"tuner": {
    "builtinTunerName": "TPE",
    "classArgs": {"optimize_mode": "maximize"}
}
```

### Random
#### Arguments
(None)
#### Example config
```
"tuner": {
    "builtinTunerName": "Random"
}
```

### Anneal
#### Arguments
* optimize_mode
    * "maximize" or "minimize" (default: "maximize")
#### Example config
```
"tuner": {
    "builtinTunerName": "Anneal",
    "classArgs": {"optimize_mode": "maximize"}
}
```

### Naïve Evolution
#### Arguments
* optimize_mode
    * "maximize" or "minimize" (default: "maximize")
* population_size
    * The initial size of the population in the evolution tuner.
#### Example config
```
"tuner": {
    "builtinTunerName": "Evolution",
    "classArgs": {"optimize_mode": "maximize", "population_size": 100}
}
```

### Grid Search
#### Arguments
(None)
#### Note
It only accepts the following types of search space: 
* `choice`
* `quniform`
* `randint`

#### Example config
```
"tuner": {
    "builtinTunerName": "GridSearch"
}
```

### GP Tuner `(Not available now)`
```diff
- Note: Currently errors may occur while using this tuner. GPTuner is not recommended to use now.
```


#### Arguments
* optimize_mode
    * maximize or minimize, default = maximize
* utility ('ei', 'ucb' or 'poi', optional, default = 'ei')
    * The kind of utility function (acquisition function)
* kappa (float, optional, default = 5) 
    * Used by utility function 'ucb'
* xi (float, optional, default = 0)
    * Used by the 'ei' and 'poi' utility functions, which controls the tendency to explore.
* nu (float, optional, default = 2.5)
    * Used to specify the Matern kernel. It represents the smoothness of the approximated function.
* alpha (float, optional, default = 1e-6)
    * Used to specify noise level in the observations.
* cold_start_num (int, optional, default = 10)
    * Number of random explorations before the Gaussian Process starts.
* selection_num_warm_up (int, optional, default = 1e5) 
    * Number of random points to evaluate when getting the point that maximizes the acquisition function.
* selection_num_starting_points (int, optional, default = 250)
    * Number of times to run L-BFGS-B from a random starting point after the warmup.
    
#### Note
This tuner only supports numerical values:
* `choice` (numerical)
* `quniform`
* `randint`
* `uniform`

#### Example config
```
"tuner": {
    "builtinTunerName": "GPTuner",
    "classArgs":{
        "optimize_mode": "maximize",
        "utility": "ei",
        "kappa": 5.0,
        "xi": 0.0,
        "nu": 2.5,
        "alpha": 1e-6,
        "cold_start_num": 10
    }
}
```

# Search Space

Dr.Opt will suggest parameters according to the user-defined search space.

The define the search space for a parameter, users should provide 3 pieces of informations: parameter name, `_type` and `_value`.

* An example is shown as follow:
```
"search_space": {
    "dropout_rate": {"_type": "uniform", "_value": [0.1, 0.5]},
    "conv_size": {"_type": "choice", "_value": [2, 3, 5, 7]},
    "hidden_size": {"_type": "choice", "_value": [124, 512, 1024]},
    "batch_size": {"_type": "choice", "_value": [50, 250, 500]},
    "learning_rate": {"_type": "uniform", "_value": [0.0001, 0.1]}
}
```

The details of each search space type are listed in the below sections.

## Search space types

### Choice
The user provides a list of numbers or strings, which indicates the available options for the tuner.
#### Value format
* a list of numbers or strings: [0.1, 0.01, 0.001, 0.0001] or ["Adam", "SGD", "Adadelta"]
#### Example
```
"learn_rate":{ 
    "_type": "choice", 
    "_value": [0.1, 0.01, 0.001, 0.0001]
}
```

### Random integer
Choosing a random integer from lower (inclusive) to upper (exclusive).
#### Value format
* [ lower_bound, upper_bound ]
#### Example
```
"batch_size": {
    "_type": "randint",
    "_value": [8, 65]
}
```
* In this example, the suggested numbers of batch size will be integers that >=8 and < 65.

### Uniform
Which means the chosen value is a value uniformly between low and high.
#### Value format
* [ lower_bound, upper_bound ]
#### Example
```
"dropout_rate": {
    "_type": "uniform",
    "_value": [0.1, 0.5]
}
```
* In this example, the suggested droptout rate will be an real number between (0.1, 0.5).

### Quniform
The chosen value will be a value that between the lower bound and the upper bound, and the generated value will be constrained by the `step`.
#### Value format
* [ lower_bound, upper_bound, step ]
#### Example
```
"input_size": {
    "_type": "quniform",
    "_value": [224,417,32]
}
```
* In this example, the suggested input size will be a number that between ```[224, 417)```. To be more specific, the possible values are: [224, 256, 288, 320, ... , 384, 416].

### Normal
Which means the variable value is a real value that’s normally-distributed with mean(μ) and standard deviation(σ).
#### Value format
* [ μ, σ ]
#### Example
```
"dropout_rate": {
    "_type": "normal",
    "_value": [0.5, 0.1]
}
```
* In this example, the suggested input size will be a number that randomly sampled from the normal distribution N(0.5, 0.1^2).

# Reference
### Tuning algorithms
* https://optunity.readthedocs.io/en/latest/user/solvers/TPE.html
* https://nni.readthedocs.io/en/latest/Tuner/EvolutionTuner.html
* https://github.com/microsoft/nni/blob/master/docs/en_US/Tuner/GridsearchTuner.md
* https://github.com/microsoft/nni/blob/master/docs/en_US/Tuner/BuiltinTuner.md
### Search space
* https://nni.readthedocs.io/en/latest/Tutorial/SearchSpaceSpec.html
