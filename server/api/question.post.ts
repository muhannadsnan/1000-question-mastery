import { questions } from '../data/questions'

interface RequestBody {
  ageGroup: string
  difficulty: number
  excludeIds: string[]
  cooldowns: Record<string, string>
}

export default defineEventHandler(async (event) => {
  const body = await readBody<RequestBody>(event)
  const { ageGroup, difficulty, excludeIds = [], cooldowns = {} } = body

  // Filter questions by age group and difficulty
  const ageQuestions = questions[ageGroup as keyof typeof questions] || questions.adults

  const eligibleQuestions = ageQuestions.filter((q) => {
    // Must match difficulty
    if (q.difficulty !== difficulty) return false

    // Must not be already asked in this session
    if (excludeIds.includes(q.id)) return false

    // Check cooldown (7 days)
    const lastAsked = cooldowns[q.id]
    if (lastAsked) {
      const lastAskedDate = new Date(lastAsked)
      const now = new Date()
      const daysDiff = (now.getTime() - lastAskedDate.getTime()) / (1000 * 60 * 60 * 24)
      if (daysDiff < 7) return false
    }

    return true
  })

  // If no eligible questions (shouldn't happen with enough questions), relax constraints
  let selectedQuestion
  if (eligibleQuestions.length === 0) {
    // Fallback: just exclude already asked, ignore cooldown
    const fallbackQuestions = ageQuestions.filter(
      (q) => q.difficulty === difficulty && !excludeIds.includes(q.id)
    )
    if (fallbackQuestions.length > 0) {
      selectedQuestion = fallbackQuestions[Math.floor(Math.random() * fallbackQuestions.length)]
    } else {
      // Last resort: any question of that difficulty
      const lastResort = ageQuestions.filter((q) => q.difficulty === difficulty)
      selectedQuestion = lastResort[Math.floor(Math.random() * lastResort.length)]
    }
  } else {
    // Pick random question
    selectedQuestion = eligibleQuestions[Math.floor(Math.random() * eligibleQuestions.length)]
  }

  if (!selectedQuestion) {
    throw createError({
      statusCode: 404,
      statusMessage: 'No questions available',
    })
  }

  // Return question (without exposing more than needed)
  return {
    id: selectedQuestion.id,
    text: selectedQuestion.text,
    options: selectedQuestion.options,
    correctIndex: selectedQuestion.correctIndex,
    difficulty: selectedQuestion.difficulty,
    category: selectedQuestion.category,
  }
})
