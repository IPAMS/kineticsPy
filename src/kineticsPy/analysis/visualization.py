# -*- coding: utf-8 -*-

"""
Kinetic simulation result plotting / visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from kineticsPy.base.trajectory import Trajectory
from . import analysis

__all__ = ['plot', 'plot_average_concentrations', 'plot_equilibrium_state']

plt.style.use('ggplot')


def plot(trajectory: Trajectory, species_conf=None, time_steps=None,
         normalized=False, log='none', figsize=None, legend='best'):
	"""
	Generates a concentration / time profile plot for a trajectory.

	**Chemical species selection**

	Passing a single chemical species identifier or a list of chemical identifiers to ``species_conf`` selects
	chemical species to plot:

	.. code-block:: python

		plot(trajectory, 'H2O')  # will plot Water (H2O)
		plot(trajectory, ['H2O', 'N2'])  # will plot Water (H2O) and Nitrogen (N2)

	**Custom line styles**

	Passing a list of line chemical species with plot / line style configurations to ``species_conf`` allows to use
	custom line styles for the plot.

	The line style entries are a species name, a matplotlib format string and a color accepted by matplotlib:

	.. code-block:: python

		species_conf = [
			('H2O', '.-', 'red'),
			('N2', ':-', '#AABB22')
		]

		plot(trajectory, species_conf)


	**Time range selection**

	``time_steps`` allows to specify the plotted time steps.

	* A single integer defines the last time step to be plotted. The trajectory will be plotted from the beginning
	  to the specified upper time step.
	* A tuple of two time step indices ``(lower, upper)`` defines a lower and an upper boundary of the time step
	  range to be plotted.

	.. code-block:: python

		plot(trajectory, time_steps=150)  # will plot time steps up to 150
		plot(trajectory, time_steps=(100, 200) )  # will plot time steps between 100 and 200


	:param trajectory: The kinetic trajectory to plot
	:param species_conf: Selection of chemical species with optional line style configuration (see above for details)
	:type species_conf: list of str or list of species / line style definitions
	:param time_steps: Time step range selection (see above for details)
	:type time_steps: int or tuple of two int
	:param normalized: If true concentrations are normalized to [0, 1] for plotting
	:type normalized: bool
	:param log: Logarithmic plot mode.
		If "none" both axes are linear, if "concentration" the concentration axis is log plotted,
		if "time" the time axis is log plotted, if "both" both axes are log plotted
	:type log: str
	:param figsize: Size of the plot figure, a tuple with (width, height)
	:type figsize: tuple of two floats
	:param legend: Legend configuration / location. 'off' deactivates the legend. Matplotlib legend location string
		fixes the legend on the specfied location (see matplotlb documentation for details)
	:type legend: str
	:returns: A matplotlib figure with the plot
	"""
	species_names = trajectory.species_names
	times_s = trajectory.times * trajectory.time_scaling_factor

	style_conf_present = False  # flag if a complex species / line style configuration is present
	if isinstance(species_conf, str):  # single string means: single species name
		species_conf = [species_conf]

	if species_conf is None:
		species_to_plot = species_names
	elif isinstance(species_conf, (list, tuple)):
		#  check which types are in the elements of the given list or tuple:
		#  if all elements are string: We have a pure species identifier list
		#  if all elements are themselves lists or tuples: we have comples species / linestyle configuration

		only_strings = True
		only_lists = True
		for sp in species_conf:
			if not isinstance(sp, str):
				only_strings = False
			if not isinstance(sp, (list, tuple)):
				only_lists = False

		if only_strings:  # we have a pure species id list
			species_to_plot = species_conf
		elif only_lists:  # we have a species / line style configuration
			if not all(len(sp) == 3 for sp in species_conf):
				raise ValueError('Species / line style configurations have to have three elements '
				                 '(Species, line style, color)')

			style_conf_present = True
			species_to_plot = [sp[0] for sp in species_conf]
	else:
		raise ValueError('Illegal type for species_conf')

	time_steps_to_plot = _time_steps_to_plot(time_steps, trajectory)

	if normalized:
		max_vals = [np.max(trajectory.loc[species, time_steps_to_plot]) for species in species_to_plot]
		norm_factor = 1.0/np.max(max_vals)
	else:
		norm_factor = 1.0

	if log not in ('none', 'concentration', 'time', 'both'):
		raise ValueError('Illegal option passed for log')

	fig, ax = plt.subplots(figsize=figsize)

	if log == 'none':
		plot_fct = ax.plot
	elif log == 'concentration':
		plot_fct = ax.semilogy
	elif log == 'time':
		plot_fct = ax.semilogx
	elif log == 'both':
		plot_fct = ax.loglog


	if style_conf_present:
		for sp in species_conf:
			plot_fct(
				times_s.iloc[time_steps_to_plot],
				trajectory.loc[sp[0], time_steps_to_plot] * norm_factor,
				sp[1],
				color=sp[2],
				label=sp[0])
	else:
		for species in species_to_plot:
			plot_fct(
				times_s.iloc[time_steps_to_plot],
				trajectory.loc[species, time_steps_to_plot] * norm_factor,
				label=species)

	if legend is not None and legend != 'off':
		ax.legend(loc=legend)

	ax.set_xlabel('time (s)')
	if normalized:
		ax.set_ylabel('normalized concentration')
	else:
		ax.set_ylabel('concentration (' + trajectory.concentration_unit + ')')

	return fig


def plot_average_concentrations(trajectory: Trajectory,
                                time_steps=None,
                                species=None,
                                figsize=None,
                                legend='best',
                                log=False):
	"""
	Creates a box plot of the averaged concentrations of specified time steps.

	**Chemical species selection**

	Passing a single chemical species identifier or a list of chemical identifiers to ``species_conf`` selects
	chemical species to plot:

	.. code-block:: python

		plot_average_concentrations(trajectory, species='H2O')  # will plot Water (H2O)
		plot_average_concentrations(trajectory, species=['H2O', 'N2'])  # will plot Water (H2O) and Nitrogen (N2)

	**Time range selection**

	``time_steps`` allows to specify the plotted time steps.

	* A single integer defines selects a single time step to plot.
	* A tuple of two time step indices ``(lower, upper)`` defines a lower and an upper boundary of the time step
	  range to be plotted.

	.. code-block:: python

		plot_average_concentrations(trajectory, time_steps=150)  # will plot time step 150
		plot_average_concentrations(trajectory, time_steps=(100, 200) )  # will average time steps between 100 and 200

	:param trajectory: The kinetic trajectory to analyze and plot
	:type trajectory: kineticsPy.base.Trajectory
	:param time_steps: Time step range selection (see above for details)
	:type time_steps: int or tuple of two int
	:param figsize: Size of the plot figure, a tuple with (width, height)
	:type figsize: tuple of two floats
	:param legend: Legend configuration / location. 'off' deactivates the legend. Matplotlib legend location string
		fixes the legend on the specfied location (see matplotlb documentation for details)
	:type legend: str
	:param log: If true, the concentrations are plottet on a logarithmic scale
	:returns: A matplotlib figure with the plot
	"""

	if species is None:
		species_to_plot = list(trajectory.species_names)
	else:
		species_to_plot = list(species)


	if isinstance(time_steps, int): # we need slightly different behavior for time step selection
		average_data = trajectory.loc[species_to_plot, time_steps]
	else:
		time_steps_to_plot = _time_steps_to_plot(time_steps, trajectory)
		average_data = trajectory.loc[species_to_plot, time_steps_to_plot].mean(axis=0)

	return _concentration_box_plot(average_data, species_to_plot, figsize, legend, log, trajectory.concentration_unit)


def plot_equilibrium_state(trajectory: Trajectory,
                           time_steps=100,
                           reltol=0.01,
                           figsize=None,
                           legend='best',
                           log=False):
	"""
	Plots the concentration in the final equilibrium state of a trajectory. The equilibrium concentrations are
	assumed as the average concentations of the chemical species in the trajectory in the final time steps

	:param trajectory: The kinetic trajectory to analyze and plot
	:type trajectory: kineticsPy.base.Trajectory
	:param time_steps: The number of time steps at the end of the trajectory to consider
	:type time_steps: int
	:param reltol: The relative tolerance of the individual species. If the relative difference of a species in
		the trajectory is larger than this tolerance, the trajectory is considered as not converged / not in
		equilibrium
	:type reltol: float
	:param figsize: Size of the plot figure, a tuple with (width, height)
	:type figsize: tuple of two floats
	:param legend: Legend configuration / location. 'off' deactivates the legend. Matplotlib legend location string
		fixes the legend on the specfied location (see matplotlb documentation for details)
	:type legend: str
	:param log: If true, the equilibrium concentrations are plottet on a logarithmic scale
	:returns: A matplotlib figure with the plot
	"""

	species = trajectory.species_names
	equilibrium_data = analysis.equilibrium_state(trajectory, time_steps=time_steps, reltol=reltol)

	return _concentration_box_plot(equilibrium_data, species, figsize, legend, log, trajectory.concentration_unit)


def _time_steps_to_plot(time_steps, trajectory):
	"""
	Defines which time steps should be plotted from a user provided time_steps parameter and a trajectory
	"""
	if time_steps is None:
		time_steps_to_plot = slice(0, trajectory.number_of_timesteps)
	if isinstance(time_steps, int):
		# single int: plot all time steps until the end time step specified by the single int
		time_steps_to_plot = slice(0, time_steps)
	elif isinstance(time_steps, tuple):
		# if a tuple with two values is given: Create time step range from it

		if len(time_steps) != 2:
			raise ValueError('Time step range has to be a tuple with two elements.')
		if time_steps[1] <= time_steps[0]:
			raise ValueError('Illegal time step range definition: '
			                 'Second element of time step range tuple has to be larger than first element')
		if time_steps[0] < 0:
			raise ValueError('Lower bound of time step range has to be positive')
		if time_steps[1] >= trajectory.number_of_timesteps:
			raise ValueError('Upper bound of time step range has to be '
			                 'below number of time steps in plotted trajectory')

		time_steps_to_plot = slice(time_steps[0], time_steps[1])

	return time_steps_to_plot


def _concentration_box_plot(concs, labels, figsize, legend, log, concentration_unit):

	fig, ax = plt.subplots(figsize=figsize)

	x = np.arange(len(labels))

	for i in range(len(labels)):
		ax.bar(x[i], concs[labels[i]], label=labels[i])

	if log:
		ax.set_yscale('log')

	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.tick_params(axis="x", rotation=90)
	ax.set_ylabel('concentration (' + concentration_unit + ')')
	if legend is not None and legend is not 'off':
		ax.legend(loc=legend)

	fig.tight_layout()

	return fig