<template>
  <div class="min-h-screen">
    <NuxtPage />
    <div class="fixed bottom-2 left-2 text-xs text-gray-400">
      v{{ config.public.appVersion }}
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
</script>
