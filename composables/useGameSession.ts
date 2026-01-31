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

const STORAGE_KEY = 'quiz-mastery-session'

export const useGameSession = () => {
  const session = useState<GameSession | null>('gameSession', () => null)
  const currentQuestionData = useState<Question | null>('currentQuestion', () => null)
  const isLoading = useState('isLoading', () => false)
  const isAnswerRevealed = useState('isAnswerRevealed', () => false)
  const selectedAnswer = useState<number | null>('selectedAnswer', () => null)
  const lastAnswerCorrect = useState<boolean | null>('lastAnswerCorrect', () => null)
  const previousLevel = useState<number>('previousLevel', () => 1)

  // Calculate current difficulty level based on progress
  const currentLevel = computed(() => {
    if (!session.value) return 1
    return Math.min(10, Math.ceil(session.value.currentQuestion / 100)) as Difficulty
  })

  // Check if player leveled up
  const didLevelUp = computed(() => {
    return currentLevel.value > previousLevel.value
  })

  // Progress percentage
  const progressPercent = computed(() => {
    if (!session.value) return 0
    return ((session.value.currentQuestion - 1) / 1000) * 100
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
      if (session.value.pendingQuestion) {
        currentQuestionData.value = session.value.pendingQuestion
        isLoading.value = false
        return session.value.pendingQuestion
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

    previousLevel.value = currentLevel.value
    session.value.currentQuestion++
    saveSession()

    // Check if game is complete
    if (session.value.currentQuestion > 1000) {
      return null
    }

    return await fetchQuestion()
  }

  // Check if game is complete
  const isGameComplete = computed(() => {
    return session.value && session.value.currentQuestion > 1000
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
    const score = session.value.correctAnswers
    const percentage = (score / 1000) * 100
    let tier: 'gold' | 'silver' | 'bronze' | 'standard' = 'standard'
    if (percentage >= 90) tier = 'gold'
    else if (percentage >= 75) tier = 'silver'
    else if (percentage >= 60) tier = 'bronze'

    return {
      playerName: session.value.playerName,
      ageGroup: session.value.ageGroup,
      score,
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
