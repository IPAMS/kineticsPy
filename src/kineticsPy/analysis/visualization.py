# -*- coding: utf-8 -*-

"""
Cantera simulation result plotting / visualization
"""

import matplotlib.pyplot as plt
from kineticsPy.base.trajectory import Trajectory

__all__ = ['plot']

def plot(trajectory: Trajectory, species_conf=None, time_steps=None,
         figsize=None, legend='best'):
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
	:param figsize: Size of the plot figure, a tuple with (wdith, height)
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
	else:
		raise ValueError('Illegal type for species_conf')


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

	fig, ax = plt.subplots(figsize=figsize)

	if style_conf_present:
		for sp in species_conf:
			ax.plot(
				times_s.iloc[time_steps_to_plot],
				trajectory.loc[sp[0], time_steps_to_plot],
				sp[1],
				color=sp[2],
				label=sp[0])
	else:
		for species in species_to_plot:
			ax.plot(
				times_s.iloc[time_steps_to_plot],
				trajectory.loc[species, time_steps_to_plot],
				label=species)

	if legend is not None and legend != 'off':
		ax.legend(loc=legend)

	ax.set_xlabel('time (s)')
	ax.set_ylabel('concentration (' + trajectory.concentration_unit + ')')

	return fig
