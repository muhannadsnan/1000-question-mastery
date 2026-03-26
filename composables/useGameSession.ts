import type { AgeGroup, Difficulty, QuestionCategory } from '~/types'
import { useQuestions } from './useQuestions'

export interface Question {
  id: string
  text: string
  options: [string, string, string, string]
  correctIndex: 0 | 1 | 2 | 3
  difficulty: Difficulty
  category: QuestionCategory | string
}

export interface GameSession {
  id: string
  playerName: string
  ageGroup: AgeGroup
  currentQuestion: number
  correctAnswers: number
  wrongAnswers: number
  startedAt: string
  askedQuestionIds: string[]
  cooldowns: Record<string, string>
  pendingQuestion?: Question | null // Store the current unanswered question
}

// Total questions per age group
const TOTAL_QUESTIONS: Record<AgeGroup, number> = {
  kids: 100,
  adults: 300,
}

// Questions per level: L1-3: 10ea, L4-6: 15ea, L7-9: 6ea, L10: 7  (=100 for kids)
// Grown ups: same ratio x3  (=300 for adults)
const LEVEL_SIZES_BASE = [10, 10, 10, 15, 15, 15, 6, 6, 6, 7] // sums to 100

// Build cumulative breakpoints for each age group
function buildLevelBreakpoints(multiplier: number): number[] {
  const cumulative: number[] = []
  let sum = 0
  for (const size of LEVEL_SIZES_BASE) {
    sum += size * multiplier
    cumulative.push(sum)
  }
  return cumulative
}

const LEVEL_BREAKPOINTS: Record<AgeGroup, number[]> = {
  kids: buildLevelBreakpoints(1),   // [10,20,30,45,60,75,81,87,93,100]
  adults: buildLevelBreakpoints(3), // [30,60,90,135,180,225,243,261,279,300]
}

const STORAGE_KEY = 'quiz-mastery-session'

export const useGameSession = () => {
  const session = useState<GameSession | null>('gameSession', () => null)
  const currentQuestionData = useState<Question | null>('currentQuestion', () => null)
  const isLoading = useState('isLoading', () => false)
  const isAnswerRevealed = useState('isAnswerRevealed', () => false)
  const selectedAnswer = useState<number | null>('selectedAnswer', () => null)
  const lastAnswerCorrect = useState<boolean | null>('lastAnswerCorrect', () => null)
  const previousLevel = useState<number>('previousLevel', () => 1)

  // Get total questions for current age group
  const totalQuestions = computed(() => {
    if (!session.value) return 300 // default
    return TOTAL_QUESTIONS[session.value.ageGroup] || 300
  })

  // Calculate current difficulty level based on progress using custom breakpoints
  const currentLevel = computed(() => {
    if (!session.value) return 1
    const breakpoints = LEVEL_BREAKPOINTS[session.value.ageGroup] || LEVEL_BREAKPOINTS.adults
    const q = session.value.currentQuestion
    for (let i = 0; i < breakpoints.length; i++) {
      if (q <= breakpoints[i]) return (i + 1) as Difficulty
    }
    return 10 as Difficulty
  })

  // Check if player leveled up
  const didLevelUp = computed(() => {
    return currentLevel.value > previousLevel.value
  })

  // Progress percentage
  const progressPercent = computed(() => {
    if (!session.value) return 0
    return ((session.value.currentQuestion - 1) / totalQuestions.value) * 100
  })

  // Accuracy percentage
  const accuracy = computed(() => {
    if (!session.value) return 0
    const total = session.value.correctAnswers + session.value.wrongAnswers
    if (total === 0) return 0
    return Math.round((session.value.correctAnswers / total) * 100)
  })

  // Load session from localStorage
  const loadSession = () => {
    if (typeof window === 'undefined') return null
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored) {
      try {
        session.value = JSON.parse(stored)
        previousLevel.value = currentLevel.value
        return session.value
      } catch {
        return null
      }
    }
    return null
  }

  // Save session to localStorage
  const saveSession = () => {
    if (typeof window === 'undefined' || !session.value) return
    localStorage.setItem(STORAGE_KEY, JSON.stringify(session.value))
  }

  // Create new session
  const createSession = (playerName: string, ageGroup: AgeGroup): GameSession => {
    const newSession: GameSession = {
      id: crypto.randomUUID(),
      playerName,
      ageGroup,
      currentQuestion: 1,
      correctAnswers: 0,
      wrongAnswers: 0,
      startedAt: new Date().toISOString(),
      askedQuestionIds: [],
      cooldowns: {},
    }
    session.value = newSession
    previousLevel.value = 1
    saveSession()
    return newSession
  }

  // Fetch next question (client-side)
  const fetchQuestion = async () => {
    if (!session.value) return null

    isLoading.value = true
    isAnswerRevealed.value = false
    selectedAnswer.value = null
    lastAnswerCorrect.value = null

    try {
      // Check if there's a pending question (player quit without answering)
      // Only use pending question if it hasn't been answered yet (not in askedQuestionIds)
      if (session.value.pendingQuestion) {
        const pendingId = session.value.pendingQuestion.id
        const alreadyAnswered = session.value.askedQuestionIds.includes(pendingId)

        if (!alreadyAnswered) {
          currentQuestionData.value = session.value.pendingQuestion
          isLoading.value = false
          return session.value.pendingQuestion
        } else {
          // Clear the stale pending question
          session.value.pendingQuestion = null
        }
      }

      const { getQuestion } = useQuestions()
      const question = await getQuestion(
        session.value.ageGroup,
        currentLevel.value,
        session.value.askedQuestionIds,
        session.value.cooldowns
      )

      if (question) {
        currentQuestionData.value = question as Question
        // Save the question as pending until answered
        session.value.pendingQuestion = question as Question
        saveSession()
        return question
      }

      console.error('No questions available')
      return null
    } catch (error) {
      console.error('Failed to fetch question:', error)
      return null
    } finally {
      isLoading.value = false
    }
  }

  // Submit answer
  const submitAnswer = (answerIndex: number) => {
    if (!session.value || !currentQuestionData.value || isAnswerRevealed.value) return

    selectedAnswer.value = answerIndex
    isAnswerRevealed.value = true

    const isCorrect = answerIndex === currentQuestionData.value.correctIndex
    lastAnswerCorrect.value = isCorrect

    if (isCorrect) {
      session.value.correctAnswers++
    } else {
      session.value.wrongAnswers++
    }

    // Track asked question
    session.value.askedQuestionIds.push(currentQuestionData.value.id)
    session.value.cooldowns[currentQuestionData.value.id] = new Date().toISOString()

    // Clear pending question since it's been answered
    session.value.pendingQuestion = null

    saveSession()

    return isCorrect
  }

  // Move to next question
  const nextQuestion = async () => {
    if (!session.value) return

    // Ensure pendingQuestion is cleared - defensive check in case submitAnswer didn't clear it
    session.value.pendingQuestion = null

    previousLevel.value = currentLevel.value
    session.value.currentQuestion++
    saveSession()

    // Check if game is complete
    if (session.value.currentQuestion > totalQuestions.value) {
      return null
    }

    return await fetchQuestion()
  }

  // Check if game is complete
  const isGameComplete = computed(() => {
    return session.value && session.value.currentQuestion > totalQuestions.value
  })

  // Clear session
  const clearSession = () => {
    session.value = null
    currentQuestionData.value = null
    if (typeof window !== 'undefined') {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  // Get certificate data
  const getCertificateData = () => {
    if (!session.value) return null
    const total = TOTAL_QUESTIONS[session.value.ageGroup] || 300
    const score = session.value.correctAnswers
    const percentage = (score / total) * 100
    let tier: 'gold' | 'silver' | 'bronze' | 'standard' = 'standard'
    if (percentage >= 90) tier = 'gold'
    else if (percentage >= 75) tier = 'silver'
    else if (percentage >= 60) tier = 'bronze'

    return {
      playerName: session.value.playerName,
      ageGroup: session.value.ageGroup,
      score,
      totalQuestions: total,
      percentage,
      tier,
      completedAt: new Date().toISOString(),
      code: `QM-${session.value.id.slice(0, 8).toUpperCase()}`,
    }
  }

  return {
    session,
    currentQuestionData,
    isLoading,
    isAnswerRevealed,
    selectedAnswer,
    lastAnswerCorrect,
    currentLevel,
    didLevelUp,
    progressPercent,
    accuracy,
    totalQuestions,
    isGameComplete,
    loadSession,
    saveSession,
    createSession,
    fetchQuestion,
    submitAnswer,
    nextQuestion,
    clearSession,
    getCertificateData,
  }
}

// Export for use in other components
export const getTotalQuestionsForAgeGroup = (ageGroup: AgeGroup): number => {
  return TOTAL_QUESTIONS[ageGroup] || 300
}
