import React from 'react';
import { Download } from 'lucide-react';

interface ResultDisplayProps {
  result: string;
}

export function ResultDisplay({ result }: ResultDisplayProps) {
  const handleDownload = () => {
    if (result) {
      const link = document.createElement('a');
      link.href = result;
      link.download = 'mosaic.jpg';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <div>
      {result ? (
        <div className="space-y-4">
          <img
            src={result}
            alt="Mosaic Result"
            className="w-full rounded-lg shadow-lg"
          />
          <button 
            onClick={handleDownload}
            className="w-full flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            <Download className="mr-2" size={20} />
            <span className="text-sm sm:text-base">Download Mosaic</span>
          </button>
        </div>
      ) : (
        <div className="h-48 sm:h-64 flex items-center justify-center text-gray-500 text-sm sm:text-base">
          Your mosaic will appear here
        </div>
      )}
    </div>
  );
}