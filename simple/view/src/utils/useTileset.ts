import { ref } from "vue";

interface Dimension {
  width: number;
  height: number;
}

export interface Position {
  x: number;

  y: number;
}

// Cache for preloaded images
const imageCache: Record<string, HTMLImageElement> = {};
function preloadImage(src: string) {
  if (!imageCache[src]) {
    const image = new Image();
    image.src = src;
    imageCache[src] = image;
  }

  return imageCache[src];
}

export function useTileset(
  plane: CanvasRenderingContext2D,
  src: string,
  { width, height }: Dimension
) {
  const tileset = preloadImage(src);

  const loaded = ref(false);
  tileset.onload = () => (loaded.value = true);

  const drawTile = (tile: Position, target: Position) => {
    plane?.drawImage(
      tileset,
      tile.x * width,
      tile.y * height,
      width,
      height,
      target.x,
      target.y,
      width,
      height
    );
  };

  return { loaded, drawTile };
}
