from augmentation import *

ROOT_DIR = r"D:\White Blood Cells  RSUP Sardjito - Copy\working data 2\final dataset\train-val-test\train"
DATASET_DIR = r"single non-B"
aug = Augmentation(ROOT_DIR, DATASET_DIR)
aug.read_all_img()

aug.flip_aug(flip_type='vertical')
aug.save_flip('vertical', r'\agumentation', "V.")

aug.flip_aug(flip_type='horizontal')
aug.save_flip('horizontal', r'\agumentation', "H.")

aug.flip_aug(flip_type='ver-hor')
aug.save_flip('ver-hor', r'\agumentation', "VH.")