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
        <!-- Name Input -->
        <div class="mb-6">
          <label class="block text-sm font-medium text-slate-700 mb-2">
            Your Name
          </label>
          <input
            v-model="playerName"
            type="text"
            placeholder="Enter your name..."
            maxlength="30"
            class="w-full px-4 py-3 rounded-xl border-2 border-slate-200 focus:border-primary-500 focus:ring-4 focus:ring-primary-500/20 outline-none transition-all text-lg"
            @keyup.enter="startGame"
          />
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
                'p-4 rounded-xl border-2 transition-all duration-200 text-left',
                selectedAgeGroup === group.id
                  ? 'border-primary-500 bg-primary-50 shadow-lg shadow-primary-500/20'
                  : 'border-slate-200 hover:border-primary-300 hover:bg-slate-50'
              ]"
            >
              <div class="text-2xl mb-1">{{ group.icon }}</div>
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
            'w-full btn-success btn-lg',
            !canStart && 'opacity-50 cursor-not-allowed'
          ]"
        >
          <span class="mr-2">🚀</span>
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

const playerName = ref('')
const selectedAgeGroup = ref<AgeGroup | null>(null)

const ageGroups = [
  { id: 'kids' as AgeGroup, label: 'Kids', ageRange: '6-12 years', icon: '🧒' },
  { id: 'teens' as AgeGroup, label: 'Teens', ageRange: '13-17 years', icon: '🧑' },
  { id: 'adults' as AgeGroup, label: 'Adults', ageRange: '18-59 years', icon: '👨' },
  { id: 'seniors' as AgeGroup, label: 'Seniors', ageRange: '60+ years', icon: '👴' },
]

const canStart = computed(() => {
  return playerName.value.trim().length >= 2 && selectedAgeGroup.value !== null
})

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
</script>
