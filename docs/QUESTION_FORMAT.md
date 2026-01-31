# Question Format & Guidelines

## Question Structure

Each question is a TypeScript object with the following format:

```typescript
{
  id: '1000001',
  text: 'What color is a banana?',
  options: ['Red', 'Yellow', 'Blue', 'Green'],
  correctIndex: 1,
  difficulty: 1,
  category: 'colors'
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (see ID Format below) |
| `text` | string | The question (supports basic HTML for formatting) |
| `options` | string[4] | Exactly 4 answer options |
| `correctIndex` | 0-3 | Index of correct answer in options array |
| `difficulty` | 1-10 | Difficulty level |
| `category` | string | Topic category |

## Question ID Format

IDs follow the format: `{age_group}{6-digit-sequence}`

```
1000001  →  Age group 1 (littleKids), Question 1
1001000  →  Age group 1 (littleKids), Question 1000
1010000  →  Age group 1 (littleKids), Question 10000
2000001  →  Age group 2 (kids), Question 1
```

**Age group codes:**
| Code | Age Group | Ages |
|------|-----------|------|
| `1` | littleKids | 3-7 years |
| `2` | kids | 8-12 years |
| `3` | teens | 13-17 years |
| `4` | adults | 18-59 years |
| `5` | seniors | 60+ years |

**ID Generator:**
```typescript
const id = (n: number) => `1${n.toString().padStart(6, '0')}`
// id(1)    → '1000001'
// id(1000) → '1001000'
```

## File Organization

Questions are sharded into small files for performance:

```
server/data/
├── little-kids/
│   ├── d1/           # Difficulty 1
│   │   ├── f1.ts     # Questions 1-100
│   │   ├── f2.ts     # Questions 101-200
│   │   └── ...       # 10 files total
│   ├── d2/           # Difficulty 2
│   └── d10/          # Difficulty 10
├── kids/
├── teens/
├── adults/
└── seniors/
```

**File template:**
```typescript
// server/data/little-kids/d1/f1.ts
export const questions = [
  { id: '1000001', text: '...', options: [...], correctIndex: 0, difficulty: 1, category: '...' },
  { id: '1000002', text: '...', options: [...], correctIndex: 1, difficulty: 1, category: '...' },
  // ... 100 questions per file
]
```

## Categories

Questions are organized into the following categories:

| Category ID | Display Name | Example Topics |
|-------------|--------------|----------------|
| `math` | Mathematics | Arithmetic, geometry, algebra, statistics |
| `geography` | Geography | Countries, capitals, landmarks, maps |
| `history` | History | Events, figures, dates, civilizations |
| `science` | Science | Biology, physics, chemistry, astronomy |
| `nature` | Nature | Animals, plants, ecosystems, weather |
| `art` | Art & Culture | Paintings, artists, movements, museums |
| `music` | Music | Instruments, composers, genres, theory |
| `literature` | Literature | Authors, books, poetry, literary terms |
| `politics` | Politics | Government, leaders, systems, laws |
| `philosophy` | Philosophy | Thinkers, ideas, ethics, logic |
| `sports` | Sports | Teams, athletes, rules, records |
| `technology` | Technology | Inventions, computers, internet, gadgets |
| `language` | Language | Grammar, vocabulary, linguistics |
| `entertainment` | Entertainment | Movies, TV, games, celebrities |
| `food` | Food & Cooking | Cuisine, ingredients, recipes |
| `general` | General Knowledge | Miscellaneous facts and trivia |
| `colors` | Colors | Color recognition (for little kids) |
| `animals` | Animals | Animal facts, sounds, habitats |
| `body` | Body | Body parts, senses |
| `home` | Home | Household items, daily routines |
| `clothing` | Clothing | What to wear |
| `opposites` | Opposites | Antonyms and contrasts |
| `time` | Time | Days, months, seasons, holidays |

## Difficulty Levels

### Level 1 (Questions 1-100)
**Very Easy** - Common knowledge, obvious answers

Examples for Little Kids:
- "What color is a banana?"
- "What sound does a dog make?"
- "How many eyes do you have?"

### Level 2 (Questions 101-200)
**Easy** - Basic knowledge most people know

Examples for Little Kids:
- "How many legs does a spider have?"
- "What is 5 + 5?"
- "What season has snow?"

### Level 3 (Questions 201-300)
**Below Average** - Elementary concepts

### Level 4 (Questions 301-400)
**Average** - Requires some thinking

### Level 5 (Questions 401-500)
**Moderate** - Challenging for age group

### Level 6 (Questions 501-600)
**Above Average** - Advanced concepts

### Level 7 (Questions 601-700)
**Challenging** - Requires good knowledge

### Level 8 (Questions 701-800)
**Hard** - Specialized knowledge

### Level 9 (Questions 801-900)
**Very Hard** - Expert level for age group

### Level 10 (Questions 901-1000)
**Master** - Highly challenging

## Age Group Adaptations

### Little Kids (3-7 years)
- Very simple vocabulary
- Visual/concrete concepts
- Basic colors, shapes, animals
- Simple counting (1-10)
- Body parts, family, daily life
- No reading comprehension required
- Fun, engaging topics

**Important**: Difficulty levels 1-10 do NOT increase topic complexity for this age group. Instead, they offer variation in the same simple topics (animal sounds, colors, shapes, counting, body parts, family, clothing, daily routines). Higher difficulty = more variety, NOT harder concepts.

Example:
```typescript
{
  id: '1000001',
  text: 'What color is the sun?',
  options: ['Blue', 'Green', 'Yellow', 'Purple'],
  correctIndex: 2,
  difficulty: 1,
  category: 'colors'
}
```

### Kids (8-12 years)
- Simple vocabulary
- Elementary school concepts
- Basic math, science, geography
- No sensitive content
- Shorter question text

### Teens (13-17 years)
- School curriculum aligned
- Pop culture references
- Moderate complexity
- Age-appropriate content

### Adults (18-59 years)
- Full range of topics
- Current events included
- Professional knowledge
- All categories available

### Seniors (60+ years)
- Classic references
- Historical events they lived through
- Traditional knowledge
- Clear, readable text

## Question Count Requirements

Each age group has **10,000 questions**:

| Difficulty | Questions | Files |
|------------|-----------|-------|
| 1 | 1,000 | 10 files × 100 |
| 2 | 1,000 | 10 files × 100 |
| 3 | 1,000 | 10 files × 100 |
| 4 | 1,000 | 10 files × 100 |
| 5 | 1,000 | 10 files × 100 |
| 6 | 1,000 | 10 files × 100 |
| 7 | 1,000 | 10 files × 100 |
| 8 | 1,000 | 10 files × 100 |
| 9 | 1,000 | 10 files × 100 |
| 10 | 1,000 | 10 files × 100 |
| **Total** | **10,000** | **100 files** |

**Grand Total: 50,000 questions** (5 age groups × 10,000)

### Generation Progress

| Age Group | Status | Questions |
|-----------|--------|-----------|
| Little Kids (3-7) | ✅ Complete | 10,000 |
| Kids (8-12) | ⏳ Pending | 0 |
| Teens (13-17) | ⏳ Pending | 0 |
| Adults (18-59) | ⏳ Pending | 0 |
| Seniors (60+) | ⏳ Pending | 0 |

This ensures:
- 10x coverage for each difficulty level
- 7-day cooldown system works effectively
- Multiple playthroughs remain fresh

## Writing Guidelines

1. **Be Clear**: Avoid ambiguous wording
2. **Be Accurate**: Verify all facts
3. **Be Fair**: Only one clearly correct answer
4. **Be Balanced**: Mix categories across difficulties
5. **Avoid Bias**: No political, religious, or cultural bias
6. **No Tricks**: Questions should test knowledge, not trick players
7. **Randomize Correct Answer Position**: Don't always put correct answer in same position
8. **Age Appropriate**: Match vocabulary and concepts to age group
