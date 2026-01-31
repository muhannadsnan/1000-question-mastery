<template>
  <div class="min-h-screen flex flex-col">
    <!-- Hero Section -->
    <div class="flex-1 flex flex-col items-center justify-center px-4 py-12">
      <!-- Logo/Title -->
      <div class="text-center mb-8 animate-bounce-in">
        <div class="inline-flex items-center justify-center w-20 h-20 md:w-24 md:h-24 bg-gradient-to-br from-primary-500 to-purple-600 rounded-2xl shadow-2xl shadow-primary-500/30 mb-6 animate-float">
          <span class="text-4xl md:text-5xl">🧠</span>
        </div>
        <h1 class="text-4xl md:text-6xl font-extrabold mb-3">
          <span class="text-gradient">1000</span>
          <span class="text-slate-800"> Question</span>
        </h1>
        <h2 class="text-3xl md:text-5xl font-bold text-slate-700">Mastery</h2>
      </div>

      <!-- Tagline -->
      <p class="text-lg md:text-xl text-slate-600 text-center max-w-md mb-10 animate-slide-up">
        Challenge yourself with 1000 questions across all topics.
        <span class="text-primary-600 font-semibold">Earn your certificate!</span>
      </p>

      <!-- Main Action Buttons - Modern Card Style -->
      <div class="grid grid-cols-2 gap-4 w-full max-w-md animate-slide-up" style="animation-delay: 100ms;">
        <!-- Start New Game -->
        <button
          @click="startNewGame"
          @mouseenter="sound.hover()"
          class="menu-card group bg-gradient-to-br from-primary-500 to-purple-600 text-white"
        >
          <div class="menu-icon bg-white/20">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <span class="menu-text">New Game</span>
        </button>

        <!-- Continue Game -->
        <button
          v-if="hasExistingSession"
          @click="continueGame"
          @mouseenter="sound.hover()"
          class="menu-card group bg-gradient-to-br from-emerald-500 to-teal-600 text-white"
        >
          <div class="menu-icon bg-white/20">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <span class="menu-text">Continue</span>
        </button>

        <!-- Placeholder when no session -->
        <div v-else class="menu-card-disabled">
          <div class="menu-icon bg-slate-200">
            <svg class="w-8 h-8 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </div>
          <span class="menu-text text-slate-400">No Session</span>
        </div>
      </div>

      <!-- Existing Session Info -->
      <div
        v-if="hasExistingSession && existingSession"
        class="mt-6 text-center text-slate-500 animate-slide-up"
        style="animation-delay: 200ms;"
      >
        <p class="text-sm">
          Continue as <span class="font-semibold text-slate-700">{{ existingSession.playerName }}</span>
        </p>
        <div class="flex items-center justify-center gap-2 mt-2">
          <div class="h-2 w-32 bg-slate-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-primary-500 to-purple-500 rounded-full transition-all"
              :style="{ width: `${(existingSession.currentQuestion / 1000) * 100}%` }"
            />
          </div>
          <span class="text-xs font-medium">{{ existingSession.currentQuestion }}/1000</span>
        </div>
      </div>
    </div>

    <!-- Features -->
    <div class="bg-white/50 backdrop-blur-sm border-t border-slate-200 py-8 px-4">
      <div class="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6">
        <div class="feature-card animate-slide-up" style="animation-delay: 300ms;">
          <div class="feature-icon bg-blue-100">
            <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <div class="text-sm font-medium text-slate-700">15+ Topics</div>
        </div>
        <div class="feature-card animate-slide-up" style="animation-delay: 400ms;">
          <div class="feature-icon bg-amber-100">
            <svg class="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div class="text-sm font-medium text-slate-700">10 Levels</div>
        </div>
        <div class="feature-card animate-slide-up" style="animation-delay: 500ms;">
          <div class="feature-icon bg-green-100">
            <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <div class="text-sm font-medium text-slate-700">All Ages</div>
        </div>
        <div class="feature-card animate-slide-up" style="animation-delay: 600ms;">
          <div class="feature-icon bg-purple-100">
            <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
            </svg>
          </div>
          <div class="text-sm font-medium text-slate-700">Certificate</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const sound = useSound()
const { loadSession, session, clearSession } = useGameSession()

const existingSession = ref<ReturnType<typeof loadSession>>(null)
const hasExistingSession = computed(() => existingSession.value !== null && existingSession.value.currentQuestion <= 1000)

onMounted(() => {
  existingSession.value = loadSession()
  // Play welcome sound
  setTimeout(() => sound.gameLoad(), 300)
})

const startNewGame = () => {
  sound.click()
  if (hasExistingSession.value) {
    // Could show confirmation modal, for now just clear and start
    clearSession()
  }
  router.push('/setup')
}

const continueGame = () => {
  sound.click()
  router.push('/game')
}
</script>

<style scoped>
.menu-card {
  @apply flex flex-col items-center justify-center gap-3 p-6 rounded-2xl shadow-lg
         transition-all duration-300 transform hover:scale-105 hover:shadow-xl cursor-pointer;
}

.menu-card-disabled {
  @apply flex flex-col items-center justify-center gap-3 p-6 rounded-2xl
         bg-slate-100 border-2 border-dashed border-slate-200;
}

.menu-icon {
  @apply w-16 h-16 rounded-xl flex items-center justify-center transition-transform group-hover:scale-110;
}

.menu-text {
  @apply font-semibold text-lg;
}

.feature-card {
  @apply flex flex-col items-center gap-2 text-center;
}

.feature-icon {
  @apply w-12 h-12 rounded-xl flex items-center justify-center;
}
</style>
