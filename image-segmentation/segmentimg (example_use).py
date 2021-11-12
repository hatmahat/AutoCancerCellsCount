import segmentimg as simg
import os

# Example use of segmentation
def use_rescale(func):
    def wrapper(use_rescale):
        global base_dict
        if use_rescale:
            base_dict = 'rescaled_dict'
        else:
            base_dict = 'org_dict'
        print("######## RUNNING ########")
        func(use_rescale)
        print("########## DONE ##########")
    return wrapper

def mkdir(ROOT_DIR, DIR):
    if not os.path.exists(ROOT_DIR + DIR):
        os.makedirs(ROOT_DIR + DIR)

@use_rescale
def with_cyto(use_rescale=False):
    dirr = r"\processed\histeq (with cyto)"
    mkdir(ROOT_DIR, dirr)
    img.hist_equal_all(on=base_dict)
    img.save_hist_equal_all(dirr, "(Histogram Equal WC)")

    dirr = r"\processed\bilateral (with cyto)"
    mkdir(ROOT_DIR, dirr)
    img.bilateral_all(on='hist_equal_dict')
    img.save_bilateral_all(dirr, "(Bilateral Blur WC)")

    dirr = r"\processed\thresh green (with cyto)"
    mkdir(ROOT_DIR, dirr)
    img.thresh_green_chan_all(on='bilateral_dict')
    img.save_thresh_green_chan_all(dirr, "(Threshold Green WC)")

    dirr = r"\processed\masked (with cyto)"
    mkdir(ROOT_DIR, dirr)
    img.masked_all(on='thresh_inv_green', mask=base_dict) # ukuran harus sesuai dari thresh
    img.save_masked_all(dirr, "(Masked WC)")

@use_rescale
def with_no_cyto(use_rescale=False):
    dirr = r"\processed\bilateral (no cyto)"
    mkdir(ROOT_DIR, dirr)
    img.bilateral_all(on=base_dict)
    img.save_bilateral_all(dirr, "(Bilateral Blur WNC)")
    
    dirr = r"\processed\thresh gray (no cyto)"
    mkdir(ROOT_DIR, dirr)
    img.thresh_gray_all(on='bilateral_dict')
    img.save_thresh_gray(dirr, "(Threshold Gray WNC)")

    dirr = r"\processed\masked (no cyto)"
    mkdir(ROOT_DIR, dirr)
    img.masked_all(on='thresh_inv_gray', mask=base_dict)
    img.save_masked_all(dirr, "(Masked WNC)")

def main():
    global img
    global ROOT_DIR
    global DATASET_DIR
    ROOT_DIR = r"D:\White Blood Cells  RSUP Sardjito - Copy\working data 2\final dataset\train-val-test - Copy (2)"
    DATASET_DIR = r"test-v2"
    
    img = simg.SegmentImg(ROOT_DIR, DATASET_DIR)
    print("accessing...")
    img.read_all_img()
    
    # dirr = r"\processed\.rescale"
    # mkdir(ROOT_DIR, dirr)
    # img.rescale_all()
    # img.save_rescaled_all(dirr)

    with_cyto(use_rescale=False) # with cytoplasm
    with_no_cyto(use_rescale=False) # with no cytoplasm, only nucleus

if __name__ == '__main__':
    main()