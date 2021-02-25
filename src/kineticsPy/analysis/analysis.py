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

	:param trajectory: The kinetic trajectory to analyze
	:type trajectory: kineticsPy.base.Trajectory
	:param time_steps: The number of final time steps at the end of the kinetic trajetory to be considered for the
		averaging
	:type time_steps: int
	:param reltol: A relative tolerance. If the relative fluctuation of a species in the analyzed time segment is
		larger than this tolerance, the trajectory is considered not to be converged and a ValueError is raised
	:type reltol: float
	:returns: A Pandas DataFrame with the equilibrium concentrations
	:rtype: Pandas.DataFrame
	"""

	if time_steps>=trajectory.number_of_timesteps:
		raise ValueError('Number of time steps to average ('+str(time_steps)+') is larger than number '
		                 'of time steps in trajectory '+str(trajectory.number_of_timesteps))

	dat_segment = trajectory[-time_steps:-1, :]

	averages = dat_segment.mean(axis=0)

	# calculate relative differences for estimating if the trajectory has converged:
	max = dat_segment.max(axis=0)
	min = dat_segment.min(axis=0)
	rel_diff = ((max-min) / averages).abs()
	for sp in trajectory.species_names:
		if rel_diff[sp] > reltol:
			raise ValueError('Maximum relative difference '+ str(rel_diff[sp]) + 'of species '+ sp+
		                     ' is larger than allowed tolerance '+ str(reltol))


	return averages