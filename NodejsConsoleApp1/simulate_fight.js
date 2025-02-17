function roll_d(size) {
    return Math.floor(Math.random() * size) + 1;
}

function simulate_fight(c1, c2) {
    const c1_init = roll_d(20) + c1.initiativeBonus;
    const c2_init = roll_d(20) + c2.initiativeBonus;

    let attacker, attacker_hp, defender, defender_hp;
    if (c1_init >= c2_init) {
        [attacker, attacker_hp, defender, defender_hp] = [c1, c1.hp, c2, c2.hp];
    } else {
        [attacker, attacker_hp, defender, defender_hp] = [c2, c2.hp, c1, c1.hp];
    }

    while (attacker_hp > 0) {
        for (let i = 0; i < attacker.numAttacks; i++) { 
            const attack_roll = roll_d(20) + attacker.attackBonus; 
            if (attack_roll >= defender.ac) { 
                let damage = 0; 
                for (let j = 0; j < attacker.numDice; j++) {
                    damage += roll_d(attacker.dieType); 
                }
                if (attack_roll === 20 + attacker.attackBonus) { 
                    damage *= 2; 
                }
                defender_hp -= damage + attacker.damageBonus;
            }
        }

        [temp, temp_hp] = [defender, defender_hp];
        [defender, defender_hp] = [attacker, attacker_hp];
        [attacker, attacker_hp] = [temp, temp_hp];
    }

    return defender[0];
}

function run_simulations(c1, c2, num_fights) {
    let c1_wins = 0;
    let c2_wins = 0;

    for (let i = 0; i < num_fights; i++) {
        const winner = simulate_fight(c1, c2);
        if (winner === c1[0]) {
            c1_wins++;
        } else {
            c2_wins++;
        }
        //console.clear();
        //console.log(`${c1.name} wins: ${c1_wins}; ${c2.name} wins: ${c2_wins};`);
    }

    const c1_win_percentage = (c1_wins / num_fights) * 100;
    const c2_win_percentage = (c2_wins / num_fights) * 100;

    return [c1_win_percentage, c2_win_percentage];
}

// Creature data
const t_rex = { name: "Tyrannosaurus Rex", initiativeBonus: 0, hp: 136, ac: 13, numAttacks: 1, attackBonus: 10, numDice: 4, dieType: 12, damageBonus: 7 };
const giant_ape = { name: "Giant Ape", initiativeBonus: 2, hp: 157, ac: 12, numAttacks: 2, attackBonus: 9, numDice: 3, dieType: 10, damageBonus: 6 };

// Run 100000 simulations
const [t_rex_win_percentage, giant_ape_win_percentage] = run_simulations(t_rex, giant_ape, 100000);

console.log(`T-Rex win percentage: ${t_rex_win_percentage.toFixed(2)}%`);
console.log(`Giant Ape win percentage: ${giant_ape_win_percentage.toFixed(2)}%`);