import numpy as np
from geometry import Point3D, Vector3D
from volume import VolumeRaster


class PlaneProjector:
    """מחלקה האחראית על הטלת חתך מישורי/משולש מתוך גוש תלת-ממדי לתמונה דו-ממדית."""

    EPSILON = 0.001

    @staticmethod
    def project_triangle(volume: VolumeRaster, a: Point3D, b: Point3D, c: Point3D) -> np.ndarray:
        """
        מבצעת הטלה של משולש שווה-שוקיים a, b, c מתוך הנפח התלת-ממדי.
        מחזירה מטריצה דו-ממדית (תמונה) בגודל (Dab, Dbc).
        """
        # שלב 1: חישוב מרחקים
        dist_ab = a.distance_to(b)
        dist_ac = a.distance_to(c)
        dist_bc = b.distance_to(c)

        # בדיקת תקינות: האם המשולש שווה שוקיים עד כדי EPSILON
        if abs(dist_ab - dist_ac) >= PlaneProjector.EPSILON:
            raise ValueError(
                f"Points do not form an isosceles triangle: "
                f"|dist(a,b) - dist(a,c)| = {abs(dist_ab - dist_ac):.5f} >= {PlaneProjector.EPSILON}"
            )

        dab = int(round(dist_ab))
        dbc = int(round(dist_bc))

        if dab == 0 or dbc == 0:
            return np.zeros((max(1, dab), max(1, dbc)), dtype=np.uint8)

        # שלב 2: וקטורי כיוון יחידה לאורך השוקיים
        v_ab = a.vector_to(b).normalize()
        v_ac = a.vector_to(c).normalize()

        # שלב 3: הגדרת מטריצת הפלט E (גובה Dab, רוחב Dbc)
        # שים לב: לפי אינדוקס מטריצות (row, col) => שורה היא y, עמודה היא x
        # נשתמש ב-dtype שתואם ל-volume
        out_dtype = volume.data.dtype if hasattr(volume, 'data') else np.uint8
        E = np.zeros((dab, dbc), dtype=out_dtype)

        # שלב 4: אתחול נקודות קצה של השורה
        a1 = a
        a2 = a

        # שלב 5: סריקת השורות מלמעלה (a) למטה (לכיוון b ו-c)
        for y in range(dab):
            # 5.1 ו-5.2: התקדמות שורה אחת לאורך שתי השוקיים
            a1 = a1.add_vector(v_ab)
            a2 = a2.add_vector(v_ac)

            # 5.3 ו-5.4: נקודת התחלה ורוחב השורה הנוכחית
            p = a1
            d12 = a1.distance_to(a2)
            steps_x = int(round(d12))

            # 5.5: וקטור יחידה לרוחב השורה
            if steps_x > 0:
                dp = a1.vector_to(a2).normalize()
            else:
                dp = Vector3D(0, 0, 0)

            # חישוב הריפוד/האופסט למיקום המשולש במרכז התמונה
            x_offset = (dbc / 2.0) - (d12 / 2.0)

            # 5.6: סריקה לאורך השורה
            for x1 in range(steps_x + 1):
                # דגימת הווקסל מתוך הגוש התלת-ממדי (מחזיר 0 אם חורג)
                v = volume.get_voxel(p.x, p.y, p.z)

                x = int(round(x_offset + x1))

                # וידוא שהאינדקס לא חורג מגבולות התמונה הדו-ממדית
                if 0 <= y < dab and 0 <= x < dbc:
                    E[y, x] = v

                # התקדמות צעד אחד לאורך השורה
                p = p.add_vector(dp)

        # שלב 6: החזרת המטריצה
        return E