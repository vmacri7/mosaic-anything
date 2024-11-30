import os
import cv2
import multiprocessing
from tqdm import tqdm
import csv

class ImageAnalyzer:
    def __init__(self, dataset_path: str = "datasets"):
        """
        initialize the image analyzer.
        
        args:
            dataset_path (str): base directory containing datasets
        """
        self.dataset_path = dataset_path
        self.n_workers = multiprocessing.cpu_count()
        self.image_extensions = ('.jpg')  # what counts as an "image", setting to jpg for now to avoid alhpa channels
    
    def _get_center_crop_avg_color(self, image_path: str) -> tuple:
        """
        calculate the average color of the center square crop of an image.
        
        args:
            image_path (str): path to the image file
            
        returns:
            tuple: (image_name, (r, g, b)) or (image_name, None) if error
        """
        try:
            # read image in BGR format
            img = cv2.imread(image_path)
            if img is None:
                return os.path.basename(image_path), None
            
            # get dimensions
            h, w = img.shape[:2]
            crop_size = min(h, w)
            
            # calculate crop coords
            start_y = (h - crop_size) // 2
            start_x = (w - crop_size) // 2
            
            # get center crop
            crop = img[start_y:start_y + crop_size, start_x:start_x + crop_size]
            
            # calculate average color (returns in BGR)
            avg_color = cv2.mean(crop)[:3]
            
            # convert BGR to RGB and return as ints
            rgb = tuple(int(c) for c in avg_color[::-1])
            return os.path.basename(image_path), rgb
            
        except Exception as e:
            print(f"error processing {image_path}: {e}")
            return os.path.basename(image_path), None
    
    def analyze_dataset(self, dataset_name: str) -> str:
        """
        analyze all images in a dataset and generate a csv with average rgb values
        of center square crops.
        
        args:
            dataset_name (str): name of the dataset folder
            
        returns:
            str: path to the generated csv file
        """
        # get path to images
        dataset_dir = os.path.join(self.dataset_path, dataset_name, "images")
        if not os.path.exists(dataset_dir):
            raise ValueError(f"dataset directory not found: {dataset_dir}")
        
        # get list of image files
        image_files = [
            os.path.join(dataset_dir, f)
            for f in os.listdir(dataset_dir)
            if f.lower().endswith(self.image_extensions)
        ]
        
        print(f"analyzing {len(image_files)} images in {dataset_name}...")
        
        ctx = multiprocessing.get_context('spawn')
        with ctx.Pool(processes=self.n_workers) as pool:
            try:
                results = list(tqdm(
                    pool.imap(self._get_center_crop_avg_color, image_files),
                    total=len(image_files),
                    desc="Processing images"
                ))
            finally:
                pool.close()
                pool.join()
        
        analysis_dir = os.path.join(self.dataset_path, dataset_name, "analysis")
        os.makedirs(analysis_dir, exist_ok=True)
        
        # save results
        output_file = os.path.join(analysis_dir, "center_crop_avg_colors.csv")
        with open(output_file, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["image_name", "r", "g", "b"])
            
            for img_name, color in results:
                if color: 
                    csvwriter.writerow([img_name, *color])
        
        print(f"analysis complete!! results saved to: {output_file}")
        return output_file 