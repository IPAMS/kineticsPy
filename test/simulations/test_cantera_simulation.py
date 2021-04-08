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

	def test_isobar_adiabatic_simulation_with_equidistant_steps(self):
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

	def test_isobar_adiabatic_simulation_with_record_period(self):
		# perform a simple simulation of the example water cluster system:
		sim_result = sim.simulate_isobar_adiabatic(
			self.water_cluster_input,
			'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10',
			10000, 2e-7, 100000, record_period=7)

		# species names have to be correct:
		self.assertEqual(
			sim_result.species_names,
			['N2', 'H2O', 'H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3', 'H3O+(H2O)4'])

		# time steps have to be correct:
		self.assertEqual(
			sim_result.number_of_timesteps,
			1429
		)
		self.assertAlmostEqual(
			sim_result.times.iloc[-1],
			2e-7 * (10000-4)
		)
		# simulation result has to be correct / reproducible:
		np_test.assert_allclose(
			sim_result[0, :],
			np.array([2.426859e+19, 2.388641e+16, 9.554562e+11, 0.0, 0.0, 0.0, 0.0], dtype='float64'),
			rtol=1e-6
		)

	def test_isobar_adiabatic_simulation_with_custom_time_steps(self):
		test_times = [
			np.logspace(-2, 1, 1000),
			np.linspace(0, 10, 1000)
		]

		for times in test_times:
			with self.subTest(times=times):
				# perform a simple simulation of the example water cluster system:
				sim_result = sim.simulate_isobar_adiabatic(
					self.water_cluster_input,
					'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10',
					times, 100000)

				# species names have to be correct:
				self.assertEqual(
					sim_result.species_names,
					['N2', 'H2O', 'H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3', 'H3O+(H2O)4'])

				# time steps have to be correct:
				self.assertEqual(
					sim_result.number_of_timesteps,
					1000
				)
				self.assertAlmostEqual(
					sim_result.times.iloc[-1], 10.0
				)

				np_test.assert_allclose(sim_result.times, times)

				# simulation result has to be correct / reproducible:
				# (very small concentrations are prone to numerical error, thus compare only populated water
				# clusters)
				np_test.assert_allclose(
					sim_result[999, 4:],
					np.array([1.304673e+07, 8.699823e+10, 8.684450e+11], dtype='float64'),
					rtol=1e-6
				)