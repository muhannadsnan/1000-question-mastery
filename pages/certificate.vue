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
      id="certificate-card"
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

        <!-- Game Link -->
        <div class="mt-4 pt-4 border-t border-slate-100">
          <p class="text-xs text-slate-400">Play at</p>
          <p class="text-sm font-semibold text-primary-600">1000questionmastery.com</p>
        </div>
      </div>

      <!-- Certificate Border Bottom -->
      <div :class="['h-2', tierStyles[certificate?.tier || 'standard'].gradient]" />
    </div>

    <!-- Share Actions -->
    <div class="mt-8 text-center animate-slide-up" style="animation-delay: 300ms;">
      <p class="text-sm text-slate-500 mb-4">Share your achievement!</p>
      <div class="flex flex-wrap justify-center gap-3">
        <button @click="shareToTwitter" class="share-btn bg-black hover:bg-gray-800 text-white">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
          </svg>
        </button>

        <button @click="shareToFacebook" class="share-btn bg-[#1877F2] hover:bg-[#166FE5] text-white">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
        </button>

        <button @click="shareToWhatsApp" class="share-btn bg-[#25D366] hover:bg-[#20BD5A] text-white">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/>
          </svg>
        </button>

        <button @click="copyLink" class="share-btn bg-slate-600 hover:bg-slate-700 text-white">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Download & Actions -->
    <div class="flex flex-col sm:flex-row gap-4 mt-6 animate-slide-up" style="animation-delay: 400ms;">
      <button @click="downloadCertificate" class="btn-primary flex items-center justify-center gap-2">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        Download Certificate
      </button>

      <button @click="playAgain" class="btn-secondary flex items-center justify-center gap-2">
        <span>🔄</span>
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

    <!-- Toast -->
    <div
      v-if="showToast"
      class="fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-slate-800 text-white px-6 py-3 rounded-xl shadow-lg animate-slide-up z-50"
    >
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const sound = useSound()
const { getCertificateData, clearSession, loadSession } = useGameSession()

const certificateRef = ref<HTMLElement | null>(null)
const certificate = ref<ReturnType<typeof getCertificateData>>(null)
const showToast = ref(false)
const toastMessage = ref('')

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

const gameUrl = computed(() => {
  if (typeof window !== 'undefined') {
    return window.location.origin
  }
  return 'https://1000questionmastery.com'
})

const shareText = computed(() => {
  if (!certificate.value) return ''
  return `I just earned a ${certificate.value.tier.toUpperCase()} certificate on 1000 Question Mastery! ${certificate.value.score}/1000 correct (${certificate.value.percentage.toFixed(1)}%). Can you beat my score?`
})

const toast = (message: string) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

const downloadCertificate = async () => {
  sound.click()
  try {
    const html2canvas = (await import('html2canvas')).default
    const element = document.getElementById('certificate-card')
    if (!element) return

    const canvas = await html2canvas(element, {
      backgroundColor: '#ffffff',
      scale: 2,
    })

    const link = document.createElement('a')
    link.download = `certificate-${certificate.value?.playerName?.replace(/\s+/g, '-') || 'quiz'}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
    toast('Certificate downloaded!')
  } catch (error) {
    console.error('Failed to download:', error)
    window.print()
  }
}

const shareToTwitter = () => {
  sound.click()
  const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText.value)}&url=${encodeURIComponent(gameUrl.value)}`
  window.open(url, '_blank', 'width=600,height=400')
}

const shareToFacebook = () => {
  sound.click()
  const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(gameUrl.value)}&quote=${encodeURIComponent(shareText.value)}`
  window.open(url, '_blank', 'width=600,height=400')
}

const shareToWhatsApp = () => {
  sound.click()
  const url = `https://wa.me/?text=${encodeURIComponent(shareText.value + ' ' + gameUrl.value)}`
  window.open(url, '_blank')
}

const copyLink = async () => {
  sound.click()
  try {
    await navigator.clipboard.writeText(shareText.value + ' ' + gameUrl.value)
    toast('Copied to clipboard!')
  } catch {
    toast('Failed to copy')
  }
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
.share-btn {
  @apply w-12 h-12 rounded-full flex items-center justify-center transition-all transform hover:scale-110 shadow-lg;
}

@media print {
  body * {
    visibility: hidden;
  }
  #certificate-card,
  #certificate-card * {
    visibility: visible;
  }
  #certificate-card {
    position: absolute;
    left: 0;
    top: 0;
  }
}
</style>
