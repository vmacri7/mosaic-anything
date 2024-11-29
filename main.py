from dataset_downloader import DatasetDownloader

def main():
    downloader = DatasetDownloader()
    
    dataset_url = "https://www.kaggle.com/datasets/splcher/animefacedataset"
    print(f"Downloading dataset: {dataset_url}")
    downloader.download_dataset(dataset_url)
    

if __name__ == "__main__":
    main() 