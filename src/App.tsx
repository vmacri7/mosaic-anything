import React, { useState, useRef, useEffect } from 'react';
import { RefreshCw } from 'lucide-react';
import { DatasetUploader } from './components/DatasetUploader';
import { DatasetList } from './components/DatasetList';
import { ImageUploader } from './components/ImageUploader';
import { MosaicConfig } from './components/MosaicConfig';
import { ResultDisplay } from './components/ResultDisplay';
import { getDatasets, downloadDataset, getRandomImage } from './api/dataset';
import { createMosaic } from './api/mosaic';
import { Dataset, MosaicConfig as MosaicConfigType } from './api/types';

function App() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<string>("");
  const [targetImage, setTargetImage] = useState<string>("");
  const [outputWidth, setOutputWidth] = useState<number>(100);
  const [tileSize, setTileSize] = useState<number>(32);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [result, setResult] = useState<string>("");
  const [error, setError] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  // fetch datasets on component mount
  useEffect(() => {
    const fetchDatasets = async () => {
      try {
        setIsLoading(true);
        const response = await getDatasets();
        if (response.error) {
          setError(response.error);
        } else if (response.data) {
          setDatasets(response.data);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "failed to fetch datasets");
      } finally {
        setIsLoading(false);
      }
    };
    fetchDatasets();
  }, []);

  const handleDatasetUpload = async (url: string) => {
    setIsUploading(true);
    setError("");
    try {
      const response = await downloadDataset(url);
      if (response.error) {
        setError(response.error);
      } else {
        // refresh dataset list after successful upload
        const datasetsResponse = await getDatasets();
        if (datasetsResponse.data) {
          setDatasets(datasetsResponse.data);
        }
      }
    } finally {
      setIsUploading(false);
    }
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setTargetImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleRandomImage = async () => {
    if (!selectedDataset) {
      setError("Please select a dataset first");
      return;
    }

    setIsProcessing(true);
    setError("");

    try {
      const response = await getRandomImage(selectedDataset);
      if (response.error) {
        throw new Error(response.error);
      }
      if (response.data) {
        setTargetImage(response.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to get random image");
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCreateMosaic = async () => {
    if (!targetImage || !selectedDataset) {
      setError("Please select both a target image and a dataset");
      return;
    }

    setIsProcessing(true);
    setError("");

    try {
      // Convert base64/data URL or blob URL to blob
      const file = await (async () => {
        if (targetImage.startsWith('data:') || targetImage.startsWith('blob:')) {
          // For data URLs and blob URLs, convert to blob
          const response = await fetch(targetImage);
          const blob = await response.blob();
          return new File([blob], "target-image.jpg", { type: "image/jpeg" });
        } else {
          // For uploaded files, get from file input
          const files = fileInputRef.current?.files;
          if (files && files.length > 0) {
            return files[0];
          }
          throw new Error("No image file found");
        }
      })();

      const config: MosaicConfigType = {
        tileSize,
        colorMatch: true,
        enhanceColors: true
      };

      const mosaicResponse = await createMosaic(
        file,
        config,
        selectedDataset,
        outputWidth,
        tileSize
      );
      
      if (mosaicResponse.error) {
        throw new Error(mosaicResponse.error);
      }

      if (mosaicResponse.data) {
        setResult(mosaicResponse.data);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create mosaic");
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-4 sm:py-8">
        <header className="text-center mb-6 sm:mb-12">
          <h1 className="text-2xl sm:text-4xl font-bold text-gray-800 mb-2">Mosaic Anything 🎨</h1>
          <p className="text-sm sm:text-base text-gray-600">images + datasets into beautiful photo mosaics</p>
        </header>

        {isLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-gray-600">loading...</div>
          </div>
        ) : error ? (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
            {error}
          </div>
        ) : (
          <div className="grid lg:grid-cols-2 gap-4 sm:gap-8">
            <div className="space-y-4 sm:space-y-6">
              <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md">
                <h2 className="text-lg sm:text-xl font-semibold mb-4">1. Select Dataset</h2>
                <DatasetUploader onUpload={handleDatasetUpload} isUploading={isUploading} />
                <DatasetList
                  datasets={datasets}
                  selectedDataset={selectedDataset}
                  onSelect={setSelectedDataset}
                />
              </div>

              <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md">
                <h2 className="text-lg sm:text-xl font-semibold mb-4">2. Choose Target Image</h2>
                <ImageUploader
                  targetImage={targetImage}
                  onFileUpload={handleFileUpload}
                  onRandomImage={handleRandomImage}
                  fileInputRef={fileInputRef}
                />
              </div>

              <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md">
                <h2 className="text-lg sm:text-xl font-semibold mb-4">3. Configure Mosaic</h2>
                <MosaicConfig
                  outputWidth={outputWidth}
                  setOutputWidth={setOutputWidth}
                  tileSize={tileSize}
                  setTileSize={setTileSize}
                />
              </div>

              <button
                onClick={handleCreateMosaic}
                disabled={!selectedDataset || !targetImage || isProcessing}
                className="w-full bg-blue-600 text-white py-2 sm:py-3 px-4 sm:px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm sm:text-base"
              >
                {isProcessing ? (
                  <span className="flex items-center justify-center">
                    <RefreshCw className="animate-spin mr-2" size={20} />
                    Creating Mosaic...
                  </span>
                ) : (
                  'Create Mosaic'
                )}
              </button>
            </div>

            <div className="bg-white p-4 sm:p-6 rounded-lg shadow-md">
              <h2 className="text-lg sm:text-xl font-semibold mb-4">Result</h2>
              <ResultDisplay result={result} />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;