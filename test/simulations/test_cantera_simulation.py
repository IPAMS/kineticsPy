import unittest
import numpy.testing as np_test
import numpy as np
import os
import kineticsPy.cantera.simulation as sim


class TestCanteraAnalysis(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		data_base_path = os.path.join('test_inputs')
		cls.water_cluster_input = os.path.join(data_base_path, 'WaterCluster_RoomTemp.cti')

	def test_isobar_adiabatic_simulation(self):
		# perform a simple simulation of the example water cluster system:
		sim_result = sim.simulate_isobar_adiabatic(
			self.water_cluster_input,
			'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10',
			10000, 2e-7, 100000)

		# species names have to be correct:
		self.assertEqual(
			sim_result.species_names,
			['N2', 'H2O', 'H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3', 'H3O+(H2O)4'])

		# time steps have to be correct:
		self.assertEqual(
			sim_result.number_of_timesteps,
			10000
		)
		self.assertAlmostEqual(
			sim_result.times.iloc[-1],
			2e-7 * (10000-1)
		)

		print(sim_result[0, :].dtype)
		# simulation result has to be correct / reproducible:
		np_test.assert_allclose(
			sim_result[0, :],
			np.array([2.426859e+19, 2.388641e+16, 9.554562e+11, 0.0, 0.0, 0.0, 0.0], dtype='float64'),
			rtol=1e-6
		)

		# additional simulation run attributes have to be correct:
		self.assertEqual(
			sim_result.attributes['pressure'], 100000
		)
