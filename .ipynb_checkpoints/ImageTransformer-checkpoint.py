import os
import cv2
from PIL import Image

from utils import *
from matplotlib.pyplot import imread

class ImageTransformer():
    
    def __init__(self, experiment_path):
        
        self.experiment_path = experiment_path


    def crop_images(self):
        
        for label in os.listdir(self.experiment_path)[:2]:
            label_path = self.experiment_path + '/' + label

            for image in os.listdir(label_path):
                image_content = imread(label_path + '/' + image)
                height, width, channels = image_content.shape
                # [ height, width, channels ]
                image_content = image_content[80:490, 110:630,  :]
                im = Image.fromarray(image_content)
                im.save(f'{label_path}/{image}')
                

