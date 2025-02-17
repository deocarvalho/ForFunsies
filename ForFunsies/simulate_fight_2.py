import random
import requests
import os
clear = lambda: os.system('cls')

def roll_d(size):
    return random.randint(1, size)

def get_damage(damage):
    damage_parts = damage['damage_dice'].split('+')
    dice_parts = damage_parts[0].split('d')
    num_dice = int(dice_parts[0])
    die_type = int(dice_parts[1])
    damage_bonus = int(damage_parts[1]) or 0
    return (num_dice, die_type, damage_bonus)

def get_creature_stats(creature_name):
    """Fetches the creature's stats from the D&D 5e API."""
    response = requests.get(f"https://www.dnd5eapi.co/api/monsters/{creature_name.lower().replace(' ', '-')}")
    if response.status_code == 200:
        data = response.json()

        # Extract relevant stats
        name = data['name']
        dexterity = data['dexterity']
        initiative_bonus = (dexterity - 10) // 2  # Calculate initiative bonus from dexterity
        hp = data['hit_points']
        ac = data['armor_class'][0]['value']

        # Determine attacks from multiattack if available, otherwise use the first action
        multiattack = next((action for action in data['actions'] if action['name'].lower() == 'multiattack'), None)
        attacks = []

        if multiattack and 'actions' in multiattack:
            # Collect actions specified in multiattack
            for action_info in multiattack['actions']:
                action_name = action_info['action_name']
                count = action_info['count']
                # Find the matching action details
                action = next((act for act in data['actions'] if act['name'] == action_name), None)
                if action and 'damage' in action:
                    attack_details = {
                        'count': count,
                        'attack_bonus': action['attack_bonus'],
                        'damage_sets': []
                    }
                    for damage in action['damage']:
                        attack_details['damage_sets'].append(get_damage(damage))
                    attacks.append(attack_details)
        else:
            # Fall back to using the first action if no multiattack is present
            if data['actions']:
                action = data['actions'][0]
                if 'damage' in action:
                    attack_details = {
                        'count': 1,
                        'attack_bonus': action['attack_bonus'],
                        'damage_sets': []
                    }
                    for damage in action['damage']:
                        attack_details['damage_sets'].append(get_damage(damage))
                    attacks.append(attack_details)

        return name, initiative_bonus, hp, ac, attacks
    else:
        raise ValueError(f"Could not retrieve stats for {creature_name}")

def simulate_fight(c1, c2):
    """Simulates a basic fight between two D&D 5e creatures and returns the winner."""
    # Roll initiative
    c1_init = roll_d(20) + c1[1]
    c2_init = roll_d(20) + c2[1]

    # Determine attacker and defender based on initiative
    if c1_init >= c2_init:
        attacker, attacker_hp, defender, defender_hp = c1, c1[2], c2, c2[2]
    else:
        attacker, attacker_hp, defender, defender_hp = c2, c2[2], c1, c1[2]

    while attacker_hp > 0:
        # Perform each attack in the attacker's attacks list
        for attack in attacker[4]:
            for _ in range(attack['count']):  # Number of attacks
                attack_roll = roll_d(20) + attack['attack_bonus']  # Bonus to hit
                if attack_roll >= defender[3]:  # Defender's AC
                    total_damage = 0
                    for num_dice, die_type, damage_bonus in attack['damage_sets']:
                        damage = damage_bonus  # Start with damage bonus
                        if attack_roll == 20 + attack['attack_bonus']:  # If it was a critical hit
                            num_dice *= 2  # Double the number of damage dice
                        for _ in range(num_dice):
                            damage += roll_d(die_type)  # Type of damage die
                        total_damage += damage
                    defender_hp -= total_damage

        temp, temp_hp = attacker, attacker_hp
        attacker, attacker_hp = defender, defender_hp
        defender, defender_hp = temp, temp_hp

    return defender[0]

def run_simulations(c1_name, c2_name, num_fights):
    """Runs a specified number of fights and returns the win percentages."""
    c1 = get_creature_stats(c1_name)
    c2 = get_creature_stats(c2_name)


    c1_wins = 0
    c2_wins = 0

    for _ in range(num_fights):
        winner = simulate_fight(c1, c2)
        if winner == c1_name:
            c1_wins += 1
        else:
            c2_wins += 1
        # clear()
        # print(f"{c1_name} wins: {c1_wins}; {c2_name} wins: {c2_wins};")

    c1_win_percentage = (c1_wins / num_fights) * 100
    c2_win_percentage = (c2_wins / num_fights) * 100


    return c1_win_percentage, c2_win_percentage

# Run 100000 simulations
c1 = "Owlbear"
c2 = "Unicorn"
c1_win_percentage, c2_win_percentage = run_simulations(c1, c2, 100000)

print(f"{c1} win percentage: {c1_win_percentage:.2f}%")
print(f"{c2} win percentage: {c2_win_percentage:.2f}%")
