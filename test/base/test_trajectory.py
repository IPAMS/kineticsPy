import unittest
import kineticsPy.base.trajectory as tr


class TestTrajectory(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	def test_basic_access(self):
		tra = tr.Trajectory()
		self.assertEqual(tra.n_timesteps, -1)

