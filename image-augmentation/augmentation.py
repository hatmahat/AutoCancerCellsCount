"""
Image Augmentation for Acute Lymphoblastic Leukemia L1
Written by Mahatma Wisesa
"""

import cv2 as cv
import os

class Augmentation:

    def __init__(self, ROOT_DIR, DATASET_DIR):
        self.ROOT_DIR = ROOT_DIR
        self.DATASET_DIR = self.ROOT_DIR+f"\\{DATASET_DIR}"

        self.IMG_NAMES = []
        self.IMG_DICT = {}

        self.VER_FLIP = {}
        self.HOR_FLIP = {}
        self.VERHOR_FLIP = {}

    def read_all_img(self):
        """Create dictionary of images.
        """
        self.IMG_NAMES = [
            img_name for img_name in os.listdir(self.DATASET_DIR)
        ]
        if len(self.IMG_NAMES) == 0:
            raise IndexError("Folder is empty brother!")
        self.IMG_DICT = {
            img_name.replace(".jpg", ""):cv.imread(
                self.DATASET_DIR+f"\\{img_name}"
                ) for img_name in self.IMG_NAMES
        }

    def save(self, saved_folder, addition_name, read_dict):
        """(internal use only) Save images to "saved_folder" with addition_name.
        
        Parameters
        ------------
        saved_folder : str
                       Name of the folder to save.
        addition_name : str
                        Addition name to the image name
        read_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                    Dictionary to be saved as images
        """
        os.chdir(self.ROOT_DIR + saved_folder)
        for img_name, img in read_dict.items():
            cv.imwrite(f"{addition_name}{img_name}.jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        print("Everything is OK.")

    def flip_aug(self, flip_type="ver-hor"):
        """
        Parameters
        ------------
        flip_type : str
                    "ver-hor" -> vertical and horizontal flip
                    "horizontal" -> horizontal flip
                    "vertical" -> vertical flip
        """
        def flip_aug_run(FLIP_DICT, flipCode):
            for img_name, img in self.IMG_DICT.items():
                FLIP_DICT[img_name] = cv.flip(img, flipCode)

        if flip_type == "ver-hor":
            flip_aug_run(self.VERHOR_FLIP, -1)
        elif flip_type == "horizontal":
            flip_aug_run(self.HOR_FLIP, 1)
        elif flip_type == "vertical":
            flip_aug_run(self.VER_FLIP, 0)
        else:
            raise ValueError("The argument is not defined!")
             
    def save_flip(self, flip_type, saved_folder, addition_name):
        """
        Parameters
        ------------
        flip_type : str
                    "ver-hor" -> vertical and horizontal flip
                    "horizontal" -> horizontal flip
                    "vertical" -> vertical flip
        saved_folder : folder dictionary
        addition_name : addition file name
        """
        if flip_type == "ver-hor":
            self.save(saved_folder, addition_name, self.VERHOR_FLIP)
        elif flip_type == "horizontal":
            self.save(saved_folder, addition_name, self.HOR_FLIP)
        elif flip_type == "vertical":
            self.save(saved_folder, addition_name, self.VER_FLIP)
        else:
            raise ValueError("The argument is not defined!")
