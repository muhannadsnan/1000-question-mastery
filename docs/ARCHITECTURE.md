# Application Architecture

## Project Structure

```
1000-question-mastery/
├── nuxt.config.ts
├── package.json
├── tailwind.config.js
├── tsconfig.json
│
├── assets/
│   └── css/
│       └── main.css
│
├── components/
│   ├── game/
│   │   ├── QuestionCard.vue      # Displays question and options
│   │   ├── ProgressBar.vue       # Shows 1-1000 progress
│   │   ├── DifficultyBadge.vue   # Shows current difficulty level
│   │   ├── ScoreDisplay.vue      # Correct/wrong counter
│   │   └── Timer.vue             # Optional: time per question
│   │
│   ├── ui/
│   │   ├── Button.vue
│   │   ├── Card.vue
│   │   ├── Modal.vue
│   │   └── LoadingSpinner.vue
│   │
│   └── certificate/
│       ├── CertificatePreview.vue
│       └── CertificateDownload.vue
│
├── composables/
│   ├── useDatabase.ts            # Dexie database instance
│   ├── useGameSession.ts         # Game state management
│   ├── useQuestionSelector.ts    # Question selection logic
│   └── useCertificate.ts         # Certificate generation
│
├── layouts/
│   ├── default.vue               # Standard layout
│   └── game.vue                  # Minimal layout for gameplay
│
├── pages/
│   ├── index.vue                 # Home / Landing page
│   ├── setup.vue                 # Age selection & name input
│   ├── game.vue                  # Main game screen
│   ├── certificate/
│   │   └── [id].vue              # Certificate view/download
│   └── history.vue               # Past games & certificates
│
├── plugins/
│   └── dexie.client.ts           # Database initialization
│
├── public/
│   ├── data/
│   │   ├── questions-kids.json
│   │   ├── questions-teens.json
│   │   ├── questions-adults.json
│   │   └── questions-seniors.json
│   │
│   └── images/
│       ├── certificate-bg.png
│       └── badges/
│
├── server/
│   └── (empty - fully client-side)
│
├── stores/
│   ├── game.ts                   # Pinia store for game state
│   └── settings.ts               # User preferences
│
├── types/
│   └── index.ts                  # TypeScript interfaces
│
└── utils/
    ├── questionHelpers.ts        # Question-related utilities
    └── certificateGenerator.ts   # Canvas/PDF generation
```

## Component Architecture

### Page Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   index     │ ──► │   setup     │ ──► │    game     │ ──► │ certificate │
│  (landing)  │     │ (age/name)  │     │  (1000 Q's) │     │  (reward)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
                                        ┌─────────────┐
                                        │   history   │
                                        │ (past games)│
                                        └─────────────┘
```

### Game Page Component Tree

```
GamePage.vue
├── ProgressBar.vue
│   └── Shows: "Question 247 of 1000"
│
├── DifficultyBadge.vue
│   └── Shows: "Difficulty: 3/10"
│
├── ScoreDisplay.vue
│   └── Shows: "Correct: 198 | Wrong: 48"
│
├── QuestionCard.vue
│   ├── Question text
│   └── OptionButton.vue (x4)
│       └── A, B, C, D options
│
└── GameControls.vue
    ├── Pause button
    └── Quit button (with confirmation)
```

## State Management

### Pinia Store: `useGameStore`

```typescript
interface GameState {
  // Session info
  sessionId: string | null
  playerName: string
  ageGroup: AgeGroup | null

  // Progress
  currentQuestion: number  // 1-1000
  correctAnswers: number
  wrongAnswers: number

  // Current question
  question: Question | null
  selectedAnswer: number | null
  isAnswerRevealed: boolean

  // UI state
  isLoading: boolean
  isPaused: boolean
}

// Actions
- startNewGame(playerName, ageGroup)
- resumeGame(sessionId)
- loadNextQuestion()
- submitAnswer(optionIndex)
- pauseGame()
- quitGame()
- completeGame()
```

## Database Layer

### Dexie Schema

```typescript
// composables/useDatabase.ts
import Dexie from 'dexie'

class QuizDatabase extends Dexie {
  questions!: Table<Question>
  gameSessions!: Table<GameSession>
  certificates!: Table<Certificate>
  settings!: Table<Setting>

  constructor() {
    super('QuizMasteryDB')

    this.version(1).stores({
      questions: 'id, [ageGroup+difficulty], lastAskedAt',
      gameSessions: 'id, status, ageGroup',
      certificates: 'id, sessionId, certificateCode',
      settings: 'key'
    })
  }
}
```

## Question Selection Flow

```
┌──────────────────────────────────────────────────────────────┐
│                    Question Selection                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Get current progress (e.g., question 247)                │
│                          ▼                                   │
│  2. Calculate difficulty: ceil(247/100) = 3                  │
│                          ▼                                   │
│  3. Query DB:                                                │
│     - ageGroup = 'adults'                                    │
│     - difficulty = 3                                         │
│     - id NOT IN [...already asked IDs]                       │
│     - lastAskedAt < 7 days ago OR null                       │
│                          ▼                                   │
│  4. Random select from results                               │
│                          ▼                                   │
│  5. Update question.lastAskedAt = now()                      │
│                          ▼                                   │
│  6. Add to session.askedQuestionIds                          │
│                          ▼                                   │
│  7. Return question to game                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Certificate Generation

Uses HTML Canvas to generate a certificate image:

1. Draw certificate background template
2. Add player name
3. Add completion date
4. Add score (correct answers / 1000)
5. Add unique verification code
6. Add decorative elements based on score tier:
   - Gold (90%+): Gold border, star badge
   - Silver (75-89%): Silver border
   - Bronze (60-74%): Bronze border
   - Standard (<60%): Simple border

Export options:
- PNG image download
- Share to social media (Web Share API)
