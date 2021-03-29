# -*- coding: utf-8 -*-

"""
File input and output of kinetic results and kinetic trajectories
"""

import os
import pandas as pd
from kineticsPy.base.trajectory import Trajectory


def read_idsimf_rs_result(rs_file_path):
	"""
	Reads an IDSimF reaction simulatio (RS) result from an RS result file

	:param rs_file_path: The path to the IDSimF-RS result file
	:type rs_file_path: path
	:return: A kinetic trajectory with the results
	:rtype: Trajectory
	"""

	df = pd.read_csv(rs_file_path, skiprows=1, delimiter=';').iloc[:, :-1].rename(columns=lambda x: x.strip())
	names = df.columns.tolist()[2:]
	times = df['Time'].tolist()
	data = df[names].values

	trajectory = Trajectory(names, times, data)
	return trajectory
