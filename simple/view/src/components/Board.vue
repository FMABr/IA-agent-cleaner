<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { whenever, useElementSize } from "@vueuse/core";

import { useTileset, type Position } from "@/utils/useTileset";

import Tileset from "@/assets/interior_main.png";

interface BoardProps {
  rows?: number;
  columns?: number;
}

const props = withDefaults(defineProps<BoardProps>(), {
  rows: 10,
  columns: 10,
});

const board = ref<HTMLCanvasElement | null>(null);
const { width, height } = useElementSize(board);

const columnSize = computed(() => width.value / props.columns);
const rowSize = computed(() => height.value / props.rows);

const tiles: Record<string, Position> = {
  clean: {
    x: 2,
    y: 1,
  },
  dirty: {
    x: 0,
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

      whenever(loaded, () => {
        for (let row = 0; row < props.columns; row++) {
          for (let col = 0; col < props.rows; col++) {
            const tile = [tiles.dirty, tiles.clean][row % 2];
            drawTile(
              tile,
              {
                x: row * rowSize.value,
                y: col * columnSize.value,
              },
              { width: columnSize.value, height: rowSize.value }
            );
          }
        }
      });
    }
  }
});
</script>

<template>
  <canvas ref="board" class="board" :width="width" :height="height" />
</template>

<style scoped>
.board {
  justify-self: center;
  align-self: center;

  height: round(up, 50%, 32px);
  aspect-ratio: 1 / 1;
}
</style>
