# Rosenbrock Function
The Rosenbrock function is defined on _n_-dimensional Euclidean space.
To be more explicit,

![Rosenbrock formula][formula]

Here is the graph of the function in the case _n_=2:
![Rosenbrock graph][graph]

The Rosenbrock function admits the
__global minimum 0 at (1,1,...,1)__ in ![area][area].


## Run model script
We consider the Rosebrock function in the case _n_=3.
To evaluate, run the following command:
```console
$ python rosenbrock [x] [y] [z]
```

(`[x]`, `[y]` and `[z]` are float.)


## Apply DrOpt service
See trial readme.



[formula]: https://latex.codecogs.com/png.latex?f(\mathbf&space;x)=\sum_{i=1}^{n-1}\left[100\left(x_{i&plus;1}-x_i^2\right)^2&plus;(1-x_i)^2&space;\right&space;]
[graph]: https://i.imgur.com/XiKQ9LN.jpg
[area]: https://latex.codecogs.com/png.latex?\mathbb&space;R^n
