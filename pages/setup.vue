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
              @focus="showNameDropdown = savedPlayers.length > 0"
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

          <!-- Saved Players Dropdown -->
          <div
            v-if="showNameDropdown && savedPlayers.length > 0"
            class="mt-2 bg-white rounded-xl border border-slate-200 shadow-lg overflow-hidden z-10"
          >
            <div class="px-3 py-2 bg-slate-50 border-b border-slate-100">
              <span class="text-xs font-medium text-slate-500">Recent players</span>
            </div>
            <div class="max-h-48 overflow-y-auto">
              <div
                v-for="player in savedPlayers"
                :key="player.name"
                class="flex items-center justify-between px-4 py-3 hover:bg-slate-50 cursor-pointer group"
                @mousedown.prevent="selectName(player.name)"
              >
                <div class="flex-1">
                  <div class="text-slate-700 font-medium">{{ player.name }}</div>
                  <div class="text-xs text-slate-500 flex items-center gap-2">
                    <span v-if="player.gamesPlayed">{{ player.gamesPlayed }} games</span>
                    <span v-if="player.certificates" class="text-amber-600">{{ player.certificates }} 🏆</span>
                  </div>
                </div>
                <button
                  @mousedown.prevent.stop="removeSavedPlayer(player.name)"
                  class="text-slate-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Selected Player Stats -->
          <div v-if="selectedPlayerStats && selectedPlayerStats.gamesPlayed > 0" class="mt-3 p-3 bg-slate-50 rounded-lg">
            <div class="text-xs text-slate-500 mb-1">Player Stats</div>
            <div class="flex items-center gap-4 text-sm">
              <span class="text-slate-700">{{ selectedPlayerStats.gamesPlayed }} games</span>
              <span class="text-amber-600">{{ selectedPlayerStats.certificates }} 🏆</span>
              <span v-if="selectedPlayerStats.bestPercentage" class="text-green-600">Best: {{ selectedPlayerStats.bestPercentage }}%</span>
            </div>
          </div>
        </div>

        <!-- Mastery Level Selection -->
        <div class="mb-8">
          <label class="block text-sm font-medium text-slate-700 mb-3">
            Select Mastery Level
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
        Complete {{ selectedAgeGroup ? questionCountForAge : 'all' }} questions to earn your certificate
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AgeGroup } from '~/types'
import { getTotalQuestionsForAgeGroup } from '~/composables/useGameSession'
import { usePlayerProgress } from '~/composables/usePlayerProgress'

const router = useRouter()
const sound = useSound()
const { createSession } = useGameSession()
const { getPlayersWithStats, getPlayerStats, removePlayer } = usePlayerProgress()

// Get question count for selected age group
const questionCountForAge = computed(() => {
  if (!selectedAgeGroup.value) return 0
  return getTotalQuestionsForAgeGroup(selectedAgeGroup.value)
})

const playerName = ref('')
const selectedAgeGroup = ref<AgeGroup | null>(null)
const savedPlayers = ref<{ name: string; gamesPlayed: number; certificates: number; lastPlayed: string }[]>([])
const showNameDropdown = ref(false)
const nameInputRef = ref<HTMLInputElement | null>(null)

// Selected player stats
const selectedPlayerStats = computed(() => {
  if (!playerName.value.trim()) return null
  return getPlayerStats(playerName.value)
})

const ageGroups = [
  {
    id: 'kids' as AgeGroup,
    label: 'Kid',
    ageRange: '100 Questions',
    emoji: '🎈',
    iconBg: 'bg-blue-100',
  },
  {
    id: 'adults' as AgeGroup,
    label: 'Grown Up',
    ageRange: '300 Questions',
    emoji: '🏆',
    iconBg: 'bg-amber-100',
  },
]

const canStart = computed(() => {
  return playerName.value.trim().length >= 2 && selectedAgeGroup.value !== null
})

// Load saved players from progress storage
const loadSavedPlayers = () => {
  if (typeof window === 'undefined') return
  savedPlayers.value = getPlayersWithStats()
}

// Remove a player from saved list
const removeSavedPlayer = (name: string) => {
  removePlayer(name)
  savedPlayers.value = getPlayersWithStats()
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

  createSession(playerName.value.trim(), selectedAgeGroup.value!)

  setTimeout(() => {
    router.push('/game')
  }, 400)
}

onMounted(() => {
  loadSavedPlayers()
  // Pre-fill with last used player name if available
  if (savedPlayers.value.length > 0) {
    playerName.value = savedPlayers.value[0].name
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
