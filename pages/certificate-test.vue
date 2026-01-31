<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 py-8 bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
    <!-- Fireworks Canvas -->
    <canvas ref="fireworksCanvas" class="fixed inset-0 pointer-events-none z-10" />

    <!-- Ambient glow -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-amber-500/10 rounded-full blur-3xl" />
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl" />
    </div>

    <!-- Header -->
    <div class="text-center mb-6 animate-bounce-in relative z-20">
      <h1 class="text-2xl md:text-3xl font-bold text-white mb-2">Certificate Preview</h1>
      <p class="text-slate-400 text-sm">Test page for design preview</p>
    </div>

    <!-- Tier Selector -->
    <div class="flex gap-2 mb-6 z-20 animate-slide-up">
      <button
        v-for="tier in ['gold', 'silver', 'bronze', 'standard']"
        :key="tier"
        @click="selectedTier = tier; launchFireworks()"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-all capitalize text-sm',
          selectedTier === tier
            ? tierButtonStyles[tier]
            : 'bg-white/10 text-white/70 hover:bg-white/20'
        ]"
      >
        {{ tier }}
      </button>
    </div>

    <!-- Premium Certificate -->
    <div
      id="certificate-card"
      :class="[
        'w-full max-w-xl relative animate-slide-up z-20',
        'bg-gradient-to-br from-slate-50 via-white to-slate-100',
        'rounded-lg shadow-2xl overflow-hidden',
        tierStyles[selectedTier].outerRing
      ]"
    >
      <!-- Decorative Corner Ornaments -->
      <div class="absolute top-0 left-0 w-24 h-24 opacity-20">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[selectedTier].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>
      <div class="absolute top-0 right-0 w-24 h-24 opacity-20 rotate-90">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[selectedTier].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>
      <div class="absolute bottom-0 left-0 w-24 h-24 opacity-20 -rotate-90">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[selectedTier].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>
      <div class="absolute bottom-0 right-0 w-24 h-24 opacity-20 rotate-180">
        <svg viewBox="0 0 100 100" class="w-full h-full" :class="tierStyles[selectedTier].ornamentColor">
          <path d="M0,0 L100,0 L100,20 C60,20 20,60 20,100 L0,100 Z" fill="currentColor"/>
        </svg>
      </div>

      <!-- Top Border Gradient -->
      <div :class="['h-3', tierStyles[selectedTier].gradient]" />

      <!-- Inner decorative border -->
      <div class="m-4 p-6 border-2 border-dashed rounded" :class="tierStyles[selectedTier].innerBorder">
        <div class="text-center">
          <!-- Seal/Badge -->
          <div class="relative inline-block mb-4">
            <div :class="[
              'w-24 h-24 rounded-full flex items-center justify-center text-5xl',
              'shadow-xl ring-4',
              tierStyles[selectedTier].badge,
              tierStyles[selectedTier].ring
            ]">
              {{ tierStyles[selectedTier].icon }}
            </div>
            <!-- Ribbon effect -->
            <div class="absolute -bottom-2 left-1/2 -translate-x-1/2 flex gap-1">
              <div :class="['w-4 h-8 rounded-b-full', tierStyles[selectedTier].ribbonColor]" />
              <div :class="['w-4 h-6 rounded-b-full', tierStyles[selectedTier].ribbonColor]" />
            </div>
          </div>

          <!-- Certificate Header -->
          <div class="mt-4 mb-2">
            <p class="text-sm font-medium tracking-[0.3em] text-slate-400 uppercase">Certificate of</p>
          </div>
          <h3 :class="[
            'text-4xl md:text-5xl font-black tracking-wide mb-6',
            tierStyles[selectedTier].titleColor
          ]">
            {{ tierStyles[selectedTier].title }}
          </h3>

          <!-- Decorative Line -->
          <div class="flex items-center justify-center gap-4 mb-6">
            <div :class="['h-px w-16', tierStyles[selectedTier].lineColor]" />
            <div :class="['w-2 h-2 rotate-45', tierStyles[selectedTier].diamondColor]" />
            <div :class="['h-px w-16', tierStyles[selectedTier].lineColor]" />
          </div>

          <!-- Recipient -->
          <p class="text-slate-500 text-sm mb-1">This certifies that</p>
          <p class="text-3xl md:text-4xl font-bold text-slate-800 mb-2 font-serif italic">
            {{ testName }}
          </p>

          <!-- Achievement Text -->
          <p class="text-slate-500 mb-6 max-w-sm mx-auto">
            has successfully completed the<br />
            <span class="font-semibold text-slate-700">1000 Question Mastery Challenge</span>
          </p>

          <!-- Stats Section -->
          <div :class="['rounded-xl p-5 mb-6', tierStyles[selectedTier].statsBg]">
            <div class="grid grid-cols-3 gap-4">
              <div>
                <div :class="['text-3xl font-bold', tierStyles[selectedTier].statsText]">
                  {{ tierScores[selectedTier] }}
                </div>
                <div class="text-xs text-slate-500 uppercase tracking-wider mt-2">Correct</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-slate-800">
                  {{ tierPercentages[selectedTier] }}%
                </div>
                <div class="text-xs text-slate-500 uppercase tracking-wider mt-2">Accuracy</div>
              </div>
              <div>
                <div :class="['text-3xl font-bold capitalize', tierStyles[selectedTier].statsText]">
                  {{ selectedTier }}
                </div>
                <div class="text-xs text-slate-500 uppercase tracking-wider mt-2">Tier</div>
              </div>
            </div>
          </div>

          <!-- Date & Code -->
          <div class="text-sm text-slate-400 space-y-1">
            <p>{{ formattedDate }}</p>
            <p class="font-mono text-xs tracking-wider">QM-TEST1234</p>
          </div>

          <!-- Footer -->
          <div class="mt-6 pt-4 border-t border-slate-200">
            <p class="text-xs text-slate-400">1000 Question Mastery</p>
          </div>
        </div>
      </div>

      <!-- Bottom Border Gradient -->
      <div :class="['h-3', tierStyles[selectedTier].gradient]" />
    </div>

    <!-- Download Button -->
    <div class="mt-8 flex gap-4 animate-slide-up z-20" style="animation-delay: 200ms;">
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

const fireworksCanvas = ref<HTMLCanvasElement | null>(null)
const selectedTier = ref<'gold' | 'silver' | 'bronze' | 'standard'>('gold')
const showToast = ref(false)
const toastMessage = ref('')
const isDownloading = ref(false)

const testName = 'Test Player'

const tierScores = {
  gold: 920,
  silver: 800,
  bronze: 650,
  standard: 500,
}

const tierPercentages = {
  gold: 92,
  silver: 80,
  bronze: 65,
  standard: 50,
}

const tierButtonStyles = {
  gold: 'bg-gradient-to-r from-amber-500 to-yellow-500 text-white',
  silver: 'bg-gradient-to-r from-slate-400 to-slate-500 text-white',
  bronze: 'bg-gradient-to-r from-orange-500 to-orange-600 text-white',
  standard: 'bg-gradient-to-r from-primary-500 to-purple-500 text-white',
}

const tierStyles = {
  gold: {
    outerRing: 'ring-4 ring-amber-400/50',
    gradient: 'bg-gradient-to-r from-amber-500 via-yellow-400 to-amber-500',
    badge: 'bg-gradient-to-br from-amber-400 via-yellow-300 to-amber-500',
    ring: 'ring-amber-300',
    innerBorder: 'border-amber-300/50',
    ornamentColor: 'text-amber-400',
    titleColor: 'text-amber-600',
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
    titleColor: 'text-slate-600',
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
    titleColor: 'text-orange-600',
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
    titleColor: 'text-primary-600',
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
  return new Date().toLocaleDateString('en-US', {
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

    if (frameCount % 30 === 0 && frameCount < 150) {
      createFirework(
        100 + Math.random() * (canvas.width - 200),
        100 + Math.random() * (canvas.height / 2)
      )
    }

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i]
      p.x += p.vx
      p.y += p.vy
      p.vy += 0.05
      p.vx *= 0.99
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

  setTimeout(() => {
    cancelAnimationFrame(animationId)
    ctx.clearRect(0, 0, canvas.width, canvas.height)
  }, 6000)
}

const downloadCertificate = async () => {
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
    link.download = `certificate-${testName.replace(/\s+/g, '-')}-${selectedTier.value}.png`
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

const goHome = () => {
  router.push('/')
}

onMounted(() => {
  setTimeout(() => launchFireworks(), 500)
})
</script>
