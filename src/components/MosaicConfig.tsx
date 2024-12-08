import React from 'react';

interface MosaicConfigProps {
  outputWidth: number;
  setOutputWidth: (width: number) => void;
  tileSize: number;
  setTileSize: (size: number) => void;
}

export function MosaicConfig({ outputWidth, setOutputWidth, tileSize, setTileSize }: MosaicConfigProps) {
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Output Width (tiles)
        </label>
        <input
          type="range"
          value={outputWidth}
          onChange={(e) => setOutputWidth(Number(e.target.value))}
          min="10"
          max="200"
          className="w-full"
        />
        <span className="text-sm text-gray-500">{outputWidth} tiles</span>
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          Tile Size (pixels)
        </label>
        <input
          type="range"
          value={tileSize}
          onChange={(e) => setTileSize(Number(e.target.value))}
          min="16"
          max="64"
          className="w-full"
        />
        <span className="text-sm text-gray-500">{tileSize} pixels</span>
      </div>
    </div>
  );
}