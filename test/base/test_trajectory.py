import unittest
import kineticsPy.base.trajectory as tr
import pandas as pd
import pandas.testing as pd_test


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
		attributes = None

		tra = tr.Trajectory(species_names, times, data_as_lists, attributes)
		self.assertEqual(tra.number_of_timesteps, 7)
		self.assertEqual(tra.species_names, species_names)

		# test access methods:

		# high level access with "loc":
		self.assertEqual(tra.loc['B'].iloc[2], 200)
		self.assertEqual(tra.loc['B', 2], 200)
		pd_test.assert_series_equal(
			tra.loc['A', 2:4],
			pd.Series([14, 16], name='A', index=pd.Index([5.0, 7.5], name='Time')))


