import { ref } from "vue";
import { useEventListener } from "@vueuse/core";

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
  tileSize: Dimension
) {
  const tileset = preloadImage(src);
  const { width: sw, height: sh } = tileSize;

  const loaded = ref(false);

  useEventListener(tileset, "load", () => (loaded.value = true));

  const drawTile = (
    source: Position,
    destination: Position,
    destSize?: Dimension
  ) => {
    const { width: dw, height: dh } = destSize ?? tileSize;
    plane.drawImage(
      tileset,
      source.x * sw,
      source.y * sh,
      sw,
      sh,
      destination.x,
      destination.y,
      dw,
      dh
    );
  };

  return { loaded, drawTile };
}
