import { questions as staticQuestions } from '../data/questions'

interface RequestBody {
  ageGroup: string
  difficulty: number
  excludeIds: string[]
  cooldowns: Record<string, string>
}

// Map age group names to folder names
const ageGroupFolders: Record<string, string> = {
  littleKids: 'little-kids',
  kids: 'kids',
  teens: 'teens',
  adults: 'adults',
  seniors: 'seniors',
}

export default defineEventHandler(async (event) => {
  const body = await readBody<RequestBody>(event)
  const { ageGroup, difficulty, excludeIds = [], cooldowns = {} } = body

  // Convert excludeIds to Set for O(1) lookup
  const excludeSet = new Set(excludeIds)

  // Get folder name for age group
  const folder = ageGroupFolders[ageGroup] || 'adults'

  // Try up to 10 files to find an eligible question
  const fileOrder = shuffleArray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
  let foundAnyFile = false

  for (const fileNum of fileOrder) {
    try {
      // Dynamic import - only loads the specific file needed
      const module = await import(`../data/${folder}/d${difficulty}/f${fileNum}.ts`)
      const questions = module.questions || []
      foundAnyFile = true

      // Filter questions (only 100 items - very fast)
      const eligibleQuestions = questions.filter((q: any) => {
        // Must not be already asked in this session
        if (excludeSet.has(q.id)) return false

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

      if (eligibleQuestions.length > 0) {
        // Pick random question from this file
        const selectedQuestion = eligibleQuestions[Math.floor(Math.random() * eligibleQuestions.length)]

        return {
          id: selectedQuestion.id,
          text: selectedQuestion.text,
          options: selectedQuestion.options,
          correctIndex: selectedQuestion.correctIndex,
          difficulty: selectedQuestion.difficulty,
          category: selectedQuestion.category,
        }
      }
      // If no eligible questions in this file, continue to next file
    } catch (e) {
      // File doesn't exist or error loading - continue to next file
    }
  }

  // If we've exhausted all files but found some, try fallback (ignore cooldown)
  if (foundAnyFile) {
    for (const fileNum of fileOrder) {
      try {
        const module = await import(`../data/${folder}/d${difficulty}/f${fileNum}.ts`)
        const questions = module.questions || []

        const fallbackQuestions = questions.filter((q: any) => !excludeSet.has(q.id))

        if (fallbackQuestions.length > 0) {
          const selectedQuestion = fallbackQuestions[Math.floor(Math.random() * fallbackQuestions.length)]

          return {
            id: selectedQuestion.id,
            text: selectedQuestion.text,
            options: selectedQuestion.options,
            correctIndex: selectedQuestion.correctIndex,
            difficulty: selectedQuestion.difficulty,
            category: selectedQuestion.category,
          }
        }
      } catch (e) {
        // Continue
      }
    }
  }

  // Fallback to static questions from questions.ts for age groups without folder structure
  const staticAgeQuestions = staticQuestions[ageGroup as keyof typeof staticQuestions] || staticQuestions.adults
  const questionsForDifficulty = staticAgeQuestions.filter((q: any) => q.difficulty === difficulty)

  // Filter out already asked questions
  const eligibleStaticQuestions = questionsForDifficulty.filter((q: any) => {
    if (excludeSet.has(q.id)) return false

    const lastAsked = cooldowns[q.id]
    if (lastAsked) {
      const lastAskedDate = new Date(lastAsked)
      const now = new Date()
      const daysDiff = (now.getTime() - lastAskedDate.getTime()) / (1000 * 60 * 60 * 24)
      if (daysDiff < 7) return false
    }

    return true
  })

  if (eligibleStaticQuestions.length > 0) {
    const selectedQuestion = eligibleStaticQuestions[Math.floor(Math.random() * eligibleStaticQuestions.length)]
    return {
      id: selectedQuestion.id,
      text: selectedQuestion.text,
      options: selectedQuestion.options,
      correctIndex: selectedQuestion.correctIndex,
      difficulty: selectedQuestion.difficulty,
      category: selectedQuestion.category,
    }
  }

  // Last resort: any question from static that hasn't been asked this session
  const anyEligible = questionsForDifficulty.filter((q: any) => !excludeSet.has(q.id))
  if (anyEligible.length > 0) {
    const selectedQuestion = anyEligible[Math.floor(Math.random() * anyEligible.length)]
    return {
      id: selectedQuestion.id,
      text: selectedQuestion.text,
      options: selectedQuestion.options,
      correctIndex: selectedQuestion.correctIndex,
      difficulty: selectedQuestion.difficulty,
      category: selectedQuestion.category,
    }
  }

  throw createError({
    statusCode: 404,
    statusMessage: 'No questions available for this difficulty',
  })
})

// Fisher-Yates shuffle
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}
