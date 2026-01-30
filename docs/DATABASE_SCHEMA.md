# Database Schema

## Overview

The application uses a **simplified architecture** with no traditional database:

- **Server-side**: Questions stored as TypeScript modules
- **Client-side**: Session state in localStorage (minimal data)

## Server-Side: Question Storage

Questions are stored in `server/data/questions.ts` as TypeScript objects organized by age group.

### Question Structure

```typescript
interface Question {
  id: string
  text: string
  options: [string, string, string, string]  // Exactly 4 options
  correctIndex: 0 | 1 | 2 | 3
  difficulty: 1-10
  category: string
}
```

### Age Groups

- `kids`: Ages 6-12, simpler vocabulary and concepts
- `teens`: Ages 13-17, school curriculum aligned
- `adults`: Ages 18-59, full range of topics
- `seniors`: Ages 60+, classic references

Each age group has questions for all 10 difficulty levels.

## Client-Side: Session Storage

The client stores minimal data in `localStorage` under key `quiz-mastery-session`:

```typescript
interface GameSession {
  id: string                      // Session UUID
  playerName: string              // Player's display name
  ageGroup: string                // Selected age category
  currentQuestion: number         // Progress (1-1000)
  correctAnswers: number          // Score
  wrongAnswers: number            // Mistakes
  startedAt: string               // ISO timestamp
  askedQuestionIds: string[]      // Prevent repeats in session
  cooldowns: Record<string, string>  // Question cooldown tracking
}
```

**Size estimate**: ~10-50 KB per session (depending on progress)

## API Endpoint

### POST /api/question

Fetches the next question for the player.

**Request:**
```json
{
  "ageGroup": "adults",
  "difficulty": 3,
  "excludeIds": ["id1", "id2"],
  "cooldowns": { "id3": "2026-01-25T10:00:00Z" }
}
```

**Response:**
```json
{
  "id": "a3-001",
  "text": "What is the boiling point of water?",
  "options": ["90°C", "100°C", "110°C", "120°C"],
  "correctIndex": 1,
  "difficulty": 3,
  "category": "science"
}
```

## Question Selection Algorithm

```
1. Calculate difficulty from currentQuestion:
   difficulty = Math.ceil(currentQuestion / 100)

2. Filter questions:
   - Match ageGroup
   - Match difficulty
   - NOT in excludeIds (already asked this session)
   - NOT in cooldowns within 7 days

3. Random select from filtered results

4. Return question to client
```

## Benefits of This Approach

- **No database setup** - Just static files
- **Fast** - No DB queries, just array filtering
- **Simple deployment** - Deploy as static site + serverless
- **Tiny client footprint** - Only session data stored locally
- **Offline-friendly session** - Can resume if connection drops mid-answer
