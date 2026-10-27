# 3D Volume to Plane Projection Tool

An object-oriented Python implementation for slicing 3D volumetric data (NRRD) using parameterized isosceles triangle cutting planes, exported directly to an MP4 video sequence.

## Project Structure
- `geometry.py`: 3D spatial primitives (`Point3D`, `Vector3D`) and vector operations.
- `volume.py`: Volume loading and voxel boundary validation (`VolumeRaster`).
- `projector.py`: Core isosceles triangle plane projection and interpolation algorithm (`PlaneProjector`).
- `video_writer.py`: OpenCV video streaming and encoding context manager (`VideoExporter`).
- `Ex0.py`: Main CLI entry point and CSV coordinate parser.
- `generate_csv.py`: Utility script to generate sample cutting planes.

## Installation
```bash
pip install -r requirements.txt