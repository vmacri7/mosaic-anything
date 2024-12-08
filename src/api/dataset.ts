import { Dataset, ApiResponse } from './types';

const API_BASE_URL = 'http://localhost:5002';

// get list of available datasets
export const getDatasets = async (): Promise<ApiResponse<Dataset[]>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/datasets`);
    if (!response.ok) {
      throw new Error('failed to fetch datasets');
    }
    const result = await response.json();
    // Transform the response to match the Dataset interface
    const datasets = result.data.map((dataset: any) => ({
      name: dataset.name,
      imageCount: dataset.image_count
    }));
    return { data: datasets };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'unknown error occurred' };
  }
};

// download a new dataset from kaggle url
export const downloadDataset = async (url: string): Promise<ApiResponse<void>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/datasets/download`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to download dataset');
    }
    
    return {};
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'unknown error occurred' };
  }
};

// get random image from dataset
export const getRandomImage = async (datasetName: string): Promise<ApiResponse<string>> => {
  try {
    const response = await fetch(`${API_BASE_URL}/datasets/${datasetName}/random`);
    
    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || 'Failed to get random image');
    }
    
    // Convert the image blob to a data URL
    const blob = await response.blob();
    const dataUrl = URL.createObjectURL(blob);
    return { data: dataUrl };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'unknown error occurred' };
  }
};
