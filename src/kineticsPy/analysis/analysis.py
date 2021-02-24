# -*- coding: utf-8 -*-

"""
Simulation result analysis
"""

def equilibrium_state(trajectory, time_steps=100, reltol=0.01):
	"""
	Calculates the final equilibrium state of a kinetic trajectory. The final equilibrium state is determined
	by calculating the average concentrations of the individual chemical species in the final time steps
	of the trajectory. If the relative fluctuation in the considered time range is larger than
	``reltol``, the trajectory is considered as not to be converged.

	:param trajectory:
	:param time_steps:
	:param reltol:
	"""

	dat_segment = trajectory[-time_steps:-1, :]
	averages = dat_segment.mean(axis=0)
	return averages