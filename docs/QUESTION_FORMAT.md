# Question Format & Guidelines

## Question Structure

Each question is a JSON object with the following format:

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "text": "What is the capital of France?",
  "options": ["London", "Paris", "Berlin", "Madrid"],
  "correctIndex": 1,
  "difficulty": 2,
  "category": "geography"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID string | Unique identifier |
| `text` | string | The question (supports basic HTML for formatting) |
| `options` | string[4] | Exactly 4 answer options |
| `correctIndex` | 0-3 | Index of correct answer in options array |
| `difficulty` | 1-10 | Difficulty level |
| `category` | string | Topic category |

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

## Difficulty Levels

### Level 1 (Questions 1-100)
**Very Easy** - Common knowledge, obvious answers

Examples:
- "How many days are in a week?"
- "What color is the sky on a clear day?"
- "What sound does a dog make?"

### Level 2 (Questions 101-200)
**Easy** - Basic knowledge most people know

Examples:
- "What is the largest planet in our solar system?"
- "Who wrote Romeo and Juliet?"

### Level 3 (Questions 201-300)
**Below Average** - Elementary school level

Examples:
- "What is the boiling point of water in Celsius?"
- "On which continent is Egypt located?"

### Level 4 (Questions 301-400)
**Average** - Middle school level

Examples:
- "What is the chemical symbol for gold?"
- "In what year did World War II end?"

### Level 5 (Questions 401-500)
**Moderate** - High school level

Examples:
- "What is the powerhouse of the cell?"
- "Who painted the Mona Lisa?"

### Level 6 (Questions 501-600)
**Above Average** - Advanced high school

Examples:
- "What is the smallest prime number greater than 50?"
- "Who was the first woman to win a Nobel Prize?"

### Level 7 (Questions 601-700)
**Challenging** - College level

Examples:
- "What is the half-life of Carbon-14?"
- "Who wrote 'The Republic'?"

### Level 8 (Questions 701-800)
**Hard** - Specialized knowledge

Examples:
- "In what year was the Treaty of Westphalia signed?"
- "What is the Heisenberg Uncertainty Principle?"

### Level 9 (Questions 801-900)
**Very Hard** - Expert level

Examples:
- "What is the Riemann Hypothesis about?"
- "Who composed 'The Rite of Spring'?"

### Level 10 (Questions 901-1000)
**Master** - Highly specialized trivia

Examples:
- "What is the Chandrasekhar limit?"
- "In what year was the Edict of Nantes revoked?"

## Age Group Adaptations

### Kids (6-12 years)
- Simple vocabulary
- Visual/concrete concepts
- Fun, engaging topics
- No sensitive content
- Shorter question text

Example:
```json
{
  "text": "What is the largest animal on Earth?",
  "options": ["Elephant", "Blue Whale", "Giraffe", "Shark"],
  "correctIndex": 1,
  "difficulty": 3,
  "category": "nature"
}
```

### Teens (13-17 years)
- School curriculum aligned
- Pop culture references
- Moderate complexity
- Age-appropriate content

Example:
```json
{
  "text": "What is the formula for the area of a circle?",
  "options": ["2πr", "πr²", "πd", "2r²"],
  "correctIndex": 1,
  "difficulty": 4,
  "category": "math"
}
```

### Adults (18-59 years)
- Full range of topics
- Current events included
- Professional knowledge
- All categories available

Example:
```json
{
  "text": "What economic principle states that bad money drives out good?",
  "options": ["Pareto Principle", "Gresham's Law", "Law of Diminishing Returns", "Say's Law"],
  "correctIndex": 1,
  "difficulty": 7,
  "category": "general"
}
```

### Seniors (60+ years)
- Classic references
- Historical events they lived through
- Traditional knowledge
- Clear, readable text

Example:
```json
{
  "text": "Who was the lead actor in 'Casablanca' (1942)?",
  "options": ["Clark Gable", "Humphrey Bogart", "Cary Grant", "James Stewart"],
  "correctIndex": 1,
  "difficulty": 3,
  "category": "entertainment"
}
```

## Question Count Requirements

Each age group should have **at minimum**:

| Difficulty | Min Questions | Purpose |
|------------|---------------|---------|
| 1 | 500+ | Ensure variety for Q 1-100 |
| 2 | 500+ | Ensure variety for Q 101-200 |
| 3 | 500+ | Ensure variety for Q 201-300 |
| 4 | 500+ | Ensure variety for Q 301-400 |
| 5 | 500+ | Ensure variety for Q 401-500 |
| 6 | 500+ | Ensure variety for Q 501-600 |
| 7 | 500+ | Ensure variety for Q 601-700 |
| 8 | 500+ | Ensure variety for Q 701-800 |
| 9 | 500+ | Ensure variety for Q 801-900 |
| 10 | 500+ | Ensure variety for Q 901-1000 |

**Total: 5,000+ questions per age group**
**Grand Total: 20,000+ questions**

This ensures:
- 5x coverage for each difficulty level
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
