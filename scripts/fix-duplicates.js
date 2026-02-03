/**
 * Script to find and fix duplicate questions
 * Run with: node scripts/fix-duplicates.js
 */

import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const dataDir = path.join(__dirname, '..', 'server', 'data')

// Age groups and their ID prefixes
const ageGroups = ['little-kids', 'kids', 'teens', 'adults', 'seniors']
const ageGroupPrefixes = {
  'little-kids': '1',
  'kids': '2',
  'teens': '3',
  'adults': '4',
  'seniors': '5'
}

// Store all questions globally
const allQuestions = new Map() // id -> {ageGroup, difficulty, file, question}
const allTexts = new Map() // text -> [{ageGroup, difficulty, file, id}]
const duplicateIds = []
const duplicateTextsWithinAge = []
const crossAgeDuplicates = []

// Parse a question file and extract questions
function parseQuestionFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8')

  // Extract questions array using regex
  const questionsMatch = content.match(/export\s+const\s+questions\s*=\s*\[([\s\S]*?)\];?\s*$/m)
  if (!questionsMatch) {
    console.log(`Warning: Could not parse ${filePath}`)
    return []
  }

  const questionsStr = questionsMatch[1]
  const questions = []

  // Match individual question objects
  const questionRegex = /\{\s*id:\s*['"]([^'"]+)['"]\s*,\s*text:\s*['"]([^'"]+)['"]\s*,\s*options:\s*\[([^\]]+)\]\s*,\s*correctIndex:\s*(\d)\s*,\s*difficulty:\s*(\d+)\s*,\s*category:\s*['"]([^'"]+)['"]\s*\}/g

  let match
  while ((match = questionRegex.exec(questionsStr)) !== null) {
    questions.push({
      id: match[1],
      text: match[2],
      options: match[3].split(',').map(o => o.trim().replace(/^['"]|['"]$/g, '')),
      correctIndex: parseInt(match[4]),
      difficulty: parseInt(match[5]),
      category: match[6]
    })
  }

  return questions
}

// Scan all question files
function scanAllQuestions() {
  console.log('Scanning all question files...\n')

  for (const ageGroup of ageGroups) {
    const ageDir = path.join(dataDir, ageGroup)
    if (!fs.existsSync(ageDir)) {
      console.log(`Skipping ${ageGroup} - directory not found`)
      continue
    }

    let ageGroupCount = 0

    for (let d = 1; d <= 10; d++) {
      const diffDir = path.join(ageDir, `d${d}`)
      if (!fs.existsSync(diffDir)) continue

      for (let f = 1; f <= 10; f++) {
        const filePath = path.join(diffDir, `f${f}.ts`)
        if (!fs.existsSync(filePath)) continue

        const questions = parseQuestionFile(filePath)
        ageGroupCount += questions.length

        for (const q of questions) {
          // Check for duplicate ID
          if (allQuestions.has(q.id)) {
            const existing = allQuestions.get(q.id)
            duplicateIds.push({
              id: q.id,
              first: existing,
              second: { ageGroup, difficulty: d, file: `f${f}.ts`, question: q }
            })
          } else {
            allQuestions.set(q.id, { ageGroup, difficulty: d, file: `f${f}.ts`, question: q })
          }

          // Track text occurrences
          const textKey = q.text.toLowerCase().trim()
          if (!allTexts.has(textKey)) {
            allTexts.set(textKey, [])
          }
          allTexts.get(textKey).push({ ageGroup, difficulty: d, file: `f${f}.ts`, id: q.id, text: q.text })
        }
      }
    }

    console.log(`${ageGroup}: ${ageGroupCount} questions`)
  }

  console.log(`\nTotal unique IDs: ${allQuestions.size}`)
  console.log(`Total duplicate IDs: ${duplicateIds.length}`)
}

// Analyze text duplicates
function analyzeTextDuplicates() {
  console.log('\nAnalyzing text duplicates...\n')

  for (const [text, occurrences] of allTexts) {
    if (occurrences.length > 1) {
      // Group by age group
      const byAgeGroup = {}
      for (const occ of occurrences) {
        if (!byAgeGroup[occ.ageGroup]) byAgeGroup[occ.ageGroup] = []
        byAgeGroup[occ.ageGroup].push(occ)
      }

      const ageGroupsWithDup = Object.keys(byAgeGroup)

      // Within same age group
      for (const ag of ageGroupsWithDup) {
        if (byAgeGroup[ag].length > 1) {
          duplicateTextsWithinAge.push({
            text: occurrences[0].text,
            ageGroup: ag,
            occurrences: byAgeGroup[ag]
          })
        }
      }

      // Cross age group
      if (ageGroupsWithDup.length > 1) {
        crossAgeDuplicates.push({
          text: occurrences[0].text,
          ageGroups: ageGroupsWithDup,
          occurrences
        })
      }
    }
  }

  console.log(`Duplicate texts within same age group: ${duplicateTextsWithinAge.length}`)
  console.log(`Cross-age duplicate texts: ${crossAgeDuplicates.length}`)
}

// Generate report
function generateReport() {
  const report = {
    summary: {
      totalUniqueIds: allQuestions.size,
      duplicateIds: duplicateIds.length,
      duplicateTextsWithinAge: duplicateTextsWithinAge.length,
      crossAgeDuplicates: crossAgeDuplicates.length
    },
    duplicateIds: duplicateIds.slice(0, 50), // First 50 for review
    duplicateTextsWithinAge: duplicateTextsWithinAge.slice(0, 50),
    crossAgeDuplicates: crossAgeDuplicates.slice(0, 50)
  }

  fs.writeFileSync(
    path.join(__dirname, 'duplicates-report.json'),
    JSON.stringify(report, null, 2)
  )

  console.log('\nReport saved to scripts/duplicates-report.json')
}

// Main
scanAllQuestions()
analyzeTextDuplicates()
generateReport()

console.log('\n--- Summary ---')
console.log(`Total questions scanned: ${allQuestions.size + duplicateIds.length}`)
console.log(`Duplicate IDs to fix: ${duplicateIds.length}`)
console.log(`Duplicate texts within age groups: ${duplicateTextsWithinAge.length}`)
console.log(`Cross-age duplicates: ${crossAgeDuplicates.length}`)
