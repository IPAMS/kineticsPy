# -*- coding: utf-8 -*-

#__all__ = (
#	'Trajectory')


class Trajectory:
	"""
	Base kinetic trajectory class:
	A kinetic trajectory is an abstracted kinetic simulation result, consisting of a time series of concentrations,
	simulation run meta data and convenient data access methods.

	The trajectory class is based on numpy and pandas.
	"""

	def __init__(self):

		self.n_timesteps = -1

	def number_of_timesteps(self):
		return self.n_timesteps
