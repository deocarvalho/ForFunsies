// Roll a die with a specified number of sides
function roll_d(size) {
    return Math.floor(Math.random() * size) + 1;
}

// Extract damage details from a damage string
function get_damage(damage) {
    const damage_parts = damage.damage_dice.split('+');
    const dice_parts = damage_parts[0].split('d');
    const num_dice = parseInt(dice_parts[0]);
    const die_type = parseInt(dice_parts[1]);
    const damage_bonus = parseInt(damage_parts[1]) || 0;
    return [num_dice, die_type, damage_bonus];
}

// Fetch creature stats from the D&D 5e API
async function get_creature_stats(creature_name) {
    const response = await fetch(`https://www.dnd5eapi.co/api/monsters/${creature_name.toLowerCase().replace(' ', '-')}`);

    if (response.status === 200) {
        const data = await response.json();

        // Extract relevant stats
        const initiative_bonus = Math.floor((data.dexterity - 10) / 2);

        // Determine attacks from multiattack if available, otherwise use the first action
        const multiattack = data.actions.find((action) => action.name.toLowerCase() === 'multiattack');
        let attacks = [];

        if (multiattack && multiattack.actions) {
            // Collect actions specified in multiattack
            for (const action_info of multiattack.actions) {
                const action_name = action_info.action_name;
                const count = action_info.count;
                // Find the matching action details
                const action = data.actions.find((act) => act.name === action_name);

                if (action && action.damage) {
                    const attack_details = {
                        count: count,
                        attack_bonus: action.attack_bonus,
                        damage_sets: [],
                    };

                    for (const damage of action.damage) {
                        attack_details.damage_sets.push(get_damage(damage));
                    }

                    attacks.push(attack_details);
                }
            }
        } else {
            // Fall back to using the first action if no multiattack is present
            if (data.actions) {
                const action = data.actions[0];

                if (action.damage) {
                    const attack_details = {
                        count: 1,
                        attack_bonus: action.attack_bonus,
                        damage_sets: [],
                    };

                    for (const damage of action.damage) {
                        attack_details.damage_sets.push(get_damage(damage));
                    }

                    attacks.push(attack_details);
                }
            }
        }

        return {
            name: data.name,
            initiative_bonus: initiative_bonus,
            hp: data.hit_points, 
            ac: data.armor_class[0].value,
            attacks: attacks
        };
    } else {
        throw new Error(`Could not retrieve stats for ${creature_name}`);
    }
}

// Simulate a fight between two D&D 5e creatures
async function simulate_fight(c1, c2) {
    // Roll initiative
    const c1_init = roll_d(20) + c1.initiative_bonus;
    const c2_init = roll_d(20) + c2.initiative_bonus;

    // Determine attacker and defender based on initiative
    let attacker, attacker_hp, defender, defender_hp;
    if (c1_init >= c2_init) {
        [attacker, attacker_hp, defender, defender_hp] = [c1, c1.hp, c2, c2.hp];
    } else {
        [attacker, attacker_hp, defender, defender_hp] = [c2, c2.hp, c1, c1.hp];
    }

    while (attacker_hp > 0) {
        // Perform each attack in the attacker's attacks list
        for (const attack of attacker.attacks) {
            for (let i = 0; i < attack.count; i++) {
                // Roll to hit
                const attack_roll = roll_d(20) + attack.attack_bonus;

                // If hit, calculate damage
                if (attack_roll >= defender.ac) {
                    let total_damage = 0;

                    for (const [num_dice, die_type, damage_bonus] of attack.damage_sets) {
                        let damage = damage_bonus; // Start with damage bonus

                        for (let j = 0; j < num_dice; j++) {
                            damage += roll_d(die_type); // Type of damage die
                        }

                        if (attack_roll === 20 + attack.attack_bonus) // Critical hit
                            damage += damage;

                        total_damage += damage;
                    }

                    defender_hp -= total_damage;
                }
            }

            // Switch attacker and defender
            [attacker, attacker_hp, defender, defender_hp] = [defender, defender_hp, attacker, attacker_hp];
        }
    }

    return defender.name;
}

// Run a specified number of fights and return the win percentages
async function run_simulations(c1_name, c2_name, num_fights) {
    const c1 = await get_creature_stats(c1_name);
    const c2 = await get_creature_stats(c2_name);

    let c1_wins = 0;
    let c2_wins = 0;

    for (let i = 0; i < num_fights; i++) {
        const winner = await simulate_fight(c1, c2);

        if (winner === c1_name) {
            c1_wins++;
        } else {
            c2_wins++;
        }
    //    console.clear();
    //    console.log(`${c1.name} wins: ${c1_wins}; ${c2.name} wins: ${c2_wins};`);
    }

    const c1_win_percentage = (c1_wins / num_fights) * 100;
    const c2_win_percentage = (c2_wins / num_fights) * 100;

    return [c1_win_percentage, c2_win_percentage];
}

// Run 1000 simulations
const c1_name = 'Owlbear';
const c2_name = 'Unicorn';
const [c1_win_percentage, c2_win_percentage] = await run_simulations(c1_name, c2_name, 1000);

console.log(`${c1} win percentage: ${c1_win_percentage.toFixed(2)}%`);
console.log(`${c2} win percentage: ${c2_win_percentage.toFixed(2)}%`);