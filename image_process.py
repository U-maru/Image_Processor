from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import shutil

from Processor.GrayScale import GrayScaleProcessor
from Processor.Binary import BinaryProcessor
from Processor.Mozaiku import MozaikuProcessor

class ImageProcessor():

    img_dir_path_list = [
        "./upload_images",
        "./output_images/bin",
        "./output_images/gs",
        "./output_images/mozaiku"
    ]

    def process(self, path):
        GrayScaleProcessor().process(path)
        BinaryProcessor().process(path)
        MozaikuProcessor().process(path)

    def delete_images(self):
        for dir in self.img_dir_path_list:
            shutil.rmtree(dir)
            os.mkdir(dir)