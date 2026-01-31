<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 py-8">
    <!-- Back Button -->
    <div class="fixed top-4 left-4">
      <button
        @click="goBack"
        class="flex items-center gap-2 text-slate-500 hover:text-slate-700 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <span>Back</span>
      </button>
    </div>

    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="text-center mb-8 animate-bounce-in">
        <h1 class="text-3xl md:text-4xl font-bold text-slate-800 mb-2">Let's Get Started!</h1>
        <p class="text-slate-500">Tell us a bit about yourself</p>
      </div>

      <!-- Form -->
      <div class="card animate-slide-up">
        <!-- Name Input with History -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-slate-700 mb-2">
            Your Name
          </label>
          <div class="relative">
            <input
              ref="nameInputRef"
              v-model="playerName"
              type="text"
              placeholder="Enter your name..."
              maxlength="30"
              class="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 outline-none transition-all text-lg pr-10"
              @keyup.enter="startGame"
              @focus="showNameDropdown = savedNames.length > 0"
              @blur="hideDropdownDelayed"
            />
            <!-- Clear input button -->
            <button
              v-if="playerName"
              @click="playerName = ''"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Saved Names Dropdown -->
          <div
            v-if="showNameDropdown && savedNames.length > 0"
            class="mt-2 bg-white rounded-xl border border-slate-200 shadow-lg overflow-hidden z-10"
          >
            <div class="px-3 py-2 bg-slate-50 border-b border-slate-100">
              <span class="text-xs font-medium text-slate-500">Recent names</span>
            </div>
            <div class="max-h-40 overflow-y-auto">
              <div
                v-for="name in savedNames"
                :key="name"
                class="flex items-center justify-between px-4 py-3 hover:bg-slate-50 cursor-pointer group"
                @mousedown.prevent="selectName(name)"
              >
                <span class="text-slate-700">{{ name }}</span>
                <button
                  @mousedown.prevent.stop="removeName(name)"
                  class="text-slate-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Age Group Selection -->
        <div class="mb-8">
          <label class="block text-sm font-medium text-slate-700 mb-3">
            Select Your Age Group
          </label>
          <div class="grid grid-cols-2 gap-3">
            <button
              v-for="group in ageGroups"
              :key="group.id"
              @click="selectAgeGroup(group.id)"
              @mouseenter="sound.hover()"
              :class="[
                'age-group-btn',
                selectedAgeGroup === group.id
                  ? 'border-primary-500 bg-primary-50 shadow-lg shadow-primary-500/20'
                  : 'border-slate-200 hover:border-primary-300 hover:bg-slate-50'
              ]"
            >
              <div class="age-icon" :class="group.iconBg">
                <span class="text-3xl">{{ group.emoji }}</span>
              </div>
              <div class="font-semibold text-slate-800">{{ group.label }}</div>
              <div class="text-xs text-slate-500">{{ group.ageRange }}</div>
            </button>
          </div>
        </div>

        <!-- Start Button -->
        <button
          @click="startGame"
          @mouseenter="sound.hover()"
          :disabled="!canStart"
          :class="[
            'w-full btn-success btn-lg flex items-center justify-center gap-2',
            !canStart && 'opacity-50 cursor-not-allowed'
          ]"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Begin Quiz!
        </button>
      </div>

      <!-- Info -->
      <p class="text-center text-sm text-slate-400 mt-6 animate-slide-up" style="animation-delay: 200ms;">
        Complete 1000 questions to earn your certificate
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AgeGroup } from '~/types'

const router = useRouter()
const sound = useSound()
const { createSession } = useGameSession()

const NAMES_STORAGE_KEY = 'quiz-mastery-names'

const playerName = ref('')
const selectedAgeGroup = ref<AgeGroup | null>(null)
const savedNames = ref<string[]>([])
const showNameDropdown = ref(false)
const nameInputRef = ref<HTMLInputElement | null>(null)

const ageGroups = [
  {
    id: 'littleKids' as AgeGroup,
    label: 'Little Kids',
    ageRange: '3-7 years',
    emoji: '👶',
    iconBg: 'bg-pink-100',
  },
  {
    id: 'kids' as AgeGroup,
    label: 'Kids',
    ageRange: '8-12 years',
    emoji: '🧒',
    iconBg: 'bg-blue-100',
  },
  {
    id: 'teens' as AgeGroup,
    label: 'Teens',
    ageRange: '13-17 years',
    emoji: '🎮',
    iconBg: 'bg-purple-100',
  },
  {
    id: 'adults' as AgeGroup,
    label: 'Adults',
    ageRange: '18-35 years',
    emoji: '👨‍💼',
    iconBg: 'bg-emerald-100',
  },
  {
    id: 'seniors' as AgeGroup,
    label: 'Seniors',
    ageRange: '35+ years',
    emoji: '🎓',
    iconBg: 'bg-amber-100',
  },
]

const canStart = computed(() => {
  return playerName.value.trim().length >= 2 && selectedAgeGroup.value !== null
})

// Load saved names from localStorage
const loadSavedNames = () => {
  if (typeof window === 'undefined') return
  try {
    const stored = localStorage.getItem(NAMES_STORAGE_KEY)
    if (stored) {
      savedNames.value = JSON.parse(stored)
    }
  } catch {
    savedNames.value = []
  }
}

// Save name to localStorage
const saveName = (name: string) => {
  if (typeof window === 'undefined') return
  const trimmed = name.trim()
  if (!trimmed || savedNames.value.includes(trimmed)) return

  // Add to beginning, limit to 5 names
  savedNames.value = [trimmed, ...savedNames.value.filter(n => n !== trimmed)].slice(0, 5)
  localStorage.setItem(NAMES_STORAGE_KEY, JSON.stringify(savedNames.value))
}

// Remove name from saved list
const removeName = (name: string) => {
  savedNames.value = savedNames.value.filter(n => n !== name)
  localStorage.setItem(NAMES_STORAGE_KEY, JSON.stringify(savedNames.value))
}

// Select a name from dropdown
const selectName = (name: string) => {
  playerName.value = name
  showNameDropdown.value = false
}

// Hide dropdown with delay (for click handling)
const hideDropdownDelayed = () => {
  setTimeout(() => {
    showNameDropdown.value = false
  }, 150)
}

const selectAgeGroup = (group: AgeGroup) => {
  sound.select()
  selectedAgeGroup.value = group
}

const goBack = () => {
  sound.click()
  router.push('/')
}

const startGame = () => {
  if (!canStart.value) return

  sound.matchStart()

  // Save the name for future use
  saveName(playerName.value)

  createSession(playerName.value.trim(), selectedAgeGroup.value!)

  setTimeout(() => {
    router.push('/game')
  }, 400)
}

onMounted(() => {
  loadSavedNames()
  // Pre-fill with last used name if available
  if (savedNames.value.length > 0) {
    playerName.value = savedNames.value[0]
  }
})
</script>

<style scoped>
.age-group-btn {
  @apply p-5 rounded-xl border-2 transition-all duration-200 text-left flex flex-col items-center text-center;
}

.age-icon {
  @apply w-16 h-16 rounded-2xl flex items-center justify-center mb-3;
}
</style>
