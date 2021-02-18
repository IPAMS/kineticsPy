# -*- coding: utf-8 -*-

"""
Interface to run kinetic simulations with cantera_simulation
"""
import os
import numpy as np
import cantera as ct
import kineticsPy.base.trajectory as tra

def simulate_isobar_adiabatic(inputFile, initConfiguration, steps, dt, pressure):
	"""
	Constant-pressure, adiabatic kinetics simulation with Cantera: 
	Simulates chemical kinetics in an ideally stirred, isobar and adiabatic reactor. 
	
	:param inputFile: 
	:param initConfiguration: 
	:param steps: 
	:param dt: 
	:param pressure: 
	:return: 
	"""

	# check if input file exists:
	if not os.path.isfile(inputFile):
		return "NO FILE"

	sol = ct.Solution(inputFile)
	air = ct.Solution('air.xml')

	sol.TPX = sol.T, pressure, initConfiguration

	species_names = sol.species_names
	n_species = len(species_names)
	reac = ct.IdealGasReactor(sol)
	env = ct.Reservoir(air)

	# Define a wall between the reactor and the environment, and
	# make it flexible, so that the pressure in the reactor is held
	# at the environment pressure.
	wall = ct.Wall(reac, env)
	wall.expansion_rate_coeff = 1.0e0  # set expansion parameter. dV/dt = KA(P_1 - P_2)
	wall.area = 0.0

	# Initialize simulation.
	sim = ct.ReactorNet([reac])
	time = 0.0
	times = np.zeros([steps, 1])
	data = np.zeros((steps, n_species))

	for n in range(steps):
		time += dt
		sim.advance(time)
		times[n] = time  # time in s
		data[n, :] = reac.thermo[species_names].concentrations * 6.022E20
		if n % 30000 == 0:
			print('%5d %10.3e %10.3f %10.3f %14.6e' % (n, sim.time, reac.T, reac.thermo.P, reac.thermo.u))
		#print(data[n,:])

	return {'data': data, 'time': times}
