.. _usersguide-trajectory:

====================
Kinetic Trajectories
====================

Result data sets of kinetic simulations are referred to as "kinetic trajectory". The :py:class:`.Trajectory` class realizes such data sets which combine the calculated time series of chemical species concentrations and some data set / simulation attributes. Those attributes are typically simulation parameters like temperature or background pressures. 

Currently, the concentration time series have to be temporally aligned. There is only one vector of stored times and the the concentration time series for the individual species have to have a valid value for all stored simulation times.

There is currently no explicit formal notion of concentration units in kineticsPy. This means, that the concentration unit are not explicitly specified in the :py:class:`.Trajectory`, which means in turn that the user has to pay attention which units are used in a concrete :py:class:`.Trajectory` object. Only the name of the concentration unit is retained in the :py:class:`.Trajectory`, so that plotting methods can use it.  

However, the used time unit is implicitly specified as ``time_scaling_factor`` to `seconds`. For example, if this factor is ``1e-6``, the used time unit is microseconds. 

Accessing and indexing Trajectories
===================================

Trajectories combine the names / identifiers of chemical species, their concentration time series and simulation attributes. They provide a set of methods to retrieve and access the stored data. 

----------------------------------------------
Accessing / Indexing concentration time series
----------------------------------------------

The core of a kinetic trajectory are the stored concentration time series. They can be accessed and indexed by a high level method ``.loc``, which is loosely inspired by the ``loc`` method of Pandas DataFrames.  

High Level access with ``loc``
------------------------------

Given a trajectory `tra` containing data of species with the names ``A``, ``B`` and ``H2O``, the time series of `B` is retrieved by:

.. code-block:: python

    ts_B = tra.loc['B']

The returned time series is a `Pandas Series <https://pandas.pydata.org/pandas-docs/stable/reference/series.html>`_ object with the time vector of the Trajectory as index, so it can be further accessed by the usual access methods of Pandas: 

.. code-block:: python

    # access values by integer index: 
    vals = ts_B.iloc[2:5]

    # access specific simulation time: 
    vals = ts_B.loc[15.5]

Since the access of individual simulation times is common, the ``.loc`` function of Trajectories allow the indexing of time steps directly: 

.. code-block:: python 

    val = tra.loc['B', 2]
    vals = tra.loc['B', 2:5]

Multiple time series can be indexed by providing a list of species names to the ``loc`` function: 

.. code-block:: python 

    vals = tra.loc[ ['B', 'H2O'], 2:5]

When multiple species are selected, a `Pandas DataFrame <https://pandas.pydata.org/pandas-docs/stable/reference/frame.html>`_  is returned.


Low level indexing
------------------

Trajectories can be directly indexed and sliced with numerical indices. The trajectory behaves roughly similar to an NumPy Array. 

Accessing a single index, gives a time series for the i-th species. Given a trajectory `tra` containing data of species with the names ``A``, ``B`` and ``H2O``, the time series of `B`  has index 1 and is retrieved by: 
.. code-block:: python 

    vals = tra[1]

The second parameter to the indexing function selects time steps: 

.. code-block:: python 

    val = tra[1, 3]

gives the value of the species with index 1 for the time step with index 3. 

Slicing of species and time steps is possible: 

.. code-block:: python 

		vals1 = tra[1:4, 1:5] # selects a slice of species and time steps
		vals2 = tra[:, 0] # selects the values of all species for the first time step