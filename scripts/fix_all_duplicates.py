#!/usr/bin/env python3
"""
Comprehensive script to fix all duplicate questions:
1. Reassign unique IDs to ALL questions
2. Replace duplicate texts within same age group
3. Replace cross-age duplicate texts

ID Format: {age_prefix}{difficulty:02d}{sequence:04d}
- age_prefix: 1=little-kids, 2=kids, 3=teens, 4=adults, 5=seniors
- difficulty: 01-10
- sequence: 0001-9999 (per difficulty per age group)
"""

import os
import re
import json
from collections import defaultdict
from pathlib import Path
import random
import sys

# Add script directory to path for imports
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from replacement_questions import get_replacement_question

data_dir = script_dir.parent / 'server' / 'data'

AGE_GROUPS = ['little-kids', 'kids', 'teens', 'adults', 'seniors']
AGE_PREFIXES = {
    'little-kids': '1',
    'kids': '2',
    'teens': '3',
    'adults': '4',
    'seniors': '5'
}

# Global tracking
all_texts_seen = set()  # Track all texts globally to avoid cross-age duplicates
generated_texts = set()  # Track generated replacement texts to avoid creating new duplicates

def parse_question_file(file_path):
    """Parse a TypeScript question file and extract questions."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    questions = []

    # Match question objects - handle multiline and escaped quotes
    pattern = r"\{\s*id:\s*['\"]([^'\"]+)['\"]\s*,\s*text:\s*['\"]((?:[^'\"\\]|\\.)*)['\"]\s*,\s*options:\s*\[((?:[^\]]|\n)*)\]\s*,\s*correctIndex:\s*(\d)\s*,\s*difficulty:\s*(\d+)\s*,\s*category:\s*['\"]([^'\"]+)['\"]\s*\}"

    for match in re.finditer(pattern, content, re.DOTALL):
        q_id, text, options_str, correct_idx, difficulty, category = match.groups()

        # Clean up text
        text = text.replace("\\'", "'").replace('\\"', '"').replace('\\n', ' ').strip()

        # Parse options
        opts = []
        for opt_match in re.finditer(r"['\"]([^'\"]*)['\"]", options_str):
            opt = opt_match.group(1).replace("\\'", "'").replace('\\"', '"')
            opts.append(opt)

        if len(opts) == 4:
            questions.append({
                'id': q_id,
                'text': text,
                'options': opts,
                'correctIndex': int(correct_idx),
                'difficulty': int(difficulty),
                'category': category
            })

    return questions

def generate_unique_replacement(age_group, category, difficulty):
    """Generate a replacement question that hasn't been used before."""
    global generated_texts

    max_attempts = 100
    for _ in range(max_attempts):
        q = get_replacement_question(age_group, category, difficulty)
        text_key = q['text'].lower().strip()

        if text_key not in all_texts_seen and text_key not in generated_texts:
            generated_texts.add(text_key)
            all_texts_seen.add(text_key)
            return q

    # Fallback: generate a truly unique math question
    while True:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        answer = a + b
        text = f"Calculate: {a} + {b} = ?"
        text_key = text.lower().strip()

        if text_key not in all_texts_seen and text_key not in generated_texts:
            wrong = [answer + random.randint(1, 10), answer - random.randint(1, 10), answer + random.randint(11, 20)]
            options = [str(answer)] + [str(w) for w in wrong]
            random.shuffle(options)
            generated_texts.add(text_key)
            all_texts_seen.add(text_key)
            return {
                'text': text,
                'options': options,
                'correctIndex': options.index(str(answer))
            }

def generate_new_id(age_group, difficulty, sequence):
    """Generate a new unique ID."""
    prefix = AGE_PREFIXES[age_group]
    return f"{prefix}{difficulty:02d}{sequence:04d}"

def write_question_file(file_path, questions, difficulty):
    """Write questions back to a TypeScript file."""
    lines = ["export const questions = ["]

    for i, q in enumerate(questions):
        # Escape single quotes in text and options
        text = q['text'].replace("'", "\\'")
        options = [opt.replace("'", "\\'") for opt in q['options']]
        options_str = ", ".join([f"'{opt}'" for opt in options])

        comma = "," if i < len(questions) - 1 else ""
        line = f"  {{ id: '{q['id']}', text: '{text}', options: [{options_str}], correctIndex: {q['correctIndex']}, difficulty: {difficulty}, category: '{q['category']}' }}{comma}"
        lines.append(line)

    lines.append("]")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")

def process_all_files():
    """Process all question files, fixing IDs and duplicates."""
    global all_texts_seen

    stats = {
        'total_questions': 0,
        'fixed_ids': 0,
        'fixed_within_age': 0,
        'fixed_cross_age': 0,
        'by_age_group': {}
    }

    for age_group in AGE_GROUPS:
        age_dir = data_dir / age_group
        if not age_dir.exists():
            print(f"Skipping {age_group} - directory not found")
            continue

        print(f"\nProcessing {age_group}...")

        age_texts_seen = set()  # Track texts seen in this age group
        age_stats = {'questions': 0, 'fixed_ids': 0, 'fixed_within': 0, 'fixed_cross': 0}

        for d in range(1, 11):
            diff_dir = age_dir / f'd{d}'
            if not diff_dir.exists():
                continue

            sequence = 1  # Reset sequence for each difficulty

            for f_num in range(1, 11):
                file_path = diff_dir / f'f{f_num}.ts'
                if not file_path.exists():
                    continue

                questions = parse_question_file(file_path)
                if not questions:
                    print(f"  Warning: Could not parse {file_path}")
                    continue

                new_questions = []

                for q in questions:
                    text_key = q['text'].lower().strip()

                    # Generate new unique ID
                    new_id = generate_new_id(age_group, d, sequence)
                    sequence += 1

                    if new_id != q['id']:
                        age_stats['fixed_ids'] += 1

                    # Check for duplicate text within age group
                    if text_key in age_texts_seen:
                        replacement = generate_unique_replacement(age_group, q['category'], d)
                        new_q = {
                            'id': new_id,
                            'text': replacement['text'],
                            'options': replacement['options'],
                            'correctIndex': replacement['correctIndex'],
                            'difficulty': d,
                            'category': q['category']
                        }
                        age_stats['fixed_within'] += 1
                    # Check for cross-age duplicate
                    elif text_key in all_texts_seen:
                        replacement = generate_unique_replacement(age_group, q['category'], d)
                        new_q = {
                            'id': new_id,
                            'text': replacement['text'],
                            'options': replacement['options'],
                            'correctIndex': replacement['correctIndex'],
                            'difficulty': d,
                            'category': q['category']
                        }
                        age_stats['fixed_cross'] += 1
                    else:
                        # Keep original question with new ID
                        new_q = {
                            'id': new_id,
                            'text': q['text'],
                            'options': q['options'],
                            'correctIndex': q['correctIndex'],
                            'difficulty': d,
                            'category': q['category']
                        }
                        age_texts_seen.add(text_key)
                        all_texts_seen.add(text_key)

                    new_questions.append(new_q)
                    age_stats['questions'] += 1

                # Write fixed file
                write_question_file(file_path, new_questions, d)

            print(f"  d{d}: {sequence - 1} questions processed")

        stats['by_age_group'][age_group] = age_stats
        stats['total_questions'] += age_stats['questions']
        stats['fixed_ids'] += age_stats['fixed_ids']
        stats['fixed_within_age'] += age_stats['fixed_within']
        stats['fixed_cross_age'] += age_stats['fixed_cross']

        print(f"  Summary: {age_stats['questions']} questions, {age_stats['fixed_ids']} IDs fixed, {age_stats['fixed_within']} within-age dups, {age_stats['fixed_cross']} cross-age dups")

    return stats

def main():
    print("=" * 70)
    print("FIXING ALL DUPLICATE QUESTIONS")
    print("=" * 70)

    stats = process_all_files()

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"Total questions processed: {stats['total_questions']}")
    print(f"Total IDs reassigned: {stats['fixed_ids']}")
    print(f"Total within-age duplicates fixed: {stats['fixed_within_age']}")
    print(f"Total cross-age duplicates fixed: {stats['fixed_cross_age']}")
    print()

    print("By age group:")
    for ag, ag_stats in stats['by_age_group'].items():
        print(f"  {ag}: {ag_stats['questions']} questions, {ag_stats['fixed_within']} within-age, {ag_stats['fixed_cross']} cross-age")

    print("\nAll question files have been updated!")

    # Save stats
    stats_path = script_dir / 'fix-stats.json'
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2)
    print(f"\nStats saved to: {stats_path}")

if __name__ == '__main__':
    main()
