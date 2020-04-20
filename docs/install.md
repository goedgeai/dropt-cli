---
title: Install
---
# Install
Here we show how one can install the
client Python package of DrOpt (`dropt-cli`).


## Required packages
- `Python>=3.5`
- `pip>=20.0.0`
- `virtualenv` (recommended)


## Install required package
If running linux distribution such as Ubuntu,
one can perform the following commands to install
required packages.

```console
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install python3 python3-pip
$ sudo pip install --upgrade pip
```


## [Optional] Set up Python virtual environment
We recommend users to set up virtual environment
for `dropt-cli`.

- Install `virtualenv`
  ```console
  $ sudo pip install --upgrade virtualenv
  ```

- Create and activate virtual environment
  ```console
  $ virtualenv venv
  $ source venv/bin/activate
  ```

- Deactivate virtual environment
  ```console
  $ deactivate
  ```


## Download/Install `dropt-cli`
A repository of `dropt-cli` is hosted on
[GitHub](https://github.com/NeuralScope/dropt-cli).

### with Git
One can download the source code from GitHub with Git and
install the package.

- Download the source code
  ```console
  $ git clone https://github.com/NeuralScope/dropt-cli
  ```

- Install the package
  ```console
  $ cd dropt-cli
  $ pip install .
  ```

### without Git
Alternatively, we provide __wheel binary distribution__
and __source code archive__ for the
[latest release of `dropt-cli`](https://github.com/NeuralScope/dropt-cli/releases/latest).
Simply click links on the page to acquire these files.

The `.whl` file is sufficient for installing `dropt-cli`.
Nevertheless, if one needs the source code and examples of `dropt-cli`,
she/he needs to download the source code archive (`.zip` or `.tar.gz` files).

- Install the package from wheel binary distribution
  ```
  $ pip install [the filename of the wheel file]
  ```
