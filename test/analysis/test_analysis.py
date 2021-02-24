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

	def test_equilibrium_state(self):
		sim_long = util.water_cluster_simulation()

		result = kpy.equilibrium_state(sim_long)

		print(result)
		np_test.assert_allclose(result['N2'], 2.426859e+19)
