import math
import requests
import random

def get_proficiency_bonus(char_level):
    # Calculate proficiency bonus based on character level
    return math.ceil(char_level / 4) + 1

def calculate_damage(spell_data, char_level):
    # Calculate damage based on the spell level or character level
    if "damage" in spell_data:
        damage_info = spell_data["damage"]
        if "damage_at_character_level" in damage_info:
            damage_levels = damage_info["damage_at_character_level"]
            for level_cap in sorted(map(int, damage_levels.keys()), reverse=True):
                if char_level >= level_cap:
                    damage_rolls = damage_levels[str(level_cap)]
                    break
        elif "damage_at_slot_level" in damage_info:
            # Find the base level of the spell to fetch damage data
            base_level = spell_data['level']
            if str(base_level) in damage_info["damage_at_slot_level"]:
                damage_rolls = damage_info["damage_at_slot_level"][str(base_level)]
            else:
                return None  # No damage information for the base level
        else:
            return None

        num_dice, dice_type = map(int, damage_rolls.split("d"))
        return sum(random.randint(1, dice_type) for _ in range(num_dice))
    return None

def cast_spell(spell_name, char_level, caster_spell_mod, target_ac, target_prof_bonus, target_ability_mods):
    # Prepare the spell name for API request
    spell_name_formatted = spell_name.lower().replace(" ", "-")
    url = f"https://www.dnd5eapi.co/api/spells/{spell_name_formatted}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Error: Could not retrieve spell details for {spell_name}"
    
    spell_data = response.json()
    caster_prof_bonus = get_proficiency_bonus(char_level)
    result = f"Casting {spell_name}: "

    # Check for attack type in the spell data
    if "attack_type" in spell_data:
        # Handle spell requiring an attack roll
        attack_roll = random.randint(1, 20) + caster_prof_bonus + caster_spell_mod
        if attack_roll >= target_ac:
            result += f"Hit! (Roll: {attack_roll}, Target AC: {target_ac})"
            damage = calculate_damage(spell_data, char_level)
            if damage:
                result += f", Damage: {damage}"
        else:
            result += f"Miss! (Roll: {attack_roll}, Target AC: {target_ac})"
    elif "dc" in spell_data:
        # Handle spell requiring a saving throw
        dc_type = spell_data["dc"]["dc_type"]["name"][:3].lower()
        target_index = ["str", "dex", "con", "int", "wis", "cha"].index(dc_type)
        saving_throw = random.randint(1, 20) + target_ability_mods[target_index] + target_prof_bonus
        spell_save_dc = 8 + caster_prof_bonus + caster_spell_mod

        if saving_throw >= spell_save_dc:
            result += f"Saved! (Roll: {saving_throw}, DC: {spell_save_dc})"
        else:
            result += f"Failed save! (Roll: {saving_throw}, DC: {spell_save_dc})"
            damage = calculate_damage(spell_data, char_level)
            if damage:
                result += f", Damage: {damage}"

    # Checking for conditions applied by the spell
    conditions = ["blinded", "charmed", "deafened", "exhaustion", "frightened", "grappled", "incapacitated",
                  "invisible", "paralyzed", "petrified", "poisoned", "prone", "restrained", "stunned",
                  "unconscious"]
    description_text = " ".join(spell_data["desc"]).lower()
    applied_conditions = [condition for condition in conditions if condition in description_text]
    if applied_conditions:
        result += f", Conditions: {', '.join(applied_conditions)}"
    elif "conditions" in spell_data:
        result += f", Conditions: {spell_data['conditions']}"

    return result


# Example usages
print(cast_spell("Fire Bolt", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))

print(cast_spell("Guiding Bolt", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))

print(cast_spell("Entangle", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))

print(cast_spell("Magic Missile", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))

print(cast_spell("Tiny Hut", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))

print(cast_spell("Fireball", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))

print(cast_spell("Black Tentacles", char_level=5, caster_spell_mod=4, target_ac=15, target_prof_bonus=2, target_ability_mods=[1, 2, 3, 0, 1, -1]))