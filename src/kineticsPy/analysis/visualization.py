# -*- coding: utf-8 -*-

"""
Cantera simulation result plotting / visualization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from kineticsPy.base.trajectory import Trajectory


def plot(trajectory: Trajectory,
         species_conf=None,
         time_steps=None,
         figsize=None):
	"""
	Generates a concentration / time profile plot for a trajectory

	@param trajectory The kinetic trajectory to plot
	"""
	species_names = trajectory.species_names
	times_s = trajectory.times * trajectory.time_scaling_factor

	if isinstance(species_conf, str):  # single string means: single species name
		species_conf = [species_conf]

	if isinstance(species_conf, (list, tuple)):
		for sp in species_conf:
			if sp not in species_names:
				raise ValueError('Species ' + sp + ' is not found in trajectory.')
		species_to_plot = species_conf
	else:
		species_to_plot = species_names

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
	for species in species_to_plot:
		ax.plot(
			times_s.iloc[time_steps_to_plot],
			trajectory.loc[species, time_steps_to_plot],
			label=species)

	ax.legend()
	ax.set_xlabel('time (s)')
	ax.set_ylabel('concentration (' + trajectory.concentration_unit + ')')

	return fig
