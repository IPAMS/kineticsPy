.. _usersguide-cantera-simulation:

===================
Cantera Simulations
===================

The kineticsPy package provides with the :py:mod:`kineticsPy.cantera.simulation` module an interface for simulations with `Cantera <https://www.cantera.org/>`_. Cantera is a versatile and highly capable simulation package. However, basic but common simulation tasks can be conveniently performed with the interface provided by kineticsPy. 

Cantera simulations (thermodynamic phases, chemical species and chemical reactions) are defined by configuration files (`.cti` files). The details of this, rather complex, file format are not discussed here. Refer to the Cantera documentation / tutorials for details. 

Adiabatic, isobar kinetics simulation
=====================================

A simulation of chemical kinetics in an ideally stirred, isobar and adiabatic reactor is performed by :py:func:`kineticsPy.cantera.simulation.simulate_isobar_adiabatic`. It takes a system configuration (thermodynamic phase, chemical species and chemical reactions of the species), an inital state of the system and simulates the temporal development of the chemical system. The result is returned as kinetic trajectory (:py:class:`kineticsPy.base.trajectory.Trajectory`).

------------------
Parameter overview
------------------

The simulation function has the following parameters can be called with two different signatures. It can be called either with a number of time steps to simulate ``n_steps`` and a time step length ``dt``

.. code-block:: python

		simulate_isobar_adiabatic(input_file, initial_mole_fractions, n_steps, dt, pressure, record_period=1, rtol=None)

or with a custom array of time steps to simulate ``custom_steps``:

.. code-block:: python

		simulate_isobar_adiabatic(input_file, initial_mole_fractions, custom_steps, pressure, record_period=1, rtol=None)


The arguments to the function mean in detail: 

  + The name of an Cantera configuration (``cti``) file, defining a thermodynamic phase in which the reactions takes place, the chemical species and the chemical reactions of the chemical species (``input_file``)
  + the initial mole fractions of the individual chemical species (``inital_mole_fractions``)
  + the background pressure in the reaction vessel in Pascals (``pressure``)

The time steps to simulate are controlled either by 

  + the number of time steps to calculate (``n_steps``)
  + the time step length (``dt``) 

or 

  + an array of custom times to simulate (``custom_steps``) 

.. note::
    The simulation starts always at time = 0.0, even if ``custom_steps`` defines a list of times not beginning with 0.0. In this case, the initial state is not written to the resulting kinetic trajectory.

.. note::
    The units for ``dt`` and ``pressure`` are the units specified by the Cantera input file. Usually the time unit is seconds and the pressure unit is Pascal. 

.. note::
    Currently, the temperature in the reaction vessel is defined by the Cantera input file, while the pressure specified in the Cantera input file is overwritten by the value passed as ``pressure``. 


The two optional / named parameters mean

  + ``record_period`` is the period in terms of simulated time steps which is used to write data to the resulting kinetic trajectory. For example: If this parameter is 10, only every 10th time step is written to the kinetic trajectory. This parameter is intended to control the size of kinetic trajectories with simulations which require very fine grained time steps. 
  + ``rtol`` tolerance parameter which is passed to the Cantera solver

----------------------
Initial mole fractions
----------------------

The initial concentrations of the chemical species are defined as mole fractions. The given mole fractions are taken as relative values and are normalized by Cantera. The absolute concentrations are calculated from the thermodynamic state (temperature, pressure etc.) and the thermodynamic model of the phase in the reactor. Typically an ideal gas is specified by the input file. The ``initial_mole_fractions`` parameter is a string in the format expected by Cantera as mole fraction initialization. The format is a comma (``,``) separated list of substance identifiers with mole fraction values separated by a colon (``:``). 

For example, if a simulation defines a simulation with water ``H2O``, nitrogen ``N2`` and protnated water ions ``H3O+``, a valid concentration initialization string would be:

.. code-block::

    'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10'

.. note::
    Species can be omitted in the initialization. Omitted species are initialized with no concentration.

-----------------
Simulation result
-----------------

The simulation result is a kinetic trajectory (see :ref:`usersguide-trajectory`). It contains the absolute concentration of the individual species in :math:`\text{molecules} \: \text{cm}^{-3}`. 


------------------
Example simulation
------------------

Equidistant, linear time steps
------------------------------

Example simulation with an input file ``WaterCluster_RoomTemp.cti``, the initial mole fraction mentioned above, 10000 equidistant time steps with 2e-9 seconds length and a pressure of 1e5 Pascal: 

.. code-block:: python 

    import kineticsPy as kpy

    input_file = 'WaterCluster_RoomTemp.cti'

    simulation_result = kpy.cantera.simulate_isobar_adiabatic(
            input_file,
            'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10',
            10000, 2e-9, 1e5)


Custom logarithmic time steps
------------------------------

Example simulation with an input file ``WaterCluster_RoomTemp.cti``, the initial mole fraction mentioned above, and 10000 logarithmically distributed time steps between :math:`10^{-7}` and :math:`10^{-1}` seconds defined by the ``logspace`` function of numpy and a pressure of 1e5 Pascal: 

.. code-block:: python 

    import kineticsPy as kpy
    import numpy as np

    input_file = 'WaterCluster_RoomTemp.cti'
    custom_time_steps = np.logspace(-7, -1, 10000)

    simulation_result = kpy.cantera.simulate_isobar_adiabatic(
            input_file,
            'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10',
            custom_time_steps, 1e5)

