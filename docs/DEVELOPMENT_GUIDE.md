# Development Guide

## Prerequisites

- Node.js 18+
- npm or pnpm
- Git

## Quick Start

```bash
# Clone/navigate to project
cd 1000-question-mastery

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Initial Setup Commands

```bash
# Create Nuxt 3 project
npx nuxi@latest init 1000-question-mastery
cd 1000-question-mastery

# Install dependencies
npm install

# Add Tailwind CSS
npm install -D @nuxtjs/tailwindcss

# Add Pinia for state management
npm install @pinia/nuxt pinia

# Add Dexie for IndexedDB
npm install dexie

# Add UUID generation
npm install uuid
npm install -D @types/uuid

# Add date utilities
npm install date-fns

# Add canvas/PDF for certificates (optional)
npm install html2canvas jspdf
```

## Configuration Files

### nuxt.config.ts

```typescript
export default defineNuxtConfig({
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
  ],

  app: {
    head: {
      title: '1000 Question Mastery',
      meta: [
        { name: 'description', content: 'Master 1000 questions across all topics!' }
      ]
    }
  },

  // Enable client-side only (no SSR needed)
  ssr: false,

  compatibilityDate: '2024-01-01'
})
```

### tailwind.config.js

```javascript
module.exports = {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      }
    },
  },
  plugins: [],
}
```

## Development Phases

### Phase 1: Foundation
- [x] Project documentation
- [ ] Nuxt 3 project setup
- [ ] Tailwind CSS configuration
- [ ] TypeScript types definition
- [ ] Database layer (Dexie)
- [ ] Basic layout components

### Phase 2: Core Game
- [ ] Home page
- [ ] Setup page (age/name selection)
- [ ] Game page
- [ ] Question card component
- [ ] Progress tracking
- [ ] Score display
- [ ] Answer feedback (correct/wrong)

### Phase 3: Data & Persistence
- [ ] Question JSON structure
- [ ] Sample questions (50 per difficulty per age)
- [ ] Database seeding on first load
- [ ] Game session persistence
- [ ] Resume game functionality

### Phase 4: Completion & Polish
- [ ] Certificate page
- [ ] Certificate generation (Canvas)
- [ ] Download certificate
- [ ] History page
- [ ] Sound effects (optional)
- [ ] Animations

### Phase 5: Content
- [ ] Expand question database
- [ ] 500+ questions per difficulty per age group
- [ ] Content review & QA

## Folder Creation Commands

```bash
# Create all directories
mkdir -p components/game
mkdir -p components/ui
mkdir -p components/certificate
mkdir -p composables
mkdir -p layouts
mkdir -p pages/certificate
mkdir -p plugins
mkdir -p public/data
mkdir -p public/images/badges
mkdir -p stores
mkdir -p types
mkdir -p utils
```

## Sample Question Data File

Create `public/data/questions-adults.json`:

```json
{
  "ageGroup": "adults",
  "questions": [
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "text": "What is the chemical symbol for water?",
      "options": ["H2O", "CO2", "NaCl", "O2"],
      "correctIndex": 0,
      "difficulty": 1,
      "category": "science"
    },
    {
      "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
      "text": "Who painted the Sistine Chapel ceiling?",
      "options": ["Leonardo da Vinci", "Michelangelo", "Raphael", "Donatello"],
      "correctIndex": 1,
      "difficulty": 3,
      "category": "art"
    }
  ]
}
```

## Testing

```bash
# Run type checking
npm run typecheck

# Run linter
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

### Netlify (Recommended)

The app is configured for Netlify with SSR support:

1. Connect GitHub repo to Netlify
2. Build command: `npm run build`
3. Publish directory: `dist`

The `netlify.toml` handles all configuration automatically.

### Other Platforms

- **Vercel**: `vercel deploy`
- **GitHub Pages**: Use `nuxt generate`
- **Any static host**: Upload `dist/` folder

```bash
# Generate static site
npm run generate
```

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

IndexedDB is required for the app to function.
