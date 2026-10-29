import unittest
import math
from geometry import Point3D, Vector3D


class TestGeometry(unittest.TestCase):
    def test_point_distance(self):
        p1 = Point3D(0.0, 0.0, 0.0)
        p2 = Point3D(3.0, 4.0, 0.0)
        self.assertAlmostEqual(p1.distance_to(p2), 5.0, places=5)

    def test_vector_length_and_normalize(self):
        v = Vector3D(0.0, 3.0, 4.0)
        self.assertAlmostEqual(v.length(), 5.0, places=5)

        norm_v = v.normalize()
        self.assertAlmostEqual(norm_v.length(), 1.0, places=5)
        self.assertAlmostEqual(norm_v.x, 0.0, places=5)
        self.assertAlmostEqual(norm_v.y, 3.0 / 5.0, places=5)
        self.assertAlmostEqual(norm_v.z, 4.0 / 5.0, places=5)

    def test_zero_vector_normalize(self):
        v_zero = Vector3D(0.0, 0.0, 0.0)
        norm_zero = v_zero.normalize()
        self.assertEqual(norm_zero.x, 0.0)
        self.assertEqual(norm_zero.y, 0.0)
        self.assertEqual(norm_zero.z, 0.0)

    def test_point_add_vector(self):
        p = Point3D(10.0, 20.0, 30.0)
        v = Vector3D(1.0, -2.0, 5.0)
        p_res = p.add_vector(v)
        self.assertAlmostEqual(p_res.x, 11.0, places=5)
        self.assertAlmostEqual(p_res.y, 18.0, places=5)
        self.assertAlmostEqual(p_res.z, 35.0, places=5)


if __name__ == "__main__":
    unittest.main()