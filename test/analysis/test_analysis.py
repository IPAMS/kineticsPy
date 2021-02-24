import unittest
import os
import numpy.testing as np_test
import kineticsPy as kpy
from . import util


class TestAnalysis(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.result_base_path = os.path.join('test_results')
		if not os.path.exists(cls.result_base_path):
			os.mkdir(cls.result_base_path)

	def test_equilibrium_state_with_precise_trajectory(self):
		sim_long = util.water_cluster_simulation(rtol=1e-11)

		result = kpy.equilibrium_state(sim_long)

		np_test.assert_allclose(result['N2'], 2.426859e+19)
		np_test.assert_allclose(result['H2O'], 2.388267e+16)
		np_test.assert_allclose(result['H3O+(H2O)4'], 8.684450e+11)

	def test_equilibrium_state_exceptions(self):

		with self.assertRaises(ValueError) as ve:
			sim = util.water_cluster_simulation(time_steps=500)
			kpy.equilibrium_state(sim, time_steps=1000)
		self.assertTrue('Number of time steps to average' in str(ve.exception))

		with self.assertRaises(ValueError) as ve:
			sim = util.water_cluster_simulation(time_steps=500)
			kpy.equilibrium_state(sim, time_steps=100)
		self.assertTrue('Maximum relative difference' in str(ve.exception))




