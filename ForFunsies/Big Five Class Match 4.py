# Personality Trait Evaluator and D&D Class Matcher
# Applies OCEAN trait scores to determine best-fitting D&D classes
# using psychological profiling, class-specific weighting, and lore-based frequency adjustment.

TRAITS = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
TRAIT_LABELS = TRAITS
MAX_SCORE = 100

CLASS_FLAVORS = {
    "Barbarian": "A fierce warrior fueled by primal rage and instinct.",
    "Bard": "A charismatic performer whose magic weaves through word and song.",
    "Cleric": "A divine agent empowered by faith and duty.",
    "Druid": "A shapeshifting mystic in tune with the natural world.",
    "Fighter": "A seasoned combatant mastering martial disciplines.",
    "Monk": "A spiritual warrior channeling ki through precision and balance.",
    "Paladin": "A righteous crusader bound by sacred oaths.",
    "Ranger": "A skilled tracker and survivalist at home in the wild.",
    "Rogue": "A cunning infiltrator who thrives on subtlety and speed.",
    "Sorcerer": "A being of innate magic, shaped by emotion and ancestry.",
    "Warlock": "A wielder of forbidden power, sustained by a pact.",
    "Wizard": "A scholarly spellcaster bending arcane laws through study.",
}

CLASS_WEIGHTS = {
    "Barbarian": [40, 40, 90, 30, 85],
    "Bard": [85, 50, 85, 80, 55],
    "Cleric": [60, 85, 45, 90, 35],
    "Druid": [90, 60, 30, 75, 45],
    "Fighter": [50, 80, 65, 50, 45],
    "Monk": [60, 85, 25, 70, 30],
    "Paladin": [55, 85, 45, 85, 30],
    "Ranger": [75, 70, 35, 65, 40],
    "Rogue": [65, 60, 55, 40, 55],
    "Sorcerer": [90, 35, 85, 50, 80],
    "Warlock": [85, 40, 60, 35, 85],
    "Wizard": [90, 90, 30, 55, 40],
}

TRAIT_WEIGHTS = {
    "Barbarian": [0.1, 0.1, 0.3, 0.1, 0.4],
    "Bard": [0.3, 0.1, 0.3, 0.2, 0.1],
    "Cleric": [0.1, 0.3, 0.1, 0.4, 0.1],
    "Druid": [0.3, 0.2, 0.1, 0.3, 0.1],
    "Fighter": [0.1, 0.4, 0.2, 0.2, 0.1],
    "Monk": [0.2, 0.4, 0.1, 0.2, 0.1],
    "Paladin": [0.1, 0.4, 0.1, 0.3, 0.1],
    "Ranger": [0.2, 0.3, 0.1, 0.3, 0.1],
    "Rogue": [0.2, 0.2, 0.2, 0.2, 0.2],
    "Sorcerer": [0.3, 0.1, 0.3, 0.1, 0.2],
    "Warlock": [0.3, 0.1, 0.2, 0.1, 0.3],
    "Wizard": [0.4, 0.3, 0.1, 0.1, 0.1],
}

FREQUENCY_MODIFIERS = {
    "Fighter": 1.10,
    "Rogue": 1.08,
    "Cleric": 1.06,
    "Ranger": 1.04,
    "Paladin": 1.03,
    "Bard": 1.00,
    "Druid": 0.97,
    "Barbarian": 0.95,
    "Wizard": 0.93,
    "Warlock": 0.90,
    "Sorcerer": 0.88,
    "Monk": 0.85,
}

def describe_trait(trait, score):
    percentile = round(score / MAX_SCORE * 100)
    thresholds = {
        "Openness": [(80, "high"), (50, "moderate")],
        "Conscientiousness": [(85, "high"), (55, "moderate")],
        "Extraversion": [(80, "high"), (45, "moderate")],
        "Agreeableness": [(90, "high"), (60, "moderate")],
        "Neuroticism": [(70, "high"), (40, "moderate")],
    }
    levels = thresholds[trait]
    for threshold, label in levels:
        if score >= threshold:
            return f"{trait} ({percentile}th percentile, {label}): " + trait_descriptions(trait, label)
    return f"{trait} ({percentile}th percentile, low): " + trait_descriptions(trait, "low")

def trait_descriptions(trait, level):
    messages = {
        "Openness": {
            "high": "You are highly imaginative and curious, constantly exploring new ideas and experiences.",
            "moderate": "You balance creativity with practicality, open to novelty but grounded in reality.",
            "low": "You prefer the familiar and value tradition, favoring clarity over abstraction."
        },
        "Conscientiousness": {
            "high": "You are organized and disciplined, thriving on structure and responsibility.",
            "moderate": "You are moderately self-disciplined, balancing planning with flexibility.",
            "low": "You prefer spontaneity and intuition over planning and routine."
        },
        "Extraversion": {
            "high": "You are outgoing and energized by social interactions.",
            "moderate": "You enjoy both solitude and socializing, balancing reflection with expression.",
            "low": "You are quiet and introspective, preferring calm and thoughtfulness."
        },
        "Agreeableness": {
            "high": "You are deeply compassionate and cooperative, prioritizing harmony.",
            "moderate": "You are kind and fair, blending empathy with assertiveness.",
            "low": "You are direct and self-reliant, unafraid of conflict to pursue your goals."
        },
        "Neuroticism": {
            "high": "You experience emotions intensely, deeply attuned to emotional fluctuations.",
            "moderate": "You feel both stress and joy strongly, but usually remain composed.",
            "low": "You are emotionally stable, calm, and resilient in the face of adversity."
        },
    }
    return messages[trait][level]

def trait_match_summary(ocean, class_vector):
    summary = []
    for trait, user_val, ideal_val in zip(TRAIT_LABELS, ocean, class_vector):
        diff = abs(user_val - ideal_val)
        if diff < 10:
            match = "excellent match"
        elif diff < 25:
            match = "good alignment"
        else:
            match = "some mismatch"
        summary.append(f"{trait}: {match}")
    return ", ".join(summary)

def calculate_scores(ocean, use_lore=False):
    results = {}
    for cls, weights in CLASS_WEIGHTS.items():
        importance = TRAIT_WEIGHTS.get(cls, [0.2]*5)
        base_score = sum((1 - abs(o - w) / MAX_SCORE) * imp for o, w, imp in zip(ocean, weights, importance))
        if use_lore:
            base_score *= FREQUENCY_MODIFIERS.get(cls, 1.0)
        results[cls] = (base_score, trait_match_summary(ocean, weights))
    return results

def print_results(title, scores):
    print("")
    print(title + ":")
    for cls, (score, summary) in sorted(scores.items(), key=lambda x: x[1][0], reverse=True)[:3]:
        print(f"{cls}: {CLASS_FLAVORS[cls]} (score: {round(score, 2)})")
        print(f"  Alignment: {summary}")

def validate_input(ocean):
    if not isinstance(ocean, list):
        raise ValueError("Input must be a list of five integers.")
    if len(ocean) != 5:
        raise ValueError("Input must contain exactly five trait scores.")
    for i, score in enumerate(ocean):
        if not isinstance(score, int):
            raise ValueError(f"Score at position {i+1} is not an integer.")
        if not (0 <= score <= MAX_SCORE):
            raise ValueError(f"Score at position {i+1} must be between 0 and {MAX_SCORE}.")

def generate_dnd_class_result(ocean):
    validate_input(ocean)
    print("Your Personality Profile:")
    for i, trait in enumerate(TRAITS):
        print(describe_trait(trait, ocean[i]))
    print_results("Top Matches (Pure Personality Match)", calculate_scores(ocean, use_lore=False))
    print_results("Top Matches (Lore-Aware Match)", calculate_scores(ocean, use_lore=True))
        
# Examples
generate_dnd_class_result([83, 50, 58, 66, 73])
generate_dnd_class_result([88, 81, 76, 77, 48])
