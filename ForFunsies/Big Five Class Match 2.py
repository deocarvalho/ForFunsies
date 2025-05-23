# Class profiles: target OCEAN values and base flavor text
dnd_classes = {
    "Barbarian": {
        "traits": [30, 20, 85, 25, 50],
        "flavor": "You are a Barbarian — a primal force of fury and instinct, guided more by heart than by thought."
    },
    "Bard": {
        "traits": [95, 35, 90, 60, 45],
        "flavor": "You are a Bard — a vibrant soul who weaves music, charm, and cleverness into every moment."
    },
    "Cleric": {
        "traits": [60, 80, 50, 85, 30],
        "flavor": "You are a Cleric — grounded by faith and guided by purpose, a healer and protector in equal measure."
    },
    "Druid": {
        "traits": [90, 60, 35, 80, 25],
        "flavor": "You are a Druid — a quiet guardian of balance, at home in both wilderness and wonder."
    },
    "Fighter": {
        "traits": [35, 85, 50, 50, 20],
        "flavor": "You are a Fighter — resilient and adaptable, you thrive on skill and discipline."
    },
    "Monk": {
        "traits": [70, 90, 30, 80, 15],
        "flavor": "You are a Monk — a vessel of calm precision and spiritual strength."
    },
    "Paladin": {
        "traits": [60, 90, 70, 90, 25],
        "flavor": "You are a Paladin — a righteous warrior bound by sacred oaths and unshakable ideals."
    },
    "Ranger": {
        "traits": [75, 65, 40, 55, 25],
        "flavor": "You are a Ranger — patient, perceptive, and deeply attuned to the world around you."
    },
    "Rogue": {
        "traits": [70, 30, 25, 30, 50],
        "flavor": "You are a Rogue — quick of wit and hand, thriving in shadows and outsmarting every trap."
    },
    "Sorcerer": {
        "traits": [90, 35, 85, 50, 80],
        "flavor": "You are a Sorcerer — a being of raw magic and emotion, born to shape the world with will alone."
    },
    "Warlock": {
        "traits": [85, 55, 35, 30, 85],
        "flavor": "You are a Warlock — marked by otherworldly power, you navigate life through arcane bargains and inner resolve."
    },
    "Wizard": {
        "traits": [95, 95, 25, 25, 20],
        "flavor": "You are a Wizard — a scholar of reality, using logic, learning, and precision to alter existence itself."
    }
}

# Always-included trait interpretations
def trait_flavor(ocean):
    def describe(trait, score):
        if trait == "Openness":
            if score >= 70:
                return "You are imaginative and curious, always seeking new ideas and experiences."
            elif score >= 40:
                return "You balance creativity with practicality, open to novelty but grounded in experience."
            else:
                return "You are practical and prefer the familiar, valuing tradition and clarity over abstraction."
        
        elif trait == "Conscientiousness":
            if score >= 70:
                return "You are organized and diligent, thriving on structure and responsibility."
            elif score >= 40:
                return "You are moderately self-disciplined, flexible but generally reliable when it matters."
            else:
                return "You prefer spontaneity to planning, acting on intuition rather than routine."

        elif trait == "Extraversion":
            if score >= 70:
                return "You are outgoing and energetic, drawing strength from social interaction."
            elif score >= 40:
                return "You enjoy both solitude and connection, balancing reflection with expression."
            else:
                return "You are quiet and introspective, finding comfort in thought and personal space."

        elif trait == "Agreeableness":
            if score >= 70:
                return "You are compassionate and cooperative, often putting others’ needs before your own."
            elif score >= 40:
                return "You balance empathy with assertiveness, kind but not easily swayed."
            else:
                return "You are direct and independent, unafraid of conflict when pursuing your own path."

        elif trait == "Neuroticism":
            if score >= 70:
                return "You feel emotions deeply and frequently, attuned to the highs and lows of experience."
            elif score >= 40:
                return "You experience stress and joy in equal measure, generally able to stay composed."
            else:
                return "You are calm and emotionally resilient, steady in the face of challenges."

    traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
    return [
        f"🧠 **{traits[0]}**: {describe(traits[0], ocean[0])}",
        f"📋 **{traits[1]}**: {describe(traits[1], ocean[1])}",
        f"🎤 **{traits[2]}**: {describe(traits[2], ocean[2])}",
        f"💛 **{traits[3]}**: {describe(traits[3], ocean[3])}",
        f"🌊 **{traits[4]}**: {describe(traits[4], ocean[4])}"
    ]

# Match function with top 3 results
def match_top_classes(ocean_scores, top_n=3):
    def score_distance(user, target):
        return sum(abs(u - t) for u, t in zip(user, target))

    scored = sorted(
        [(name, score_distance(ocean_scores, data["traits"])) for name, data in dnd_classes.items()],
        key=lambda x: x[1]
    )[:top_n]

    personality = "\n".join(trait_flavor(ocean_scores))

    results = []
    for name, _ in scored:
        results.append({
            "class": name,
            "flavor": dnd_classes[name]["flavor"],
            "personality": personality
        })

    return results

# Example usage
example_scores = [82, 66, 34, 40, 25]
results = match_top_classes(example_scores)

for r in results:
    print(f"\n🧭 **Class**: {r['class']}\n{r['flavor']}\n\n{r['personality']}\n" + "-"*60)
