# -*- coding: utf-8 -*-

import pandas as pd

__all__ = ["Trajectory"]


class TrajectoryIndexer:
	"""
	Simple indexer for the trajectory class
	(similar to the indexer classes used by Pandas)
	"""

	def __init__(self, parent_trajectory):
		self._tajectory = parent_trajectory

	def __getitem__(self, arg):
		if len(arg) == 1:
			return self._tajectory.data[arg]
		elif len(arg) == 2:
			return self._tajectory.data[arg[0]].iloc[arg[1]]
		else:
			raise ValueError('Argument is not 1 or 2 dimensional');


class Trajectory:
	"""
	Base kinetic trajectory class:
	A kinetic trajectory is an abstracted kinetic simulation result, consisting of a time series of concentrations,
	simulation run meta data and convenient data access methods.

	The trajectory class is based on numpy and pandas.
	"""

	def __init__(self, species_names, times, data, attributes=None):
		"""
		Constructs a new kinetic Trajectory

		:param species_names: Names of chemical species in the trajectory
		:type species_names: list[str]
		:param times: Times of recorded concentration data points in the trajectory
		:type times: numpy.ndarray with shape ``[n timesteps, 1]``
		:param data: Concentration time series, essentially a two dimensional matrix of concentration
		values for every time step and every time
		:type times: numpy.ndarray with shape ``[numbe of species, number of time steps]``
		:param attributes: Optional trajectory attributes / meta data describing the trajectory (e.g. temperatures, pressures)
		:type attributes: dict
		"""

		self._species_names = species_names
		self._times = pd.Series(times)
		self._n_timesteps = len(times)
		self._data = pd.DataFrame(data=data, columns=species_names, index=times)
		self._data.index.name = "Time"
		self._indexer = TrajectoryIndexer(self)

	@property
	def number_of_timesteps(self):
		return self._n_timesteps

	@property
	def species_names(self):
		return self._species_names

	@property
	def data(self):
		return self._data

	@property
	def loc(self):
		return self._indexer

	def __len__(self):
		return self._n_timesteps
