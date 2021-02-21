import unittest
import os
import numpy as np
import matplotlib.pyplot as plt
import kineticsPy as kpy


class TestVisualization(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		data_base_path = os.path.join('test_inputs')
		cls.water_cluster_input = os.path.join(data_base_path, 'WaterCluster_RoomTemp.cti')

		cls.result_base_path = os.path.join('test_results')
		if not os.path.exists(cls.result_base_path):
			os.mkdir(cls.result_base_path)

	@classmethod
	def water_cluster_simulation(cls):
		sim_result = kpy.cantera.simulate_isobar_adiabatic(
			cls.water_cluster_input,
			'H2O:2.5e+14, N2:2.54e+17, H3O+:1e+10',
			10000, 2e-9, 100000)

		return sim_result

	@classmethod
	def simple_synthetic_trajectory(cls):
		species_names = ["Cl1", "Cl2", "H2O"]
		times = np.linspace(0, 4, 100)
		c_cl1 = np.exp(times * 0.3)
		c_cl2 = 5 - c_cl1
		c_H2O = times * 0.1

		data_array = np.vstack([c_cl1, c_cl2, c_H2O]).transpose()
		attributes = {'temperature': 298}

		tra = kpy.Trajectory(
			species_names, times, data_array, attributes,
			concentration_unit='mol/m^3',
			time_scaling_factor=1e-6)

		return tra

	def test_concentration_plots_with_simulation(self):
		sim_result = self.water_cluster_simulation()

		# plot full trajectory:
		plot = kpy.plot(sim_result)
		plt.savefig(os.path.join(self.result_base_path,'watercluster_plot_simple_01.png'))


		# plot full trajectory:
		plot = kpy.plot(sim_result, figsize=(15,5))
		plt.savefig(os.path.join(self.result_base_path,'watercluster_plot_simple_02.png'))

		# simple species selection:
		plot = kpy.plot(sim_result, ['H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3', 'H3O+(H2O)4'])
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_03.png'))

		plot = kpy.plot(sim_result, ('H3O+', 'H3O+(H2O)') )
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_04.png'))

		plot = kpy.plot(sim_result, 'H3O+')
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_05.png'))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, 'I am not a species')

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, ['H3O+', 'I am not a species'])

		# time step ranges -------------- :

		# plotting up to end time step:
		plot = kpy.plot(sim_result, ('H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3'), 30)
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_06.png'))

		# plotting of time step range:
		plot = kpy.plot(sim_result, ('H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3'), (50, 100))
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_07.png'))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, time_steps=(100, 50))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, time_steps=(-5, 1000))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, time_steps=(1000, 10001))

	def test_concentration_plots_with_species_line_specifications(self):
		sim_result = self.simple_synthetic_trajectory()

		species_line_config_1 = [
			['Cl1', 'x-', 'red'],
			['Cl2', '--', '#112222'],
			['H2O', 'o-', '#0022CC']
		]

		species_line_config_2 = (
			('Cl1', '.-', 'grey'),
			('Cl2', '--', '#AAAA22')
		)

		kpy.plot(sim_result, species_line_config_1, 100, legend='upper left')
		plt.savefig(os.path.join(self.result_base_path, 'synthetic_data_plot_customized_01.png'))

		kpy.plot(sim_result, species_line_config_2, 100, legend='off')
		plt.savefig(os.path.join(self.result_base_path, 'synthetic_data_plot_customized_02.png'))