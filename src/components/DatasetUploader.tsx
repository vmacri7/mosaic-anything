import React, { useState } from 'react';
import { Plus, RefreshCw } from 'lucide-react';

interface DatasetUploaderProps {
  onUpload: (url: string) => void;
  isUploading: boolean;
}

export function DatasetUploader({ onUpload, isUploading }: DatasetUploaderProps) {
  const [url, setUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.includes('kaggle.com/datasets/')) {
      setError('Please enter a valid Kaggle dataset URL');
      return;
    }
    setError('');
    onUpload(url);
    setUrl('');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <div className="flex flex-col sm:flex-row gap-2">
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter Kaggle dataset URL"
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm sm:text-base"
          disabled={isUploading}
        />
        <button
          type="submit"
          disabled={isUploading || !url}
          className="flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isUploading ? (
            <span className="flex items-center">
              <RefreshCw className="animate-spin mr-2" size={20} />
              Downloading...
            </span>
          ) : (
            <>
              <Plus size={20} className="mr-2" />
              <span className="text-sm sm:text-base">Add Dataset</span>
            </>
          )}
        </button>
      </div>
      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
    </form>
  );
}