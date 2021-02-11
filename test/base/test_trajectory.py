import unittest
import kineticsPy.base.trajectory as tr
import pandas as pd
import pandas.testing as pd_test
import numpy.testing as np_test


class TestTrajectory(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	def test_basic_creation_and_access(self):

		species_names = ["A", "B", "H2O", "NO2"]
		times = [0.0, 2.5, 5.0, 7.5, 10.0, 15.0, 20.0]
		data_as_lists = [
			[10, 50,   20.0, 0.005],
			[12, 100,  19.8, 0.004],
			[14, 200,  19.6, 0.003],
			[16, 400,  19.8, 0.002],
			[18, 800,  18.5, 0.001],
			[20, 1600, 17.9, 0.00001],
			[22, 3200, 19.9, 0.0000001]
		]
		attributes = {'temperature':298}

		tra = tr.Trajectory(species_names, times, data_as_lists, attributes)
		self.assertEqual(tra.number_of_timesteps, 7)
		self.assertEqual(tra.species_names, species_names)
		self.assertEqual(tra.attributes['temperature'], 298)

		# test data access methods:

		# low level access with direct numeric indexing:
		with self.assertRaises(ValueError):
			buf = tra['B', 2]

		self.assertEqual(tra[2, 1], 200)
		np_test.assert_array_equal(tra[2], [1.40e+01, 2.00e+02, 1.96e+01, 3.00e-03])
		np_test.assert_array_equal(tra[1:4, 1], [100, 200, 400])
		np_test.assert_array_equal(tra[:, 0], [10, 12, 14, 16, 18, 20, 22])

		# high level access with "loc":

		# access of the time dimension with numeric (integer) index: (loc returns pandas objects)
		self.assertEqual(tra.loc['B'].iloc[2], 200)
		self.assertEqual(tra.loc['B', 2], 200)

		# access of the time with real time value:
		self.assertEqual(tra.loc['B'].loc[5.0], 200)

		# slicing is possible:
		pd_test.assert_series_equal(
			tra.loc['A', 2:4],
			pd.Series([14, 16], name='A', index=pd.Index([5.0, 7.5], name='Time')))


