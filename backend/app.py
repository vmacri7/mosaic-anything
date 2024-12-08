from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from utilities import get_datasets, get_random_image
from dataset_downloader import DatasetDownloader
from image_analyzer import ImageAnalyzer
from mosaic import Mosaic
from typing import Optional, Dict
import json
import time

app = FastAPI()

# configure cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# configure upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# initialize components
downloader = DatasetDownloader()
analyzer = ImageAnalyzer()

@app.get("/")
async def index():
    return {"message": "Welcome to the Mosaic Creator API"}

@app.get("/datasets")
async def list_datasets():
    datasets = get_datasets()
    return {"data": datasets}

@app.get("/datasets/{dataset_name}/random")
async def get_random_dataset_image(dataset_name: str):
    try:
        # Get random image from dataset
        random_image_path = get_random_image(dataset_name)
        
        if not os.path.exists(random_image_path):
            raise ValueError(f"Random image not found in dataset: {dataset_name}")
            
        return FileResponse(random_image_path, media_type='image/jpeg')
    except Exception as e:
        return {"error": str(e)}

@app.post("/datasets/download")
async def download_dataset(request: Dict):
    try:
        url = request.get("url")
        if not url:
            raise ValueError("URL is required")
            
        is_duplicate, dataset_name, img_count = downloader.duplicate_check(url)
        if not is_duplicate:
            downloader.download_dataset(url)
            analyzer.analyze_dataset(dataset_name)
            return {"message": "dataset downloaded and analyzed", "dataset_name": dataset_name}
        else:
            return {"message": "dataset already exists", "dataset_name": dataset_name, "image_count": img_count}
    except Exception as e:
        return {"error": str(e)}

@app.post("/mosaic/create")
async def create_mosaic(
    file: UploadFile = File(...),
    dataset_name: str = Form(...),
    output_width: Optional[int] = Form(100),
    tile_size: Optional[int] = Form(32),
    config: Optional[str] = Form(None)
):
    try:
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Get dataset analysis file
        dataset_path = os.path.join("datasets", dataset_name)
        analysis_path = os.path.join(dataset_path, "analysis", "center_crop_avg_colors.csv")
        
        if not os.path.exists(analysis_path):
            raise ValueError(f"Dataset analysis not found for {dataset_name}")

        # Create mosaic
        mosaic_creator = Mosaic(
            avg_colors_csv=analysis_path,
            target_image_path=file_path,
            output_width=output_width,
            mosaic_image_size=tile_size
        )
        
        # Generate unique filename for output
        output_filename = f"mosaic_{int(time.time())}.jpg"
        output_path = os.path.join(UPLOAD_FOLDER, output_filename)
        
        # Create mosaic
        mosaic_creator.create_mosaic(output_path)
        
        return {"filename": output_filename}
        
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.get("/mosaic/{filename}")
async def serve_mosaic(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type='image/jpeg',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    else:
        return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5002)
