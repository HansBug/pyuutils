# pyuutils

Python Wrapper for Uppaal [UUtils](https://github.com/UPPAALModelChecker/UUtils).

This wrapper project is merely a simple experimental library with limited practical value. In the future, we will
consider supporting the wrapping of more Uppaal C++ libraries into Python versions for inclusion in this project.

## Installation

### From PyPI

```shell
pip install pyuutils
```

The following platforms are supported:

1. Most of the common linuxes and architectures
2. Windows AMD64 (win32/arm64 not ported)
3. MacOS x86_64/arm64 (python3.8 version of arm64 not supported)

### From Source Code

Install the system requirements

* On Ubuntu

```shell
apt-get install -y git ninja-build make gcc g++
```

* On Windows

```shell
choco install ninja make mingw
```

* On macOS

```shell
brew install git ninja make gcc
```

And then install the code

```shell
git clone https://github.com/HansBug/pyuutils.git
cd pyuutils
git submodule update --init  # check out the submodule
pip install -U -r requirements-build.txt
make bin  # build UUtils
pip install .
```

## How to Use

See [our documentation](https://hansbug.github.io/pyuutils/index.html).

Only approximately half of the features in UUtils have been ported here. We can port more if necessary.

