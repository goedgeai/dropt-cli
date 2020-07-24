# dropt-cli
Dr.Opt is an ML model optimization platform consisting of
- Hyper-parameter optimization service
- Client Python package for service connoction & project control
- Project visualization & analysis via WubUI

`dropt-cli` is the Python client package that allows user
to connect to a Dr.Opt online service.

A public Dr.Opt server is hosted on <https://dropt.goedge.ai>.
Registration is required before using the service.


## Prerequisites
- `Python>=3.6`
- `pip`


## Installation
```console
$ pip install dropt-cli
```


## Examples
One can download our examples from GitHub:

```console
$ git clone https://github.com/GoEdge-ai/dropt-example.git
```


## About
* The modules under [src/dropt/client](./src/dropt/client)
  (`endpoint.py`, `exception.py`, `interface.py`, `objects.py`,
  `requestor.py`, `resource.py`) are modified from
  [sigopt-python](https://github.com/sigopt/sigopt-python),
  which is under the MIT license:

  ```
  The MIT License (MIT)
  
  Copyright (c) 2014-2015 SigOpt Inc.
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```

* The implementation of tuner algorithms are modified from
  [NNI (Neural Network Intelligence)](https://github.com/microsoft/nni),
  which is under the MIT license:

  ```
  Copyright (c) Microsoft Corporation.
  
  MIT License
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  
  THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
  ```
