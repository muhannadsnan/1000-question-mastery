#!/usr/bin/env python3
"""
Analyze duplicate questions across all age groups and difficulties.
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path

# Get the data directory
script_dir = Path(__file__).parent
data_dir = script_dir.parent / 'server' / 'data'

age_groups = ['little-kids', 'kids', 'teens', 'adults', 'seniors']

# Store all questions
all_questions = {}  # id -> {ageGroup, difficulty, file, text, ...}
all_texts = defaultdict(list)  # normalized_text -> [occurrences]

def parse_question_file(file_path):
    """Parse a TypeScript question file and extract questions."""
    questions = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return questions

    # Match question objects - handle both single and double quotes
    pattern = r"\{\s*id:\s*['\"]([^'\"]+)['\"]\s*,\s*text:\s*['\"](.+?)['\"]\s*,\s*options:\s*\[([^\]]+)\]\s*,\s*correctIndex:\s*(\d)\s*,\s*difficulty:\s*(\d+)\s*,\s*category:\s*['\"]([^'\"]+)['\"]\s*\}"

    for match in re.finditer(pattern, content, re.DOTALL):
        q_id, text, options_str, correct_idx, difficulty, category = match.groups()

        # Clean up text (handle escaped quotes)
        text = text.replace("\\'", "'").replace('\\"', '"')

        questions.append({
            'id': q_id,
            'text': text,
            'options_str': options_str,
            'correctIndex': int(correct_idx),
            'difficulty': int(difficulty),
            'category': category
        })

    return questions

def scan_all_questions():
    """Scan all question files and collect data."""
    print("Scanning all question files...\n")

    duplicate_ids = []
    stats = {}

    for age_group in age_groups:
        age_dir = data_dir / age_group
        if not age_dir.exists():
            print(f"Skipping {age_group} - directory not found")
            continue

        count = 0

        for d in range(1, 11):
            diff_dir = age_dir / f'd{d}'
            if not diff_dir.exists():
                continue

            for f in range(1, 11):
                file_path = diff_dir / f'f{f}.ts'
                if not file_path.exists():
                    continue

                questions = parse_question_file(file_path)
                count += len(questions)

                for q in questions:
                    # Check for duplicate ID
                    if q['id'] in all_questions:
                        existing = all_questions[q['id']]
                        duplicate_ids.append({
                            'id': q['id'],
                            'first': {
                                'ageGroup': existing['ageGroup'],
                                'difficulty': existing['difficulty'],
                                'file': existing['file'],
                                'text': existing['text'][:80]
                            },
                            'second': {
                                'ageGroup': age_group,
                                'difficulty': d,
                                'file': f'f{f}.ts',
                                'text': q['text'][:80]
                            }
                        })
                    else:
                        all_questions[q['id']] = {
                            'ageGroup': age_group,
                            'difficulty': d,
                            'file': f'f{f}.ts',
                            'text': q['text'],
                            'category': q['category']
                        }

                    # Track text occurrences
                    text_key = q['text'].lower().strip()
                    all_texts[text_key].append({
                        'ageGroup': age_group,
                        'difficulty': d,
                        'file': f'f{f}.ts',
                        'id': q['id'],
                        'text': q['text']
                    })

        stats[age_group] = count
        print(f"{age_group}: {count} questions")

    return duplicate_ids, stats

def analyze_text_duplicates():
    """Find duplicate texts within and across age groups."""
    within_age = []
    cross_age = []

    for text_key, occurrences in all_texts.items():
        if len(occurrences) <= 1:
            continue

        # Group by age group
        by_age = defaultdict(list)
        for occ in occurrences:
            by_age[occ['ageGroup']].append(occ)

        # Within same age group duplicates
        for ag, occs in by_age.items():
            if len(occs) > 1:
                within_age.append({
                    'text': occurrences[0]['text'][:100],
                    'ageGroup': ag,
                    'count': len(occs),
                    'locations': [{'d': o['difficulty'], 'f': o['file'], 'id': o['id']} for o in occs]
                })

        # Cross age group duplicates
        if len(by_age) > 1:
            cross_age.append({
                'text': occurrences[0]['text'][:100],
                'ageGroups': list(by_age.keys()),
                'count': len(occurrences),
                'locations': [{'age': o['ageGroup'], 'd': o['difficulty'], 'f': o['file'], 'id': o['id']} for o in occurrences]
            })

    return within_age, cross_age

def main():
    duplicate_ids, stats = scan_all_questions()
    within_age_dups, cross_age_dups = analyze_text_duplicates()

    print(f"\n=== SUMMARY ===")
    print(f"Total unique IDs: {len(all_questions)}")
    print(f"Duplicate IDs found: {len(duplicate_ids)}")
    print(f"Duplicate texts within same age group: {len(within_age_dups)}")
    print(f"Cross-age duplicate texts: {len(cross_age_dups)}")

    # Count within-age duplicates by age group
    print(f"\n=== WITHIN-AGE DUPLICATES BY GROUP ===")
    by_group = defaultdict(int)
    for d in within_age_dups:
        by_group[d['ageGroup']] += 1
    for ag in age_groups:
        print(f"{ag}: {by_group.get(ag, 0)} duplicate texts")

    # Save detailed report
    report = {
        'stats': stats,
        'summary': {
            'total_unique_ids': len(all_questions),
            'duplicate_ids': len(duplicate_ids),
            'within_age_duplicates': len(within_age_dups),
            'cross_age_duplicates': len(cross_age_dups)
        },
        'duplicate_ids': duplicate_ids[:100],  # First 100
        'within_age_duplicates': within_age_dups,
        'cross_age_duplicates': cross_age_dups[:200]  # First 200
    }

    report_path = script_dir / 'duplicates-report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\nDetailed report saved to: {report_path}")

if __name__ == '__main__':
    main()
