import numpy as np
import cv2
from insightface.app import FaceAnalysis
import db
import time

app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))

def cos_sim(feat1, feat2):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))

face_num = 2  # 登録した顔の数
faces = []
for i in range(face_num):
    img = cv2.imread(f'faces/{i}.jpg')
    tmp = app.get(img)
    vec = tmp[0].embedding
    faces.append(vec)

def match(vec):
    ans = [0, -1]
    for i in range(len(faces)):
        if cos_sim(vec, faces[i]) > ans[1]:
            ans = [i, cos_sim(vec, faces[i])]
    if ans[1] > 0.5:
        return ans[0]
    else:
        return -1

capture = cv2.VideoCapture(0)

while True:
    ret, flame = capture.read()

    if(ret == False):
        break

    embs = app.get(flame)

    for emb in embs:
        vec = emb.embedding
        m = match(vec)
        if m != -1:
            db.write(m, int(time.time()))
            print(m, int(time.time()))

    detect = app.draw_on(flame, embs)
    cv2.imshow("flame", detect)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break