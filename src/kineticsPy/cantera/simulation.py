# -*- coding: utf-8 -*-

"""
Interface to run kinetic simulations with cantera_simulation
"""
import os
import numpy as np
import cantera as ct
from kineticsPy.base.trajectory import Trajectory

__all__ = ["simulate_isobar_adiabatic"]

def simulate_isobar_adiabatic(input_file, initial_mole_fractions, steps, dt, pressure):
	"""
	Constant-pressure, adiabatic kinetics simulation with Cantera: 
	Simulation of chemical kinetics in an ideally stirred, isobar and adiabatic reactor.
	It takes an Cantera input file which defines a phase, chemical species and chemical reactions and runs an isobar
	and adiabatic time dependent kinetics simulation with the defined reaction system.

	The initial concentrations of the chemical species are defined as mole fractions. The given mole fractions
	are taken as relative values and are normalized by Cantera. The absolute concentrations are calculated from
	the thermodynamic state (temperature, pressure etc.) and the thermodynamic model of the phase in the reactor. Typically an ideal gas
	is specified by the input file.
	The initial mole fractions are set by ``initial_mole_fractions`` which is a string
	in the format expected by Cantera as mole fraction initialization. The format is a comma (``,``) separated list
	of substance identifiers with mole fraction values separated by a colon (``:``).

	For example, if a simulation defines a simulation with water ``H2O``, nitrogen ``N2`` and protnated water ions
	``H3O+``, a valid concentration initalization string would be:

	.. code-block:: shell

		'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10'

	.. note::
		Species can be omitted in the initialization. Omitted species are initalized with no concentration.

	:param input_file: Path to a configuration (.cti) file
	:type input_file: path
	:param initial_mole_fractions: Inital mole fraction configuration
	:type initial_mole_fractions: str
	:param steps: Number of time steps to simulate
	:type steps: int
	:param dt: Length of a time step
	:type dt: float
	:param pressure: Background pressure in the reaction vessel
	:type pressure: float
	:return: :class:`kineticsPy.base.trajectory.Trajectory` (a kinetic trajectory object)
	"""

	# check if input file exists:
	if not os.path.isfile(input_file):
		return "NO FILE"

	sol = ct.Solution(input_file)
	air = ct.Solution('air.xml')

	sol.TPX = sol.T, pressure, initial_mole_fractions

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
	times = np.zeros(steps)
	data = np.zeros((steps, n_species))

	for n in range(steps):
		sim.advance(time)
		times[n] = time  # time in s
		# .concentrations of a ThermoPhase returns concentrations in [kmol/m^3],
		# we want to use molecules / cm^3 and have to convert:
		data[n, :] = reac.thermo[species_names].concentrations * 6.022E20
		if n % 30000 == 0:
			print('%5d %10.3e %10.3f %10.3f %14.6e' % (n, sim.time, reac.T, reac.thermo.P, reac.thermo.u))

		time += dt

	sim_attributes = {'pressure': pressure}
	result = Trajectory(species_names, times, data, sim_attributes)
	return result

