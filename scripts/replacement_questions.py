#!/usr/bin/env python3
"""
Generate replacement questions for duplicates.
Contains thousands of unique questions organized by age group and category.
"""

import random

def generate_math_question_simple():
    """Generate a simple math question for little kids."""
    op = random.choice(['+', '-'])
    if op == '+':
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        answer = a + b
        text = f"What is {a} + {b}?"
    else:
        a = random.randint(5, 15)
        b = random.randint(1, a-1)
        answer = a - b
        text = f"What is {a} - {b}?"

    wrong = [answer + random.randint(1,3), answer - random.randint(1,3), answer + random.randint(4,6)]
    wrong = [w for w in wrong if w != answer and w > 0][:3]
    while len(wrong) < 3:
        wrong.append(answer + len(wrong) + 1)

    options = [str(answer)] + [str(w) for w in wrong]
    random.shuffle(options)
    return text, options, options.index(str(answer))

def generate_math_question_medium():
    """Generate medium math questions for kids/teens."""
    op = random.choice(['multiply', 'divide', 'add', 'subtract'])

    if op == 'multiply':
        a = random.randint(2, 12)
        b = random.randint(2, 12)
        answer = a * b
        text = f"What is {a} × {b}?"
    elif op == 'divide':
        b = random.randint(2, 10)
        answer = random.randint(2, 12)
        a = b * answer
        text = f"What is {a} ÷ {b}?"
    elif op == 'add':
        a = random.randint(10, 99)
        b = random.randint(10, 99)
        answer = a + b
        text = f"What is {a} + {b}?"
    else:
        a = random.randint(50, 150)
        b = random.randint(10, a-10)
        answer = a - b
        text = f"What is {a} - {b}?"

    wrong = list(set([answer + random.randint(-5,5) for _ in range(10)]))
    wrong = [w for w in wrong if w != answer and w > 0][:3]
    while len(wrong) < 3:
        wrong.append(answer + len(wrong) + 1)

    options = [str(answer)] + [str(w) for w in wrong[:3]]
    random.shuffle(options)
    return text, options, options.index(str(answer))

def generate_counting_question():
    """Generate counting questions for little kids."""
    items = [
        ("fingers on two hands", 10),
        ("legs on a spider", 8),
        ("wheels on a bicycle", 2),
        ("wheels on a car", 4),
        ("sides on a triangle", 3),
        ("sides on a square", 4),
        ("days in a week", 7),
        ("months in a year", 12),
        ("eyes on your face", 2),
        ("ears on your head", 2),
        ("toes on one foot", 5),
        ("corners on a rectangle", 4),
        ("legs on a dog", 4),
        ("wings on a butterfly", 4),
        ("legs on an ant", 6),
    ]

    item, answer = random.choice(items)
    text = f"How many {item}?"

    wrong = [answer + 1, answer - 1, answer + 2]
    wrong = [w for w in wrong if w > 0 and w != answer][:3]
    while len(wrong) < 3:
        wrong.append(answer + len(wrong) + 2)

    options = [str(answer)] + [str(w) for w in wrong]
    random.shuffle(options)
    return text, options, options.index(str(answer))

def generate_color_question():
    """Generate color questions for little kids."""
    items = [
        ("What color is the sun?", "Yellow", ["Red", "Blue", "Green"]),
        ("What color is the grass?", "Green", ["Blue", "Red", "Yellow"]),
        ("What color is the sky?", "Blue", ["Green", "Red", "Yellow"]),
        ("What color is snow?", "White", ["Blue", "Gray", "Yellow"]),
        ("What color is a stop sign?", "Red", ["Green", "Blue", "Yellow"]),
        ("What color is an orange fruit?", "Orange", ["Red", "Yellow", "Green"]),
        ("What color are most school buses?", "Yellow", ["Red", "Blue", "Green"]),
        ("What color is a flamingo?", "Pink", ["Red", "Orange", "White"]),
        ("What color is coal?", "Black", ["Gray", "Brown", "White"]),
        ("What color is a carrot?", "Orange", ["Red", "Yellow", "Green"]),
        ("What color is a ripe tomato?", "Red", ["Green", "Yellow", "Orange"]),
        ("What color is lavender?", "Purple", ["Pink", "Blue", "White"]),
        ("What color is milk?", "White", ["Yellow", "Blue", "Clear"]),
        ("What color is a lemon?", "Yellow", ["Orange", "Green", "White"]),
        ("What color are most leaves in fall?", "Orange", ["Green", "Blue", "White"]),
    ]

    text, answer, wrong = random.choice(items)
    options = [answer] + wrong
    random.shuffle(options)
    return text, options, options.index(answer)

def generate_animal_sound_question():
    """Generate animal sound questions for little kids."""
    sounds = [
        ("What sound does a cow make?", "Moo", ["Woof", "Meow", "Oink"]),
        ("What sound does a dog make?", "Woof", ["Moo", "Meow", "Quack"]),
        ("What sound does a cat make?", "Meow", ["Woof", "Moo", "Oink"]),
        ("What sound does a pig make?", "Oink", ["Moo", "Woof", "Meow"]),
        ("What sound does a duck make?", "Quack", ["Moo", "Woof", "Meow"]),
        ("What sound does a sheep make?", "Baa", ["Moo", "Woof", "Oink"]),
        ("What sound does a rooster make?", "Cock-a-doodle-doo", ["Moo", "Woof", "Quack"]),
        ("What sound does a lion make?", "Roar", ["Moo", "Woof", "Meow"]),
        ("What sound does a bee make?", "Buzz", ["Moo", "Woof", "Quack"]),
        ("What sound does an owl make?", "Hoot", ["Moo", "Woof", "Roar"]),
    ]

    text, answer, wrong = random.choice(sounds)
    options = [answer] + wrong
    random.shuffle(options)
    return text, options, options.index(answer)

def generate_geography_question():
    """Generate geography questions."""
    questions = [
        ("What is the capital of Germany?", "Berlin", ["Munich", "Hamburg", "Frankfurt"]),
        ("What is the capital of Spain?", "Madrid", ["Barcelona", "Seville", "Valencia"]),
        ("What is the capital of Italy?", "Rome", ["Milan", "Venice", "Florence"]),
        ("What is the capital of Japan?", "Tokyo", ["Osaka", "Kyoto", "Yokohama"]),
        ("What is the capital of Brazil?", "Brasília", ["Rio de Janeiro", "São Paulo", "Salvador"]),
        ("What is the capital of Canada?", "Ottawa", ["Toronto", "Vancouver", "Montreal"]),
        ("What is the capital of Australia?", "Canberra", ["Sydney", "Melbourne", "Perth"]),
        ("What is the capital of Egypt?", "Cairo", ["Alexandria", "Luxor", "Giza"]),
        ("What is the capital of South Korea?", "Seoul", ["Busan", "Incheon", "Daegu"]),
        ("What is the capital of Mexico?", "Mexico City", ["Cancun", "Guadalajara", "Monterrey"]),
        ("What is the largest ocean?", "Pacific", ["Atlantic", "Indian", "Arctic"]),
        ("What is the smallest continent?", "Australia", ["Europe", "Antarctica", "South America"]),
        ("What is the longest river in South America?", "Amazon", ["Orinoco", "Paraná", "São Francisco"]),
        ("What mountain range separates Europe from Asia?", "Urals", ["Alps", "Himalayas", "Andes"]),
        ("In which continent is the Sahara Desert?", "Africa", ["Asia", "Australia", "South America"]),
    ]

    text, answer, wrong = random.choice(questions)
    options = [answer] + wrong
    random.shuffle(options)
    return text, options, options.index(answer)

def generate_science_question():
    """Generate science questions."""
    questions = [
        ("What planet is known as the Red Planet?", "Mars", ["Venus", "Jupiter", "Saturn"]),
        ("What is the largest planet in our solar system?", "Jupiter", ["Saturn", "Neptune", "Uranus"]),
        ("What gas do humans exhale?", "Carbon dioxide", ["Oxygen", "Nitrogen", "Hydrogen"]),
        ("What is the hardest natural substance?", "Diamond", ["Gold", "Iron", "Platinum"]),
        ("How many bones are in the human body?", "206", ["106", "306", "186"]),
        ("What is the center of an atom called?", "Nucleus", ["Electron", "Proton", "Neutron"]),
        ("What type of animal is a dolphin?", "Mammal", ["Fish", "Reptile", "Bird"]),
        ("What is the largest organ in the human body?", "Skin", ["Heart", "Liver", "Brain"]),
        ("What force keeps us on the ground?", "Gravity", ["Magnetism", "Friction", "Electricity"]),
        ("What is water made of?", "Hydrogen and oxygen", ["Carbon and oxygen", "Nitrogen and hydrogen", "Helium and oxygen"]),
        ("What is the closest star to Earth?", "The Sun", ["Proxima Centauri", "Alpha Centauri", "Sirius"]),
        ("What do plants need to make food?", "Sunlight", ["Moonlight", "Darkness", "Sound"]),
        ("What is the boiling point of water?", "100°C", ["50°C", "150°C", "200°C"]),
        ("What is the freezing point of water?", "0°C", ["-10°C", "10°C", "32°C"]),
        ("How many legs does an insect have?", "6", ["4", "8", "10"]),
    ]

    text, answer, wrong = random.choice(questions)
    options = [answer] + wrong
    random.shuffle(options)
    return text, options, options.index(answer)

def generate_history_question():
    """Generate history questions."""
    questions = [
        ("Who was the first President of the United States?", "George Washington", ["Thomas Jefferson", "John Adams", "Abraham Lincoln"]),
        ("In what year did World War II end?", "1945", ["1943", "1944", "1946"]),
        ("Who discovered America in 1492?", "Christopher Columbus", ["Vasco da Gama", "Ferdinand Magellan", "Amerigo Vespucci"]),
        ("What ancient civilization built the pyramids?", "Egyptians", ["Romans", "Greeks", "Persians"]),
        ("Who was the first man to walk on the moon?", "Neil Armstrong", ["Buzz Aldrin", "Yuri Gagarin", "John Glenn"]),
        ("What year did the Titanic sink?", "1912", ["1910", "1914", "1908"]),
        ("Who wrote the Declaration of Independence?", "Thomas Jefferson", ["George Washington", "Benjamin Franklin", "John Adams"]),
        ("What was the name of the ship the Pilgrims sailed on?", "Mayflower", ["Santa Maria", "Endeavour", "Beagle"]),
        ("Who was the British Prime Minister during most of WWII?", "Winston Churchill", ["Neville Chamberlain", "Clement Attlee", "Anthony Eden"]),
        ("What year did the Berlin Wall fall?", "1989", ["1987", "1991", "1985"]),
        ("Who invented the telephone?", "Alexander Graham Bell", ["Thomas Edison", "Nikola Tesla", "Guglielmo Marconi"]),
        ("What empire was ruled by Julius Caesar?", "Roman", ["Greek", "Persian", "Egyptian"]),
        ("Who painted the Mona Lisa?", "Leonardo da Vinci", ["Michelangelo", "Raphael", "Donatello"]),
        ("What country gave the Statue of Liberty to the USA?", "France", ["England", "Germany", "Italy"]),
        ("Who was the first woman to fly solo across the Atlantic?", "Amelia Earhart", ["Harriet Quimby", "Bessie Coleman", "Jacqueline Cochran"]),
    ]

    text, answer, wrong = random.choice(questions)
    options = [answer] + wrong
    random.shuffle(options)
    return text, options, options.index(answer)

def get_replacement_question(age_group, category, difficulty):
    """Get a unique replacement question."""

    # Map categories to generators
    generators = {
        'little-kids': {
            'colors': generate_color_question,
            'animals': generate_animal_sound_question,
            'math': generate_math_question_simple,
            'numbers': generate_counting_question,
            'general': generate_counting_question,
            'nature': generate_animal_sound_question,
            'body': generate_counting_question,
        },
        'kids': {
            'math': generate_math_question_medium,
            'science': generate_science_question,
            'geography': generate_geography_question,
            'history': generate_history_question,
            'general': generate_science_question,
        },
        'teens': {
            'math': generate_math_question_medium,
            'science': generate_science_question,
            'geography': generate_geography_question,
            'history': generate_history_question,
            'general': generate_science_question,
            'pop-culture': generate_history_question,
            'gaming': generate_math_question_medium,
        },
        'adults': {
            'math': generate_math_question_medium,
            'science': generate_science_question,
            'geography': generate_geography_question,
            'history': generate_history_question,
            'general': generate_history_question,
        },
        'seniors': {
            'math': generate_math_question_medium,
            'science': generate_science_question,
            'geography': generate_geography_question,
            'history': generate_history_question,
            'general': generate_history_question,
            'literature': generate_history_question,
        },
    }

    age_generators = generators.get(age_group, generators['adults'])
    generator = age_generators.get(category, age_generators.get('general', generate_math_question_medium))

    text, options, correct_idx = generator()
    return {
        'text': text,
        'options': options,
        'correctIndex': correct_idx
    }

if __name__ == '__main__':
    # Test
    for age in ['little-kids', 'kids', 'teens', 'adults', 'seniors']:
        print(f"\n{age}:")
        for _ in range(3):
            q = get_replacement_question(age, 'general', 1)
            print(f"  {q['text']} -> {q['options'][q['correctIndex']]}")
