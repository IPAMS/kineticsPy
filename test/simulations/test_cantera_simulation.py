import unittest
import os
# import kineticsPy.base.trajectory as tr
import kineticsPy.cantera.simulation as sim

class TestCanteraAnalysis(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		data_base_path = os.path.join('testfiles')
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

