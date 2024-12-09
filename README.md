# Mosaic Anything 🎨

Create stunning mosaics from any image using Python! Upload or randomly select an image, adjust resolution, and generate dynamic mosaics from a custom dataset with a user-friendly GUI.

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.9+
- Node.js 16+
- npm or yarn
- (Optional) Kaggle account for dataset access

## 📦 Installation

### Setup

1. Clone the repository:
```bash
git clone https://github.com/vmacri7/mosaic-anything.git
cd mosaic-anything
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional but reccomended) Kaggle Dataset Configuration
   - Create a Kaggle API token
   - Place `kaggle.json` in `~/.kaggle/` directory
   - Set appropriate permissions: `chmod 600 ~/.kaggle/kaggle.json`
   See more ([Kaggle API Docs](https://www.kaggle.com/docs/api))

5. Install npm packages:
```bash
# From project root (mosaic-anything)
npm install
```

## 🚀 Running the Application

### Start Backend Server
```bash
cd backend
python -m uvicorn app:app --reload --port 5002
```

### Start Frontend Development Server
```bash
# change to project root directory
cd ..
npm run dev
```

## 🎨 Usage

1. Open the web application in your browser (default: `http://localhost:5174`)
2. Find a dataset to use on [kaggle](https://www.kaggle.com/) and copy the Kaggle dataset URL
3. Paste the URL into the dataset uploader and click "Add Dataset"
4. Select datasets from the list once uploaded
5. Upload an image or select a random image from the selected dataset
6. Configure mosaic parameters:
   - Output width (unit: tiles)
   - Tile size (unit: pixels)
7. Click "Create Mosaic"
8. Mosaic artwork will be displayed under Results
9. Download your masterpiece!
