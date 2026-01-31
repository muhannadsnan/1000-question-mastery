<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 py-8 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
    <!-- Fireworks Canvas -->
    <canvas ref="fireworksCanvas" class="fixed inset-0 pointer-events-none z-10" />

    <!-- Ambient glow -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
    </div>

    <!-- Celebration Header -->
    <div class="text-center mb-8 animate-bounce-in relative z-20">
      <div class="text-6xl mb-4">🎉</div>
      <h1 class="text-3xl md:text-4xl font-bold text-white mb-2">Congratulations!</h1>
      <p class="text-slate-300">You've completed the 1000 Question Mastery Challenge!</p>
    </div>

    <!-- Premium Certificate -->
    <div
      id="certificate-card"
      :class="[
        'w-full max-w-xl relative animate-slide-up z-20',
        'bg-gradient-to-br from-slate-50 via-white to-slate-100',
        'rounded-lg shadow-2xl overflow-hidden',
        tierStyles[certificate?.tier || 'standard'].outerRing
      ]"
      style="animation-delay: 200ms;"
    >
      <!-- Decorative Corner Ornaments -->
      <div class="absolute top-0 left-0 w-24 h-24 opacity-20">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[certificate?.tier || 'standard'].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>
      <div class="absolute top-0 right-0 w-24 h-24 opacity-20 rotate-90">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[certificate?.tier || 'standard'].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>
      <div class="absolute bottom-0 left-0 w-24 h-24 opacity-20 -rotate-90">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[certificate?.tier || 'standard'].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>
      <div class="absolute bottom-0 right-0 w-24 h-24 opacity-20 rotate-180">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[certificate?.tier || 'standard'].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>

      <!-- Top Border Gradient -->
      <div :class="['h-3', tierStyles[certificate?.tier || 'standard'].gradient]" />

      <!-- Inner decorative border -->
      <div class="m-4 p-6 border-2 border-dashed rounded" :class="tierStyles[certificate?.tier || 'standard'].innerBorder">
        <div class="text-center">
          <!-- Seal/Badge -->
          <div class="relative inline-block mb-4">
            <div :class="[
              'w-24 h-24 rounded-full flex items-center justify-center text-5xl',
              'shadow-xl ring-4',
              tierStyles[certificate?.tier || 'standard'].badge,
              tierStyles[certificate?.tier || 'standard'].ring
            ]">
              {{ tierStyles[certificate?.tier || 'standard'].icon }}
            </div>
            <!-- Ribbon effect -->
            <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 flex gap-1">
              <div :class="['w-4 h-8 rounded-b-full', tierStyles[certificate?.tier || 'standard'].ribbonColor]" />
              <div :class="['w-4 h-6 rounded-b-full', tierStyles[certificate?.tier || 'standard'].ribbonColor]" />
            </div>
          </div>

          <!-- Certificate Header -->
          <div class="mt-4 mb-2">
            <p class="text-sm font-medium tracking-[0.3em] text-slate-400 uppercase">Certificate of</p>
          </div>
          <h3 :class="[
            'text-4xl md:text-5xl font-black tracking-wide mb-6',
            tierStyles[certificate?.tier || 'standard'].titleGradient
          ]">
            {{ tierStyles[certificate?.tier || 'standard'].title }}
          </h3>

          <!-- Decorative Line -->
          <div class="flex items-center justify-center gap-4 mb-6">
            <div :class="['h-px w-16', tierStyles[certificate?.tier || 'standard'].lineColor]" />
            <div :class="['w-2 h-2 rotate-45', tierStyles[certificate?.tier || 'standard'].diamondColor]" />
            <div :class="['h-px w-16', tierStyles[certificate?.tier || 'standard'].lineColor]" />
          </div>

          <!-- Recipient -->
          <p class="text-slate-500 text-sm mb-1">This certifies that</p>
          <p class="text-3xl md:text-4xl font-bold text-slate-800 mb-2 font-serif italic">
            {{ certificate?.playerName }}
          </p>

          <!-- Achievement Text -->
          <p class="text-slate-500 mb-6 max-w-sm mx-auto">
            has successfully completed the<br />
            <span class="font-semibold text-slate-700">1000 Question Mastery Challenge</span>
          </p>

          <!-- Stats Section -->
          <div :class="['rounded-xl p-5 mb-6', tierStyles[certificate?.tier || 'standard'].statsBg]">
            <div class="grid grid-cols-3 gap-4">
              <div>
                <div :class="['text-3xl font-bold', tierStyles[certificate?.tier || 'standard'].statsText]">
                  {{ certificate?.score }}
                </div>
                <div class="text-xs text-slate-500 uppercase tracking-wider">Correct</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-slate-800">
                  {{ certificate?.percentage?.toFixed(1) }}%
                </div>
                <div class="text-xs text-slate-500 uppercase tracking-wider">Accuracy</div>
              </div>
              <div>
                <div :class="['text-3xl font-bold capitalize', tierStyles[certificate?.tier || 'standard'].statsText]">
                  {{ certificate?.tier }}
                </div>
                <div class="text-xs text-slate-500 uppercase tracking-wider">Tier</div>
              </div>
            </div>
          </div>

          <!-- Date & Code -->
          <div class="text-sm text-slate-400 space-y-1">
            <p>{{ formattedDate }}</p>
            <p class="font-mono text-xs tracking-wider">{{ certificate?.code }}</p>
          </div>

          <!-- Footer -->
          <div class="mt-6 pt-4 border-t border-slate-200">
            <p class="text-xs text-slate-400">1000 Question Mastery</p>
          </div>
        </div>
      </div>

      <!-- Bottom Border Gradient -->
      <div :class="['h-3', tierStyles[certificate?.tier || 'standard'].gradient]" />
    </div>

    <!-- Download Button -->
    <div class="mt-8 flex flex-col sm:flex-row gap-4 animate-slide-up z-20" style="animation-delay: 400ms;">
      <button
        @click="downloadCertificate"
        :disabled="isDownloading"
        class="btn-lg px-8 py-4 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white rounded-xl font-semibold shadow-lg shadow-amber-500/30 transition-all transform hover:scale-105 flex items-center justify-center gap-3 disabled:opacity-50"
      >
        <svg v-if="!isDownloading" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        <svg v-else class="w-6 h-6 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
        {{ isDownloading ? 'Downloading...' : 'Download Certificate' }}
      </button>

      <button @click="playAgain" class="btn-secondary btn-lg flex items-center justify-center gap-2 bg-white/10 border-white/20 text-white hover:bg-white/20">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        Play Again
      </button>
    </div>

    <!-- Home Link -->
    <button
      @click="goHome"
      class="mt-6 text-slate-400 hover:text-white transition-colors z-20"
    >
      Back to Home
    </button>

    <!-- Toast -->
    <div
      v-if="showToast"
      class="fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-white text-slate-800 px-6 py-3 rounded-xl shadow-lg animate-slide-up z-50"
    >
      {{ toastMessage }}
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const sound = useSound()
const { getCertificateData, clearSession, loadSession } = useGameSession()

const fireworksCanvas = ref<HTMLCanvasElement | null>(null)
const certificate = ref<ReturnType<typeof getCertificateData>>(null)
const showToast = ref(false)
const toastMessage = ref('')
const isDownloading = ref(false)

const tierStyles = {
  gold: {
    outerRing: 'ring-4 ring-amber-400/50',
    gradient: 'bg-gradient-to-r from-amber-500 via-yellow-400 to-amber-500',
    badge: 'bg-gradient-to-br from-amber-400 via-yellow-300 to-amber-500',
    ring: 'ring-amber-300',
    innerBorder: 'border-amber-300/50',
    ornamentColor: 'text-amber-400',
    titleGradient: 'bg-gradient-to-r from-amber-600 via-yellow-500 to-amber-600 bg-clip-text text-transparent',
    title: 'MASTERY',
    icon: '🏆',
    lineColor: 'bg-amber-300',
    diamondColor: 'bg-amber-400',
    ribbonColor: 'bg-amber-500',
    statsBg: 'bg-amber-50',
    statsText: 'text-amber-600',
  },
  silver: {
    outerRing: 'ring-4 ring-slate-400/50',
    gradient: 'bg-gradient-to-r from-slate-400 via-slate-300 to-slate-400',
    badge: 'bg-gradient-to-br from-slate-300 via-slate-200 to-slate-400',
    ring: 'ring-slate-300',
    innerBorder: 'border-slate-300/50',
    ornamentColor: 'text-slate-400',
    titleGradient: 'bg-gradient-to-r from-slate-600 via-slate-500 to-slate-600 bg-clip-text text-transparent',
    title: 'EXCELLENCE',
    icon: '🥈',
    lineColor: 'bg-slate-300',
    diamondColor: 'bg-slate-400',
    ribbonColor: 'bg-slate-500',
    statsBg: 'bg-slate-100',
    statsText: 'text-slate-600',
  },
  bronze: {
    outerRing: 'ring-4 ring-orange-400/50',
    gradient: 'bg-gradient-to-r from-orange-500 via-orange-400 to-orange-500',
    badge: 'bg-gradient-to-br from-orange-400 via-orange-300 to-orange-500',
    ring: 'ring-orange-300',
    innerBorder: 'border-orange-300/50',
    ornamentColor: 'text-orange-400',
    titleGradient: 'bg-gradient-to-r from-orange-600 via-orange-500 to-orange-600 bg-clip-text text-transparent',
    title: 'ACHIEVEMENT',
    icon: '🥉',
    lineColor: 'bg-orange-300',
    diamondColor: 'bg-orange-400',
    ribbonColor: 'bg-orange-500',
    statsBg: 'bg-orange-50',
    statsText: 'text-orange-600',
  },
  standard: {
    outerRing: 'ring-4 ring-primary-400/50',
    gradient: 'bg-gradient-to-r from-primary-500 via-purple-500 to-primary-500',
    badge: 'bg-gradient-to-br from-primary-400 via-purple-400 to-primary-500',
    ring: 'ring-primary-300',
    innerBorder: 'border-primary-300/50',
    ornamentColor: 'text-primary-400',
    titleGradient: 'bg-gradient-to-r from-primary-600 via-purple-500 to-primary-600 bg-clip-text text-transparent',
    title: 'COMPLETION',
    icon: '🎓',
    lineColor: 'bg-primary-300',
    diamondColor: 'bg-primary-400',
    ribbonColor: 'bg-primary-500',
    statsBg: 'bg-primary-50',
    statsText: 'text-primary-600',
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

const toast = (message: string) => {
  toastMessage.value = message
  showToast.value = true
  setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Fireworks animation
const launchFireworks = () => {
  const canvas = fireworksCanvas.value
  if (!canvas) return

  const ctx = canvas.getContext('2d')
  if (!ctx) return

  canvas.width = window.innerWidth
  canvas.height = window.innerHeight

  interface Particle {
    x: number
    y: number
    vx: number
    vy: number
    color: string
    life: number
    maxLife: number
  }

  const particles: Particle[] = []
  const colors = ['#FFD700', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

  const createFirework = (x: number, y: number) => {
    const particleCount = 60
    const color = colors[Math.floor(Math.random() * colors.length)]

    for (let i = 0; i < particleCount; i++) {
      const angle = (Math.PI * 2 * i) / particleCount
      const speed = 2 + Math.random() * 4
      particles.push({
        x,
        y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        color,
        life: 1,
        maxLife: 60 + Math.random() * 40,
      })
    }
  }

  let animationId: number
  let frameCount = 0

  const animate = () => {
    ctx.fillStyle = 'rgba(0, 0, 0, 0.1)'
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    // Launch new fireworks periodically
    if (frameCount % 30 === 0 && frameCount < 150) {
      createFirework(
        100 + Math.random() * (canvas.width - 200),
        100 + Math.random() * (canvas.height / 2)
      )
    }

    // Update and draw particles
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i]
      p.x += p.vx
      p.y += p.vy
      p.vy += 0.05 // gravity
      p.vx *= 0.99 // friction
      p.life++

      const alpha = 1 - p.life / p.maxLife
      if (alpha <= 0) {
        particles.splice(i, 1)
        continue
      }

      ctx.beginPath()
      ctx.arc(p.x, p.y, 3 * alpha, 0, Math.PI * 2)
      ctx.fillStyle = p.color + Math.floor(alpha * 255).toString(16).padStart(2, '0')
      ctx.fill()
    }

    frameCount++

    if (frameCount < 300 || particles.length > 0) {
      animationId = requestAnimationFrame(animate)
    } else {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    }
  }

  animate()

  // Cleanup after animation
  setTimeout(() => {
    cancelAnimationFrame(animationId)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
  }, 6000)
}

const downloadCertificate = async () => {
  sound.click()
  isDownloading.value = true

  try {
    const html2canvas = (await import('html2canvas')).default
    const element = document.getElementById('certificate-card')
    if (!element) return

    const canvas = await html2canvas(element, {
      backgroundColor: '#ffffff',
      scale: 2,
      logging: false,
    })

    const link = document.createElement('a')
    link.download = `certificate-${certificate.value?.playerName?.replace(/\s+/g, '-') || 'quiz'}.png`
    link.href = canvas.toDataURL('image/png')
    link.click()
    toast('Certificate downloaded!')
  } catch (error) {
    console.error('Failed to download:', error)
    toast('Failed to download. Try again.')
  } finally {
    isDownloading.value = false
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

  // Play victory sound and launch fireworks
  setTimeout(() => {
    sound.victory()
    launchFireworks()
  }, 500)
})
</script>

<style scoped>
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
