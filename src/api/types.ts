// api response types
export interface Dataset {
  name: string;
  imageCount: number;
}

export interface MosaicConfig {
  tileSize: number;
  colorMatch: boolean;
  enhanceColors: boolean;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
}
