import csv

# נייצר 30 חיתוכים עוקבים לאורך ציר Z (מ-10 עד 150)
num_frames = 30
rows = []

for i in range(num_frames):
    z = 10.0 + i * 4.0
    
    # משולש שווה שוקיים במישור XY בגובה Z קבוע:
    # a: קודקוד עליון (50, 100, z)
    # b: בסיס שמאל (10, 20, z) -> מרחק ל-a הוא sqrt(40^2 + 80^2) = sqrt(8000)
    # c: בסיס ימין (90, 20, z) -> מרחק ל-a הוא sqrt(40^2 + 80^2) = sqrt(8000)
    # dist(a,b) == dist(a,c) בדיוק מושלם!
    ax, ay, az = 50.0, 100.0, z
    bx, by, bz = 10.0, 20.0, z
    cx, cy, cz = 90.0, 20.0, z
    
    rows.append([ax, ay, az, bx, by, bz, cx, cy, cz])

with open("planes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Created planes.csv with {num_frames} isosceles triangle planes.")