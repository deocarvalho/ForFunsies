// Função para buscar dados de uma magia
async function fetchSpellData(spellName) {
    const formattedName = spellName.toLowerCase().replace(/\s+/g, '-');
    const response = await fetch(`${BASE_URL}spells/${formattedName}`);
    if (!response.ok) {
        throw new Error(`Error fetching spell data: ${response.status}`);
    }
    return await response.json();
}

// Função para buscar lista de condições
async function fetchConditions() {
    const response = await fetch(`${BASE_URL}conditions`);
    if (!response.ok) {
        throw new Error(`Error fetching conditions: ${response.status}`);
    }
    const data = await response.json();
    return data.results.map(condition => condition.index);
}

// Função para rolar um dado de 20 lados
function rollD20() {
    return Math.floor(Math.random() * 20) + 1;
}

// Função para calcular o bonus de proficiência
function calculateProficiencyBonus(level) {
    return Math.ceil(1 + (level / 4));
}

// Função para calcular a classe de dificuldade do teste de salvaguarda da magia
function calculateSpellSaveDC(casterLevel, spellcastingAbilityMod) {
    const proficiencyBonus = calculateProficiencyBonus(casterLevel);
    return 8 + proficiencyBonus + spellcastingAbilityMod;
}

// Função para calcular a rolagem de ataque
function handleAttackRoll(spell, casterLevel, spellcastingAbilityMod, targetAC) {
    const proficiencyBonus = calculateProficiencyBonus(casterLevel);
    const attackRoll = rollD20() + spellcastingAbilityMod + proficiencyBonus;
    const hit = attackRoll >= targetAC;
    return { hit, attackRoll };
}

// Função para calcular a rolagem de salvaguarda
function handleSavingThrow(spell, spellSaveDC, targetAbilityMod, targetProficiencyBonus) {
    const savingThrow = rollD20() + targetAbilityMod + targetProficiencyBonus;
    const save = savingThrow >= spellSaveDC;
    return { save, savingThrow };
}

// Função para calcular o dano da magia
function calculateDamage(spell, casterLevel) {
    let damageString;
    if (spell.level === 0) {  // O dano do feitiço escala de acordo com o nível do personagem
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
    return totalDamage;
}

// Função para encontrar condições no texto de descrição da magia
async function detectConditions(spell) {
    return conditions.filter(condition =>
        spell.desc.some(description =>
            description.toLowerCase().includes(condition.toLowerCase())
        )
    );
}

// Função principal para lançar a magia
async function castSpell(spellName, casterLevel, spellcastingAbilityMod, targetAC, targetProficiencyBonus, targetAbilityMods) {
    try {
        const spell = await fetchSpellData(spellName);
        let result = `Casting ${spellName}...\n`;
        
        if (spell.desc[0].toLowerCase().includes('attack')) {
            const { hit, attackRoll } = handleAttackRoll(spell, casterLevel, spellcastingAbilityMod, targetAC);
            if (hit) {
                const damage = calculateDamage(spell, casterLevel);
                result += `Attack roll: ${attackRoll} (hit!)\nDamage: ${damage}\n`;
            } else {
                result += `Attack roll: ${attackRoll} (miss)\n`;
            }
        } 
        else if (spell.desc[0].toLowerCase().includes('saving throw')) {
            const targetAbility = spell.dc.dc_type.index;
            const abilityIndex = ['str', 'dex', 'con', 'int', 'wis', 'cha']
                .indexOf(targetAbility);
            const targetAbilityMod = targetAbilityMods[abilityIndex];
            const spellSaveDC = calculateSpellSaveDC(casterLevel, spellcastingAbilityMod);
            const { save, savingThrow } = handleSavingThrow(
                spell, spellSaveDC, targetAbilityMod, targetProficiencyBonus
            );
            
            if (save) {
                result += `Saving throw: ${savingThrow} (saved)\n`;
            } else {
                const damage = calculateDamage(spell, casterLevel);
                result += `Saving throw: ${savingThrow} (failed)\nDamage: ${damage}\n`;
            }
        } 
        else {
            result += "This spell does not require an attack roll or saving throw.\n";
        }
        
        const conditions = await detectConditions(spell);
        if (conditions.length > 0) {
            result += `Conditions applied: ${conditions.join(', ')}\n`;
        }
        
        return result;
    } catch (error) {
        return error.message;
    }
}

// URL base para as requisições
const BASE_URL = "https://www.dnd5eapi.co/api/";  

// Exemplo de uso
const casterLevel = 8;
const spellcastingAbilityMod = 5;
const targetAC = 18;
const targetProficiencyBonus = 3;
const targetAbilityMods = [3, 2, 3, 0, 1, -1];

const spells = ["Fire Bolt", "Guiding Bolt", "Entangle", "Tiny Hut", "Magic Missile", "Fireball", "Black Tentacles"];

const conditions = await fetchConditions();

async function runExamples() {
    for (const spellName of spells) {
        const result = await castSpell(
            spellName, 
            casterLevel, 
            spellcastingAbilityMod, 
            targetAC, 
            targetProficiencyBonus, 
            targetAbilityMods
        );
        console.log(result);
        console.log('-'.repeat(40));
    }
}

runExamples();