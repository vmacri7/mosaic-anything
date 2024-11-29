from dataset_downloader import DatasetDownloader

def main():
    downloader = DatasetDownloader()
    
    dataset_url = "https://www.kaggle.com/datasets/sayehkargari/disney-characters-dataset"
    is_duplicate, dataset_name, img_count = downloader.duplicate_check(dataset_url)
    if is_duplicate:
        print(f"Dataset {dataset_name} was found in the dataset folder with {img_count} images.")
    else:
        downloader.download_dataset(dataset_url)
    

if __name__ == "__main__":
    main() 