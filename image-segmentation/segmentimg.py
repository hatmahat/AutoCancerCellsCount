import cv2 as cv
import os

# fitur tambahan untuk kerjaan ke depan --> batch_size (in case resolusi tinggi)
# docstrings are not updated yet
class SegmentImg:
    """Image segmentation for Acute Lymphoblastic Leukemia L1
       coded by Mahatma Wisesa

    Parameters
    ------------
    ROOT_DIR : str
               Root directory.
    child : str
            Raw images folder directory.
    """
    def __init__(self, ROOT_DIR, child):
        self.ROOT_DIR = ROOT_DIR
        self.child = self.ROOT_DIR+f"\\{child}"
        self.img_names = [] # nama gambar yg ada di folder
        
        self.img_dict = {} # nama gambar sama arraynya
        self.img_dict_rescaled = {} 
        self.img_hist_eq_dict = {} 
        self.img_bilateral_dict = {}
        self.thresh_inv_green = {}
        self.img_masked = {}
        self.thresh_inv_gray = {}

    def get_img_dict(self):
        """
        Returns
        ------------
        self.img_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                        Dictionary of images with their original names.
        """
        return self.img_dict

    def get_img_dict_rescaled(self):
        """
        Returns
        ------------
        self.img_dict_rescaled : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                                 Dictionary of rescaled images with their original names.
        """
        return self.img_dict_rescaled

    def get_img_hist_eq_dict(self):
        """
        Returns
        ------------
        self.img_hist_eq_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                                Dictionary of hist equalization images with their original names.
        """
        return self.img_hist_eq_dict

    def get_bilateral_dict(self):
        """
        Returns
        ------------
        self.img_bilateral_dict : dict, {"IMG_NAME": <class 'numpy.ndarray'>}
                                  Dictionary of bilateral blur images with their original names.
        """
        return self.img_bilateral_dict

    def read_all_img(self):
        """Create dictionary of images.
        """
        self.img_names = [img_name for img_name in os.listdir(self.child)]
        if len(self.img_names) == 0:
            raise IndexError("Folder is empty brother!")
        self.img_dict = {
            img_name.replace(".jpg", ""):cv.imread(self.child+f"\\{img_name}") for img_name in self.img_names
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
        os.chdir(self.ROOT_DIR+f"\{saved_folder}")
        for img_name, img in read_dict.items():
            cv.imwrite(f"{img_name} {addition_name}.jpg", img)
        print("Image saved.")
        os.chdir(self.ROOT_DIR)
        #print("Back to ROOT_DIR")
        print("Everything is OK.")

    def rescale_all(self, scale=0.2): # belum ada count
        """Rescale all images in self.img_dict

        Parameters
        ------------
        scale : float 
                Rescale image from 0 to 1 times.
        """
        def rescale(frame, scale):
            width = int(frame.shape[1]*scale)
            height = int(frame.shape[0]*scale)
            dimensions = (width, height)
            return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)
        
        count = 1
        dict_len = len(self.img_dict.items())
        for img_name, img in self.img_dict.items(): # karena ada ".jpg" di nama makannya -4
            #img_name = img_name.replace(".jpg", "")
            self.img_dict_rescaled[img_name] = rescale(img, scale)
            print(f'Rescale Processed: {count}/{dict_len}')
            count += 1

    def save_rescaled_all(self, saved_folder, addition_name='(rescaled)'):
        """Save images from img_dict_rescaled to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        addition_name : str
                        Additional name for file name.
        """
        self.save(saved_folder, f'{addition_name}', self.img_dict_rescaled)

    def hist_equal_all(self, on='rescaled_dict'):
        """Histogram equalization.
        
        Parameters
        ------------
        on  : str            
              'rescaled_dict' iterate over self.img_dict_rescaled
              'org_dict' iterate over self.img_dict
        """
        def hist_equal(read_dict):
            count = 1
            dict_len = len(read_dict.items())
            for img_name, img in read_dict.items():
                #img_name = img_name.replace(".jpg", "")
                self.img_hist_eq_dict[img_name] = cv.cvtColor(img, cv.COLOR_BGR2YUV)
                self.img_hist_eq_dict[img_name][:,:,0] = cv.equalizeHist(self.img_hist_eq_dict[img_name][:,:,0])
                self.img_hist_eq_dict[img_name] = cv.cvtColor(self.img_hist_eq_dict[img_name], cv.COLOR_YUV2BGR)
                print(f'Hist Equal Processed: {count}/{dict_len}')
                count += 1

        if on == 'rescaled_dict':
            # make rescaled
            hist_equal(self.img_dict_rescaled)
        elif on == 'org_dict':
            # make gambar ori
            hist_equal(self.img_dict)
        else:
            raise ValueError('The argument is not defined!')

    def save_hist_equal_all(self, saved_folder, addition_name='(hist equal)'):
        """Save images from img_hist_eq_dict to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        addition_name : str
                        Additional name for file name.
        """
        self.save(saved_folder, f'{addition_name}', self.img_hist_eq_dict)

    def bilateral_all(self, on='org_dict'):
        """Histogram equalization.
        
        Parameters
        ------------
        on : str
            'hist_equal_dict' iterate over self.img_hist_eq_dict
            'rescaled_dict' iterate over self.img_dict_rescaled
            'org_dict' iterate over self.img_dict
        """
        def bilateralFilter(read_dict):
            count = 1
            dict_len = len(read_dict.items())
            for img_name, img in read_dict.items():
                self.img_bilateral_dict[img_name] = cv.bilateralFilter(img, 25, 75, 75) #cv.bilateralFilter(img, 10, 50, 50)
                print(f'Bilateral Filter Processed: {count}/{dict_len}')
                count += 1

        if on == 'hist_equal_dict':
            bilateralFilter(self.img_hist_eq_dict)
        elif on == 'rescaled_dict':
            bilateralFilter(self.img_dict_rescaled)
        elif on == 'org_dict':
            bilateralFilter(self.img_dict)
        else:
            raise ValueError('The argument is not defined!')

    def save_bilateral_all(self, saved_folder, addition_name='(bilateral blur)'):
        """Save images from img_bilateral_dict to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        addition_name : str
                        Additional name for file name.
        """
        self.save(saved_folder, f'{addition_name}', self.img_bilateral_dict)

    def thresh_green_chan_all(self, on='org_dict'):
        """Thresholding on the Green Channel.
        
        Parameters
        ------------
        on : str
            'hist_equal_dict' iterate over self.img_hist_eq_dict
            'rescaled_dict' iterate over self.img_dict_rescaled
            'org_dict' iterate over self.img_dict
            'bilateral_dict' iterate over self.img_bilateral_dict
        """
        def thresh_green_chan(read_dict):
            count = 1
            dict_len = len(read_dict.items())
            for img_name, img in read_dict.items():
                b, g, r = cv.split(img)
                ret, thresh_inv_green = cv.threshold(g, 100, 255, cv.THRESH_BINARY_INV)
                self.thresh_inv_green[img_name] = thresh_inv_green
                print(f'Green Thresh Processed: {count}/{dict_len}')
                count += 1

        if on == 'hist_equal_dict':
            thresh_green_chan(self.img_hist_eq_dict)
        elif on == 'rescaled_dict':
            thresh_green_chan(self.img_dict_rescaled)
        elif on == 'org_dict':
            thresh_green_chan(self.img_dict)
        elif on == 'bilateral_dict':
            thresh_green_chan(self.img_bilateral_dict)
        else:
            raise ValueError('The argument is not defined!')

    def save_thresh_green_chan_all(self, saved_folder, addition_name='(thresh green)'):
        """Save images from thresh_inv_green to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        addition_name : str
                        Additional name for file name.
        """
        self.save(saved_folder, f'{addition_name}', self.thresh_inv_green)

    def thresh_gray_all(self, on='org_dict'):
        """Thresholding on the Gray.
        
        Parameters
        ------------
        on : str
            'hist_equal_dict' iterate over self.img_hist_eq_dict
            'rescaled_dict' iterate over self.img_dict_rescaled
            'org_dict' iterate over self.img_dict
            'bilateral_dict' iterate over self.img_bilateral_dict
        """
        def gray(read_dict):
            count = 1
            dict_len = len(read_dict.items())
            for img_name, img in read_dict.items():
                gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                ret, thresh_inv_gray = cv.threshold(gray, 110, 255, cv.THRESH_BINARY_INV)
                self.thresh_inv_gray[img_name] = thresh_inv_gray
                print(f'Gray Thresh Processed: {count}/{dict_len}')
                count += 1

        if on == 'hist_equal_dict':
            gray(self.img_hist_eq_dict)
        elif on == 'rescaled_dict':
            gray(self.img_dict_rescaled)
        elif on == 'org_dict':
            gray(self.img_dict)
        elif on == 'bilateral_dict':
            gray(self.img_bilateral_dict)
        else:
            raise ValueError('The argument is no defined!')

    def save_thresh_gray(self, saved_folder, addition_name='(thresh gray)'):
        """Save images from thresh_inv_gray to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        addition_name : str
                        Additional name for file name.
        """
        self.save(saved_folder, f'{addition_name}', self.thresh_inv_gray)

    def masked_all(self, on='thresh_inv_green', mask='org_dict'): # perbaiki masik make rescaled dict
        """Masking Thresholded imag to original image.
        
        Parameters
        ------------
        on : str
            'hist_equal_dict' iterate over self.img_hist_eq_dict
            'rescaled_dict' iterate over self.img_dict_rescaled
            'org_dict' iterate over self.img_dict
            'bilateral_dict' iterate over self.img_bilateral_dict
            'thresh_inv_green' iterate over self.thresh_inv_green
        mask : str
               'org_dict' mask on self.img_dict
               'rescaled_dict' mask on self.img_dict_rescaled
        """
        def masked(read_dict, mask_dict):
            count = 1
            dict_len = len(read_dict.items())
            for img_name, img in read_dict.items():
                masked_hist = cv.bitwise_and(
                    mask_dict[img_name], mask_dict[img_name], mask=img
                    )
                self.img_masked[img_name] = masked_hist
                print(f'Masked Processed: {count}/{dict_len}')
                count += 1

        if mask == 'org_dict':
            mask = self.img_dict
        elif mask == 'rescaled_dict':
            mask = self.img_dict_rescaled
        else:
            raise ValueError('The argument is not defined!')

        if on == 'thresh_inv_green':
            masked(self.thresh_inv_green, mask)
        elif on == 'thresh_inv_gray':
            masked(self.thresh_inv_gray, mask)
        else:
            raise ValueError('The argument is not defined!')

    def save_masked_all(self, saved_folder, addition_name='(masked)'):
        """Save images from img_masked to the "saved_folder" folder.

        Parameters
        ------------
        saved_folder : str
                       Name of the new folder where images will be saved.
        addition_name : str
                        Additional name for file name.
        """
        self.save(saved_folder, f'{addition_name}', self.img_masked)