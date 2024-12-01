import os
import random
from dataset_downloader import DatasetDownloader
from image_analyzer import ImageAnalyzer
from mosaic import Mosaic

def get_datasets():
    """
    get list of downloaded datasets

    returns: 
        list: list of dicts, where each dictionary contains:
            - "name" (str): name of the dataset (subdirectory name in datasets folder).
            - "image_count" (int): number of image files in the "images" subdirectory.
    
    """
    datasets = []
    datasets_dir = "datasets"
    if os.path.exists(datasets_dir):
        for dataset in os.listdir(datasets_dir):
            if os.path.isdir(os.path.join(datasets_dir, dataset)):
                img_count = len(os.listdir(os.path.join(datasets_dir, dataset, "images")))
                datasets.append({"name": dataset, "image_count": img_count})
    return datasets

def get_random_image(dataset_name):
    """
    get random image path from dataset

    args:
        dataset_name (str): dataset subfolder name
    
    returns:
        str: path to randomly selected image
    """
    images_dir = os.path.join("datasets", dataset_name, "images")
    images = os.listdir(images_dir)
    random_image = random.choice(images)
    return os.path.join(images_dir, random_image)

def main():
    downloader = DatasetDownloader()
    analyzer = ImageAnalyzer()

    while True:

        print("\n=== Welcome to Mosaic Anything ===")
        print("Create beautiful mosaics from images!\n")
        
        # show available datasets
        datasets = get_datasets()
        if datasets:
            print("Downloaded datasets:")
            for i, dataset in enumerate(datasets, 1):
                print(f"{i}. {dataset['name']} ({dataset['image_count']} images)")
        else:
            print("No datasets found.")
        
        print("\nYou can either:")
        print("Select an existing dataset (enter the number) or,")
        print("Download a new dataset (paste Kaggle URL)")
        choice = input("\nDataset selection: ").strip()
        
        dataset_name = None
        if choice.isdigit() and 1 <= int(choice) <= len(datasets):
            dataset_name = datasets[int(choice)-1]["name"]
        else:
            # assume kaggle url
            is_duplicate, dataset_name, img_count = downloader.duplicate_check(choice)
            if not is_duplicate:
                print("\nDownloading dataset...")
                downloader.download_dataset(choice)
                print("Analyzing images...")
                analyzer.analyze_dataset(dataset_name)
            else:
                print(f"\nDataset {dataset_name} already exists with {img_count} images.")

        print(f"Selected '{dataset_name}' dataset.")
        
        # get target image
        print("\nEnter image path (or press Enter for random image from dataset):")
        image_path = input().strip()
        if not image_path:
            image_path = get_random_image(dataset_name)
            print(f"Using random image: {image_path}")
        
        # get mosaic params
        try:
            output_width = input("\nEnter output width in tiles (default: 100): ").strip()
            output_width = int(output_width) if output_width else 100
            
            mosaic_size = input("Enter mosaic tile size in pixels (default: 32): ").strip()
            mosaic_size = int(mosaic_size) if mosaic_size else 32
        except ValueError:
            print("Invalid input, using default values.")
            output_width = 100
            mosaic_size = 32
        
        # create mosaic
        avg_colors_csv = os.path.join("datasets", dataset_name, "analysis", "center_crop_avg_colors.csv")
        
        mosaic_creator = Mosaic(
            avg_colors_csv=avg_colors_csv,
            target_image_path=image_path,
            output_width=output_width,
            mosaic_image_size=mosaic_size
        )
        
        output_path = "output_mosaic.jpg"
        mosaic_creator.create_mosaic(output_path)
        print(f"\nMosaic created successfully!")
        print(f"Output saved to: {os.path.abspath(output_path)}")

        restart_prog = input("Would you like to create another mosaic? [Y/N]: ")

        if restart_prog.lower() != "y" and restart_prog.lower() != "yes":
            break

if __name__ == "__main__":
    main() 