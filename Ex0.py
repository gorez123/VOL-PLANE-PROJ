import sys
import os
import time
import csv
from geometry import Point3D
from volume import VolumeRaster
from projector import PlaneProjector
from video_writer import VideoExporter


def parse_csv_planes(csv_path: str):
    """
    Parses a CSV file containing plane cutting definitions.
    Supports:
      - 3 points (9 floats): a, b, c (Isosceles triangle)
      - 4 points (12 floats): a1, a2, b, c (Isosceles trapezoid)
    """
    planes = []
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader, start=1):
            cleaned = [val.strip() for val in row if val.strip()]
            if not cleaned:
                continue

            try:
                coords = [float(val) for val in cleaned]
            except ValueError as err:
                print(f"Warning: Line {row_idx} contains invalid numeric data: {err}. Skipping.")
                continue

            if len(coords) == 9:
                a = Point3D(coords[0], coords[1], coords[2])
                b = Point3D(coords[3], coords[4], coords[5])
                c = Point3D(coords[6], coords[7], coords[8])
                planes.append((a, b, c))
            elif len(coords) == 12:
                a1 = Point3D(coords[0], coords[1], coords[2])
                a2 = Point3D(coords[3], coords[4], coords[5])
                b = Point3D(coords[6], coords[7], coords[8])
                c = Point3D(coords[9], coords[10], coords[11])
                planes.append((a1, a2, b, c))
            else:
                print(f"Warning: Line {row_idx} has {len(coords)} coordinates (expected 9 or 12). Skipping.")

    return planes


def main():
    if len(sys.argv) < 4:
        print("Usage: python Ex0.py <file.nrrd> <file.csv> <file.mp4>")
        sys.exit(1)

    nrrd_path = sys.argv[1]
    csv_path = sys.argv[2]
    mp4_path = sys.argv[3]

    print(f"[1/4] Loading volume from: {nrrd_path}...")
    start_time = time.time()
    try:
        volume = VolumeRaster(nrrd_path)
    except Exception as err:
        print(f"Error loading volume raster: {err}")
        sys.exit(1)
    print(f"      Volume loaded successfully: shape={volume.shape}, dtype={volume.data.dtype}")

    print(f"[2/4] Parsing cutting planes from: {csv_path}...")
    try:
        planes = parse_csv_planes(csv_path)
    except Exception as err:
        print(f"Error parsing CSV file: {err}")
        sys.exit(1)

    total_frames = len(planes)
    print(f"      Found {total_frames} valid cutting planes to project.")

    if total_frames == 0:
        print("Error: No valid planes found in CSV file. Terminating.")
        sys.exit(1)

    print(f"[3/4] Processing projections and encoding to video: {mp4_path}...")
    render_start = time.time()

    with VideoExporter(mp4_path, fps=30) as video:
        for idx, plane in enumerate(planes, start=1):
            if len(plane) == 3:
                a, b, c = plane
                frame = PlaneProjector.project_triangle(volume, a, b, c)
            else:
                a1, a2, b, c = plane
                frame = PlaneProjector.project_trapezoid(volume, a1, a2, b, c)

            video.write_frame(frame)

            if idx % 10 == 0 or idx == total_frames:
                print(f"      Rendered frame {idx}/{total_frames}...")

    render_duration = time.time() - render_start
    total_duration = time.time() - start_time
    fps = total_frames / render_duration if render_duration > 0 else 0.0

    print("[4/4] Execution completed successfully!")
    print(f"      Rendering time: {render_duration:.2f}s ({fps:.1f} FPS)")
    print(f"      Total execution time: {total_duration:.2f}s")
    print(f"      Video output saved to: {mp4_path}")


if __name__ == "__main__":
    main()