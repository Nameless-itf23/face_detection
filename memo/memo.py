
import cv2
from insightface.app import FaceAnalysis

app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))

path = 'memo/face.jpg' # file path
img = cv2.imread(path)

faces = app.get(img)
vec = faces[0].embedding
print(vec)