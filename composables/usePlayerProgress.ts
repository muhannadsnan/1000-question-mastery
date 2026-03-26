import type { AgeGroup } from '~/types'

export interface PlayerGameRecord {
  masteryLevel: AgeGroup
  score: number
  totalQuestions: number
  percentage: number
  tier: 'gold' | 'silver' | 'bronze' | 'standard'
  completedAt: string
}

export interface PlayerProgress {
  name: string
  gamesPlayed: number
  bestScores: Partial<Record<AgeGroup, PlayerGameRecord>>
  lastPlayed: string
  certificates: number
}

const PROGRESS_STORAGE_KEY = 'quiz-mastery-players'

export const usePlayerProgress = () => {
  // Get all players progress
  const getAllPlayers = (): Record<string, PlayerProgress> => {
    if (typeof window === 'undefined') return {}
    try {
      const stored = localStorage.getItem(PROGRESS_STORAGE_KEY)
      return stored ? JSON.parse(stored) : {}
    } catch {
      return {}
    }
  }

  // Save all players progress
  const saveAllPlayers = (players: Record<string, PlayerProgress>) => {
    if (typeof window === 'undefined') return
    localStorage.setItem(PROGRESS_STORAGE_KEY, JSON.stringify(players))
  }

  // Get a specific player's progress
  const getPlayerProgress = (name: string): PlayerProgress | null => {
    const players = getAllPlayers()
    const normalizedName = name.trim().toLowerCase()

    // Find player (case-insensitive)
    for (const [key, player] of Object.entries(players)) {
      if (key.toLowerCase() === normalizedName) {
        return player
      }
    }
    return null
  }

  // Save a game completion
  const saveGameCompletion = (
    playerName: string,
    masteryLevel: AgeGroup,
    score: number,
    totalQuestions: number,
    tier: 'gold' | 'silver' | 'bronze' | 'standard'
  ) => {
    const players = getAllPlayers()
    const normalizedName = playerName.trim()
    const percentage = Math.round((score / totalQuestions) * 100)

    const gameRecord: PlayerGameRecord = {
      masteryLevel,
      score,
      totalQuestions,
      percentage,
      tier,
      completedAt: new Date().toISOString()
    }

    // Find existing player (case-insensitive) or create new
    let existingKey: string | null = null
    for (const key of Object.keys(players)) {
      if (key.toLowerCase() === normalizedName.toLowerCase()) {
        existingKey = key
        break
      }
    }

    if (existingKey) {
      const player = players[existingKey]
      player.gamesPlayed++
      player.lastPlayed = new Date().toISOString()
      player.certificates++

      // Update best score for this mastery level if better
      const currentBest = player.bestScores[masteryLevel]
      if (!currentBest || percentage > currentBest.percentage) {
        player.bestScores[masteryLevel] = gameRecord
      }
    } else {
      // Create new player
      players[normalizedName] = {
        name: normalizedName,
        gamesPlayed: 1,
        bestScores: { [masteryLevel]: gameRecord },
        lastPlayed: new Date().toISOString(),
        certificates: 1
      }
    }

    saveAllPlayers(players)
  }

  // Get player stats summary
  const getPlayerStats = (name: string) => {
    const player = getPlayerProgress(name)
    if (!player) return null

    const bestOverall = Object.values(player.bestScores).reduce((best, current) => {
      if (!best || current.percentage > best.percentage) return current
      return best
    }, null as PlayerGameRecord | null)

    return {
      gamesPlayed: player.gamesPlayed,
      certificates: player.certificates,
      bestPercentage: bestOverall?.percentage || 0,
      bestTier: bestOverall?.tier || null,
      lastPlayed: player.lastPlayed,
      levelsCompleted: Object.keys(player.bestScores).length
    }
  }

  // Get all player names with their stats (for dropdown display)
  const getPlayersWithStats = () => {
    const players = getAllPlayers()
    return Object.values(players).map(player => ({
      name: player.name,
      gamesPlayed: player.gamesPlayed,
      certificates: player.certificates,
      lastPlayed: player.lastPlayed
    })).sort((a, b) => new Date(b.lastPlayed).getTime() - new Date(a.lastPlayed).getTime())
  }

  // Remove a player
  const removePlayer = (name: string) => {
    const players = getAllPlayers()
    const normalizedName = name.trim().toLowerCase()

    for (const key of Object.keys(players)) {
      if (key.toLowerCase() === normalizedName) {
        delete players[key]
        break
      }
    }

    saveAllPlayers(players)
  }

  return {
    getAllPlayers,
    getPlayerProgress,
    saveGameCompletion,
    getPlayerStats,
    getPlayersWithStats,
    removePlayer
  }
}
