<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 py-8 bg-gradient-to-br from-amber-50 via-white to-purple-50">
    <!-- Celebration Header -->
    <div class="text-center mb-8 animate-bounce-in">
      <div class="text-6xl mb-4">🎉</div>
      <h1 class="text-3xl md:text-4xl font-bold text-slate-800 mb-2">Congratulations!</h1>
      <p class="text-slate-600">You've completed the 1000 Question Mastery Challenge!</p>
    </div>

    <!-- Certificate -->
    <div
      ref="certificateRef"
      :class="[
        'w-full max-w-lg bg-white rounded-2xl shadow-2xl overflow-hidden animate-slide-up',
        tierStyles[certificate?.tier || 'standard'].border
      ]"
      style="animation-delay: 200ms;"
    >
      <!-- Certificate Border Top -->
      <div :class="['h-2', tierStyles[certificate?.tier || 'standard'].gradient]" />

      <div class="p-8 text-center">
        <!-- Badge -->
        <div :class="[
          'w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center text-4xl',
          tierStyles[certificate?.tier || 'standard'].badge
        ]">
          {{ tierStyles[certificate?.tier || 'standard'].icon }}
        </div>

        <!-- Title -->
        <h2 class="text-2xl font-bold text-slate-400 uppercase tracking-widest mb-1">Certificate of</h2>
        <h3 :class="['text-4xl font-extrabold mb-6', tierStyles[certificate?.tier || 'standard'].text]">
          {{ tierStyles[certificate?.tier || 'standard'].title }}
        </h3>

        <!-- Divider -->
        <div class="w-24 h-1 bg-slate-200 mx-auto mb-6 rounded-full" />

        <!-- Name -->
        <p class="text-slate-500 mb-1">This certifies that</p>
        <p class="text-3xl font-bold text-slate-800 mb-4">{{ certificate?.playerName }}</p>

        <!-- Achievement -->
        <p class="text-slate-500 mb-6">
          has successfully completed the<br />
          <span class="font-semibold text-slate-700">1000 Question Mastery Challenge</span>
        </p>

        <!-- Stats -->
        <div class="bg-slate-50 rounded-xl p-4 mb-6">
          <div class="grid grid-cols-3 gap-4">
            <div>
              <div class="text-2xl font-bold text-primary-600">{{ certificate?.score }}</div>
              <div class="text-xs text-slate-500">Correct</div>
            </div>
            <div>
              <div class="text-2xl font-bold text-slate-800">{{ certificate?.percentage?.toFixed(1) }}%</div>
              <div class="text-xs text-slate-500">Accuracy</div>
            </div>
            <div>
              <div :class="['text-2xl font-bold capitalize', tierStyles[certificate?.tier || 'standard'].text]">
                {{ certificate?.tier }}
              </div>
              <div class="text-xs text-slate-500">Tier</div>
            </div>
          </div>
        </div>

        <!-- Date & Code -->
        <div class="text-sm text-slate-400">
          <p>{{ formattedDate }}</p>
          <p class="font-mono mt-1">{{ certificate?.code }}</p>
        </div>
      </div>

      <!-- Certificate Border Bottom -->
      <div :class="['h-2', tierStyles[certificate?.tier || 'standard'].gradient]" />
    </div>

    <!-- Actions -->
    <div class="flex flex-col sm:flex-row gap-4 mt-8 animate-slide-up" style="animation-delay: 400ms;">
      <button @click="downloadCertificate" class="btn-primary">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Download Certificate
      </button>

      <button @click="playAgain" class="btn-secondary">
        <span class="mr-2">🔄</span>
        Play Again
      </button>
    </div>

    <!-- Home Link -->
    <button
      @click="goHome"
      class="mt-6 text-slate-500 hover:text-slate-700 transition-colors"
    >
      Back to Home
    </button>

    <!-- Confetti Background -->
    <div class="fixed inset-0 pointer-events-none z-0 overflow-hidden">
      <div
        v-for="i in 30"
        :key="i"
        class="confetti-particle"
        :style="{
          left: `${Math.random() * 100}%`,
          backgroundColor: ['#FFD700', '#C0C0C0', '#CD7F32', '#3B82F6', '#8B5CF6'][i % 5],
          animationDelay: `${Math.random() * 3}s`,
          animationDuration: `${3 + Math.random() * 3}s`
        }"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const sound = useSound()
const { getCertificateData, clearSession, loadSession } = useGameSession()

const certificateRef = ref<HTMLElement | null>(null)

const certificate = ref<ReturnType<typeof getCertificateData>>(null)

const tierStyles = {
  gold: {
    border: 'ring-4 ring-amber-400',
    gradient: 'bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-400',
    badge: 'bg-gradient-to-br from-amber-400 to-yellow-500',
    text: 'text-amber-600',
    icon: '🏆',
    title: 'MASTERY',
  },
  silver: {
    border: 'ring-4 ring-slate-400',
    gradient: 'bg-gradient-to-r from-slate-400 via-slate-300 to-slate-400',
    badge: 'bg-gradient-to-br from-slate-400 to-slate-500',
    text: 'text-slate-600',
    icon: '🥈',
    title: 'EXCELLENCE',
  },
  bronze: {
    border: 'ring-4 ring-orange-400',
    gradient: 'bg-gradient-to-r from-orange-400 via-orange-300 to-orange-400',
    badge: 'bg-gradient-to-br from-orange-400 to-orange-600',
    text: 'text-orange-600',
    icon: '🥉',
    title: 'ACHIEVEMENT',
  },
  standard: {
    border: 'ring-2 ring-slate-200',
    gradient: 'bg-gradient-to-r from-primary-400 via-purple-400 to-primary-400',
    badge: 'bg-gradient-to-br from-primary-400 to-purple-500',
    text: 'text-primary-600',
    icon: '🎓',
    title: 'COMPLETION',
  },
}

const formattedDate = computed(() => {
  if (!certificate.value?.completedAt) return ''
  return new Date(certificate.value.completedAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
})

const downloadCertificate = async () => {
  sound.click()
  // Simple approach: use browser print
  window.print()
}

const playAgain = () => {
  sound.click()
  clearSession()
  router.push('/setup')
}

const goHome = () => {
  sound.click()
  clearSession()
  router.push('/')
}

onMounted(() => {
  loadSession()
  certificate.value = getCertificateData()

  if (!certificate.value) {
    router.push('/')
    return
  }

  // Play victory sound
  setTimeout(() => sound.victory(), 500)
})
</script>

<style scoped>
@media print {
  body * {
    visibility: hidden;
  }
  .certificate-ref,
  .certificate-ref * {
    visibility: visible;
  }
  .certificate-ref {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>
