import React from 'react';
import { Upload, Image } from 'lucide-react';

interface ImageUploaderProps {
  targetImage: string;
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
  onRandomImage: () => void;
  fileInputRef: React.RefObject<HTMLInputElement>;
}

export function ImageUploader({ targetImage, onFileUpload, onRandomImage, fileInputRef }: ImageUploaderProps) {
  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      onFileUpload(event);
    }
  };

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center justify-center px-4 py-2 border-2 border-dashed border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
        >
          <Upload className="mr-2" size={20} />
          <span className="text-sm sm:text-base">Upload Image</span>
        </button>
        <button
          onClick={onRandomImage}
          className="flex items-center justify-center px-4 py-2 border-2 border-gray-300 rounded-lg hover:border-blue-500 hover:bg-blue-50 transition-colors"
        >
          <Image className="mr-2" size={20} />
          <span className="text-sm sm:text-base">Random Image</span>
        </button>
      </div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
        accept="image/jpeg,image/png,image/webp"
      />
      {targetImage && (
        <div className="mt-4">
          <img
            src={targetImage}
            alt="Target"
            className="w-full h-auto rounded-lg shadow-md"
          />
        </div>
      )}
    </div>
  );
}