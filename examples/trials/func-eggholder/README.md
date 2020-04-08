# Eggholder Function
The Eggholder function is a function defined on the two-dimensional Euclidean space.
To be more explicit,

![Eggholder formula][formula]

The graph of the function is as follows:

![The graph of Eggholder][graph]

Within area ![area formula][area], the Eggholder function admits the
__global minimum -959.6407 at (512,404.2319)__.


## Run model script
Run the following command to evaluate the function:
```console
$ python eggholder [x] [y]
```

(`[x]` and `[y]` are __float__.)


## Apply DrOpt service
See trial readme.



[formula]: https://latex.codecogs.com/png.latex?f(x,y)=-(y&plus;47)\sin\sqrt{\left\lvert\frac{x}{2}&plus;(y&plus;47)\right\rvert}-x\sin\sqrt{\left\lvert&space;x-(y&plus;47)\right\rvert}
[graph]: https://i.imgur.com/u9MsMJZ.jpg
[area]: https://latex.codecogs.com/png.latex?\inline&space;-512\le&space;x,y\le&space;512
