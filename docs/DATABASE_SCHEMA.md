# Database Schema

## Overview

The application uses **IndexedDB** (via Dexie.js) for client-side storage. This allows for:
- Offline functionality
- Large dataset storage (tens of thousands of questions)
- Fast querying by difficulty and category
- Persistent game state

## Tables

### 1. `questions`

Stores all quiz questions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | string (UUID) | Primary key |
| `text` | string | The question text |
| `options` | string[] | Array of 4 answer options |
| `correctIndex` | number (0-3) | Index of the correct answer |
| `difficulty` | number (1-10) | Question difficulty level |
| `ageGroup` | string | Target age group: 'kids', 'teens', 'adults', 'seniors' |
| `category` | string | Topic category (math, geography, etc.) |
| `lastAskedAt` | Date | null | Timestamp when last asked (for cooldown) |

**Indexes:**
- `[ageGroup+difficulty]` - Compound index for efficient question selection
- `lastAskedAt` - For cooldown filtering

### 2. `gameSessions`

Stores active and completed game sessions.

| Column | Type | Description |
|--------|------|-------------|
| `id` | string (UUID) | Primary key |
| `playerName` | string | Player's display name |
| `ageGroup` | string | Selected age category |
| `currentQuestion` | number (1-1000) | Current progress |
| `correctAnswers` | number | Total correct answers |
| `wrongAnswers` | number | Total wrong answers |
| `startedAt` | Date | Session start timestamp |
| `completedAt` | Date | null | Completion timestamp |
| `askedQuestionIds` | string[] | IDs of questions already asked |
| `status` | string | 'active', 'completed', 'abandoned' |

### 3. `certificates`

Stores earned certificates.

| Column | Type | Description |
|--------|------|-------------|
| `id` | string (UUID) | Primary key |
| `sessionId` | string | Reference to game session |
| `playerName` | string | Player's name for certificate |
| `ageGroup` | string | Age category completed |
| `score` | number | Final score (correct/1000) |
| `earnedAt` | Date | Certificate issue date |
| `certificateCode` | string | Unique verification code |

### 4. `settings`

Stores user preferences.

| Column | Type | Description |
|--------|------|-------------|
| `key` | string | Setting name (primary key) |
| `value` | any | Setting value |

## Question Selection Algorithm

When selecting the next question:

```
1. Determine required difficulty based on progress:
   - difficulty = Math.ceil(currentQuestion / 100)

2. Query questions where:
   - ageGroup = player's age group
   - difficulty = required difficulty
   - id NOT IN session's askedQuestionIds
   - lastAskedAt IS NULL OR lastAskedAt < (now - 7 days)

3. Randomly select one question from results

4. Update question's lastAskedAt to current timestamp

5. Add question ID to session's askedQuestionIds
```

## Initial Data Seeding

On first app load, the database is seeded with questions from bundled JSON files:

```
/public/data/
  ├── questions-kids.json
  ├── questions-teens.json
  ├── questions-adults.json
  └── questions-seniors.json
```

Each file contains thousands of questions structured as:

```json
{
  "questions": [
    {
      "id": "uuid",
      "text": "What is 2 + 2?",
      "options": ["3", "4", "5", "6"],
      "correctIndex": 1,
      "difficulty": 1,
      "category": "math"
    }
  ]
}
```

## Storage Estimates

- Average question size: ~500 bytes
- 10,000 questions per age group: ~5 MB
- 4 age groups total: ~20 MB
- IndexedDB limit: Usually 50MB-unlimited depending on browser

This is well within browser storage limits.
