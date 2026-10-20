import sys, cv2, numpy as np
sys.path.insert(0, '.')
from engine import src
d = sys.argv[1]; out = sys.argv[2]; times = [float(x) for x in sys.argv[3:]]
s = src(d); tiles = []
for t in times:
    f = cv2.resize(s.frame(t), (216, 384))
    cv2.putText(f, f'{t:.2f}', (6, 372), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    tiles.append(f)
cols = min(10, len(tiles)); rows = (len(tiles) + cols - 1) // cols
while len(tiles) < rows * cols: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite(out, np.vstack([np.hstack(tiles[r * cols:(r + 1) * cols]) for r in range(rows)]))
