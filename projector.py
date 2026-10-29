import numpy as np
from numba import njit
from geometry import Point3D, Vector3D
from volume import VolumeRaster


@njit(fastmath=True)
def _render_projection_kernel(
    volume_data: np.ndarray,
    start_a1: np.ndarray,
    start_a2: np.ndarray,
    v_side1: np.ndarray,
    v_side2: np.ndarray,
    dab: int,
    dbc: int,
    out_matrix: np.ndarray
):
    """
    ליבת חישוב מואצת ב-Numba שמבצעת את סריקת החתך והדגימה מהנפח ישירות.
    עובדת הן עבור משולש (כש-start_a1 == start_a2) והן עבור טרפז.
    """
    sx, sy, sz = volume_data.shape

    curr_a1 = start_a1.copy()
    curr_a2 = start_a2.copy()

    for y in range(dab):
        # 5.1 & 5.2: התקדמות שורה אחת לאורך שתי השוקיים
        curr_a1[0] += v_side1[0]
        curr_a1[1] += v_side1[1]
        curr_a1[2] += v_side1[2]

        curr_a2[0] += v_side2[0]
        curr_a2[1] += v_side2[1]
        curr_a2[2] += v_side2[2]

        # מרחק השורה הנוכחית d12
        dx = curr_a2[0] - curr_a1[0]
        dy = curr_a2[1] - curr_a1[1]
        dz = curr_a2[2] - curr_a1[2]
        d12 = np.sqrt(dx * dx + dy * dy + dz * dz)
        steps_x = int(np.round(d12))

        # 5.5: וקטור יחידה dp לאורך השורה
        if steps_x > 0 and d12 > 1e-9:
            inv_d = 1.0 / d12
            dp_x = dx * inv_d
            dp_y = dy * inv_d
            dp_z = dz * inv_d
        else:
            dp_x, dp_y, dp_z = 0.0, 0.0, 0.0

        # ריפוד למיקום במרכז התמונה
        x_offset = (dbc / 2.0) - (d12 / 2.0)

        # 5.3: נקודת התחלה p לשורה הנוכחית
        px = curr_a1[0]
        py = curr_a1[1]
        pz = curr_a1[2]

        # 5.6: סריקת השורה
        for x1 in range(steps_x + 1):
            ix = int(np.round(px))
            iy = int(np.round(py))
            iz = int(np.round(pz))

            # בדיקת גבולות (דגימת ווקסל / 0 אם חורג)
            if 0 <= ix < sx and 0 <= iy < sy and 0 <= iz < sz:
                v = volume_data[ix, iy, iz]
            else:
                v = 0

            x = int(np.round(x_offset + x1))
            if 0 <= y < dab and 0 <= x < dbc:
                out_matrix[y, x] = v

            px += dp_x
            py += dp_y
            pz += dp_z


class PlaneProjector:
    """מחלקה האחראית על הטלת חתך מישורי מתוך גוש תלת-ממדי לתמונה דו-ממדית."""

    EPSILON = 0.001

    @staticmethod
    def project_triangle(volume: VolumeRaster, a: Point3D, b: Point3D, c: Point3D) -> np.ndarray:
        """הטלת משולש שווה שוקיים (a קודקוד ראש, b ו-c בסיס)."""
        dist_ab = a.distance_to(b)
        dist_ac = a.distance_to(c)

        if abs(dist_ab - dist_ac) >= PlaneProjector.EPSILON:
            raise ValueError(
                f"Points do not form an isosceles triangle: "
                f"|dist(a,b) - dist(a,c)| = {abs(dist_ab - dist_ac):.5f} >= {PlaneProjector.EPSILON}"
            )

        return PlaneProjector._project_core(volume, a, a, b, c)

    @staticmethod
    def project_trapezoid(volume: VolumeRaster, a1: Point3D, a2: Point3D, b: Point3D, c: Point3D) -> np.ndarray:
        """
        הטלת טרפז שווה שוקיים:
        a1 -> b ו-a2 -> c מייצגים את שתי השוקיים באותו האורך.
        """
        dist_a1_b = a1.distance_to(b)
        dist_a2_c = a2.distance_to(c)

        if abs(dist_a1_b - dist_a2_c) >= PlaneProjector.EPSILON:
            raise ValueError(
                f"Points do not form an isosceles trapezoid: "
                f"|dist(a1,b) - dist(a2,c)| = {abs(dist_a1_b - dist_a2_c):.5f} >= {PlaneProjector.EPSILON}"
            )

        dist_a1_a2 = a1.distance_to(a2)
        dist_bc = b.distance_to(c)

        if dist_a1_a2 > dist_bc + PlaneProjector.EPSILON:
            raise ValueError(
                f"Invalid trapezoid base order: dist(a1,a2) [{dist_a1_a2:.3f}] > dist(b,c) [{dist_bc:.3f}]"
            )

        return PlaneProjector._project_core(volume, a1, a2, b, c)

    @staticmethod
    def _project_core(volume: VolumeRaster, a1: Point3D, a2: Point3D, b: Point3D, c: Point3D) -> np.ndarray:
        dab = int(round(a1.distance_to(b)))
        dbc = int(round(b.distance_to(c)))

        if dab <= 0 or dbc <= 0:
            return np.zeros((max(1, dab), max(1, dbc)), dtype=volume.data.dtype)

        v_side1 = a1.vector_to(b).normalize()
        v_side2 = a2.vector_to(c).normalize()

        E = np.zeros((dab, dbc), dtype=volume.data.dtype)

        start_a1 = np.array([a1.x, a1.y, a1.z], dtype=np.float64)
        start_a2 = np.array([a2.x, a2.y, a2.z], dtype=np.float64)
        v_s1 = np.array([v_side1.x, v_side1.y, v_side1.z], dtype=np.float64)
        v_s2 = np.array([v_side2.x, v_side2.y, v_side2.z], dtype=np.float64)

        _render_projection_kernel(
            volume.data,
            start_a1,
            start_a2,
            v_s1,
            v_s2,
            dab,
            dbc,
            E
        )

        return E