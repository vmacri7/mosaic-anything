import os
from dataset_downloader import DatasetDownloader
from image_analyzer import ImageAnalyzer
from mosaic import Mosaic

def main():
    downloader = DatasetDownloader()
    analyzer = ImageAnalyzer()
    
    # dataset_url = "https://www.kaggle.com/datasets/sayehkargari/disney-characters-dataset"
    # dataset_url = "https://www.kaggle.com/datasets/splcher/animefacedataset"
    # dataset_url = "https://www.kaggle.com/datasets/andrewmvd/animal-faces"
    dataset_url = "https://www.kaggle.com/datasets/phucthaiv02/butterfly-image-classification"

    is_duplicate, dataset_name, img_count = downloader.duplicate_check(dataset_url)
    if is_duplicate:
        print(f"Dataset {dataset_name} was found in the dataset folder with {img_count} images.")
    else:
        downloader.download_dataset(dataset_url)
    
    avg_colors_csv_path = os.path.join("datasets",dataset_name,"analysis","center_crop_avg_colors.csv")
    # determine and save avg pixel values for each image and save to csv
    if not os.path.exists(os.path.join("datasets",dataset_name,"analysis","center_crop_avg_colors.csv")):
        avg_colors_csv_path = analyzer.analyze_dataset(dataset_name)

    # initialize mosaic
    mosaic_creator = Mosaic(
        avg_colors_csv=avg_colors_csv_path,
        target_image_path="",
        output_width=64,  
        mosaic_image_size=32 
    )

    # create and save the mosaic
    mosaic_creator.create_mosaic("output_mosaic.jpg")

if __name__ == "__main__":
    main() 