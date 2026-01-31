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
                <component :is="group.iconComponent" class="w-6 h-6" :class="group.iconColor" />
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

// Icon components as render functions
const BabyIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" stroke-width="2"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c-4 0-7 2-7 5v3h14v-3c0-3-3-5-7-5z"/></svg>`
}

const ChildIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>`
}

const TeenIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>`
}

const AdultIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>`
}

const SeniorIcon = {
  template: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/></svg>`
}

const ageGroups = [
  {
    id: 'littleKids' as AgeGroup,
    label: 'Little Kids',
    ageRange: '3-7 years',
    iconComponent: BabyIcon,
    iconBg: 'bg-pink-100',
    iconColor: 'text-pink-600'
  },
  {
    id: 'kids' as AgeGroup,
    label: 'Kids',
    ageRange: '8-12 years',
    iconComponent: ChildIcon,
    iconBg: 'bg-blue-100',
    iconColor: 'text-blue-600'
  },
  {
    id: 'teens' as AgeGroup,
    label: 'Teens',
    ageRange: '13-17 years',
    iconComponent: TeenIcon,
    iconBg: 'bg-purple-100',
    iconColor: 'text-purple-600'
  },
  {
    id: 'adults' as AgeGroup,
    label: 'Adults',
    ageRange: '18-35 years',
    iconComponent: AdultIcon,
    iconBg: 'bg-emerald-100',
    iconColor: 'text-emerald-600'
  },
  {
    id: 'seniors' as AgeGroup,
    label: 'Seniors',
    ageRange: '35+ years',
    iconComponent: SeniorIcon,
    iconBg: 'bg-amber-100',
    iconColor: 'text-amber-600'
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
  @apply p-4 rounded-xl border-2 transition-all duration-200 text-left flex flex-col items-center text-center;
}

.age-icon {
  @apply w-12 h-12 rounded-full flex items-center justify-center mb-2;
}
</style>
