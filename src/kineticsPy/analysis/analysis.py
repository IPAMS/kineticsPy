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

def get_config_concentrations(trajectory,time_steps,rel_tol=0.01):
    	"""
	Generates a string for an concentrations input of a kinetic trajectory for another cantera simulation. It uses the above defined equilibrium_state function to get the result concentrations of an initial cantera simulation. After splitting and inserting certain characters, a string with the result concentrations is generated, which can be used for another cantera simulation.

	:param trajectory: The kinetic trajectory to analyze
	:type trajectory: kineticsPy.base.Trajectory
	:param time_steps: The number of final time steps at the end of the kinetic trajetory to be considered for the
		averaging
	:type time_steps: int
	:param reltol: A relative tolerance (see equilibrium_state function). If the relative fluctuation of a species in the analyzed time segment is larger than this tolerance, the trajectory is considered not to be converged and a ValueError is raised
	:type reltol: float
	:returns: A string with result concentrations
	:rtype: string
	"""
    eq_conc = kpy.analysis.equilibrium_state(trajectory, time_steps=time_steps, reltol=rel_tol)
    string_eq = eq_conc.to_string() # convert dataframe to string
    split_eq = string_eq.split() # split the string (gets also rid of the blank spaces)
    # insert ":" after each chemical species key (":" is requiered for cantera)
    for i in range(len(split_eq),0,-1):
        if i%2 != 0:
            split_eq.insert(i,':')
    # also insert "," after each number concentration to separate the chemical species concentrations
    for j in range(len(split_eq)-1,1,-1):
        if j%3 == 0:
            split_eq.insert(j,',')
    # merge everything to one string
    final_conc_str = ''.join(split_eq)
    return final_conc_str