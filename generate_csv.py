import csv
import math


def generate_sample_csv(output_path: str = "planes.csv"):
    """
    Generates a CSV file containing both isosceles triangle (3 points / 9 values)
    and isosceles trapezoid (4 points / 12 values) slicing planes.
    """
    rows = []

    # 1. 15 פריימים של משולש שווה שוקיים עוקב לאורך ציר Z
    for i in range(15):
        z = 10.0 + i * 8.0
        # קודקוד ראש a=(50, 100, z)
        # בסיס b=(10, 20, z), c=(90, 20, z)
        # dist(a,b) = dist(a,c) = sqrt(40^2 + 80^2) = sqrt(8000)
        ax, ay, az = 50.0, 100.0, z
        bx, by, bz = 10.0, 20.0, z
        cx, cy, cz = 90.0, 20.0, z
        rows.append([ax, ay, az, bx, by, bz, cx, cy, cz])

    # 2. 15 פריימים של טרפז שווה שוקיים עוקב לאורך ציר Z
    for i in range(15):
        z = 10.0 + i * 8.0
        # בסיס עליון קצר: a1=(30, 80, z), a2=(70, 80, z) -> רוחב = 40
        # בסיס תחתון ארוך: b=(10, 20, z), c=(90, 20, z) -> רוחב = 80
        # שוק 1 (a1 -> b): dx=20, dy=60 -> אורך sqrt(20^2 + 60^2) = sqrt(4000)
        # שוק 2 (a2 -> c): dx=20, dy=60 -> אורך sqrt(20^2 + 60^2) = sqrt(4000)
        # שוקיים שוות, ורוחב בסיס עליון (40) קטן מרוחב בסיס תחתון (80)
        a1x, a1y, a1z = 30.0, 80.0, z
        a2x, a2y, a2z = 70.0, 80.0, z
        bx, by, bz = 10.0, 20.0, z
        cx, cy, cz = 90.0, 20.0, z
        rows.append([a1x, a1y, a1z, a2x, a2y, a2z, bx, by, bz, cx, cy, cz])

    with open(output_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} planes in '{output_path}'.")


if __name__ == "__main__":
    generate_sample_csv("planes.csv")