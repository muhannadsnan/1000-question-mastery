import type { AgeGroup, Difficulty } from '~/types'
import { questions as staticQuestions } from '~/server/data/questions'

interface Question {
  id: string
  text: string
  options: [string, string, string, string]
  correctIndex: 0 | 1 | 2 | 3
  difficulty: Difficulty
  category: string
}

// Use import.meta.glob to pre-bundle all question files at build time
const littleKidsModules = import.meta.glob<{ questions: Question[] }>(
  '../server/data/little-kids/d*/f*.ts',
  { eager: false }
)

const kidsModules = import.meta.glob<{ questions: Question[] }>(
  '../server/data/kids/d*/f*.ts',
  { eager: false }
)

const adultsModules = import.meta.glob<{ questions: Question[] }>(
  '../server/data/adults/d*/f*.ts',
  { eager: false }
)

const seniorsModules = import.meta.glob<{ questions: Question[] }>(
  '../server/data/seniors/d*/f*.ts',
  { eager: false }
)

// Map age group to their question modules
const ageGroupModules: Record<string, Record<string, () => Promise<{ questions: Question[] }>>> = {
  'little-kids': littleKidsModules,
  'kids': kidsModules,
  'adults': adultsModules,
  'seniors': seniorsModules,
}

// Map age group to folder names
const ageGroupFolders: Record<string, string> = {
  littleKids: 'little-kids',
  kids: 'kids',
  teens: 'teens',
  adults: 'adults',
  seniors: 'seniors',
}

// Fisher-Yates shuffle
function shuffleArray<T>(array: T[]): T[] {
  const shuffled = [...array]
  for (let i = shuffled.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
  }
  return shuffled
}

// Cache for loaded question files
const questionCache = new Map<string, Question[]>()

export const useQuestions = () => {
  const getQuestion = async (
    ageGroup: AgeGroup,
    difficulty: Difficulty,
    excludeIds: string[],
    cooldowns: Record<string, string>
  ): Promise<Question | null> => {
    const excludeSet = new Set(excludeIds)
    const folder = ageGroupFolders[ageGroup] || 'adults'
    const fileOrder = shuffleArray([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    let foundAnyFile = false

    // Try folder-based structure first (little-kids and kids have files)
    const questionModules = ageGroupModules[folder]
    if (questionModules) {
      for (const fileNum of fileOrder) {
        const modulePath = `../server/data/${folder}/d${difficulty}/f${fileNum}.ts`
        const cacheKey = modulePath

        try {
          let questions: Question[]

          if (questionCache.has(cacheKey)) {
            questions = questionCache.get(cacheKey)!
          } else {
            const loader = questionModules[modulePath]
            if (!loader) continue

            const module = await loader()
            questions = module.questions || []
            questionCache.set(cacheKey, questions)
          }

          foundAnyFile = true

          // Filter questions
          const eligibleQuestions = questions.filter((q) => {
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

          if (eligibleQuestions.length > 0) {
            return eligibleQuestions[Math.floor(Math.random() * eligibleQuestions.length)]
          }
        } catch (e) {
          // File doesn't exist - continue
        }
      }

      // Fallback: try ignoring cooldowns
      if (foundAnyFile) {
        for (const fileNum of fileOrder) {
          const modulePath = `../server/data/${folder}/d${difficulty}/f${fileNum}.ts`
          const questions = questionCache.get(modulePath)

          if (questions) {
            const eligible = questions.filter((q) => !excludeSet.has(q.id))
            if (eligible.length > 0) {
              return eligible[Math.floor(Math.random() * eligible.length)]
            }
          }
        }
      }
    }

    // Fallback: static questions for other age groups
    const ageQuestions = staticQuestions[ageGroup] || staticQuestions.adults
    const questionsForDifficulty = ageQuestions.filter((q: any) => q.difficulty === difficulty)

    if (questionsForDifficulty.length > 0) {
      const eligible = questionsForDifficulty.filter((q: any) => {
        if (excludeSet.has(q.id)) return false
        const lastAsked = cooldowns[q.id]
        if (lastAsked) {
          const daysDiff = (Date.now() - new Date(lastAsked).getTime()) / (1000 * 60 * 60 * 24)
          if (daysDiff < 7) return false
        }
        return true
      })

      if (eligible.length > 0) {
        return eligible[Math.floor(Math.random() * eligible.length)] as Question
      }

      // Ignore cooldowns as last resort
      const anyEligible = questionsForDifficulty.filter((q: any) => !excludeSet.has(q.id))
      if (anyEligible.length > 0) {
        return anyEligible[Math.floor(Math.random() * anyEligible.length)] as Question
      }
    }

    return null
  }

  return { getQuestion }
}
