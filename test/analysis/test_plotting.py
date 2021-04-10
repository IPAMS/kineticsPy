import unittest
import os
import matplotlib.pyplot as plt
import kineticsPy as kpy
from . import util


class TestVisualization(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.result_base_path = os.path.join('test_results')
		if not os.path.exists(cls.result_base_path):
			os.mkdir(cls.result_base_path)

	def test_concentration_plots_with_simulation(self):
		sim_result = util.water_cluster_simulation()

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

		plot = kpy.plot(sim_result, ('H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3'), 30, normalized=True)
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_07.png'))

		# plotting of time step range:
		plot = kpy.plot(sim_result, ('H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3'), (50, 100))
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_08.png'))

		plot = kpy.plot(sim_result, ('H3O+', 'H3O+(H2O)', 'H3O+(H2O)2', 'H3O+(H2O)3'), (50, 100), normalized=True)
		plt.savefig(os.path.join(self.result_base_path, 'watercluster_plot_simple_09.png'))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, time_steps=(100, 50))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, time_steps=(-5, 1000))

		with self.assertRaises(ValueError):
			kpy.plot(sim_result, time_steps=(1000, 10001))

	def test_concentration_plots_with_species_line_specifications(self):
		sim_result = util.simple_synthetic_trajectory()

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

		kpy.plot(sim_result, species_line_config_2, 100, normalized=True)
		plt.savefig(os.path.join(self.result_base_path, 'synthetic_data_plot_customized_03.png'))

	def test_equilibrium_state_plot(self):
		sim_result = util.water_cluster_simulation()

		kpy.plot_equilibrium_state(sim_result, reltol=0.02)
		plt.savefig(os.path.join(self.result_base_path, 'water_cluster_equilibrium_plot_01.png'))

		kpy.plot_equilibrium_state(sim_result, reltol=0.02, log=True)
		plt.savefig(os.path.join(self.result_base_path, 'water_cluster_equilibrium_plot_02.png'))

