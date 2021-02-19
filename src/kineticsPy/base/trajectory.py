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
			return self._tajectory.data[arg[0]]
		elif len(arg) == 2:
			if type(arg[0]) == str and type(arg[1]) == str:  # two species names given
				return self._tajectory.data[arg]
			else:
				return self._tajectory.data[arg[0]].iloc[arg[1]]
		else:
			return self._tajectory.data[arg]


class Trajectory:
	"""
	Base kinetic trajectory class:
	A kinetic trajectory is an abstracted kinetic simulation result, consisting of a time series of concentrations,
	simulation run meta data and convenient data access methods.

	The trajectory class is based on numpy and pandas.
	"""

	def __init__(self, species_names, times, data, attributes=None):
		"""
		Constructs a new kinetic trajectory

		:param species_names: Names of chemical species in the trajectory
		:type species_names: list[str]
		:param times: Times of recorded concentration data points in the trajectory
		:type times: array_like with shape ``[n timesteps]``
		:param data: Concentration time series, essentially a two dimensional matrix of concentration
		 values for every time step and every time
		:type data: array_like with shape ``[number of time steps, number of species]``
		:param attributes: Optional trajectory attributes / meta data describing the trajectory (e.g. temperatures, pressures)
		:type attributes: dict

		"""

		self._species_names = species_names
		self._times = pd.Series(times)
		self._n_timesteps = len(times)
		self._data = pd.DataFrame(data=data, columns=species_names, index=times)
		self._data.index.name = "Time"
		self._indexer = TrajectoryIndexer(self)
		self._attributes = attributes

	@property
	def number_of_timesteps(self):
		"""
		Returns the number of timesteps in the kinetic trajectory
		"""
		return self._n_timesteps

	@property
	def times(self):
		"""
		Returns the times of the simulated time steps
		"""

		return self._times

	@property
	def species_names(self):
		"""
		Returns the chemical species names in the kinetic trajectory
		"""
		return self._species_names

	@property
	def data(self):
		"""
		Returns the underlying low level data object (currently a Pandas DataFrame)
		"""
		return self._data

	@property
	def attributes(self):
		"""
		Returns the attributes
		"""
		return self._attributes

	@property
	def loc(self):
		"""
		High level indexing of the trajectory.

		Allowed inputs are:

			+ a single species name ``tra.loc['B']`` which gives the time series for the specified species
			+ a species name and a time step index ``tra.loc['B', 2]`` which gives the value of the species at the
			  specified time index
			+ a species name and a time index slice ``tra.loc['B', 2:5]`` which gives a series of values of the species
			  at the specified time indices
			+ a list of species names ``tra.loc[['B', 'H2O']]`` returning the time series for all specified species as
			  Pandas DaaFrame
			+ a list of species names and a time index ``tra.loc[['B', 'H2O'], 5]`` or a time index slice
			  ``tra.loc[['B', 'H2O'], 5:10]`` returning the time series for all specified species and times
			  as Pandas DataFrame

		"""
		return self._indexer

	def __len__(self):
		return self._n_timesteps

	def __getitem__(self, arg):
		buf = self._data.iloc[arg]
		if type(buf) in (pd.DataFrame, pd.Series):
			return buf.values
		else:
			return buf