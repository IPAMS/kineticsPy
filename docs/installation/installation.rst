.. _installation:

==============================
Prerequisites and Installation
==============================

Prerequisites
=============

IDSimPy is a Python 3 package. It requires a working and up to date Python 3 environment and an properly installed `Cantera <https://cantera.org/>`_ . IDSimPy was tested with Python 3.6. All other dependencies (Numpy, Matplotlib, Pandas) will be installed by the setup script. 

.. note:: 
    This guide assumes that the user has basic familiarity with a text base shell on the operating system where kineticsPy is intended to be used.

Installation
============

IDSimPy is currently not yet listed on `PyPi <https://pypi.org>`_.  Therefore, the `Git repository <https://team.ipams.uni-wuppertal.de/PTC/kineticsPy>`_ on the IPAMS git server has to be cloned and the package has to be installed from source. 

.. note::
    If you are using an anaconda / miniconda environment, be sure to use an anaconda shell or activate the right conda environment in the shell respectively, before installing kineticsPy. 

With git installed clone the repository to a local directory with your IPAMS git server credentials: 

.. code-block:: console

    git clone http://team.ipams.uni-wuppertal.de/PTC/kineticsPy.git

The kineticsPy package can conveniently be installed from the checked out local repository with `pip <http://https://pypi.org/project/pip/>`_. Move into the cloned directory and install with pip:

.. code-block:: console

    cd kineticsPy
    pip install .

Alternatively, the install script in the cloned directory can be invoked directly:

.. code-block:: console

    cd kineticsPy
    python setup.py install


.. note::
    With this installation method, changes in the cloned kineticsPy directory are *not* immediately visible in the package system of Python. You have to repeat the installation to update the Python package system. However, ``pip`` allows to install packages as "editable" package with the ``-e`` switch. If a package is installed as editable package, pip creates links from the Python package system to the cloned directory, so that every change in the cloned directory is immediately visible for Python. 

    To install kineticsPy in editable mode: 

    .. code-block:: console

        cd kineticsPy
        pip install -e .

        