Installation
===================

pyuutils is currently hosted on PyPI. It required python >= 3.8.

You can simply install pyuutils from PyPI with the following command:

.. code:: shell

    pip install pyuutils

You can also install with the newest version through GitHub:

* On Ubuntu

.. code:: shell

    apt-get install -y git ninja-build make gcc g++

* On Windows

.. code:: shell

    choco install ninja make mingw


* On macOS

.. code:: shell

    brew install git ninja make gcc


And then install the code

.. code:: shell

    git clone https://github.com/HansBug/pyuutils.git
    cd pyuutils
    git submodule update --init  # check out the submodule
    pip install -U -r requirements-build.txt
    make bin  # build UUtils
    pip install .

You can check your installation by the following python \
script:

.. literalinclude:: install_check.demo.py
    :language: python
    :linenos:

The output should be like below, which means your installation \
is successful.

.. literalinclude:: install_check.demo.py.txt
    :language: text
    :linenos:

pyuutils is still under development, you can also check out the \
documents in stable version through `https://hansbug.github.io/pyuutils/main/index.html <https://hansbug.github.io/pyuutils/main/index.html>`_.
