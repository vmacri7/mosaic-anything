from dataset_downloader import DatasetDownloader
from image_analyzer import ImageAnalyzer

def main():
    downloader = DatasetDownloader()
    analyzer = ImageAnalyzer()
    
    dataset_url = "https://www.kaggle.com/datasets/sayehkargari/disney-characters-dataset"
    # dataset_url = "https://www.kaggle.com/datasets/splcher/animefacedataset"
    # dataset_url = "https://www.kaggle.com/datasets/andrewmvd/animal-faces"

    is_duplicate, dataset_name, img_count = downloader.duplicate_check(dataset_url)
    if is_duplicate:
        print(f"Dataset {dataset_name} was found in the dataset folder with {img_count} images.")
    else:
        downloader.download_dataset(dataset_url)
    
    # determine and save avg pixel values for each image and save to csv
    analyzer.analyze_dataset(dataset_name)

if __name__ == "__main__":
    main() 