#!/usr/bin/env python3
"""
Generate missing questions to fill all files to 100 questions each.
Total target: 50,000 questions (5 age groups × 10 difficulties × 10 files × 100 questions)
"""

import os
import re
import random
from pathlib import Path
from collections import defaultdict

script_dir = Path(__file__).parent
data_dir = script_dir.parent / 'server' / 'data'

AGE_GROUPS = ['little-kids', 'kids', 'teens', 'adults', 'seniors']
AGE_PREFIXES = {
    'little-kids': '1',
    'kids': '2',
    'teens': '3',
    'adults': '4',
    'seniors': '5'
}

# Track all existing texts to avoid duplicates
all_existing_texts = set()
generated_texts = set()

def load_existing_questions():
    """Load all existing question texts."""
    global all_existing_texts

    for age_group in AGE_GROUPS:
        age_dir = data_dir / age_group
        if not age_dir.exists():
            continue

        for d in range(1, 11):
            diff_dir = age_dir / f'd{d}'
            if not diff_dir.exists():
                continue

            for f_num in range(1, 11):
                file_path = diff_dir / f'f{f_num}.ts'
                if not file_path.exists():
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Extract question texts
                    for match in re.finditer(r"text:\s*'((?:[^'\\]|\\.)*)'", content):
                        text = match.group(1).replace("\\'", "'").lower().strip()
                        all_existing_texts.add(text)
                except:
                    pass

    print(f"Loaded {len(all_existing_texts)} existing question texts")

def count_questions_in_file(file_path):
    """Count questions in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return len(re.findall(r"\bid:\s*'[^']+'", content))
    except:
        return 0

def get_max_sequence(file_path, age_prefix, difficulty):
    """Get the maximum sequence number in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        pattern = f"id:\\s*'{age_prefix}{difficulty:02d}(\\d{{4}})'"
        sequences = [int(m.group(1)) for m in re.finditer(pattern, content)]
        return max(sequences) if sequences else 0
    except:
        return 0

# =============================================================================
# QUESTION GENERATORS BY AGE GROUP
# =============================================================================

# -----------------------------------------------------------------------------
# LITTLE KIDS (3-7 years) - Simple, fun, visual
# -----------------------------------------------------------------------------

LITTLE_KIDS_COLORS = [
    ("red", "the color of a fire truck"),
    ("blue", "the color of the sky"),
    ("yellow", "the color of a banana"),
    ("green", "the color of grass"),
    ("orange", "the color of a carrot"),
    ("purple", "the color of grapes"),
    ("pink", "the color of a flamingo"),
    ("brown", "the color of chocolate"),
    ("white", "the color of snow"),
    ("black", "the color of night"),
]

LITTLE_KIDS_ANIMALS = [
    ("dog", "barks", "puppy", "pet"),
    ("cat", "meows", "kitten", "pet"),
    ("cow", "moos", "calf", "farm"),
    ("pig", "oinks", "piglet", "farm"),
    ("duck", "quacks", "duckling", "farm"),
    ("horse", "neighs", "foal", "farm"),
    ("sheep", "baas", "lamb", "farm"),
    ("chicken", "clucks", "chick", "farm"),
    ("lion", "roars", "cub", "wild"),
    ("elephant", "trumpets", "calf", "wild"),
    ("monkey", "chatters", "baby", "wild"),
    ("bear", "growls", "cub", "wild"),
    ("fish", "swims", "fry", "water"),
    ("bird", "chirps", "chick", "sky"),
    ("butterfly", "flutters", "caterpillar", "insect"),
]

LITTLE_KIDS_SHAPES = [
    ("circle", 0, "round like a ball"),
    ("square", 4, "has 4 equal sides"),
    ("triangle", 3, "has 3 sides"),
    ("rectangle", 4, "like a door"),
    ("star", 5, "twinkles in the sky"),
    ("heart", 0, "shows love"),
    ("oval", 0, "like an egg"),
    ("diamond", 4, "like a kite"),
]

LITTLE_KIDS_NUMBERS = list(range(1, 21))

LITTLE_KIDS_BODY_PARTS = [
    ("eyes", 2, "see"),
    ("ears", 2, "hear"),
    ("nose", 1, "smell"),
    ("mouth", 1, "eat and talk"),
    ("hands", 2, "hold things"),
    ("feet", 2, "walk"),
    ("fingers", 10, "count"),
    ("toes", 10, "wiggle"),
    ("arms", 2, "hug"),
    ("legs", 2, "run"),
]

def generate_little_kids_question(difficulty, category):
    """Generate a question for little kids (ages 3-7)."""

    if category == 'colors':
        color, desc = random.choice(LITTLE_KIDS_COLORS)
        templates = [
            (f"What color is {desc}?", color.capitalize(),
             [c.capitalize() for c, _ in random.sample([x for x in LITTLE_KIDS_COLORS if x[0] != color], 3)]),
            (f"Which color is {color}?", color.capitalize(),
             [c.capitalize() for c, _ in random.sample([x for x in LITTLE_KIDS_COLORS if x[0] != color], 3)]),
        ]
        text, answer, wrong = random.choice(templates)

    elif category == 'animals':
        animal, sound, baby, habitat = random.choice(LITTLE_KIDS_ANIMALS)
        others = [a for a in LITTLE_KIDS_ANIMALS if a[0] != animal]
        templates = [
            (f"What sound does a {animal} make?", sound.capitalize(),
             [random.choice(others)[1].capitalize() for _ in range(3)]),
            (f"Which animal {sound}?", animal.capitalize(),
             [random.choice(others)[0].capitalize() for _ in range(3)]),
            (f"A baby {animal} is called a...", baby.capitalize(),
             [random.choice(others)[2].capitalize() for _ in range(3)]),
            (f"Where does a {animal} live?", "Farm" if habitat == "farm" else ("Zoo" if habitat == "wild" else "Water"),
             ["Space", "Moon", "Cloud"]),
        ]
        text, answer, wrong = random.choice(templates)

    elif category == 'shapes':
        shape, sides, desc = random.choice(LITTLE_KIDS_SHAPES)
        others = [s for s in LITTLE_KIDS_SHAPES if s[0] != shape]
        if sides > 0:
            templates = [
                (f"How many sides does a {shape} have?", str(sides),
                 [str(sides + i) for i in [1, -1, 2] if sides + i > 0][:3]),
                (f"What shape has {sides} sides?", shape.capitalize(),
                 [random.choice(others)[0].capitalize() for _ in range(3)]),
            ]
        else:
            templates = [
                (f"What shape is {desc}?", shape.capitalize(),
                 [random.choice(others)[0].capitalize() for _ in range(3)]),
            ]
        text, answer, wrong = random.choice(templates)

    elif category == 'numbers':
        if difficulty <= 3:
            a = random.randint(1, 5)
            b = random.randint(1, 5)
        elif difficulty <= 6:
            a = random.randint(1, 10)
            b = random.randint(1, 10)
        else:
            a = random.randint(5, 15)
            b = random.randint(1, min(a-1, 10))

        op = random.choice(['+', '-']) if difficulty > 2 else '+'
        if op == '+':
            result = a + b
            text = f"What is {a} + {b}?"
        else:
            result = a - b
            text = f"What is {a} - {b}?"

        answer = str(result)
        wrong = [str(result + i) for i in [1, -1, 2] if result + i >= 0][:3]
        while len(wrong) < 3:
            wrong.append(str(result + len(wrong) + 2))

    elif category == 'body':
        part, count, action = random.choice(LITTLE_KIDS_BODY_PARTS)
        templates = [
            (f"How many {part} do you have?", str(count),
             [str(count + i) for i in [1, -1, 2] if count + i >= 0][:3]),
            (f"What body part helps you {action}?", part.capitalize(),
             [random.choice([p for p, _, _ in LITTLE_KIDS_BODY_PARTS if p != part])[0].capitalize() for _ in range(3)]),
        ]
        text, answer, wrong = random.choice(templates)

    else:  # general/nature
        items = [
            ("How many days are in a week?", "7", ["5", "6", "8"]),
            ("How many fingers on one hand?", "5", ["4", "6", "3"]),
            ("What comes after Monday?", "Tuesday", ["Wednesday", "Sunday", "Friday"]),
            ("What season comes after winter?", "Spring", ["Summer", "Fall", "Winter"]),
            ("What do you use to write?", "Pencil", ["Fork", "Pillow", "Shoe"]),
            ("What do bees make?", "Honey", ["Milk", "Bread", "Juice"]),
            ("What falls from clouds?", "Rain", ["Leaves", "Rocks", "Stars"]),
            ("Where does the sun rise?", "East", ["West", "North", "South"]),
            ("What do we breathe?", "Air", ["Water", "Food", "Light"]),
            ("How many legs does a spider have?", "8", ["6", "4", "10"]),
        ]
        text, answer, wrong = random.choice(items)

    while len(wrong) < 3:
        wrong.append(f"Option {len(wrong) + 1}")

    options = [answer] + wrong[:3]
    random.shuffle(options)
    return text, options, options.index(answer)

# -----------------------------------------------------------------------------
# KIDS (8-12 years) - School knowledge, fun facts
# -----------------------------------------------------------------------------

KIDS_SCIENCE = [
    ("What is the largest planet in our solar system?", "Jupiter", ["Saturn", "Mars", "Neptune"]),
    ("What do plants need to make food?", "Sunlight", ["Darkness", "Music", "Wind"]),
    ("What is the center of an atom called?", "Nucleus", ["Electron", "Proton", "Shell"]),
    ("How many planets are in our solar system?", "8", ["9", "7", "10"]),
    ("What is the hardest natural substance?", "Diamond", ["Gold", "Iron", "Steel"]),
    ("What type of animal is a whale?", "Mammal", ["Fish", "Reptile", "Bird"]),
    ("What gas do plants release?", "Oxygen", ["Carbon dioxide", "Nitrogen", "Helium"]),
    ("What is the largest organ in the human body?", "Skin", ["Heart", "Brain", "Liver"]),
    ("How many bones are in the human body?", "206", ["106", "306", "156"]),
    ("What force pulls things toward Earth?", "Gravity", ["Magnetism", "Wind", "Electricity"]),
]

KIDS_GEOGRAPHY = [
    ("What is the largest continent?", "Asia", ["Africa", "Europe", "Australia"]),
    ("What is the longest river in the world?", "Nile", ["Amazon", "Mississippi", "Yangtze"]),
    ("What is the largest ocean?", "Pacific", ["Atlantic", "Indian", "Arctic"]),
    ("What country has the most people?", "China", ["India", "USA", "Brazil"]),
    ("What is the capital of France?", "Paris", ["London", "Rome", "Berlin"]),
    ("What is the capital of Japan?", "Tokyo", ["Beijing", "Seoul", "Bangkok"]),
    ("On which continent is Egypt?", "Africa", ["Asia", "Europe", "Australia"]),
    ("What is the smallest country in the world?", "Vatican City", ["Monaco", "Malta", "Luxembourg"]),
    ("What mountain is the tallest?", "Mount Everest", ["K2", "Kilimanjaro", "Denali"]),
    ("What desert is the largest?", "Sahara", ["Gobi", "Kalahari", "Mojave"]),
]

KIDS_HISTORY = [
    ("Who was the first President of the USA?", "George Washington", ["Abraham Lincoln", "Thomas Jefferson", "John Adams"]),
    ("What did ancient Egyptians build?", "Pyramids", ["Castles", "Skyscrapers", "Bridges"]),
    ("Who discovered America in 1492?", "Christopher Columbus", ["Marco Polo", "Vasco da Gama", "Ferdinand Magellan"]),
    ("What year did World War II end?", "1945", ["1944", "1946", "1943"]),
    ("Who invented the light bulb?", "Thomas Edison", ["Nikola Tesla", "Benjamin Franklin", "Alexander Graham Bell"]),
    ("What ship sank in 1912?", "Titanic", ["Lusitania", "Britannic", "Olympic"]),
    ("Who was the first man on the moon?", "Neil Armstrong", ["Buzz Aldrin", "John Glenn", "Yuri Gagarin"]),
    ("What civilization built the Colosseum?", "Romans", ["Greeks", "Egyptians", "Persians"]),
    ("Who wrote the Declaration of Independence?", "Thomas Jefferson", ["George Washington", "Benjamin Franklin", "John Adams"]),
    ("What year did Columbus sail to America?", "1492", ["1482", "1502", "1472"]),
]

KIDS_MATH_WORD_PROBLEMS = [
    ("If you have 12 apples and give away 5, how many are left?", "7", ["6", "8", "5"]),
    ("What is 7 × 8?", "56", ["54", "58", "48"]),
    ("What is 144 ÷ 12?", "12", ["11", "13", "14"]),
    ("If a rectangle has length 6 and width 4, what is its area?", "24", ["20", "28", "22"]),
    ("What is 25% of 100?", "25", ["20", "30", "15"]),
    ("How many sides does a hexagon have?", "6", ["5", "7", "8"]),
    ("What is the next prime number after 7?", "11", ["9", "10", "13"]),
    ("If you buy 3 items at $4 each, what is the total?", "$12", ["$10", "$14", "$7"]),
    ("What is 15 × 4?", "60", ["55", "65", "50"]),
    ("How many minutes are in 2 hours?", "120", ["100", "140", "90"]),
]

def generate_kids_question(difficulty, category):
    """Generate a question for kids (ages 8-12)."""

    if category == 'science':
        text, answer, wrong = random.choice(KIDS_SCIENCE)
    elif category == 'geography':
        text, answer, wrong = random.choice(KIDS_GEOGRAPHY)
    elif category == 'history':
        text, answer, wrong = random.choice(KIDS_HISTORY)
    elif category == 'math':
        if difficulty <= 4:
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            result = a * b
            text = f"What is {a} × {b}?"
            answer = str(result)
            wrong = [str(result + i) for i in [1, -1, 2]]
        elif difficulty <= 7:
            b = random.randint(2, 12)
            result = random.randint(2, 12)
            a = b * result
            text = f"What is {a} ÷ {b}?"
            answer = str(result)
            wrong = [str(result + i) for i in [1, -1, 2]]
        else:
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            result = a + b
            text = f"What is {a} + {b}?"
            answer = str(result)
            wrong = [str(result + i) for i in [1, -1, 10]]
    else:  # general
        all_q = KIDS_SCIENCE + KIDS_GEOGRAPHY + KIDS_HISTORY + KIDS_MATH_WORD_PROBLEMS
        text, answer, wrong = random.choice(all_q)

    options = [answer] + list(wrong)[:3]
    random.shuffle(options)
    return text, options, options.index(answer)

# -----------------------------------------------------------------------------
# TEENS (13-17 years) - Pop culture, gaming, sports, social media
# -----------------------------------------------------------------------------

TEENS_POP_CULTURE = [
    ("What streaming platform is known for 'Stranger Things'?", "Netflix", ["Hulu", "Disney+", "Amazon Prime"]),
    ("What social media app uses stories that disappear?", "Snapchat", ["Facebook", "Twitter", "LinkedIn"]),
    ("What is the most subscribed YouTube channel?", "T-Series", ["PewDiePie", "MrBeast", "Cocomelon"]),
    ("What app is known for short video clips and dances?", "TikTok", ["Instagram", "Snapchat", "YouTube"]),
    ("What music streaming service has a green logo?", "Spotify", ["Apple Music", "Pandora", "Tidal"]),
    ("What company makes the iPhone?", "Apple", ["Samsung", "Google", "Microsoft"]),
    ("What gaming console is made by Sony?", "PlayStation", ["Xbox", "Nintendo Switch", "Wii"]),
    ("What is Discord primarily used for?", "Gaming chat", ["Email", "Shopping", "Banking"]),
    ("What does 'LOL' stand for?", "Laugh Out Loud", ["Lots Of Love", "Living Our Lives", "Look Out Loud"]),
    ("What platform is known for live streaming games?", "Twitch", ["YouTube", "Netflix", "Hulu"]),
]

TEENS_GAMING = [
    ("What game features a battle royale on an island?", "Fortnite", ["Minecraft", "Roblox", "Tetris"]),
    ("What game involves building with blocks?", "Minecraft", ["Fortnite", "Call of Duty", "FIFA"]),
    ("What company created Mario?", "Nintendo", ["Sony", "Microsoft", "Sega"]),
    ("What game has characters like Pikachu?", "Pokemon", ["Mario", "Zelda", "Sonic"]),
    ("What is the best-selling video game of all time?", "Minecraft", ["Tetris", "GTA V", "Wii Sports"]),
    ("What game features Link as the main character?", "Zelda", ["Mario", "Pokemon", "Sonic"]),
    ("What does 'GG' mean in gaming?", "Good Game", ["Get Going", "Great Goal", "Go Go"]),
    ("What is the main currency in Fortnite?", "V-Bucks", ["Coins", "Gems", "Credits"]),
    ("What game has creepers and endermen?", "Minecraft", ["Fortnite", "Roblox", "Terraria"]),
    ("What type of game is FIFA?", "Sports/Soccer", ["Racing", "Shooter", "Puzzle"]),
]

TEENS_SPORTS = [
    ("How many players are on a soccer team?", "11", ["10", "12", "9"]),
    ("What sport uses a puck?", "Hockey", ["Soccer", "Basketball", "Tennis"]),
    ("How many points is a touchdown worth?", "6", ["7", "5", "3"]),
    ("What country hosted the 2020 Olympics?", "Japan", ["China", "Brazil", "USA"]),
    ("How many quarters are in a basketball game?", "4", ["2", "3", "6"]),
    ("What sport is Serena Williams famous for?", "Tennis", ["Golf", "Swimming", "Soccer"]),
    ("How long is a marathon in miles?", "26.2", ["25", "30", "20"]),
    ("What is the highest score in bowling?", "300", ["200", "250", "350"]),
    ("What sport has a slam dunk?", "Basketball", ["Football", "Baseball", "Golf"]),
    ("How many sets to win a tennis match?", "3", ["2", "4", "5"]),
]

TEENS_MUSIC = [
    ("What instrument has 88 keys?", "Piano", ["Guitar", "Violin", "Drums"]),
    ("What music genre originated in Jamaica?", "Reggae", ["Hip-hop", "Jazz", "Blues"]),
    ("How many strings does a standard guitar have?", "6", ["4", "5", "8"]),
    ("What is the highest female voice type?", "Soprano", ["Alto", "Tenor", "Bass"]),
    ("What does 'DJ' stand for?", "Disc Jockey", ["Dance Jammer", "Digital Jukebox", "Disco Jump"]),
    ("What musical symbol means to play loudly?", "Forte", ["Piano", "Allegro", "Tempo"]),
    ("What genre is known for heavy bass drops?", "EDM/Dubstep", ["Country", "Classical", "Jazz"]),
    ("How many members in a quartet?", "4", ["3", "5", "6"]),
    ("What is a song without instruments called?", "A cappella", ["Acoustic", "Unplugged", "Solo"]),
    ("What app is known for music creation?", "GarageBand", ["Photoshop", "Excel", "Chrome"]),
]

def generate_teens_question(difficulty, category):
    """Generate a question for teens (ages 13-17)."""

    if category in ['pop-culture', 'general']:
        text, answer, wrong = random.choice(TEENS_POP_CULTURE)
    elif category == 'gaming':
        text, answer, wrong = random.choice(TEENS_GAMING)
    elif category == 'sports':
        text, answer, wrong = random.choice(TEENS_SPORTS)
    elif category == 'music':
        text, answer, wrong = random.choice(TEENS_MUSIC)
    elif category == 'science':
        text, answer, wrong = random.choice(KIDS_SCIENCE)
    elif category == 'geography':
        text, answer, wrong = random.choice(KIDS_GEOGRAPHY)
    elif category == 'history':
        text, answer, wrong = random.choice(KIDS_HISTORY)
    elif category == 'math':
        a = random.randint(10, 50)
        b = random.randint(10, 50)
        result = a * b
        text = f"What is {a} × {b}?"
        answer = str(result)
        wrong = [str(result + random.randint(-20, 20)) for _ in range(3)]
    else:
        all_q = TEENS_POP_CULTURE + TEENS_GAMING + TEENS_SPORTS + TEENS_MUSIC
        text, answer, wrong = random.choice(all_q)

    options = [answer] + list(wrong)[:3]
    random.shuffle(options)
    return text, options, options.index(answer)

# -----------------------------------------------------------------------------
# ADULTS (18-35 years) - General knowledge, current affairs, movies
# -----------------------------------------------------------------------------

ADULTS_MOVIES = [
    ("What movie features a character named Darth Vader?", "Star Wars", ["Star Trek", "Alien", "Blade Runner"]),
    ("Who directed 'Pulp Fiction'?", "Quentin Tarantino", ["Martin Scorsese", "Steven Spielberg", "Christopher Nolan"]),
    ("What movie won Best Picture at the 2020 Oscars?", "Parasite", ["1917", "Joker", "Once Upon a Time"]),
    ("In what year was the first Harry Potter movie released?", "2001", ["1999", "2003", "2000"]),
    ("What is the highest-grossing film of all time?", "Avatar", ["Avengers: Endgame", "Titanic", "Star Wars"]),
    ("Who plays Iron Man in the MCU?", "Robert Downey Jr.", ["Chris Evans", "Chris Hemsworth", "Mark Ruffalo"]),
    ("What movie features a DeLorean time machine?", "Back to the Future", ["Terminator", "The Matrix", "Blade Runner"]),
    ("Who directed 'Inception'?", "Christopher Nolan", ["Ridley Scott", "James Cameron", "Denis Villeneuve"]),
    ("What was the first Pixar movie?", "Toy Story", ["Finding Nemo", "Monsters Inc", "The Incredibles"]),
    ("In 'The Shawshank Redemption', what is Andy's profession?", "Banker", ["Lawyer", "Doctor", "Teacher"]),
]

ADULTS_BUSINESS = [
    ("What company has the ticker symbol AAPL?", "Apple", ["Amazon", "Alphabet", "Adobe"]),
    ("Who founded Amazon?", "Jeff Bezos", ["Elon Musk", "Bill Gates", "Mark Zuckerberg"]),
    ("What does CEO stand for?", "Chief Executive Officer", ["Chief Executive Operator", "Company Executive Officer", "Central Executive Officer"]),
    ("What is the currency of the European Union?", "Euro", ["Pound", "Dollar", "Franc"]),
    ("What company owns Instagram?", "Meta (Facebook)", ["Google", "Twitter", "Snapchat"]),
    ("What does IPO stand for?", "Initial Public Offering", ["Internal Private Offering", "International Public Offering", "Initial Private Operation"]),
    ("Who is the CEO of Tesla?", "Elon Musk", ["Jeff Bezos", "Tim Cook", "Sundar Pichai"]),
    ("What year was Bitcoin created?", "2009", ["2007", "2011", "2013"]),
    ("What company's slogan is 'Just Do It'?", "Nike", ["Adidas", "Puma", "Reebok"]),
    ("What does GDP stand for?", "Gross Domestic Product", ["General Domestic Production", "Gross Daily Production", "Global Domestic Product"]),
]

ADULTS_SCIENCE_ADV = [
    ("What is the chemical symbol for gold?", "Au", ["Ag", "Go", "Gd"]),
    ("How many chromosomes do humans have?", "46", ["44", "48", "42"]),
    ("What is the speed of light in km/s?", "299,792", ["150,000", "500,000", "100,000"]),
    ("What is the atomic number of carbon?", "6", ["8", "12", "4"]),
    ("What particle has a negative charge?", "Electron", ["Proton", "Neutron", "Positron"]),
    ("What is the powerhouse of the cell?", "Mitochondria", ["Nucleus", "Ribosome", "Golgi apparatus"]),
    ("What is the chemical formula for water?", "H2O", ["HO2", "H2O2", "OH"]),
    ("What planet has the most moons?", "Saturn", ["Jupiter", "Neptune", "Uranus"]),
    ("What is the smallest bone in the human body?", "Stapes (ear)", ["Finger bone", "Toe bone", "Wrist bone"]),
    ("What gas makes up most of Earth's atmosphere?", "Nitrogen", ["Oxygen", "Carbon dioxide", "Argon"]),
]

def generate_adults_question(difficulty, category):
    """Generate a question for adults (ages 18-35)."""

    if category in ['movies', 'entertainment']:
        text, answer, wrong = random.choice(ADULTS_MOVIES)
    elif category in ['business', 'economics']:
        text, answer, wrong = random.choice(ADULTS_BUSINESS)
    elif category == 'science':
        text, answer, wrong = random.choice(ADULTS_SCIENCE_ADV)
    elif category == 'geography':
        text, answer, wrong = random.choice(KIDS_GEOGRAPHY)
    elif category == 'history':
        text, answer, wrong = random.choice(KIDS_HISTORY)
    elif category == 'math':
        if difficulty <= 5:
            a = random.randint(10, 100)
            b = random.randint(10, 100)
            result = a * b
            text = f"What is {a} × {b}?"
        else:
            a = random.randint(100, 500)
            b = random.randint(10, 50)
            result = a + b
            text = f"What is {a} + {b}?"
        answer = str(result)
        wrong = [str(result + random.randint(-50, 50)) for _ in range(3)]
    else:
        all_q = ADULTS_MOVIES + ADULTS_BUSINESS + ADULTS_SCIENCE_ADV
        text, answer, wrong = random.choice(all_q)

    options = [answer] + list(wrong)[:3]
    random.shuffle(options)
    return text, options, options.index(answer)

# -----------------------------------------------------------------------------
# SENIORS (35+ years) - Classic knowledge, history, literature
# -----------------------------------------------------------------------------

SENIORS_LITERATURE = [
    ("Who wrote '1984'?", "George Orwell", ["Aldous Huxley", "Ray Bradbury", "H.G. Wells"]),
    ("Who wrote 'Pride and Prejudice'?", "Jane Austen", ["Charlotte Bronte", "Emily Bronte", "Mary Shelley"]),
    ("What is the first book of the Bible?", "Genesis", ["Exodus", "Leviticus", "Psalms"]),
    ("Who wrote 'Romeo and Juliet'?", "William Shakespeare", ["Christopher Marlowe", "Ben Jonson", "John Milton"]),
    ("Who wrote 'The Great Gatsby'?", "F. Scott Fitzgerald", ["Ernest Hemingway", "John Steinbeck", "William Faulkner"]),
    ("What Russian author wrote 'War and Peace'?", "Leo Tolstoy", ["Fyodor Dostoevsky", "Anton Chekhov", "Ivan Turgenev"]),
    ("Who wrote 'The Odyssey'?", "Homer", ["Virgil", "Sophocles", "Euripides"]),
    ("Who wrote 'Moby-Dick'?", "Herman Melville", ["Mark Twain", "Nathaniel Hawthorne", "Edgar Allan Poe"]),
    ("What is Don Quixote known for fighting?", "Windmills", ["Dragons", "Giants", "Knights"]),
    ("Who wrote 'A Tale of Two Cities'?", "Charles Dickens", ["Thomas Hardy", "Oscar Wilde", "George Eliot"]),
]

SENIORS_CLASSICAL = [
    ("Who composed 'The Four Seasons'?", "Vivaldi", ["Bach", "Mozart", "Beethoven"]),
    ("Who painted the Sistine Chapel ceiling?", "Michelangelo", ["Leonardo da Vinci", "Raphael", "Donatello"]),
    ("Who composed 'Moonlight Sonata'?", "Beethoven", ["Mozart", "Chopin", "Liszt"]),
    ("Who sculpted 'David'?", "Michelangelo", ["Donatello", "Bernini", "Rodin"]),
    ("Who wrote 'The Magic Flute'?", "Mozart", ["Bach", "Beethoven", "Handel"]),
    ("What art movement is Monet associated with?", "Impressionism", ["Cubism", "Surrealism", "Realism"]),
    ("Who painted 'Starry Night'?", "Van Gogh", ["Monet", "Picasso", "Cezanne"]),
    ("Who composed 'Swan Lake'?", "Tchaikovsky", ["Stravinsky", "Prokofiev", "Rachmaninoff"]),
    ("Who painted 'The Birth of Venus'?", "Botticelli", ["Raphael", "Titian", "Caravaggio"]),
    ("What nationality was Chopin?", "Polish", ["German", "Austrian", "Russian"]),
]

SENIORS_HISTORY_ADV = [
    ("What year did the French Revolution begin?", "1789", ["1776", "1799", "1815"]),
    ("Who was the first Roman Emperor?", "Augustus", ["Julius Caesar", "Nero", "Caligula"]),
    ("What treaty ended World War I?", "Treaty of Versailles", ["Treaty of Paris", "Treaty of Vienna", "Treaty of Berlin"]),
    ("Who was the British monarch during WWI?", "George V", ["Edward VII", "Victoria", "George VI"]),
    ("What year did the Soviet Union collapse?", "1991", ["1989", "1993", "1985"]),
    ("Who was the longest-reigning British monarch?", "Queen Elizabeth II", ["Queen Victoria", "George III", "Henry VIII"]),
    ("What empire was Constantinople the capital of?", "Byzantine", ["Roman", "Ottoman", "Persian"]),
    ("What year did India gain independence?", "1947", ["1945", "1950", "1942"]),
    ("Who was the first female Prime Minister of the UK?", "Margaret Thatcher", ["Theresa May", "Queen Victoria", "Elizabeth I"]),
    ("What was the name of the ship Darwin sailed on?", "HMS Beagle", ["HMS Victory", "Mayflower", "Endeavour"]),
]

def generate_seniors_question(difficulty, category):
    """Generate a question for seniors (ages 35+)."""

    if category == 'literature':
        text, answer, wrong = random.choice(SENIORS_LITERATURE)
    elif category in ['art', 'music', 'classical']:
        text, answer, wrong = random.choice(SENIORS_CLASSICAL)
    elif category == 'history':
        text, answer, wrong = random.choice(SENIORS_HISTORY_ADV)
    elif category == 'science':
        text, answer, wrong = random.choice(ADULTS_SCIENCE_ADV)
    elif category == 'geography':
        text, answer, wrong = random.choice(KIDS_GEOGRAPHY)
    elif category == 'math':
        a = random.randint(50, 200)
        b = random.randint(10, 100)
        result = a + b
        text = f"What is {a} + {b}?"
        answer = str(result)
        wrong = [str(result + random.randint(-30, 30)) for _ in range(3)]
    else:
        all_q = SENIORS_LITERATURE + SENIORS_CLASSICAL + SENIORS_HISTORY_ADV
        text, answer, wrong = random.choice(all_q)

    options = [answer] + list(wrong)[:3]
    random.shuffle(options)
    return text, options, options.index(answer)

# =============================================================================
# MAIN GENERATION LOGIC
# =============================================================================

CATEGORIES_BY_AGE = {
    'little-kids': ['colors', 'animals', 'shapes', 'numbers', 'body', 'general'],
    'kids': ['math', 'science', 'geography', 'history', 'general'],
    'teens': ['pop-culture', 'gaming', 'sports', 'music', 'science', 'geography', 'math', 'general'],
    'adults': ['movies', 'business', 'science', 'geography', 'history', 'math', 'general'],
    'seniors': ['literature', 'classical', 'history', 'science', 'geography', 'math', 'general'],
}

GENERATORS = {
    'little-kids': generate_little_kids_question,
    'kids': generate_kids_question,
    'teens': generate_teens_question,
    'adults': generate_adults_question,
    'seniors': generate_seniors_question,
}

def generate_unique_question(age_group, difficulty):
    """Generate a unique question that hasn't been used before."""
    global generated_texts

    categories = CATEGORIES_BY_AGE[age_group]
    generator = GENERATORS[age_group]

    max_attempts = 500
    for attempt in range(max_attempts):
        category = random.choice(categories)
        text, options, correct_idx = generator(difficulty, category)

        # Normalize for comparison
        text_key = text.lower().strip()

        if text_key not in all_existing_texts and text_key not in generated_texts:
            generated_texts.add(text_key)
            return {
                'text': text,
                'options': options,
                'correctIndex': correct_idx,
                'category': category
            }

    # Fallback: generate truly unique math question
    while True:
        a = random.randint(100, 9999)
        b = random.randint(100, 9999)
        result = a + b
        text = f"What is {a} + {b}?"
        text_key = text.lower().strip()

        if text_key not in all_existing_texts and text_key not in generated_texts:
            generated_texts.add(text_key)
            wrong = [str(result + random.randint(-100, 100)) for _ in range(3)]
            options = [str(result)] + wrong
            random.shuffle(options)
            return {
                'text': text,
                'options': options,
                'correctIndex': options.index(str(result)),
                'category': 'math'
            }

def append_questions_to_file(file_path, questions, age_group, difficulty):
    """Append new questions to an existing file."""

    # Read existing content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        content = "export const questions = [\n]"

    # Find the closing bracket
    if ']' in content:
        # Remove trailing ] and whitespace
        content = content.rstrip()
        if content.endswith(']'):
            content = content[:-1].rstrip()
            if content.endswith(','):
                content = content  # Keep trailing comma
            else:
                content += ','  # Add trailing comma

    # Get next sequence number
    age_prefix = AGE_PREFIXES[age_group]
    existing_sequences = re.findall(f"id:\\s*'{age_prefix}{difficulty:02d}(\\d{{4}})'", content)
    next_seq = max([int(s) for s in existing_sequences], default=0) + 1

    # Format new questions
    new_lines = []
    for q in questions:
        q_id = f"{age_prefix}{difficulty:02d}{next_seq:04d}"
        next_seq += 1

        text = q['text'].replace("'", "\\'")
        options = [opt.replace("'", "\\'") for opt in q['options']]
        options_str = ", ".join([f"'{opt}'" for opt in options])

        line = f"  {{ id: '{q_id}', text: '{text}', options: [{options_str}], correctIndex: {q['correctIndex']}, difficulty: {difficulty}, category: '{q['category']}' }}"
        new_lines.append(line)

    # Combine
    new_content = content + '\n' + ',\n'.join(new_lines) + '\n]'

    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def process_all_files():
    """Process all files and fill them to 100 questions each."""

    print("Loading existing questions...")
    load_existing_questions()

    stats = {
        'total_generated': 0,
        'by_age_group': {}
    }

    for age_group in AGE_GROUPS:
        age_dir = data_dir / age_group
        if not age_dir.exists():
            print(f"Creating directory for {age_group}")
            age_dir.mkdir(parents=True, exist_ok=True)

        age_generated = 0
        print(f"\nProcessing {age_group}...")

        for d in range(1, 11):
            diff_dir = age_dir / f'd{d}'
            diff_dir.mkdir(exist_ok=True)

            diff_generated = 0

            for f_num in range(1, 11):
                file_path = diff_dir / f'f{f_num}.ts'

                # Create file if it doesn't exist
                if not file_path.exists():
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("export const questions = [\n]")

                current_count = count_questions_in_file(file_path)
                needed = 100 - current_count

                if needed > 0:
                    # Generate new questions
                    new_questions = []
                    for _ in range(needed):
                        q = generate_unique_question(age_group, d)
                        new_questions.append(q)

                    # Append to file
                    append_questions_to_file(file_path, new_questions, age_group, d)
                    diff_generated += needed

            if diff_generated > 0:
                print(f"  d{d}: generated {diff_generated} questions")
                age_generated += diff_generated

        stats['by_age_group'][age_group] = age_generated
        stats['total_generated'] += age_generated
        print(f"  Total for {age_group}: {age_generated} questions")

    return stats

def main():
    print("=" * 70)
    print("GENERATING MISSING QUESTIONS")
    print("Target: 50,000 questions (5 age groups × 10 difficulties × 10 files × 100)")
    print("=" * 70)

    stats = process_all_files()

    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"Total questions generated: {stats['total_generated']}")
    print()
    print("By age group:")
    for ag, count in stats['by_age_group'].items():
        print(f"  {ag}: +{count} questions")

    print("\nAll files now have 100 questions each!")

if __name__ == '__main__':
    main()
