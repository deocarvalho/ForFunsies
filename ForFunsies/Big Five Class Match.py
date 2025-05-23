# Define D&D class profiles with their target OCEAN scores and flavor text
dnd_classes = {
    "Barbarian": {
        "traits": [30, 20, 85, 25, 50],
        "flavor": "Driven by instinct and fury, you are a Barbarian - a primal force who thrives in chaos and battles with heart more than mind."
    },
    "Bard": {
        "traits": [95, 35, 90, 60, 45],
        "flavor": "With charm, wit, and creativity, you are a Bard - a storyteller and performer who influences the world through inspiration and improvisation."
    },
    "Cleric": {
        "traits": [60, 80, 50, 85, 30],
        "flavor": "Faithful and steadfast, you are a Cleric - a beacon of divine purpose who heals, guides, and smites in equal measure."
    },
    "Druid": {
        "traits": [90, 60, 35, 80, 25],
        "flavor": "You are a Druid - a guardian of nature and shapeshifter whose wisdom runs as deep as the forest roots."
    },
    "Fighter": {
        "traits": [35, 85, 50, 50, 20],
        "flavor": "Disciplined and tactical, you are a Fighter - a master of arms and strategy who adapts to any battlefield."
    },
    "Monk": {
        "traits": [70, 90, 30, 80, 15],
        "flavor": "Serene and focused, you are a Monk - a spiritual warrior whose strength flows from inner harmony and disciplined motion."
    },
    "Paladin": {
        "traits": [60, 90, 70, 90, 25],
        "flavor": "Noble and resolute, you are a Paladin - a holy warrior bound by oaths and driven by an unshakable moral compass."
    },
    "Ranger": {
        "traits": [75, 65, 40, 55, 25],
        "flavor": "You are a Ranger - a lone hunter and protector of the wild, ever watchful and ever resourceful."
    },
    "Rogue": {
        "traits": [70, 30, 25, 30, 50],
        "flavor": "Clever and elusive, you are a Rogue - a shadow in the night who trusts their instincts and lives by their own code."
    },
    "Sorcerer": {
        "traits": [90, 35, 85, 50, 80],
        "flavor": "Brimming with innate power, you are a Sorcerer - emotion and magic are one within you, shaping reality itself."
    },
    "Warlock": {
        "traits": [85, 55, 35, 30, 85],
        "flavor": "You are a Warlock - one who has made a pact for power, walking a mysterious path between control and surrender."
    },
    "Wizard": {
        "traits": [95, 95, 25, 25, 20],
        "flavor": "Methodical and brilliant, you are a Wizard - a scholar of the arcane who bends the laws of the universe through study and will."
    }
}

def score_distance(user, target):
    return sum(abs(u - t) for u, t in zip(user, target))

def match_class(ocean_scores):
    best_match = None
    lowest_score = float('inf')

    for class_name, data in dnd_classes.items():
        distance = score_distance(ocean_scores, data["traits"])
        if distance < lowest_score:
            lowest_score = distance
            best_match = class_name

    return {
        "class": best_match,
        "flavor": dnd_classes[best_match]["flavor"]
    }

def match_class2(ocean_scores):
    best_match = None
    lowest_score = float('inf')

    for class_name, data in dnd_classes.items():
        distance = score_distance(ocean_scores, data["traits"])
        if distance < lowest_score:
            lowest_score = distance
            best_match = class_name

    traits = ocean_scores
    flavor_base = dnd_classes[best_match]["flavor"]
    
    # Personalized additions based on OCEAN
    details = []
    if traits[0] > 80:
        details.append("Your imagination and openness to new experiences let you see magic where others see rules.")
    elif traits[0] < 30:
        details.append("You value tradition and practicality, which grounds your choices in experience rather than novelty.")

    if traits[1] > 80:
        details.append("Highly disciplined and detail-oriented, your path is marked by structure and precision.")
    elif traits[1] < 30:
        details.append("You prefer spontaneity over planning, relying on instinct and adaptability.")

    if traits[2] > 80:
        details.append("Your outgoing and energetic spirit makes you a natural leader and communicator.")
    elif traits[2] < 30:
        details.append("Quiet and introspective, you find strength in observation rather than attention.")

    if traits[3] > 80:
        details.append("Compassionate and cooperative, you're driven by a deep sense of loyalty and harmony.")
    elif traits[3] < 30:
        details.append("Independent and skeptical, you prefer to forge your own way rather than rely on others.")

    if traits[4] > 80:
        details.append("Deeply sensitive to emotion and intensity, you thrive in complex, dramatic narratives.")
    elif traits[4] < 30:
        details.append("Calm and emotionally steady, you handle stress with confidence and clarity.")

    return {
        "class": best_match,
        "flavor": flavor_base,
        "personalized_flavor": f"{flavor_base} " + " ".join(details)
    }


# Example usage
print(match_class2([90, 29, 33, 62, 56])['personalized_flavor'])
print(match_class2([76, 12, 29, 25, 66])['personalized_flavor'])
print(match_class2([89, 1, 13, 78, 87])['personalized_flavor'])
print(match_class2([76, 7, 8, 30, 70])['personalized_flavor'])




