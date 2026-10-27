import os
import nrrd
import numpy as np


class VolumeRaster:
    """מחלקה לניהול ודגימת נתוני נפח תלת-ממדיים מקובץ NRRD."""

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"NRRD file not found: {file_path}")

        # טעינת המידע וה-Header מהקובץ
        self.data, self.header = nrrd.read(file_path)

        # וידוא שמדובר במטריצה תלת-ממדית
        if self.data.ndim != 3:
            raise ValueError(f"Expected a 3D NRRD volume, got {self.data.ndim} dimensions.")

        # שמירת הממדים: sx, sy, sz
        self.shape = self.data.shape
        self.sx, self.sy, self.sz = self.shape

    def get_voxel(self, x: float, y: float, z: float) -> int:
        """
        דוגמת ערך ווקסל לפי שיטת השכן הקרוב (Nearest Neighbor).
        אם הקואורדינטה חורגת מגבולות המטריצה, מוחזר 0.
        """
        ix = int(round(x))
        iy = int(round(y))
        iz = int(round(z))

        # בדיקת גבולות (Boundaries Check)
        if 0 <= ix < self.sx and 0 <= iy < self.sy and 0 <= iz < self.sz:
            return int(self.data[ix, iy, iz])
        return 0

    def __repr__(self) -> str:
        return f"VolumeRaster(shape=({self.sx}, {self.sy}, {self.sz}), dtype={self.data.dtype})"