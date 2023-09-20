import numpy as np
import cv2
from insightface.app import FaceAnalysis
import db
import time
import os

app = FaceAnalysis()
app.prepare(ctx_id=1, det_size=(640, 640))

def cos_sim(feat1, feat2):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))

faces_dir = './faces'
folders = {}
with os.scandir(faces_dir) as fs:
    for entry in fs:
        if entry.is_dir():
            folders[entry.name] = []
            with os.scandir(faces_dir+'/'+entry.name) as folder:
                for face in folder:
                    img = cv2.imread(faces_dir+'/'+entry.name+'/'+face.name)
                    tmp = app.get(img)
                    vec = tmp[0].embedding
                    folders[entry.name].append(vec)

def match(vec):
    ans = [0, -1]
    for name, faces in folders.items():
        for face in faces:
            if cos_sim(vec, face) > ans[1]:
                ans = [name, cos_sim(vec, face)]
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