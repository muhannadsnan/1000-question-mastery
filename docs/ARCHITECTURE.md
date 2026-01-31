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
│   ├── useGameSession.ts         # Game state management
│   ├── useQuestionSelector.ts    # Question selection logic
│   ├── useSound.ts               # Sound effects
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
├── public/
│   └── images/
│       ├── certificate-bg.png
│       └── badges/
│
├── server/
│   ├── api/
│   │   └── question.post.ts      # Question fetching endpoint
│   │
│   └── data/                     # Sharded question files
│       ├── little-kids/          # Age group 1 (ages 3-7)
│       │   ├── d1/               # Difficulty 1
│       │   │   ├── f1.ts         # 100 questions
│       │   │   ├── f2.ts         # 100 questions
│       │   │   ├── ...
│       │   │   └── f10.ts        # 100 questions
│       │   ├── d2/               # Difficulty 2
│       │   │   ├── f1.ts
│       │   │   └── ...
│       │   └── d10/              # Difficulty 10
│       │       └── ...
│       │
│       ├── kids/                 # Age group 2 (ages 8-12)
│       │   └── (same structure)
│       │
│       ├── teens/                # Age group 3 (ages 13-17)
│       │   └── (same structure)
│       │
│       ├── adults/               # Age group 4 (ages 18-59)
│       │   └── (same structure)
│       │
│       └── seniors/              # Age group 5 (ages 60+)
│           └── (same structure)
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

## Question File Sharding

Questions are split into small files for optimal performance:

```
Total per age group: 10,000 questions
├── 10 difficulty levels × 1,000 questions each
└── Each difficulty: 10 files × 100 questions each

File size: ~15-20 KB per file (100 questions)
Load time: <50ms per file
```

**Benefits:**
- Only load 100 questions per request (not 10,000)
- Instant filtering (100 items vs 10,000)
- Minimal memory footprint
- No database needed

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

## Question Selection Algorithm

```
┌──────────────────────────────────────────────────────────────┐
│                    Question Selection                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Get current progress (e.g., question 247)                │
│                          ▼                                   │
│  2. Calculate difficulty: ceil(247/100) = 3                  │
│                          ▼                                   │
│  3. Pick random file (1-10) from d3/                         │
│                          ▼                                   │
│  4. Load that file (100 questions only)                      │
│                          ▼                                   │
│  5. Convert excludeIds to Set for O(1) lookup                │
│                          ▼                                   │
│  6. Filter: exclude asked IDs + cooldown check               │
│                          ▼                                   │
│  7. If empty, try next file                                  │
│                          ▼                                   │
│  8. Random select from filtered results                      │
│                          ▼                                   │
│  9. Return question to client                                │
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
