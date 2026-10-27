import math


class Vector3D:
    """מחלקה לייצוג וקטור במרחב תלת-ממדי (dx, dy, dz)."""

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def length(self) -> float:
        """חישוב אורך הווקטור (נורמה אוקלידית)."""
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def normalize(self) -> "Vector3D":
        """מחזירה וקטור יחידה באותו כיוון (אורך = 1)."""
        l = self.length()
        if l == 0:
            return Vector3D(0.0, 0.0, 0.0)
        return Vector3D(self.x / l, self.y / l, self.z / l)

    def __add__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector3D") -> "Vector3D":
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float) -> "Vector3D":
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __repr__(self) -> str:
        return f"Vector3D({self.x:.3f}, {self.y:.3f}, {self.z:.3f})"


class Point3D:
    """מחלקה לייצוג נקודה במרחב תלת-ממדי (x, y, z)."""

    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def distance_to(self, other: "Point3D") -> float:
        """מרחק אוקלידי לנקודה אחרת במרחב."""
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    def vector_to(self, target: "Point3D") -> Vector3D:
        """מחזירה וקטור שמצביע מנקודה זו לעבר נקודת היעד target."""
        return Vector3D(target.x - self.x, target.y - self.y, target.z - self.z)

    def add_vector(self, v: Vector3D) -> "Point3D":
        """קידום הנקודה במרחב לפי וקטור."""
        return Point3D(self.x + v.x, self.y + v.y, self.z + v.z)

    def __repr__(self) -> str:
        return f"Point3D({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"