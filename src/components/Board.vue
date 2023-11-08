<script setup lang="ts">
import { useTileset, type Position } from "@/utils/useTileset";
import { onMounted, ref } from "vue";
import Tileset from "@/assets/interior_main.png";

interface BoardProps {
  rows?: number;
  columns?: number;
}

withDefaults(defineProps<BoardProps>(), {
  rows: 10,
  columns: 10,
});

const board = ref<HTMLCanvasElement | null>(null);

const tiles: Record<string, Position> = {
  wood: {
    x: 1,
    y: 1,
  },
};

onMounted(() => {
  if (board) {
    const context = board.value?.getContext("2d");

    if (context) {
      const { loaded, drawTile } = useTileset(context, Tileset, {
        width: 32,
        height: 32,
      });

      drawTile(tiles.wood, { x: 0, y: 0 });
      alert();
    }
  }
});
</script>

<template>
  <canvas ref="board" class="board"> </canvas>
</template>

<style scoped>
.board {
  width: 64px;
  height: 64px;
}
</style>
