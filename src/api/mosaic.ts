import { MosaicConfig, ApiResponse } from './types';

const API_BASE_URL = 'http://localhost:5002';

// create a mosaic from uploaded image and config
export const createMosaic = async (
  image: File,
  config: MosaicConfig,
  dataset_name: string,
  output_width: number = 100,
  tile_size: number = 32
): Promise<ApiResponse<string>> => {
  try {
    const formData = new FormData();
    formData.append('file', image);
    formData.append('dataset_name', dataset_name);
    formData.append('output_width', output_width.toString());
    formData.append('tile_size', tile_size.toString());
    formData.append('config', JSON.stringify(config));

    const response = await fetch(`${API_BASE_URL}/mosaic/create`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to create mosaic');
    }

    if (data.error) {
      throw new Error(data.error);
    }

    // Return the URL to the mosaic image
    return { data: `${API_BASE_URL}/mosaic/${data.filename}` };
  } catch (error) {
    return { error: error instanceof Error ? error.message : 'unknown error occurred' };
  }
};
