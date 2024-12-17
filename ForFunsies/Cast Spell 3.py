import requests
import random
import math

# Constants
BASE_URL = "https://www.dnd5eapi.co/api/"

def get_spell_data(spell_name):
    formatted_name = spell_name.lower().replace(' ', '-')
    response = requests.get(f"{BASE_URL}spells/{formatted_name}")
    if response.status_code != 200:
        raise ValueError(f"Error fetching spell data: {response.status_code}")
    return response.json()

def roll_d20():
    return random.randint(1, 20)

def calculate_proficiency_bonus(level):
    return math.ceil(1 + (level / 4))

def calculate_spell_save_dc(caster_level, spellcasting_ability_mod):
    proficiency_bonus = calculate_proficiency_bonus(caster_level)
    return 8 + proficiency_bonus + spellcasting_ability_mod

def handle_attack_roll(spell, caster_level, spellcasting_ability_mod, target_ac):
    proficiency_bonus = calculate_proficiency_bonus(caster_level)
    attack_roll = roll_d20() + spellcasting_ability_mod + proficiency_bonus
    hit = attack_roll >= target_ac
    return hit, attack_roll

def handle_saving_throw(spell, spell_save_dc, target_ability_mod, target_proficiency_bonus):
    saving_throw = roll_d20() + target_ability_mod + target_proficiency_bonus
    save = saving_throw >= spell_save_dc
    return save, saving_throw

def calculate_damage(spell, caster_level):
    if spell['level'] == 0:  # Cantrip damage scales with level
        damage_level = math.ceil((caster_level + 2) // 6)
    else:
        damage_level = spell['level']
    damage_string = spell['damage']['damage_at_slot_level'].get(str(damage_level), spell['damage']['damage_at_character_level'].get(str(caster_level)))
    damage_parts = damage_string.split('d')
    num_dice = int(damage_parts[0])
    die_value = int(damage_parts[1])
    total_damage = sum(random.randint(1, die_value) for _ in range(num_dice))
    return total_damage

def detect_conditions(spell):
    response = requests.get(f"{BASE_URL}conditions")
    if response.status_code != 200:
        raise ValueError(f"Error fetching conditions: {response.status_code}")
    conditions = response.json()['results']
    condition_names = [condition['name'] for condition in conditions]
    applied_conditions = [condition for condition in condition_names if condition.lower() in spell['desc'][0].lower()]
    return applied_conditions

def cast_spell(spell_name, caster_level, spellcasting_ability_mod, target_ac, target_proficiency_bonus, target_ability_mods):
    try:
        spell = get_spell_data(spell_name)
    except ValueError as e:
        return str(e)

    result = f"Casting {spell_name}...\n"
    
    if 'attack' in spell['desc'][0].lower():
        hit, attack_roll = handle_attack_roll(spell, caster_level, spellcasting_ability_mod, target_ac)
        if hit:
            damage = calculate_damage(spell, caster_level)
            result += f"Attack roll: {attack_roll} (hit!)\nDamage: {damage}\n"
        else:
            result += f"Attack roll: {attack_roll} (miss)\n"
    
    elif 'saving throw' in spell['desc'][0].lower():
        target_ability = spell['dc']['dc_type']['index']
        target_ability_mod = target_ability_mods[['str', 'dex', 'con', 'int', 'wis', 'cha'].index(target_ability)]
        spell_save_dc = calculate_spell_save_dc(caster_level, spellcasting_ability_mod)
        save, saving_throw = handle_saving_throw(spell, spell_save_dc, target_ability_mod, target_proficiency_bonus)
        if save:
            result += f"Saving throw: {saving_throw} (saved)\n"
        else:
            damage = calculate_damage(spell, caster_level)
            result += f"Saving throw: {saving_throw} (failed)\nDamage: {damage}\n"
    
    else:
        result += "This spell does not require an attack roll or saving throw.\n"
    
    conditions = detect_conditions(spell)
    if conditions:
        result += f"Conditions applied: {', '.join(conditions)}\n"
    
    return result

# Example usage
caster_level = 8
spellcasting_ability_mod = 5
target_ac = 18
target_proficiency_bonus = 3
target_ability_mods = [3, 2, 3, 0, 1, -1]

spells = ["Fire Bolt", "Guiding Bolt", "Entangle", "Tiny Hut", "Magic Missile", "Fireball", "Black Tentacles"]

for spell_name in spells:
    print(cast_spell(spell_name, caster_level, spellcasting_ability_mod, target_ac, target_proficiency_bonus, target_ability_mods))
    print('-' * 40)
