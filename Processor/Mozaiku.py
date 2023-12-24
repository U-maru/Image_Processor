import os
import cv2

from Processor.ProcessorBase import ProcessorBase

class MozaikuProcessor(ProcessorBase):

    OUT_DIR = "./output_images/mozaiku/"

    def process(self, filepath):
        out_filename = os.path.basename(filepath)
        img_bgr = cv2.imread(filepath)

        # Haar Cascade 分類器の読み込み
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 顔検出
        faces = face_cascade.detectMultiScale(img_bgr, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        count = 0 #モザイクありなら1,なければ0
        # 検出された顔にモザイクを適用
        for (x, y, w, h) in faces:
            if(count == 0):
                count = 1
            # 顔領域の切り抜き
            face_roi = img_bgr[y:y+h, x:x+w]

            # 顔領域にモザイクを適用
            face_roi = cv2.GaussianBlur(face_roi, (99, 99), 30)
            img_bgr[y:y+h, x:x+w] = face_roi
        
        cv2.imwrite(self.OUT_DIR + out_filename, img_bgr)