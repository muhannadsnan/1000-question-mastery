# Database Schema

## Overview

The application uses a **simplified architecture** with no traditional database:

- **Server-side**: Questions stored as sharded TypeScript files
- **Client-side**: Session state in localStorage (minimal data)

## Server-Side: Question Storage

Questions are stored in `server/data/` as TypeScript files, sharded by age group, difficulty, and file number.

### File Structure

```
server/data/
├── little-kids/          # Age group 1 (ages 3-7)
│   ├── d1/               # Difficulty 1 (1000 questions)
│   │   ├── f1.ts         # Questions 1-100
│   │   ├── f2.ts         # Questions 101-200
│   │   ├── ...
│   │   └── f10.ts        # Questions 901-1000
│   ├── d2/               # Difficulty 2
│   └── ...
│
├── kids/                 # Age group 2 (ages 8-12)
├── teens/                # Age group 3 (ages 13-17)
├── adults/               # Age group 4 (ages 18-59)
└── seniors/              # Age group 5 (ages 60+)
```

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

### Question ID Format

IDs follow the format: `{age_group}{6-digit-sequence}`

```
1000001  →  Age group 1 (littleKids), Question 1
1001000  →  Age group 1 (littleKids), Question 1000
2000001  →  Age group 2 (kids), Question 1
```

**Age group codes:**
- `1` = littleKids (3-7 years)
- `2` = kids (8-12 years)
- `3` = teens (13-17 years)
- `4` = adults (18-59 years)
- `5` = seniors (60+ years)

### File Contents

Each file exports an array of 100 questions:

```typescript
// server/data/little-kids/d1/f1.ts
export const questions: Question[] = [
  { id: '1000001', text: 'What color is a banana?', ... },
  { id: '1000002', text: 'What sound does a dog make?', ... },
  // ... 100 questions total
]
```

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
  "ageGroup": "littleKids",
  "difficulty": 3,
  "excludeIds": ["1000001", "1000002"],
  "cooldowns": { "1000003": "2026-01-25T10:00:00Z" }
}
```

**Response:**
```json
{
  "id": "1000247",
  "text": "What is 2 + 2?",
  "options": ["3", "4", "5", "6"],
  "correctIndex": 1,
  "difficulty": 3,
  "category": "math"
}
```

## Question Selection Algorithm

```
1. Calculate difficulty from currentQuestion:
   difficulty = Math.ceil(currentQuestion / 100)

2. Pick random file (1-10) from difficulty folder

3. Load only that file (100 questions)

4. Convert excludeIds to Set (O(1) lookup)

5. Filter questions:
   - NOT in excludeIds (already asked this session)
   - NOT in cooldowns within 7 days

6. If no eligible questions, try next file

7. Random select from filtered results

8. Return question to client
```

## Benefits of This Approach

- **No database setup** - Just static TypeScript files
- **Ultra-fast** - Load 100 questions, not 10,000
- **O(1) filtering** - Set-based exclusion lookup
- **Simple deployment** - Deploy as static site + serverless
- **Tiny client footprint** - Only session data stored locally
- **Scales infinitely** - Add more files without performance impact
- **Easy to edit** - Questions are plain TypeScript, easy to update
