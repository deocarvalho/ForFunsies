import fetch from 'node-fetch';

async function castSpell(spellName, casterLevel, spellcastingAbilityMod, targetAC, targetProficiencyBonus, targetAbilityMods) {
    try {
        const formattedName = spellName.toLowerCase().replace(/\s+/g, '-');
        const responseSpell = await fetch(`https://www.dnd5eapi.co/api/spells/${formattedName}`); 
        const spell =  await responseSpell.json(); 

        let result = `Casting ${spellName}...\n`;

        if (spell.desc[0].toLowerCase().includes('attack')) {
            const proficiencyBonus = Math.ceil(1 + (casterLevel / 4));
            const attackRoll = Math.floor(Math.random() * 20) + 1 + spellcastingAbilityMod + proficiencyBonus;
            const hit = attackRoll >= targetAC;

            if (hit) {
                let damageString;
                if (spell.level === 0) {
                    const damageLevel = Math.floor((casterLevel - 1) / 4) * 4 + 1;
                    damageString = spell.damage.damage_at_character_level[damageLevel.toString()];
                } else {
                    damageString = spell.damage.damage_at_slot_level[spell.level.toString()];
                }

                const [numDice, dieValue] = damageString.split('d').map(Number);
                let totalDamage = 0;
                for (let i = 0; i < numDice; i++) {
                    totalDamage += Math.floor(Math.random() * dieValue) + 1;
                }

                result += `Attack roll: ${attackRoll} (hit!)\nDamage: ${totalDamage}\n`;
            } else {
                result += `Attack roll: ${attackRoll} (miss)\n`;
            }
        }
        else if (spell.desc[0].toLowerCase().includes('saving throw')) {
            const targetAbility = spell.dc.dc_type.index;
            const abilityIndex = ['str', 'dex', 'con', 'int', 'wis', 'cha']
                .indexOf(targetAbility);
            const targetAbilityMod = targetAbilityMods[abilityIndex];
            const spellSaveDC = 8 + Math.ceil(1 + (casterLevel / 4)) + spellcastingAbilityMod;

            const savingThrow = Math.floor(Math.random() * 20) + 1 + targetAbilityMod + targetProficiencyBonus;
            const save = savingThrow >= spellSaveDC;

            if (save) {
                result += `Saving throw: ${savingThrow} (saved)\n`;
            } else {
                let damageString;
                if (spell.level === 0) {
                    const damageLevel = Math.floor((casterLevel - 1) / 4) * 4 + 1;
                    damageString = spell.damage.damage_at_character_level[damageLevel.toString()];
                } else {
                    damageString = spell.damage.damage_at_slot_level[spell.level.toString()];
                }

                const [numDice, dieValue] = damageString.split('d').map(Number);
                let totalDamage = 0;
                for (let i = 0; i < numDice; i++) {
                    totalDamage += Math.floor(Math.random() * dieValue) + 1;
                }
                result += `Saving throw: ${savingThrow} (failed)\nDamage: ${totalDamage}\n`;
            }
        }
        else {
            result += "This spell does not require an attack roll or saving throw.\n";
        }

        const responseConditions = await fetch(`https://www.dnd5eapi.co/api/conditions`); 
        const data = await responseConditions.json(); 
        const conditionNames = data.results.map(condition => condition.name);
        const conditions = conditionNames.filter(condition =>
            spell.desc[0].toLowerCase().includes(condition.toLowerCase())
        );
        if (conditions.length > 0) {
            result += `Conditions applied: ${conditions.join(', ')}\n`;
        }

        return result;
    } catch (error) {
        return error.message;
    }
}


const casterLevel = 8;
const spellcastingAbilityMod = 5;
const targetAC = 18;
const targetProficiencyBonus = 3;
const targetAbilityMods = [3, 2, 3, 0, 1, -1];

const spells = ["Fire Bolt", "Guiding Bolt", "Entangle", "Tiny Hut", "Magic Missile", "Fireball", "Black Tentacles"];

async function runExamples() {
    for (const spellName of spells) {
        const result = await castSpell(spellName, casterLevel, spellcastingAbilityMod, targetAC, targetProficiencyBonus, targetAbilityMods); 
        console.log(result);
        console.log('-'.repeat(40));
    }
}


runExamples();