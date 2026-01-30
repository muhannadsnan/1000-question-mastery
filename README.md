# 1000 Question Mastery

A progressive quiz game where players answer 1000 questions across all topics, gradually increasing in difficulty. Complete the challenge to earn your certificate of mastery!

## Features

- **4 Age Groups**: Kids, Teens, Adults, Seniors - each with tailored questions
- **Progressive Difficulty**: Questions scale from easy (1) to master (10)
- **15+ Categories**: Math, science, history, geography, art, music, and more
- **Offline Support**: All data stored locally in browser
- **Save & Resume**: Continue your game anytime
- **Achievement Certificate**: Downloadable certificate upon completion

## Tech Stack

- Vue 3 + Nuxt 3
- Tailwind CSS
- Pinia (state management)
- Dexie.js (IndexedDB wrapper)
- TypeScript

## Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Documentation

- [Project Overview](./docs/PROJECT_OVERVIEW.md)
- [Database Schema](./docs/DATABASE_SCHEMA.md)
- [Architecture](./docs/ARCHITECTURE.md)
- [Question Format](./docs/QUESTION_FORMAT.md)
- [Development Guide](./docs/DEVELOPMENT_GUIDE.md)

## Game Rules

1. Select your age category
2. Answer 1000 multiple-choice questions
3. Questions 1-100 are Difficulty 1, 101-200 are Difficulty 2, etc.
4. Each question has 4 options with one correct answer
5. Questions won't repeat within your game
6. Complete all 1000 to earn your certificate!

## Project Status

- [x] Documentation & Planning
- [ ] Core game implementation
- [ ] Question database
- [ ] Certificate generation

## License

MIT
