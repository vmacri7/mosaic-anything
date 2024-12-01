import os
import cv2
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
from tqdm import tqdm
from PIL import Image
import pillow_heif

class Mosaic:
    def __init__(self, avg_colors_csv: str, target_image_path: str, output_width: int, mosaic_image_size: int):
        """
        initialize mosaic creator.
        
        args:
            avg_colors_csv (str): path to csv containing image names and their average rgb values
            target_image_path (str): path to the image to create a mosaic of
            output_width (int): desired width of the output mosaic in number of source images
            mosaic_image_size (int): size of each image tile in the mosaic (will be resized and center cropped to this size)
        """
        self.mosaic_image_size = mosaic_image_size
        self.output_width = output_width
        self.target_image = self._read_image(target_image_path)
        if self.target_image is None:
            raise ValueError(f"could not read target image: {target_image_path}")
            
        # calculate output dims maintaining aspect ratio
        target_height, target_width = self.target_image.shape[:2]
        self.output_height = int(round((target_height / target_width) * output_width))
        
        # read avg colors data and setup k-d tree for color matching
        self._setup_color_matching(avg_colors_csv)
        
    def _setup_color_matching(self, avg_colors_csv: str):
        """
        setup the color matching system using a k-d tree.
        """
        self.color_data = pd.read_csv(avg_colors_csv)
        
        # convert to np array for k-d tree
        self.colors = self.color_data[['r', 'g', 'b']].values
        
        # create k-d tree for efficient nearest neighbor search
        self.color_tree = cKDTree(self.colors)
        
        # store base path
        self.source_images_path = os.path.join(os.path.dirname(avg_colors_csv), "..", "images")
        
    def _get_best_match_image(self, target_color):
        """
        find the image with the closest average color to the target color.
        
        args:
            target_color (np.array): rgb color to match
            
        returns:
            str: path to the best matching image
        """
        # find nearest neighbor in color space using k-d tree
        _, idx = self.color_tree.query(target_color)
        
        # get corresponding image name
        image_name = self.color_data.iloc[idx]['image_name']
        return os.path.join(self.source_images_path, image_name)
    
    def _get_center_crop(self, image_path: str) -> np.ndarray:
        """
        read and center crop an image to the mosaic tile size.
        """
        img = cv2.imread(image_path)
        if img is None:
            # return solid color if image can't be read
            return np.zeros((self.mosaic_image_size, self.mosaic_image_size, 3))
            
        # center crop
        h, w = img.shape[:2]
        crop_size = min(h, w)
        start_y = (h - crop_size) // 2
        start_x = (w - crop_size) // 2
        crop = img[start_y:start_y + crop_size, start_x:start_x + crop_size]
        
        # resize to mosaic tile size
        return cv2.resize(crop, (self.mosaic_image_size, self.mosaic_image_size))
    

    def _read_image(self, image_path: str) -> np.ndarray:
        """
        read an image file in various formats.
        
        args:
            image_path (str): path to the image file
            
        returns:
            np.ndarray: image in BGR format for opencv compatibility
        """
        # get file extension
        ext = os.path.splitext(image_path)[1].lower()
        
        try:
            if ext in ['.heic', '.heif']:
                # register heif opener
                pillow_heif.register_heif_opener()
                
                # open heic image
                with Image.open(image_path) as img:
                    img = img.convert('RGB')
                    img_array = np.array(img)
                    return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                # try opencv first
                img = cv2.imread(image_path)
                if img is not None:
                    return img
                    
                # if opencv fails, try PIL
                try:
                    with Image.open(image_path) as img:
                        img = img.convert('RGB')
                        img_array = np.array(img)
                        return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                except Exception as e:
                    print(f"error reading image with PIL: {e}")
                    return None
                    
        except Exception as e:
            print(f"error reading image: {e}")
            return None


    
    def create_mosaic(self, output_path: str = None):
        """
        create the mosaic image.
        
        args:
            output_path (str, optional): path to save the output image. if none, just returns the array
            
        returns:
            np.ndarray: the created mosaic image
        """
        # resize target image to desired dimensions
        target_resized = cv2.resize(self.target_image, (self.output_width, self.output_height))
        
        # create output array
        output_shape = (
            self.output_height * self.mosaic_image_size,
            self.output_width * self.mosaic_image_size,
            3
        )
        mosaic = np.zeros(output_shape, dtype=np.uint8)
        
        print("creating mosaic...")
        # iterate over each cell in the grid
        for y in tqdm(range(self.output_height)):
            for x in range(self.output_width):
                # get target color for this cell
                target_color = target_resized[y, x]
                # convert BGR to RGB 
                target_color = target_color[::-1]
                
                # find best matching image
                best_match = self._get_best_match_image(target_color)
                
                # get center cropped and resized image
                tile = self._get_center_crop(best_match)
                
                # calculate pos in output array
                y_start = y * self.mosaic_image_size
                y_end = (y + 1) * self.mosaic_image_size
                x_start = x * self.mosaic_image_size
                x_end = (x + 1) * self.mosaic_image_size
                
                # place tile in output array
                mosaic[y_start:y_end, x_start:x_end] = tile
        
        if output_path:
            cv2.imwrite(output_path, mosaic)
            
        return mosaic