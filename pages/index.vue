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

      <!-- Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 w-full max-w-sm animate-slide-up" style="animation-delay: 100ms;">
        <button
          @click="startNewGame"
          @mouseenter="sound.hover()"
          class="btn-primary btn-lg flex-1 group"
        >
          <span class="mr-2 group-hover:animate-bounce">🎮</span>
          Start New Game
        </button>

        <button
          v-if="hasExistingSession"
          @click="continueGame"
          @mouseenter="sound.hover()"
          class="btn-secondary btn-lg flex-1"
        >
          <span class="mr-2">▶️</span>
          Continue
        </button>
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
        <p class="text-xs mt-1">
          Question {{ existingSession.currentQuestion }} of 1000 • {{ Math.round((existingSession.currentQuestion / 1000) * 100) }}% complete
        </p>
      </div>
    </div>

    <!-- Features -->
    <div class="bg-white/50 backdrop-blur-sm border-t border-slate-200 py-8 px-4">
      <div class="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
        <div class="animate-slide-up" style="animation-delay: 300ms;">
          <div class="text-3xl mb-2">📚</div>
          <div class="text-sm font-medium text-slate-700">15+ Topics</div>
        </div>
        <div class="animate-slide-up" style="animation-delay: 400ms;">
          <div class="text-3xl mb-2">🎯</div>
          <div class="text-sm font-medium text-slate-700">10 Difficulty Levels</div>
        </div>
        <div class="animate-slide-up" style="animation-delay: 500ms;">
          <div class="text-3xl mb-2">👨‍👩‍👧‍👦</div>
          <div class="text-sm font-medium text-slate-700">All Ages</div>
        </div>
        <div class="animate-slide-up" style="animation-delay: 600ms;">
          <div class="text-3xl mb-2">🏆</div>
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
