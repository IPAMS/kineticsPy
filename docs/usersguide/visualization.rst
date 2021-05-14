.. _usersguide-visualization:

==========================
Visualization and Plotting
==========================

The :py:mod:`kineticsPy.analysis.visualization` module contains visualization and plotting methods for kinetic simulation results. Currently, plotting of simulated concentration-time profiles is the primary method provided by the module. 


Concentration-Time Profile Plotting
===================================

Concentration-time profiles can be plotted as line plots with :py:func:`kineticsPy.analysis.visualization.plot`. This plot function provides a convenient interface for most common plotting requirements. 

.. note::
    The following guide assumes that :py:func:`kineticsPy.analysis.visualization.plot` is used in a `jupyter <https://jupyter.org/>`_ notebook / lab environment. In other environments the plots will not be necessarily shown automatically. The plot function generates and returns `matplotlib <https://matplotlib.org/>`_ figures, which usually can be shown with their ``.show()`` method. See the matplotlib documentation and the documentation of your environment the code is run in (iPython, PyCharm, Spyder etc.). 

--------------------------------
Simple full plot of a trajectory 
--------------------------------

The plot function becomes available by importing ``kineticsPy``. Most simply, it takes a kinetic trajectory and returns a matplotlib plot of the trajectory:

.. code-block:: python

    import kineticsPy as kpy  # plot function is exported by kineticsPy directly

    # plot full trajectory (sim_result is a Trajectory containing a simulation result)
    kpy.plot(sim_result);

yields for example

.. image:: images/concentration_plot_base_01.svg
    :alt: Simple line plot of an example trajectory

-----------------------------
Selection of chemical species
-----------------------------

Chemical species can be selected by passing a list of identifier strings to the plot function as second parameter. For example, the selection of two species (``Cl2`` and ``H2O``): 

.. code-block:: python

    kpy.plot(sim_result, ['Cl2', 'H2O']);


produces a plot with only two concentration profiles: 

.. image:: images/concentration_plot_species_selection_01.svg
    :alt: Simple line plot of an example trajectory with two species selected


a tuple instead of a list is also valid:

.. code-block:: python

    kpy.plot(sim_result, ('Cl2', 'H2O'));


It is also possible to use a single identifier instead of a list:

.. code-block:: python

    kpy.plot(sim_result, 'Cl2');

.. image:: images/concentration_plot_species_selection_02.svg
    :alt: Simple line plot of an example trajectory with only one species selected


----------------------------
Selection of time step range
----------------------------

The time segment which is plotted can be selected with the ``time_steps`` parameter of the plot function, which is also the 3rd unnamed parameter of the function. The time range is specified in terms of time step numbers / time step indices. 

Without specfication of a time range, the whole trajectory is plotted: 

.. code-block:: python 

    # (cl_sim_result is an example simulation result of a water cluster equilibrium simulation)
    kpy.plot(cl_sim_result)

.. image:: images/concentration_plot_time_selection_01.svg
    :alt: Full water cluster trajectory


Plotting up to a time step
--------------------------

If a single time step index is passed, all time steps *up to* the specified time step are plotted: 

.. code-block:: python 

    kpy.plot(cl_sim_result, time_steps=100)

.. image:: images/concentration_plot_time_selection_02.svg
    :alt: Water cluster trajectory with final time step selected 

since the ``time_step`` parameter can also be used as third unnamed parameter, a species and time range selection can be combined conveniently: 

.. code-block:: python 

    kpy.plot(cl_sim_result, ['H3O+', 'H3O+(H2O)','H3O+(H2O)2'], 100)

.. image:: images/concentration_plot_time_selection_03.svg
    :alt: Water cluster trajectory with final time step and chemical species selected 


Time step range with lower and upper bound
------------------------------------------

A lower and an upper bound of the the plotted time range is selected by passing a ``tuple`` with two elements to ``time_steps``

.. code-block:: python 

    kpy.plot(cl_sim_result, time_steps=(40, 200))

.. image:: images/concentration_plot_time_selection_04.svg
    :alt: Water cluster trajectory with lower and upper bound selected


-------------------------------------------
Custom plot line / symbol styles and colors
-------------------------------------------

The drawing style and the color of the individual plot lines can be customized by passing a list of species names and their plot style configuration as second parameter to the plot function. This configuration list has one entry per line to draw. Each entry consists of a chemical species name, a matplotlib format string for the chemical species (see `matplotlib documentation <https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html#matplotlib.pyplot.plot>`_ for details), and a color (also as defined by matplotlib).

.. code-block:: python 

    plot_conf = [
        ('H3O+', '.--', 'darkblue'),    # color names are allowed
        ('H3O+(H2O)', 'o-', '#DDCC00'), # color hex codes are also allowed
        ('H3O+(H2O)2', '-', '#BB1144')
    ]

    kpy.plot(cl_sim_result, plot_conf)

.. image:: images/concentration_plot_line_styles_01.svg
    :alt: Water cluster trajectory with custom line / symbol styles


------
Legend
------

By default a legend of the species names and their line styles is presented in the plot. The rendering of the legend can be controlled with the ``legend`` named parameter of the plot function. 

The legend can be switched off by passing ``off``  as legend parameter:


.. code-block:: python 

    kpy.plot(cl_sim_result, legend='off')

.. image:: images/concentration_plot_additional_parameters_01.svg
    :alt: Water cluster trajectory without legend


By default, the legend location is optimized not to intersect with plot lines (``best`` legend location as defined by matplotlib). The legend location can be controlled by passing a legend position identifier, as defined by matplotlib (see `matplotlib legend documentation <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html#matplotlib.axes.Axes.legend>`_ for details) as legend parameter:

.. code-block:: python 

    kpy.plot(cl_sim_result, legend='upper left')

.. image:: images/concentration_plot_additional_parameters_02.svg
    :alt: Water cluster trajectory with custom legend location


---------
Plot size
---------

The size of the plot figure is set with the ``figsize`` named parameter, which takes a list or tuple of a width and a height: 

.. code-block:: python 

    kpy.plot(cl_sim_result, figsize=(10,4))

.. image:: images/concentration_plot_additional_parameters_03.svg
    :alt: Water cluster trajectory with custom width and height

----------------
Normalized Plots
----------------

Plots can be normalized on the concentration axis:

.. code-block:: python 

    kpy.plot(cl_sim_result, normalized=True)

.. image:: images/concentration_plot_additional_parameters_04.svg
    :alt: Water cluster trajectory normalized concentrations


-----------------
logarithmic Plots
-----------------

The time and concentration axis can be plotted logarithmically by setting the `log` parameter. 

The default `log='none'` plots both axes linearly: 

.. code-block:: python 

    kpy.plot(cl_sim_result, log='none')

.. image:: images/concentration_plot_additional_parameters_05.svg
    :alt: Water cluster trajectory with both axes linearly plotted


The concentration axis can be plotted logarithmically by setting `log='concentration'`: 

.. code-block:: python 

    kpy.plot(cl_sim_result, log='concentration')

.. image:: images/concentration_plot_additional_parameters_06.svg
    :alt: Water cluster trajectory with concentration axis plotted logarithmically

Similarly, by setting `log='time'` the time axis can be plotted logarithmically: 

.. code-block:: python 

    kpy.plot(cl_sim_result, log='time')

.. image:: images/concentration_plot_additional_parameters_07.svg
    :alt: Water cluster trajectory with time axis plotted logarithmically

Both axis can be plotted logarithmically in a log-log plot by specifying `log='both'`: 

.. code-block:: python 

    kpy.plot(cl_sim_result, log='both')

.. image:: images/concentration_plot_additional_parameters_08.svg
    :alt: Water cluster trajectory with both axes plotted logarithmically

Box plots of concentrations and averaged concentrations
=======================================================

The concentrations in a simulation time step or the averaged concentrations in a time step range can be plotted with :py:func:`kineticsPy.analysis.visualization.plot_average_concentrations`. This function takes a kinetic trajectory and creates a box plot of the concentrations of a time step or the averaged concentations in a time step range. 

For exammple, the plot of time step with index 10 on a logarithmic axis with 

.. code-block:: python 

    kpy.plot_average_concentrations(cl_sim_result, 10, log=True)

gives 

.. image:: images/average_concentration_box_plot_01.svg
    :alt: Simple concentration box plot

Similarly to :py:func:`kineticsPy.analysis.visualization.plot`, the species which are plotted can be specified with their identifiers. For example 

.. code-block:: python 

    selection = ['H3O+', 'H3O+(H2O)','H3O+(H2O)2','H3O+(H2O)3','H3O+(H2O)4']
    kpy.plot_average_concentrations(cl_sim_result, (40, 50), selection)

gives the average concentrations of the species selection in the specified time step range of the time steps between 40 and 50

.. image:: images/average_concentration_box_plot_02.svg
    :alt: Simple concentration box plot of a time step and species selection



Equilibrium concentration plots
===============================

Simple plots of an equilibrium state of a trajectory can be created with :py:func:`kineticsPy.analysis.visualization.plot_equilibrium_state`. This function takes a kinetic trajectory and creates a simple bar plot of the equilibrium concentrations, by averaging the concentrations in the last time steps of a kinetic trajectory:

.. code-block:: python 

    kpy.plot_equilibrium_state(cl_sim_result, log=True)

.. image:: images/equilibrium_state_plot_01.svg
    :alt: Equilibrium state concentration plot

The ``log`` option switches to logarithmic scaling of the concentration axis. The ``time_steps`` sets how many time steps at the end of the trajectory are considered for the averaging. If the relative fluctuation of a chemical species in the considered time segment is larger than ``reltol``, the trajectory is considered not to be converged and an exception will be risen: 

.. code-block:: python 

    kpy.plot_equilibrium_state(cl_sim_result, time_steps=200, reltol=0.005)
