import cv2
import numpy as np
from PIL import Image, ImageChops

class ImageQualityChecker:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError("Image not found or invalid image path.")
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def trim(self, img):
        im = img
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    def has_border(self):
        img = Image.open(self.image_path)
        if img.size[0] == img.size[1]:
            img = self.trim(img)
        return img.size[0] != img.size[1]

    def is_blurry(self, threshold=300):
        laplacian_var = cv2.Laplacian(self.gray_image, cv2.CV_64F).var()
        print('blurriness:', laplacian_var)
        return laplacian_var < threshold
    
    def is_low_sharpness(self, threshold=0.75):
        edges = cv2.Canny(self.gray_image, 100, 200)
        edge_density = np.sum(edges) / (edges.shape[0] * edges.shape[1])
        print('sharpness:', edge_density)
        return edge_density < threshold

    def is_low_resolution(self, min_width=800, min_height=600):
        height, width = self.image.shape[:2]
        print('resolution:', width, height)
        return width < min_width or height < min_height
    
    def is_square_image(self):
        height, width = self.image.shape[:2]
        return height == width

    def check_quality(self):
        results = {
            "has_border": self.has_border(),
            "is_blurry": self.is_blurry(),
            "is_low_sharpness": self.is_low_sharpness(),
            "is_low_resolution": self.is_low_resolution(),
            "is_square_image": self.is_square_image(),
        }
        return results