# UI Design Specifications

## Color Palette

### Primary Colors
- **Primary Blue**: `#3B82F6` - Main actions, buttons
- **Primary Dark**: `#1D4ED8` - Hover states
- **Primary Light**: `#EFF6FF` - Backgrounds

### Feedback Colors
- **Success Green**: `#22C55E` - Correct answers
- **Error Red**: `#EF4444` - Wrong answers
- **Warning Yellow**: `#F59E0B` - Warnings

### Neutral Colors
- **Text Dark**: `#1F2937` - Primary text
- **Text Medium**: `#6B7280` - Secondary text
- **Text Light**: `#9CA3AF` - Muted text
- **Background**: `#F9FAFB` - Page background
- **Card**: `#FFFFFF` - Card backgrounds

### Age Group Colors
- **Kids**: `#8B5CF6` (Purple) - Fun, playful
- **Teens**: `#06B6D4` (Cyan) - Modern, cool
- **Adults**: `#3B82F6` (Blue) - Professional
- **Seniors**: `#059669` (Green) - Calm, readable

### Difficulty Colors (gradient from green to red)
- Level 1-2: `#22C55E` (Green)
- Level 3-4: `#84CC16` (Lime)
- Level 5-6: `#F59E0B` (Amber)
- Level 7-8: `#F97316` (Orange)
- Level 9-10: `#EF4444` (Red)

## Typography

```css
/* Headings */
font-family: 'Inter', system-ui, sans-serif;

/* Question text */
font-size: 1.25rem; /* 20px */
line-height: 1.75rem;
font-weight: 500;

/* Options */
font-size: 1rem; /* 16px */
line-height: 1.5rem;

/* Progress/Stats */
font-size: 0.875rem; /* 14px */
font-weight: 600;
```

## Page Layouts

### Home Page
```
┌─────────────────────────────────────────┐
│              HEADER                      │
│         1000 Question Mastery           │
├─────────────────────────────────────────┤
│                                         │
│          [Hero Illustration]            │
│                                         │
│     "Master 1000 Questions Across       │
│        All Topics & Earn Your           │
│        Certificate of Mastery!"         │
│                                         │
│         [ Start New Game ]              │
│         [ Continue Game ]               │
│         [ View History ]                │
│                                         │
└─────────────────────────────────────────┘
```

### Setup Page
```
┌─────────────────────────────────────────┐
│  ← Back         Setup                   │
├─────────────────────────────────────────┤
│                                         │
│     Enter Your Name                     │
│     ┌─────────────────────────────┐    │
│     │ [Your name here...]         │    │
│     └─────────────────────────────┘    │
│                                         │
│     Select Your Age Group               │
│                                         │
│     ┌──────────┐  ┌──────────┐         │
│     │   Kids   │  │  Teens   │         │
│     │  6-12    │  │  13-17   │         │
│     └──────────┘  └──────────┘         │
│                                         │
│     ┌──────────┐  ┌──────────┐         │
│     │  Adults  │  │ Seniors  │         │
│     │  18-59   │  │   60+    │         │
│     └──────────┘  └──────────┘         │
│                                         │
│            [ Begin Quiz ]               │
│                                         │
└─────────────────────────────────────────┘
```

### Game Page
```
┌─────────────────────────────────────────┐
│  Question 247/1000         Diff: 3/10   │
│  ═══════════░░░░░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   [Category: Geography]         │   │
│  │                                 │   │
│  │   What is the capital city     │   │
│  │   of Australia?                │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  A) Sydney                      │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  B) Melbourne                   │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  C) Canberra                    │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │  D) Perth                       │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ──────────────────────────────────    │
│  ✓ 198 correct    ✗ 48 wrong           │
│                                         │
│             [Pause]  [Quit]             │
└─────────────────────────────────────────┘
```

### Answer Feedback (Correct)
```
┌─────────────────────────────────────────┐
│                                         │
│     ✓ CORRECT!                          │
│                                         │
│     The answer is:                      │
│     C) Canberra                         │
│                                         │
│         [ Next Question → ]             │
│                                         │
└─────────────────────────────────────────┘
```

### Answer Feedback (Wrong)
```
┌─────────────────────────────────────────┐
│                                         │
│     ✗ INCORRECT                         │
│                                         │
│     You selected: A) Sydney             │
│     Correct answer: C) Canberra         │
│                                         │
│         [ Next Question → ]             │
│                                         │
└─────────────────────────────────────────┘
```

### Certificate Page
```
┌─────────────────────────────────────────┐
│           🎉 Congratulations!            │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  ═══════════════════════════   │   │
│  │       CERTIFICATE OF           │   │
│  │          MASTERY               │   │
│  │                                │   │
│  │    This certifies that         │   │
│  │                                │   │
│  │      ** John Doe **            │   │
│  │                                │   │
│  │  has successfully completed    │   │
│  │  1000 Question Mastery         │   │
│  │                                │   │
│  │  Score: 847/1000 (84.7%)       │   │
│  │  Tier: SILVER                  │   │
│  │                                │   │
│  │  Date: January 30, 2026        │   │
│  │  Code: XYZ-123-ABC             │   │
│  │  ═══════════════════════════   │   │
│  └─────────────────────────────────┘   │
│                                         │
│    [ Download PNG ]  [ Share ]          │
│                                         │
│          [ Play Again ]                 │
└─────────────────────────────────────────┘
```

## Component Specifications

### Question Card
- Border radius: 12px
- Padding: 24px
- Shadow: `0 4px 6px -1px rgba(0, 0, 0, 0.1)`
- Background: White
- Min-height: 200px

### Option Button
- Border radius: 8px
- Padding: 16px 20px
- Border: 2px solid `#E5E7EB`
- Hover: Border color `#3B82F6`, background `#EFF6FF`
- Selected: Border color `#3B82F6`, background `#DBEAFE`
- Correct (revealed): Background `#DCFCE7`, border `#22C55E`
- Wrong (revealed): Background `#FEE2E2`, border `#EF4444`

### Progress Bar
- Height: 8px
- Border radius: 4px
- Background: `#E5E7EB`
- Fill: Gradient based on progress
- Animation: Smooth transition on update

### Difficulty Badge
- Border radius: 9999px (pill)
- Padding: 4px 12px
- Font size: 12px
- Font weight: 600
- Color: Based on difficulty level

## Animations

### Page Transitions
```css
.page-enter-active,
.page-leave-active {
  transition: opacity 0.2s ease;
}
.page-enter-from,
.page-leave-to {
  opacity: 0;
}
```

### Question Card Entry
```css
.question-enter-active {
  transition: all 0.3s ease-out;
}
.question-enter-from {
  opacity: 0;
  transform: translateX(20px);
}
```

### Correct Answer Celebration
- Confetti animation (optional)
- Green pulse effect on card
- Score counter increment animation

### Wrong Answer Feedback
- Red shake animation on card
- Brief red flash

## Responsive Breakpoints

```css
/* Mobile first */
/* Small (default): < 640px */

/* Medium: 640px+ */
@media (min-width: 640px) { }

/* Large: 1024px+ */
@media (min-width: 1024px) { }
```

### Mobile Adaptations
- Full-width question cards
- Stacked option buttons
- Bottom-fixed controls
- Larger touch targets (min 44px)

### Desktop Adaptations
- Centered content (max-width: 720px)
- Side-by-side stats
- Keyboard navigation support
