import random

def roll_d(size):
  return random.randint(1, size)

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
    for _ in range(attacker[4]):  # Number of attacks
      attack_roll = roll_d(20) + attacker[5]  # Bonus to hit
      if attack_roll >= defender[3]:  # Defender's AC
        damage = attacker[8]  # Damage bonus
        number_of_damage_dice = attacker[6]  # Number of damage dice
        if attack_roll == 20 + attacker[5]:  # If it was a critical hit
          number_of_damage_dice *= 2  # Double the number of damage dice
        for _ in range(number_of_damage_dice):
          damage += roll_d(attacker[7])  # Type of damage die
        defender_hp -= damage
    
    temp, temp_hp = attacker, attacker_hp
    attacker, attacker_hp = defender, defender_hp
    defender, defender_hp = temp, temp_hp

  return defender[0]

def run_simulations(c1, c2, num_fights):
  """Runs a specified number of fights and returns the win percentages."""

  c1_wins = 0
  c2_wins = 0

  for _ in range(num_fights):
    winner = simulate_fight(c1, c2)
    if winner == c1[0]:
      c1_wins += 1
    else:
      c2_wins += 1

  c1_win_percentage = (c1_wins / num_fights) * 100
  c2_win_percentage = (c2_wins / num_fights) * 100

  return c1_win_percentage, c2_win_percentage

#  (0: creature name, 
#   1: initiative bonus, 
#   2: hp, 
#   3: AC, 
#   4: number of attacks, 
#   5: attack bonus, 
#   6: number of damage dice, 
#   7: type of damage die, 
#   8: damage bonus)
t_rex = ("T-Rex", 0, 136, 13, 1, 10, 4, 12, 7)
giant_ape = ("Giant Ape", 2, 157, 12, 2, 9, 3, 10, 6)

# Run 100000 simulations
t_rex_win_percentage, giant_ape_win_percentage = run_simulations(t_rex, giant_ape, 100000)

print(f"T-Rex win percentage: {t_rex_win_percentage:.2f}%")
print(f"Giant Ape win percentage: {giant_ape_win_percentage:.2f}%")