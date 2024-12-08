import React from 'react';

interface Dataset {
  name: string;
  imageCount: number;
}

interface DatasetListProps {
  datasets: Dataset[];
  selectedDataset: string;
  onSelect: (name: string) => void;
}

export function DatasetList({ datasets, selectedDataset, onSelect }: DatasetListProps) {
  return (
    <div className="max-h-80 overflow-y-auto pr-2 space-y-2">
      {datasets.map((dataset) => (
        <label
          key={dataset.name}
          className={`flex items-center p-3 border rounded-lg cursor-pointer transition-colors ${
            selectedDataset === dataset.name
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-200 hover:bg-gray-50'
          }`}
        >
          <input
            type="radio"
            name="dataset"
            value={dataset.name}
            checked={selectedDataset === dataset.name}
            onChange={(e) => onSelect(e.target.value)}
            className="mr-3"
          />
          <div>
            <p className="font-medium">{dataset.name}</p>
            <p className="text-sm text-gray-500">{dataset.imageCount} images</p>
          </div>
        </label>
      ))}
    </div>
  );
}