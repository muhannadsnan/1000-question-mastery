# 1000 Question Mastery

## Overview

**1000 Question Mastery** is a progressive quiz game designed for all ages. Players answer 1000 questions across various topics, gradually increasing in difficulty. Upon completion, players receive a certificate of mastery.

## Target Audience

- **Little Kids** (3-7 years)
- **Kids** (8-12 years)
- **Teens** (13-17 years)
- **Adults** (18-35 years)
- **Seniors** (35+ years)

Each age group has its own curated question pool with age-appropriate content and difficulty.

## Game Flow

1. Player enters their name and selects their age category
2. Game loads/resumes their progress
3. Questions are presented one at a time (multiple choice, 4 options)
4. Progress: Question 1 → 1000
5. Difficulty scales with progress:
   - Questions 1-100: Difficulty 1
   - Questions 101-200: Difficulty 2
   - Questions 201-300: Difficulty 3
   - ... and so on ...
   - Questions 901-1000: Difficulty 10
6. Upon completing all 1000 questions, player receives a certificate

## Question Topics

Questions span all aspects of life and knowledge:

- Mathematics
- Geography
- History
- Science & Nature
- Art & Culture
- Music
- Literature
- Politics & Current Events
- Philosophy & Ideology
- Sports
- Technology
- General Knowledge
- Logic & Puzzles

## Key Features

- **Lightweight & Fast**: Questions sharded into small files for instant loading
- **Progress Persistence**: Game state saved locally, resume anytime
- **No Repeat Policy**: Questions are not repeated within the same playthrough
- **Cooldown System**: Previously asked questions have a 7-day cooldown before reappearing in new games
- **Achievement Certificate**: Downloadable/shareable certificate upon completion

## Tech Stack

- **Frontend**: Vue 3 + Nuxt 3
- **Storage**: localStorage for session state
- **Styling**: Tailwind CSS
- **State Management**: Vue Composables
- **Deployment**: Netlify (static hosting)
- **Certificate Generation**: html2canvas for image export

## Changelog

### v1.10.0
- UI improvements: Enlarged bottom bar icons on main menu
- Setup page: Elegant emoji icons for age groups with larger touch targets
- Game page: Question positioned higher, thicker option buttons for better tap targets
- Category badges now have predefined colors per topic (music=pink, science=emerald, etc.)

### v1.9.0
- Added 10,000 questions for Teens age group (13-17 years)
- Focus on music, gaming, movies, sports, and school-level knowledge
- Topics: pop culture, video games, social media, sports, basic science, geography, history
- General knowledge only - no specialist content
- All 5 age groups now complete with 50,000 total questions

### v1.8.0
- Added 10,000 questions for Seniors age group (35+ years)
- D1-D2: Reasonable/normal for educated adults
- D3-D5: Moderate difficulty requiring good general knowledge
- D6-D9: Challenging, requires wide reading and cultural literacy
- D10: Specialist/expert level (academic depth)
- Topics: history, literature, science, art, music, philosophy, economics, law, archaeology, linguistics

### v1.7.0
- Added 10,000 questions for Adults age group (18-35 years)
- Topics include pop culture, movies, music, history, geography, science, sports, literature, art, business, technology, politics, philosophy
- Progressive difficulty: D1-D2 easy, D3-D4 normal, D5-D6 moderate, D7-D10 challenging but accessible

### v1.6.1
- Fixed Kids D7-D10 questions to be age-appropriate (grades 3-6)
- Removed algebra, physics, chemical formulas from kids questions
- Added brain teasers, trivia, dinosaurs, fun facts for harder levels

### v1.6.0
- Added 10,000 questions for Kids age group (8-12 years)
- Topics include math, science, geography, history, vocabulary across 10 difficulty levels

### v1.5.0
- Client-side question loading (removed server API dependency)
- Static site generation for Netlify compatibility
- Fixed certificate download (title now renders correctly)
- Improved stats spacing in certificate

### v1.4.0
- Shareable certificate with download as image
- Modern card-style main menu with icons
- Name memory feature (remembers previous players)
- Age range updates (Adults: 18-35, Seniors: 35+)
- Premium certificate design with fireworks animation

### v1.3.0
- Dynamic question loading from sharded files
- Age-appropriate questions for all groups

### v1.2.0
- Little Kids age group with 10,000 questions

### v1.0.0
- Initial release with basic quiz functionality
