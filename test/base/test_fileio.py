import unittest
import kineticsPy as kpy
import os


class TestFileIO(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		data_base_path = os.path.join('test_inputs')
		cls.rs_input = os.path.join(data_base_path, 'qitSim_2019_04_15_001_concentrations.txt')

	def test_basic_idsimf_rs_reading(self):
		tra = kpy.read_idsimf_rs_result(self.rs_input)

		self.assertEqual(tra.number_of_timesteps, 50)
		self.assertAlmostEqual(tra.times.tolist()[-1], 9.8e-5)
		self.assertEqual(tra.loc['Cl_2'].iloc[4], 71)
