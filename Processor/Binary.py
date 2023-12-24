import os
import cv2

from Processor.ProcessorBase import ProcessorBase

class BinaryProcessor(ProcessorBase):

    OUT_DIR = "./output_images/bin/"

    def process(self, filepath):
        out_filename = os.path.basename(filepath)
        img_bgr = cv2.imread(filepath)
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        ret, img_bin = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY)

        cv2.imwrite(self.OUT_DIR + out_filename, img_bin)