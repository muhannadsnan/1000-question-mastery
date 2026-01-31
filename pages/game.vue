<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white/80 backdrop-blur-lg border-b border-slate-200 sticky top-0 z-10">
      <div class="max-w-2xl mx-auto px-4 py-3">
        <!-- Progress Bar -->
        <div class="flex items-center gap-3 mb-2">
          <span class="text-sm font-medium text-slate-600 whitespace-nowrap">
            Q {{ session?.currentQuestion || 1 }}/1000
          </span>
          <div class="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
            <div
              class="h-full bg-gradient-to-r from-primary-500 to-purple-500 transition-all duration-500"
              :style="{ width: `${progressPercent}%` }"
            />
          </div>
          <span class="text-sm font-semibold text-primary-600">{{ Math.round(progressPercent) }}%</span>
        </div>

        <!-- Stats Row -->
        <div class="flex items-center justify-between text-sm">
          <div class="flex items-center gap-4">
            <span :class="difficultyColor" class="px-2 py-0.5 rounded-full text-xs font-semibold">
              Level {{ currentLevel }}
            </span>
            <span class="text-green-600 font-medium">✓ {{ session?.correctAnswers || 0 }}</span>
            <span class="text-red-500 font-medium">✗ {{ session?.wrongAnswers || 0 }}</span>
          </div>
          <button
            @click="showQuitModal = true"
            class="text-slate-400 hover:text-slate-600 transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col items-center px-4 py-6 pt-4">
      <!-- Loading State -->
      <div v-if="isLoading" class="text-center">
        <div class="w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        <p class="text-slate-500">Loading question...</p>
      </div>

      <!-- Level Up Celebration -->
      <div
        v-else-if="showLevelUp"
        class="text-center animate-bounce-in"
      >
        <div class="text-6xl mb-4">🎉</div>
        <h2 class="text-3xl font-bold text-slate-800 mb-2">Level Up!</h2>
        <p class="text-xl text-primary-600 font-semibold mb-6">You've reached Level {{ currentLevel }}!</p>
        <button @click="dismissLevelUp" class="btn-primary">
          Continue
        </button>
      </div>

      <!-- Question Card -->
      <div
        v-else-if="currentQuestionData"
        class="w-full max-w-xl"
      >
        <!-- Category Badge -->
        <div class="text-center mb-4">
          <span
            class="inline-block px-4 py-1.5 rounded-full text-sm font-semibold capitalize"
            :class="getCategoryColor(currentQuestionData.category)"
          >
            {{ currentQuestionData.category }}
          </span>
        </div>

        <!-- Question -->
        <div
          :class="[
            'card mb-6 transition-all duration-300',
            lastAnswerCorrect === true && 'ring-4 ring-green-500/30 correct-pulse',
            lastAnswerCorrect === false && 'ring-4 ring-red-500/30 wrong-shake'
          ]"
        >
          <h2 class="text-xl md:text-2xl font-semibold text-slate-800 text-center leading-relaxed">
            {{ currentQuestionData.text }}
          </h2>
        </div>

        <!-- Options -->
        <div class="space-y-4">
          <button
            v-for="(option, index) in currentQuestionData.options"
            :key="index"
            @click="selectOption(index)"
            :disabled="isAnswerRevealed"
            :class="[
              'w-full px-5 py-5 rounded-2xl border-2 text-left transition-all duration-200 flex items-center gap-4',
              getOptionClass(index)
            ]"
            :style="{ animationDelay: `${index * 50}ms` }"
          >
            <span :class="[
              'w-10 h-10 rounded-xl flex items-center justify-center text-base font-bold shrink-0',
              getOptionBadgeClass(index)
            ]">
              {{ ['A', 'B', 'C', 'D'][index] }}
            </span>
            <span class="text-lg font-medium">{{ option }}</span>

            <!-- Correct/Wrong Icon -->
            <span v-if="isAnswerRevealed && index === currentQuestionData.correctIndex" class="ml-auto text-green-500 text-2xl">
              ✓
            </span>
            <span v-else-if="isAnswerRevealed && index === selectedAnswer && index !== currentQuestionData.correctIndex" class="ml-auto text-red-500 text-2xl">
              ✗
            </span>
          </button>
        </div>

        <!-- Next Button -->
        <div v-if="isAnswerRevealed" class="mt-6 text-center animate-slide-up">
          <button
            @click="goToNext"
            class="btn-primary btn-lg"
          >
            {{ session?.currentQuestion === 1000 ? 'Finish!' : 'Next Question' }}
            <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        </div>
      </div>
    </main>

    <!-- Quit Modal -->
    <Teleport to="body">
      <div
        v-if="showQuitModal"
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
        @click.self="showQuitModal = false"
      >
        <div class="bg-white rounded-2xl p-6 max-w-sm w-full animate-bounce-in">
          <h3 class="text-xl font-bold text-slate-800 mb-2">Quit Game?</h3>
          <p class="text-slate-500 mb-6">Your progress will be saved. You can continue later.</p>
          <div class="flex gap-3">
            <button @click="showQuitModal = false" class="btn-secondary flex-1">
              Cancel
            </button>
            <button @click="quitGame" class="btn-primary flex-1 !bg-red-500 hover:!bg-red-600">
              Quit
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Confetti -->
    <div v-if="showConfetti" class="fixed inset-0 pointer-events-none z-50 overflow-hidden">
      <div
        v-for="i in 50"
        :key="i"
        class="confetti-particle"
        :style="{
          left: `${Math.random() * 100}%`,
          backgroundColor: ['#3B82F6', '#8B5CF6', '#22C55E', '#F59E0B', '#EF4444'][i % 5],
          animationDelay: `${Math.random() * 2}s`,
          animationDuration: `${2 + Math.random() * 2}s`
        }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const sound = useSound()
const {
  session,
  currentQuestionData,
  isLoading,
  isAnswerRevealed,
  selectedAnswer,
  lastAnswerCorrect,
  currentLevel,
  didLevelUp,
  progressPercent,
  loadSession,
  fetchQuestion,
  submitAnswer,
  nextQuestion,
  isGameComplete,
} = useGameSession()

const showQuitModal = ref(false)
const showLevelUp = ref(false)
const showConfetti = ref(false)
const previousLevelRef = ref(1)

// Difficulty color based on level
const difficultyColor = computed(() => {
  const level = currentLevel.value
  if (level <= 2) return 'bg-green-100 text-green-700'
  if (level <= 4) return 'bg-lime-100 text-lime-700'
  if (level <= 6) return 'bg-amber-100 text-amber-700'
  if (level <= 8) return 'bg-orange-100 text-orange-700'
  return 'bg-red-100 text-red-700'
})

const getOptionClass = (index: number) => {
  if (!isAnswerRevealed.value) {
    if (selectedAnswer.value === index) {
      return 'border-primary-500 bg-primary-50'
    }
    return 'border-slate-200 hover:border-primary-300 hover:bg-slate-50'
  }

  // Answer revealed
  if (index === currentQuestionData.value?.correctIndex) {
    return 'border-green-500 bg-green-50'
  }
  if (index === selectedAnswer.value) {
    return 'border-red-500 bg-red-50'
  }
  return 'border-slate-200 bg-slate-50 opacity-50'
}

const getOptionBadgeClass = (index: number) => {
  if (!isAnswerRevealed.value) {
    if (selectedAnswer.value === index) {
      return 'bg-primary-500 text-white'
    }
    return 'bg-slate-100 text-slate-600'
  }

  if (index === currentQuestionData.value?.correctIndex) {
    return 'bg-green-500 text-white'
  }
  if (index === selectedAnswer.value) {
    return 'bg-red-500 text-white'
  }
  return 'bg-slate-100 text-slate-400'
}

// Category colors - predefined palette
const categoryColors: Record<string, string> = {
  math: 'bg-blue-100 text-blue-700',
  science: 'bg-emerald-100 text-emerald-700',
  geography: 'bg-cyan-100 text-cyan-700',
  history: 'bg-amber-100 text-amber-700',
  music: 'bg-pink-100 text-pink-700',
  movies: 'bg-purple-100 text-purple-700',
  'tv-shows': 'bg-violet-100 text-violet-700',
  sports: 'bg-orange-100 text-orange-700',
  gaming: 'bg-indigo-100 text-indigo-700',
  literature: 'bg-rose-100 text-rose-700',
  art: 'bg-fuchsia-100 text-fuchsia-700',
  technology: 'bg-sky-100 text-sky-700',
  'pop-culture': 'bg-red-100 text-red-700',
  'social-media': 'bg-teal-100 text-teal-700',
  food: 'bg-lime-100 text-lime-700',
  general: 'bg-slate-100 text-slate-700',
  vocabulary: 'bg-yellow-100 text-yellow-700',
  animals: 'bg-green-100 text-green-700',
  nature: 'bg-emerald-100 text-emerald-700',
  politics: 'bg-red-100 text-red-700',
  philosophy: 'bg-purple-100 text-purple-700',
  economics: 'bg-blue-100 text-blue-700',
  business: 'bg-slate-200 text-slate-700',
  psychology: 'bg-violet-100 text-violet-700',
  law: 'bg-gray-200 text-gray-700',
  religion: 'bg-amber-100 text-amber-700',
  archaeology: 'bg-orange-100 text-orange-700',
  linguistics: 'bg-cyan-100 text-cyan-700',
  anthropology: 'bg-teal-100 text-teal-700',
  mythology: 'bg-indigo-100 text-indigo-700',
  'film-theory': 'bg-purple-100 text-purple-700',
  paleography: 'bg-stone-200 text-stone-700',
  physics: 'bg-blue-200 text-blue-700',
}

const getCategoryColor = (category: string) => {
  return categoryColors[category] || 'bg-slate-100 text-slate-700'
}

const selectOption = (index: number) => {
  if (isAnswerRevealed.value) return

  sound.select()
  const isCorrect = submitAnswer(index)

  if (isCorrect) {
    sound.correct()
  } else {
    sound.wrong()
  }
}

const goToNext = async () => {
  sound.nextQuestion()

  // Check for level up
  const prevLevel = previousLevelRef.value

  await nextQuestion()

  // Check if game complete
  if (isGameComplete.value) {
    sound.victory()
    showConfetti.value = true
    setTimeout(() => {
      router.push('/certificate')
    }, 2000)
    return
  }

  // Check for level up
  if (currentLevel.value > prevLevel) {
    showLevelUp.value = true
    showConfetti.value = true
    sound.levelUp()
    setTimeout(() => {
      showConfetti.value = false
    }, 3000)
  }

  previousLevelRef.value = currentLevel.value
}

const dismissLevelUp = () => {
  showLevelUp.value = false
}

const quitGame = () => {
  sound.click()
  router.push('/')
}

onMounted(async () => {
  const existingSession = loadSession()
  if (!existingSession) {
    router.push('/setup')
    return
  }

  previousLevelRef.value = currentLevel.value
  await fetchQuestion()
})
</script>
