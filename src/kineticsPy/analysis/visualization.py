# -*- coding: utf-8 -*-

"""
Cantera simulation result plotting / visualization
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from kineticsPy.base.trajectory import Trajectory

def plot(trajectory: Trajectory,
         species_conf= None,
         figsize=None):
	"""
	Generates a concentration / time profile plot for a trajectory

	@param trajectory The kinetic trajectory to plot
	"""
	species_names = trajectory.species_names
	times_s = trajectory.times * trajectory.time_scaling_factor

	if isinstance(species_conf, str): #  single string means: single species name
		species_conf = [species_conf]

	if isinstance(species_conf, (list, tuple)):
		for sp in species_conf:
			if sp not in species_names:
				raise ValueError('Species '+sp+' is not found in trajectory')
		species_to_plot = species_conf
	else:
		species_to_plot = species_names


	fig, ax = plt.subplots(figsize=figsize)
	for species in species_to_plot:
		ax.plot(times_s, trajectory.loc[species], label=species)

	ax.legend()
	ax.set_xlabel('time (s)')
	ax.set_ylabel('concentration ('+trajectory.concentration_unit+')')

	return fig



