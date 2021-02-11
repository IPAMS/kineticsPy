.. _installation:

==============================
Prerequisites and Installation
==============================

Prerequisites
=============

IDSimPy is a Python 3 package. It requires a working and up to date Python 3 environment and an properly installed `Cantera <https://cantera.org/>`_ . IDSimPy was tested with Python 3.6. All other dependencies (Numpy, Matplotlib, Pandas) will be installed by the setup script. 

Installation
============

IDSimPy is currently not yet listed on `PyPi <https://pypi.org>`_.  Therefore, the `Git repository <https://team.ipams.uni-wuppertal.de/PTC/kineticsPy>`_ on the IPAMS git server has to be cloned and the package has to be installed from source. 

.. note::
    If you are using an anaconda / miniconda environment, be sure to use an anaconda shell or activate the right conda environment in the shell respectively, before installing kineticsPy. 

With git installed clone the repository to a local directory with your IPAMS git server credentials: 

.. code-block:: console

    git clone http://team.ipams.uni-wuppertal.de/PTC/kineticsPy.git

Then move into the cloned directory and install IDSimPy from source by invoking the setup script:

.. code-block:: console

    cd kineticsPy
    python setup.py install