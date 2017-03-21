import numpy as np
import unittest
import os
import filecmp
from trussme import truss

TEST_TRUSS_FILENAME = os.path.join(os.path.dirname(__file__), 'example.trs')


class TestSequenceFunctions(unittest.TestCase):

    def test_build_methods(self):
        # Build truss from scratch
        t1 = truss.Truss()
        t1.add_support(np.array([0.0, 0.0, 0.0]), d=2)
        t1.add_joint(np.array([1.0, 0.0, 0.0]), d=2)
        t1.add_joint(np.array([2.0, 0.0, 0.0]), d=2)
        t1.add_joint(np.array([3.0, 0.0, 0.0]), d=2)
        t1.add_joint(np.array([4.0, 0.0, 0.0]), d=2)
        t1.add_support(np.array([5.0, 0.0, 0.0]), d=2)

        t1.add_joint(np.array([0.5, 1.0, 0.0]), d=2)
        t1.add_joint(np.array([1.5, 1.0, 0.0]), d=2)
        t1.add_joint(np.array([2.5, 1.0, 0.0]), d=2)
        t1.add_joint(np.array([3.5, 1.0, 0.0]), d=2)
        t1.add_joint(np.array([4.5, 1.0, 0.0]), d=2)

        t1.joints[7].loads[1] = -20000
        t1.joints[8].loads[1] = -20000
        t1.joints[9].loads[1] = -20000

        t1.add_member(0, 1)
        t1.add_member(1, 2)
        t1.add_member(2, 3)
        t1.add_member(3, 4)
        t1.add_member(4, 5)

        t1.add_member(6, 7)
        t1.add_member(7, 8)
        t1.add_member(8, 9)
        t1.add_member(9, 10)

        t1.add_member(0, 6)
        t1.add_member(6, 1)
        t1.add_member(1, 7)
        t1.add_member(7, 2)
        t1.add_member(2, 8)
        t1.add_member(8, 3)
        t1.add_member(3, 9)
        t1.add_member(9, 4)
        t1.add_member(4, 10)
        t1.add_member(10, 5)

        t1.set_goal(min_fos_buckling=1.5,
                    min_fos_yielding=1.5,
                    max_mass=5.0,
                    max_deflection=6e-3)

        # Build truss from file
        t2 = truss.Truss(TEST_TRUSS_FILENAME)
        t2.set_goal(min_fos_buckling=1.5,
                    min_fos_yielding=1.5,
                    max_mass=5.0,
                    max_deflection=6e-3)

        # Save reports
        t1.save_report(os.path.join(os.path.dirname(__file__), 'report_1.txt'))
        t2.save_report(os.path.join(os.path.dirname(__file__), 'report_2.txt'))

        # Test for sameness
        file_are_the_same = filecmp.cmp(
            os.path.join(os.path.dirname(__file__), 'report_1.txt'),
            os.path.join(os.path.dirname(__file__), 'report_2.txt'))
        self.assertTrue(file_are_the_same)

        # Clean up
        os.remove(os.path.join(os.path.dirname(__file__), 'report_1.txt'))
        os.remove(os.path.join(os.path.dirname(__file__), 'report_2.txt'))

    def test_save_and_rebuild(self):
        # Build truss from file
        t2 = truss.Truss(TEST_TRUSS_FILENAME)
        t2.set_goal(min_fos_buckling=1.5,
                    min_fos_yielding=1.5,
                    max_mass=5.0,
                    max_deflection=6e-3)

        # Save
        t2.save_report(os.path.join(os.path.dirname(__file__), 'report_2.txt'))
        t2.save_truss(os.path.join(os.path.dirname(__file__), 'asdf.trs'))

        # Rebuild
        t3 = truss.Truss(os.path.join(os.path.dirname(__file__), 'asdf.trs'))
        t3.set_goal(min_fos_buckling=1.5,
                    min_fos_yielding=1.5,
                    max_mass=5.0,
                    max_deflection=6e-3)
        t3.save_report(os.path.join(os.path.dirname(__file__), 'report_3.txt'))

        # Test for sameness
        file_are_the_same = filecmp.cmp(
            os.path.join(os.path.dirname(__file__), 'report_3.txt'),
            os.path.join(os.path.dirname(__file__), 'report_2.txt'))
        self.assertTrue(file_are_the_same)

        # Clean up
        os.remove(os.path.join(os.path.dirname(__file__), 'report_2.txt'))
        os.remove(os.path.join(os.path.dirname(__file__), 'report_3.txt'))
        os.remove(os.path.join(os.path.dirname(__file__), 'asdf.trs'))


class TestComputations2D(unittest.TestCase):

    def build_triangle_truss(self):
        # Build truss from scratch
        # Simple triangular truss
        t4 = truss.Truss()
        t4.add_support(np.array([0.0, 0.0, 0.0]), d=2)
        t4.add_roller(np.array([2.0, 0.0, 0.0]), axis='y', d=2)
        t4.add_joint(np.array([1.0, 3.0, 0.0]), d=2)

        t4.add_member(0, 1)
        t4.add_member(1, 2)
        t4.add_member(0, 2)

        t4.joints[2].loads[0] = 0
        t4.joints[2].loads[1] = 1
        t4.joints[2].loads[2] = 0

        for m in t4.members:
            m.set_shape('arbitrary')
            m.set_parameters(a=1, I_min=1)
            m.rho = 1.0
            m.elastic_modulus = 1.0
            m.Fy = 1.0
            m.calc_properties()

        t4.g = np.array([0.0, -1.0, 0.0])

        t4.set_goal(min_fos_buckling=-1,
                    min_fos_yielding=-1,
                    max_mass=-1,
                    max_deflection=-1)

        t4.save_report(os.path.join(os.path.dirname(__file__), 'report_4.txt'))
        os.remove(os.path.join(os.path.dirname(__file__), 'report_4.txt'))
        return t4

    def test_computation_of_reactions(self):
        t = self.build_triangle_truss()
        for j in range(0, 2):
            for i in range(0, 2):
                first = t.joints[j].reactions[i]
                second = [[0], [3.66228], [0]][i]
                self.assertAlmostEqual(first, second, places=5)

    def test_computation_of_member_masses(self):
        t = self.build_triangle_truss()
        self.assertAlmostEqual(t.members[0].mass,
                               2.0,
                               places=5)
        self.assertAlmostEqual(t.members[1].mass,
                               3.16228,
                               places=5)
        self.assertAlmostEqual(t.members[2].mass,
                               3.16228,
                               places=5)

    def build_single_bar_truss(self):
        # Build truss from scratch
        t5 = truss.Truss()
        t5.add_support(np.array([0.0, 0.0, 0.0]), d=2)
        t5.add_roller(np.array([0.0, 1.0, 0.0]), axis='x', d=2)

        t5.add_member(0, 1)

        t5.joints[1].loads[0] = 0
        t5.joints[1].loads[1] = 3
        t5.joints[1].loads[2] = 0

        for m in t5.members:
            m.set_shape('arbitrary')
            m.set_parameters(area=1, I_min=1)
            m.rho = 1.0
            m.elastic_modulus = 1.0
            m.Fy = 1.0
            m.calc_properties()

        t5.g = np.array([0.0, -1.0, 0.0])

        t5.set_goal(min_fos_buckling=-1,
                    min_fos_yielding=-1,
                    max_mass=-1,
                    max_deflection=-1)

        t5.print_report()

if __name__ == "__main__":
    unittest.main()
