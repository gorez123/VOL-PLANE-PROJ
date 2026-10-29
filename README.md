# 3D Volume to Plane Projection Tool

An object-oriented, high-performance Python application designed to project 2D cross-sectional planar images from 3D volumetric raster data (NRRD format) based on geometric slicing definitions (triangles and trapezoids), and compile them into an MP4 video sequence.

Developed as part of the Software Engineering / Object-Oriented Design (OOD) curriculum.

---

## Architecture & Modular Design

The project strictly follows Object-Oriented Design (OOD) principles with single-responsibility modular separation:

- **`geometry.py`**: Encapsulates 3D spatial primitives (`Point3D`, `Vector3D`), Euclidean metrics, vector normalization, and coordinate additions.
- **`volume.py`**: Handles raster data encapsulation, NRRD file parsing, in-memory array conversion, and safe voxel extraction with nearest-neighbor interpolation (`VolumeRaster`).
- **`projector.py`**: Implements the scanline projection algorithm with Numba JIT acceleration for both isosceles triangles and trapezoids (`PlaneProjector`).
- **`video_writer.py`**: Context manager wrapping OpenCV's `VideoWriter`, managing dynamic dynamic-range normalization and multi-frame encoding (`VideoExporter`).
- **`Ex0.py`**: Command-line entry point responsible for argument parsing, CSV geometry extraction, and progress reporting.
- **`generate_csv.py`**: Utility script producing sample CSV files containing valid 3-point and 4-point slicing plane sequences.

---

## The Projection Algorithm

Given a 3D matrix $M$ of size $s_x \times s_y \times s_z$ and a planar polygon in 3D space:

### 1. Isosceles Triangle $(a, b, c)$
- **Constraints**: Vertices satisfy $|dist(a, b) - dist(a, c)| < \epsilon$ ($\epsilon = 0.001$).
- **Algorithm Flow**:
  1. $D_{ab} = dist(a, b) = dist(a, c)$ and $D_{bc} = dist(b, c)$.
  2. Unit vectors along the legs: $v(a, b) = \frac{\vec{ab}}{D_{ab}}$ and $v(a, c) = \frac{\vec{ac}}{D_{ab}}$.
  3. Output matrix $E$ initialized to dimensions $D_{ab} \times D_{bc}$.
  4. Pointers start at $a_1 = a$, $a_2 = a$.
  5. For each row $y \in [0, D_{ab})$:
     - $a_1 \leftarrow a_1 + v(a, b)$, $a_2 \leftarrow a_2 + v(a, c)$.
     - $d_{12} = dist(a_1, a_2)$, $dp = \frac{\vec{a_1 a_2}}{d_{12}}$.
     - For each step $x_1 \in [0, d_{12}]$:
       - Sample voxel $v = M[p]$ (if $p \notin M$, $v = 0$).
       - Target pixel coordinate: $x = \frac{D_{bc}}{2} - \frac{d_{12}}{2} + x_1$.
       - Store $E[y, x] = v$.
       - Advance $p \leftarrow p + dp$.

### 2. Isosceles Trapezoid $(a_1, a_2, b, c)$
- **Constraints**: $|dist(a_1, b) - dist(a_2, c)| < \epsilon$ and $dist(a_1, a_2) \le dist(b, c)$.
- **Algorithm Flow**: Slicing begins with separated endpoints $a_1$ and $a_2$, stepping along $v(a_1, b)$ and $v(a_2, c)$ respectively.

---

## Datasets

The tool accepts volumetric datasets in standard NRRD (Nearly Raw Raster Data) format. Tested data sources include:
- **3D Slicer Sample Data**: Standard clinical MRI head scan (`MRHead.nrrd`) available via the [3D Slicer Data Repository](https://github.com/Slicer/SlicerDataStore).
- **Synthetic Test Volumes**: Uniform and graded 3D matrices generated during unit test execution.

---

## Testing Strategy

The test suite covers unit tests for geometric primitives and integration tests for raster slicing:
- **Geometric Primitives**: Tests Euclidean distance calculations, vector lengths, unit normalization, and zero-vector edge cases.
- **Plane Validation**: Verifies rejection of non-isosceles configurations and malformed trapezoid geometries.
- **Voxel Extraction**: Tests projection accuracy on known synthetic 3D matrices.

Execute tests using:
```bash
python -m unittest discover tests