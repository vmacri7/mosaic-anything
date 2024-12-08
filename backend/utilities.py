import os
import random

def get_datasets(datasets_dir: str = "datasets"):
    datasets = []
    if os.path.exists(datasets_dir):
        for dataset in os.listdir(datasets_dir):
            dataset_path = os.path.join(datasets_dir, dataset)
            images_path = os.path.join(dataset_path, "images")
            if os.path.isdir(dataset_path) and os.path.isdir(images_path):
                img_count = len(os.listdir(images_path))
                datasets.append({"name": dataset, "image_count": img_count})
    return datasets

def get_random_image(dataset_name: str, datasets_dir: str = "datasets"):
    images_dir = os.path.join(datasets_dir, dataset_name, "images")
    images = os.listdir(images_dir)
    if not images:
        raise ValueError(f"No images found in dataset: {dataset_name}")
    random_image = random.choice(images)
    return os.path.join(images_dir, random_image)
