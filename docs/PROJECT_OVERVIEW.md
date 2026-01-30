# 1000 Question Mastery

## Overview

**1000 Question Mastery** is a progressive quiz game designed for all ages. Players answer 1000 questions across various topics, gradually increasing in difficulty. Upon completion, players receive a certificate of mastery.

## Target Audience

- **Kids** (6-12 years)
- **Teens** (13-17 years)
- **Adults** (18-59 years)
- **Seniors** (60+ years)

Each age group has its own curated question pool with age-appropriate content and difficulty.

## Game Flow

1. Player selects their age category
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

- **Offline-First**: All questions stored locally in client-side database
- **Progress Persistence**: Game state saved locally, resume anytime
- **No Repeat Policy**: Questions are not repeated within the same playthrough
- **Cooldown System**: Previously asked questions have a 7-day cooldown before reappearing in new games
- **Achievement Certificate**: Downloadable/shareable certificate upon completion

## Tech Stack

- **Frontend**: Vue 3 + Nuxt 3
- **Database**: IndexedDB (via Dexie.js) for client-side storage
- **Styling**: Tailwind CSS
- **State Management**: Pinia
- **Certificate Generation**: HTML Canvas / PDF generation
