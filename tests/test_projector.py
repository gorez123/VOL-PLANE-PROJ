import unittest
import numpy as np
from geometry import Point3D
from volume import VolumeRaster
from projector import PlaneProjector


class TestPlaneProjector(unittest.TestCase):
    def setUp(self):
        # יצירת נפח סינתטי בגודל 100x100x100 למטרת בדיקה מהירה ללא קובץ דיסק
        self.dummy_data = np.zeros((100, 100, 100), dtype=np.uint8)
        # סימון תיבה בעלת ערך 255 בתוכו
        self.dummy_data[20:80, 20:80, 20:80] = 255
        self.volume = VolumeRaster(self.dummy_data)

    def test_triangle_valid_projection(self):
        # משולש שווה שוקיים תקין במישור Z=50
        a = Point3D(50.0, 80.0, 50.0)
        b = Point3D(20.0, 20.0, 50.0)
        c = Point3D(80.0, 20.0, 50.0)

        # מרחק a->b שווה למרחק a->c
        image = PlaneProjector.project_triangle(self.volume, a, b, c)

        self.assertIsInstance(image, np.ndarray)
        self.assertGreater(image.shape[0], 0)
        self.assertGreater(image.shape[1], 0)
        # מוודא שנדגמו ערכים מתוך התיבה הפנימית
        self.assertIn(255, image)

    def test_triangle_non_isosceles_raises_error(self):
        # משולש שאינו שווה שוקיים
        a = Point3D(50.0, 80.0, 50.0)
        b = Point3D(20.0, 20.0, 50.0)
        c = Point3D(90.0, 10.0, 50.0)

        with self.assertRaises(ValueError):
            PlaneProjector.project_triangle(self.volume, a, b, c)

    def test_trapezoid_valid_projection(self):
        # טרפז שווה שוקיים תקין
        a1 = Point3D(35.0, 70.0, 50.0)
        a2 = Point3D(65.0, 70.0, 50.0)
        b = Point3D(20.0, 20.0, 50.0)
        c = Point3D(80.0, 20.0, 50.0)

        image = PlaneProjector.project_trapezoid(self.volume, a1, a2, b, c)

        self.assertIsInstance(image, np.ndarray)
        self.assertGreater(image.shape[0], 0)
        self.assertGreater(image.shape[1], 0)

    def test_trapezoid_invalid_base_order_raises_error(self):
        # טרפז שבו הבסיס העליון ארוך מהבסיס התחתון (בניגוד לתנאי dist(a1,a2) <= dist(b,c))
        a1 = Point3D(10.0, 70.0, 50.0)
        a2 = Point3D(90.0, 70.0, 50.0)
        b = Point3D(40.0, 20.0, 50.0)
        c = Point3D(60.0, 20.0, 50.0)

        with self.assertRaises(ValueError):
            PlaneProjector.project_trapezoid(self.volume, a1, a2, b, c)


if __name__ == "__main__":
    unittest.main()