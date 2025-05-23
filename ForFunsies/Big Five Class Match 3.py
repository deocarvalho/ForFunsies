def generate_dnd_class_result(ocean):
    traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]

    def describe(trait, score):
        if trait == "Openness":
            if score >= 90:
                return "You are highly imaginative and curious, constantly exploring new ideas and experiences."
            elif score >= 60:
                return "You balance creativity with practicality, open to novelty but grounded in reality."
            else:
                return "You prefer the familiar and value tradition, favoring clarity over abstraction."
        elif trait == "Conscientiousness":
            if score >= 90:
                return "You are organized and disciplined, thriving on structure and responsibility."
            elif score >= 60:
                return "You are moderately self-disciplined, balancing planning with flexibility."
            else:
                return "You prefer spontaneity and intuition over planning and routine."
        elif trait == "Extraversion":
            if score >= 90:
                return "You are outgoing and energized by social interactions."
            elif score >= 60:
                return "You enjoy both solitude and socializing, balancing reflection with expression."
            else:
                return "You are quiet and introspective, preferring calm and thoughtfulness."
        elif trait == "Agreeableness":
            if score >= 90:
                return "You are deeply compassionate and cooperative, prioritizing harmony."
            elif score >= 60:
                return "You are kind and fair, blending empathy with assertiveness."
            else:
                return "You are direct and self-reliant, unafraid of conflict to pursue your goals."
        elif trait == "Neuroticism":
            if score >= 90:
                return "You experience emotions intensely, deeply attuned to emotional fluctuations."
            elif score >= 60:
                return "You feel both stress and joy strongly, but usually remain composed."
            else:
                return "You are emotionally stable, calm, and resilient in the face of adversity."

    # 1. Trait Descriptions
    descriptions = [
        f"{traits[i]}: {describe(traits[i], ocean[i])}"
        for i in range(5)
    ]

    # 2.1. Score weights for D&D classes
    class_weights = {
        "Barbarian": [25, 40, 100, 30, 85],
        "Bard":      [105, 55, 110, 90, 70],
        "Cleric":    [60, 100, 60, 100, 40],
        "Druid":     [100, 65, 40, 80, 40],
        "Fighter":   [45, 95, 70, 60, 50],
        "Monk":      [70, 110, 30, 80, 20],
        "Paladin":   [55, 110, 60, 95, 35],
        "Ranger":    [75, 85, 35, 70, 45],
        "Rogue":     [65, 70, 60, 45, 60],
        "Sorcerer":  [110, 35, 100, 60, 90],
        "Warlock":   [95, 50, 70, 35, 95],
        "Wizard":    [115, 115, 25, 55, 40],
    }

    # 2.2. Lore-aware result weights
    frequency_modifiers = {
        "Fighter": 1.10,
        "Rogue": 1.08,
        "Cleric": 1.06,
        "Ranger": 1.04,
        "Wizard": 1.03,
        "Paladin": 1.02,
        "Bard": 1.00,
        "Druid": 0.95,
        "Warlock": 0.92,
        "Sorcerer": 0.90,
        "Barbarian": 0.88,
        "Monk": 0.85,
    }

    # 3. Class Matching Scores
    class_scores_pure = {}
    class_scores_lore = {}
    for cls, weights in class_weights.items():
        base_score = sum((120 - abs(o - w)) for o, w in zip(ocean, weights))
        class_scores_pure[cls] = base_score
        class_scores_lore[cls] = base_score * frequency_modifiers.get(cls, 1.0)

    # 4. Top 3 Matches
    top_pure = sorted(class_scores_pure.items(), key=lambda x: x[1], reverse=True)[:3]
    top_lore = sorted(class_scores_lore.items(), key=lambda x: x[1], reverse=True)[:3]

    # 5. Class Flavors
    class_flavor = {
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

    # 6. Output
    print("Your Personality Profile:\n")
    for line in descriptions:
        print(line)

    print("\nTop Matches (Pure Personality Match):\n")
    for cls, score in top_pure:
        print(f"{cls}: {class_flavor[cls]} (score: {round(score)})")

    print("\nTop Matches (Lore-Aware Match):\n")
    for cls, score in top_lore:
        print(f"{cls}: {class_flavor[cls]} (score: {round(score)})")

# Examples
generate_dnd_class_result([100, 60, 69, 79, 88])
generate_dnd_class_result([105, 97, 91, 92, 58])
