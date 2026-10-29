# Software Requirements Specification (SRS)

## 1. Introduction
### 1.1 Purpose
This document specifies the software requirements for the **3D Volume to Plane Projection Tool**. The system allows users to extract planar 2D slices (projections) from 3D volumetric raster data (NRRD) based on geometric cutting planes defined by triangles or trapezoids, rendering the resulting slice sequence into an MP4 video.

### 1.2 Scope
The software operates as a high-performance command-line utility (CLI). It processes 3D scalar matrices, samples voxel data along continuous geometric coordinates using nearest-neighbor interpolation, and exports standardized video streams. The design emphasizes Object-Oriented Design (OOD), memory efficiency, and real-time execution speeds exceeding 30 to 100+ frames per second (FPS).

---

## 2. Overall Description
### 2.1 Product Perspective
The system acts as a standalone volumetric slicing engine. It interfaces with external volumetric medical/scientific datasets (NRRD format) and structured coordinate specifications (CSV format), producing standard H.264/MPEG-4 encoded video streams.

### 2.2 System Architecture & Design
The architecture is decoupled into distinct single-responsibility modules:
- **Spatial Primitives (`geometry.py`)**: Vector and coordinate manipulation (`Point3D`, `Vector3D`).
- **Volume Raster Handler (`volume.py`)**: In-memory volume storage, validation, and spatial boundaries (`VolumeRaster`).
- **Projection Engine (`projector.py`)**: Scanline rasterization algorithms accelerated via Numba JIT (`PlaneProjector`).
- **Video Exporter (`video_writer.py`)**: OpenCV stream management, dynamic normalization, and video serialization (`VideoExporter`).
- **CLI Pipeline (`Ex0.py`)**: Orchestration of parsing, slicing loops, and diagnostic logging.

---

## 3. Specific Requirements

### 3.1 Functional Requirements
- **FR-1: NRRD Ingestion**: The system must load and validate 3D raster data matrix $M$ of size $s_x \times s_y \times s_z$ where $1 \le s_x, s_y, s_z < 2^{10}$.
- **FR-2: Dynamic Bit-Depth Support**: Support voxel intensities across 8-bit, 16-bit, and 32-bit unsigned integers.
- **FR-3: CSV Parsing**: The system must parse CSV rows consisting of:
  - 9 numerical values representing an isosceles triangle ($a, b, c$).
  - 12 numerical values representing an isosceles trapezoid ($a_1, a_2, b, c$).
- **FR-4: Geometric Validation**:
  - For triangles: verify $|dist(a, b) - dist(a, c)| < \epsilon$ where $\epsilon = 0.001$.
  - For trapezoids: verify $|dist(a_1, b) - dist(a_2, c)| < \epsilon$ and $dist(a_1, a_2) \le dist(b, c)$.
- **FR-5: Planar Projection & Boundary Clamping**:
  - Sample voxels $v = M[p]$ along incremental scanlines.
  - Return $v = 0$ for coordinates lying outside matrix boundaries.
  - Center sampled scanlines along horizontal dimensions $(D_{bc} / 2) - (d_{12} / 2) + x_1$.
- **FR-6: Video Serialization**:
  - Automatically normalize diverse integer ranges into viewable 8-bit frames.
  - Stream all rendered frames sequentially into an MP4 container at a minimum of 30 FPS.

### 3.2 Non-Functional Requirements
- **NFR-1: Performance & Throughput**:
  - Must achieve a minimum throughput of $\ge 30\text{ FPS}$ on test matrices ($500^3$).
  - Target throughput of $\ge 100\text{ FPS}$ utilizing JIT machine compilation (LLVM/Numba).
- **NFR-2: Robustness**: The system must handle non-existent files, corrupted inputs, empty rows, and malformed coordinates gracefully with clear CLI error messages without crashing.
- **NFR-3: Modularity & Extensibility**: Components must follow OOP principles, allowing seamless swapping of rendering backends or coordinate formats.
- **NFR-4: Portability**: Runs across standard Python environments on Linux, macOS, and Windows.

---

## 4. Verification & Testing Strategy
- Unit testing of spatial operations, vector normalization, and distance metrics.
- Projection accuracy tests verifying voxel sampling on deterministic synthetic volumes.
- Input validation testing for malformed geometries and non-isosceles configurations.
- End-to-end integration tests verifying CLI arguments and valid MP4 generation.