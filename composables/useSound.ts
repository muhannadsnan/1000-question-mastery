// Sound effects using Web Audio API - lightweight, no files needed
export const useSound = () => {
  let audioContext: AudioContext | null = null

  const getContext = () => {
    if (!audioContext && typeof window !== 'undefined') {
      audioContext = new (window.AudioContext || (window as any).webkitAudioContext)()
    }
    return audioContext
  }

  const playTone = (
    frequency: number,
    duration: number,
    type: OscillatorType = 'sine',
    volume: number = 0.3,
    fadeOut: boolean = true
  ) => {
    const ctx = getContext()
    if (!ctx) return

    const oscillator = ctx.createOscillator()
    const gainNode = ctx.createGain()

    oscillator.connect(gainNode)
    gainNode.connect(ctx.destination)

    oscillator.type = type
    oscillator.frequency.setValueAtTime(frequency, ctx.currentTime)

    gainNode.gain.setValueAtTime(volume, ctx.currentTime)
    if (fadeOut) {
      gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration)
    }

    oscillator.start(ctx.currentTime)
    oscillator.stop(ctx.currentTime + duration)
  }

  const playChord = (frequencies: number[], duration: number, volume: number = 0.15) => {
    frequencies.forEach((freq, i) => {
      setTimeout(() => playTone(freq, duration, 'sine', volume), i * 30)
    })
  }

  // Sound effects
  const sounds = {
    // Game loads - welcoming chime
    gameLoad: () => {
      const ctx = getContext()
      if (!ctx) return
      playChord([523.25, 659.25, 783.99], 0.4, 0.12) // C major chord
      setTimeout(() => playTone(1046.50, 0.3, 'sine', 0.15), 200) // High C
    },

    // Match starts - ascending triumphant
    matchStart: () => {
      const notes = [261.63, 329.63, 392.00, 523.25] // C E G C
      notes.forEach((freq, i) => {
        setTimeout(() => playTone(freq, 0.15, 'triangle', 0.2), i * 80)
      })
    },

    // Correct answer - happy ding
    correct: () => {
      playTone(880, 0.1, 'sine', 0.2)
      setTimeout(() => playTone(1108.73, 0.15, 'sine', 0.25), 80)
      setTimeout(() => playTone(1318.51, 0.2, 'sine', 0.2), 160)
    },

    // Wrong answer - gentle low tone
    wrong: () => {
      playTone(220, 0.15, 'triangle', 0.2)
      setTimeout(() => playTone(185, 0.25, 'triangle', 0.15), 100)
    },

    // Next question - subtle click/whoosh
    nextQuestion: () => {
      playTone(600, 0.05, 'sine', 0.1)
      setTimeout(() => playTone(800, 0.08, 'sine', 0.15), 30)
    },

    // Level up - celebratory fanfare
    levelUp: () => {
      const fanfare = [
        { freq: 392.00, delay: 0 },     // G
        { freq: 523.25, delay: 100 },   // C
        { freq: 659.25, delay: 200 },   // E
        { freq: 783.99, delay: 300 },   // G
        { freq: 1046.50, delay: 450 },  // High C
      ]
      fanfare.forEach(({ freq, delay }) => {
        setTimeout(() => playTone(freq, 0.25, 'triangle', 0.2), delay)
      })
      // Add sparkle
      setTimeout(() => playChord([1318.51, 1567.98, 2093.00], 0.4, 0.1), 500)
    },

    // Game complete - victory theme
    victory: () => {
      const melody = [
        { freq: 523.25, delay: 0, dur: 0.15 },
        { freq: 523.25, delay: 150, dur: 0.15 },
        { freq: 523.25, delay: 300, dur: 0.15 },
        { freq: 523.25, delay: 450, dur: 0.4 },
        { freq: 415.30, delay: 600, dur: 0.15 },
        { freq: 466.16, delay: 750, dur: 0.15 },
        { freq: 523.25, delay: 900, dur: 0.15 },
        { freq: 466.16, delay: 1050, dur: 0.1 },
        { freq: 523.25, delay: 1150, dur: 0.5 },
      ]
      melody.forEach(({ freq, delay, dur }) => {
        setTimeout(() => playTone(freq, dur, 'triangle', 0.2), delay)
      })
    },

    // Button hover - subtle
    hover: () => {
      playTone(1200, 0.03, 'sine', 0.05)
    },

    // Button click
    click: () => {
      playTone(800, 0.05, 'sine', 0.1)
    },

    // Select option
    select: () => {
      playTone(500, 0.08, 'sine', 0.15)
      setTimeout(() => playTone(700, 0.06, 'sine', 0.1), 50)
    },
  }

  return sounds
}
