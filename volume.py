import os
import nrrd
import numpy as np


class VolumeRaster:
    """Class representing 3D volumetric raster data with boundary checking and voxel sampling."""

    def __init__(self, file_path_or_array):
        """
        Initializes volume from either a filepath (NRRD format) or a direct 3D numpy array.
        """
        if isinstance(file_path_or_array, np.ndarray):
            self.data = np.ascontiguousarray(file_path_or_array)
            self.header = {}
        elif isinstance(file_path_or_array, str):
            if not os.path.exists(file_path_or_array):
                raise FileNotFoundError(f"NRRD file not found: {file_path_or_array}")
            loaded_data, self.header = nrrd.read(file_path_or_array)
            self.data = np.ascontiguousarray(loaded_data)
        else:
            raise TypeError("Expected file path string or numpy.ndarray.")

        if self.data.ndim != 3:
            raise ValueError(f"Expected 3D volume raster, got {self.data.ndim} dimensions.")

        self.shape = self.data.shape
        self.sx, self.sy, self.sz = self.shape

    def get_voxel(self, x: float, y: float, z: float) -> int:
        """
        Samples voxel value using nearest-neighbor interpolation.
        Returns 0 if coordinate lies outside volume bounds.
        """
        ix = int(round(x))
        iy = int(round(y))
        iz = int(round(z))

        if 0 <= ix < self.sx and 0 <= iy < self.sy and 0 <= iz < self.sz:
            return int(self.data[ix, iy, iz])
        return 0

    def __repr__(self) -> str:
        return f"VolumeRaster(shape=({self.sx}, {self.sy}, {self.sz}), dtype={self.data.dtype})"