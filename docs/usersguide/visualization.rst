.. _usersguide-visualization:

==========================
Visualization and Plotting
==========================

The :py:mod:`kineticsPy.analysis.visualization` module contains visualization and plotting methods for kinetic simulation results. Currently, plotting of simulated concentration-time profiles is the primary method provided by the module. 


Concentration-Time Profile Plotting
=====================================

Concentration-time profiles can be plotted as line plots with :py:func:`kineticsPy.analysis.visualization.plot`. This plot function provides a convenient interface for most common plotting requirements. 

.. note::
    The following guide assumes that :py:func:`kineticsPy.analysis.visualization.plot` is used in a `jupyter <https://jupyter.org/>`_ notebook / lab environment. In other environments the plots will not be necessarily shown automatically. The plot function generates and returns `matplotlib <https://matplotlib.org/>`_ figures, which usually can be shown with their ``.show()`` method. See the matplotlib documentation and the documentation of your environment the code is run in (iPython, PyCharm, Spyder etc.). 


Simple full plot of a trajectory 
--------------------------------


Most simply, it takes a kinetic trajectory and returns a matplotlib plot of the trajectory:

.. code-block:: python

    import kineticsPy as kpy  # plot function is exported by kineticsPy directly

    # plot full trajectory (sim_result is a Trajectory containing a simulation result)
    kpy.plot(sim_result);

yields for example

.. image:: images/concentration_plot_base_01.svg
    :alt: Simple line plot of an example trajectory

