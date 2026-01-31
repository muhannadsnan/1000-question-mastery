// Age groups for different question pools
export type AgeGroup = 'littleKids' | 'kids' | 'teens' | 'adults' | 'seniors'

// Question categories
export type QuestionCategory =
  | 'math'
  | 'geography'
  | 'history'
  | 'science'
  | 'nature'
  | 'art'
  | 'music'
  | 'literature'
  | 'politics'
  | 'philosophy'
  | 'sports'
  | 'technology'
  | 'language'
  | 'entertainment'
  | 'food'
  | 'general'

// Difficulty levels 1-10
export type Difficulty = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10

// Game session status
export type SessionStatus = 'active' | 'completed' | 'abandoned'

// Certificate tier based on score
export type CertificateTier = 'gold' | 'silver' | 'bronze' | 'standard'

/**
 * A quiz question
 */
export interface Question {
  id: string
  text: string
  options: [string, string, string, string] // Exactly 4 options
  correctIndex: 0 | 1 | 2 | 3
  difficulty: Difficulty
  ageGroup: AgeGroup
  category: QuestionCategory
  lastAskedAt?: Date | null
}

/**
 * Question as stored in JSON files (without ageGroup, added during import)
 */
export interface QuestionData {
  id: string
  text: string
  options: [string, string, string, string]
  correctIndex: 0 | 1 | 2 | 3
  difficulty: Difficulty
  category: QuestionCategory
}

/**
 * Question JSON file structure
 */
export interface QuestionFile {
  ageGroup: AgeGroup
  questions: QuestionData[]
}

/**
 * A game session tracking player progress
 */
export interface GameSession {
  id: string
  playerName: string
  ageGroup: AgeGroup
  currentQuestion: number // 1-1000
  correctAnswers: number
  wrongAnswers: number
  startedAt: Date
  completedAt?: Date | null
  askedQuestionIds: string[]
  status: SessionStatus
}

/**
 * Certificate earned upon completion
 */
export interface Certificate {
  id: string
  sessionId: string
  playerName: string
  ageGroup: AgeGroup
  score: number // Correct answers out of 1000
  percentage: number // Score as percentage
  tier: CertificateTier
  earnedAt: Date
  certificateCode: string // Unique verification code
}

/**
 * User settings stored locally
 */
export interface Setting {
  key: string
  value: unknown
}

/**
 * Current game state in Pinia store
 */
export interface GameState {
  // Session info
  sessionId: string | null
  playerName: string
  ageGroup: AgeGroup | null

  // Progress
  currentQuestion: number
  correctAnswers: number
  wrongAnswers: number

  // Current question being displayed
  question: Question | null
  selectedAnswer: number | null
  isAnswerRevealed: boolean
  wasCorrect: boolean | null

  // UI state
  isLoading: boolean
  isPaused: boolean
  isComplete: boolean
}

/**
 * Age group display information
 */
export interface AgeGroupInfo {
  id: AgeGroup
  label: string
  description: string
  ageRange: string
  icon: string
}

/**
 * Category display information
 */
export interface CategoryInfo {
  id: QuestionCategory
  label: string
  icon: string
  color: string
}

/**
 * Game statistics for display
 */
export interface GameStats {
  totalQuestions: number
  correctAnswers: number
  wrongAnswers: number
  accuracy: number
  currentDifficulty: Difficulty
  questionsRemaining: number
}

/**
 * Answer result after submitting
 */
export interface AnswerResult {
  isCorrect: boolean
  correctIndex: number
  selectedIndex: number
}
