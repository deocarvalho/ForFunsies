import requests
import random

def cast_spell(spell_name, caster_proficiency, caster_ability_mod, target_ac, target_proficiency, target_ability_mods):
    # Replace spaces with dashes and convert to lower case
    spell_name = spell_name.replace(' ', '-').lower()

    # Get the spell details
    response = requests.get(f'https://www.dnd5eapi.co/api/spells/{spell_name}')
    spell = response.json()

    # Check if the spell requires an attack roll
    if 'attack_type' in spell:
        # Make the attack roll
        attack_roll = random.randint(1, 20) + caster_proficiency + caster_ability_mod

        # Check if the attack hits
        if attack_roll >= target_ac:
            result = 'hits'
        else:
            result = 'misses'
        return f'The {spell_name} spell {result} the target with an attack roll of {attack_roll}.'


    # Check if the spell requires a saving throw
    elif 'dc' in spell:
        # Get the type of saving throw
        saving_throw = spell['dc']['dc_type']

        # Make the saving throw
        saving_throw_roll = random.randint(1, 20) + target_proficiency + target_ability_mods[saving_throw['index']]

        # Check if the saving throw is successful
        if saving_throw_roll >= (8 + caster_proficiency + caster_ability_mod):
            result = 'successfully makes'
        else:
            result = 'fails'
        return f'The target {result} the {saving_throw['name']} saving throw with a roll of {saving_throw_roll}.'

# Example 1: Casting "Fire Bolt" with a caster who has a proficiency bonus of 2 and an ability modifier of 3 against a target with an armor class of 15, a proficiency bonus of 2, and ability score modifiers of {'str': 1, 'dex': 2, 'con': 3, 'int': 4, 'wis': 5, 'cha': 6}
print(cast_spell("Fire Bolt", 2, 3, 15, 2, {'str': 1, 'dex': 2, 'con': 3, 'int': 4, 'wis': 5, 'cha': 6}))

# Example 2: Casting "Entangle" with a caster who has a proficiency bonus of 3 and an ability modifier of 4 against a target with an armor class of 16, a proficiency bonus of 3, and ability score modifiers of {'str': 2, 'dex': 3, 'con': 4, 'int': 5, 'wis': 6, 'cha': 7}
print(cast_spell("Entangle", 3, 4, 16, 3, {'str': 2, 'dex': 3, 'con': 4, 'int': 5, 'wis': 6, 'cha': 7}))

# Example 3: Casting "Magic Missile" with a caster who has a proficiency bonus of 4 and an ability modifier of 5 against a target with an armor class of 17, a proficiency bonus of 4, and ability score modifiers of {'str': 3, 'dex': 4, 'con': 5, 'int': 6, 'wis': 7, 'cha': 8}
print(cast_spell("Magic Missile", 4, 5, 17, 4, {'str': 3, 'dex': 4, 'con': 5, 'int': 6, 'wis': 7, 'cha': 8}))

# Example 4: Casting "Cure Wounds" with a caster who has a proficiency bonus of 5 and an ability modifier of 6 against a target with an armor class of 18, a proficiency bonus of 5, and ability score modifiers of {'str': 4, 'dex': 5, 'con': 6, 'int': 7, 'wis': 8, 'cha': 9}
print(cast_spell("Cure Wounds", 5, 6, 18, 5, {'str': 4, 'dex': 5, 'con': 6, 'int': 7, 'wis': 8, 'cha': 9}))

# Example 5: Casting "Shield" with a caster who has a proficiency bonus of 6 and an ability modifier of 7 against a target with an armor class of 19, a proficiency bonus of 6, and ability score modifiers of {'str': 5, 'dex': 6, 'con': 7, 'int': 8, 'wis': 9, 'cha': 10}
print(cast_spell("Shield", 6, 7, 19, 6, {'str': 5, 'dex': 6, 'con': 7, 'int': 8, 'wis': 9, 'cha': 10}))
