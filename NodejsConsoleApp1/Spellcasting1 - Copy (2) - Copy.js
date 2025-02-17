// Função para calcular o resultado de um ataque ou salvaguarda
function calculateAttackOrSave(attackRoll, targetAc) {
    return attackRoll >= targetAc ? 'hits' : 'misses';
}

function calculateSavingThrow(savingThrowRoll, dc) {
    return savingThrowRoll >= dc ? 'successfully makes' : 'does not affect';
}

// Função para calcular o dano de uma magia
function calculateDamage(spell) {
    if ("damage" in spell && "level" in spell) {
        const damageDice = ("damage_at_slot_level" in spell.damage)
            ? spell.damage.damage_at_slot_level[spell.level]
            : spell.damage.damage_at_character_level[1];
        const [numDice, diceType] = damageDice.split("d").map(Number);
        let damageRoll = 0;
        for (let i = 0; i < numDice; i++) {
            damageRoll += Math.floor(Math.random() * diceType) + 1;
        }
        const damageType = spell.damage.damage_type.name;
        return ` and deals ${damageRoll} ${damageType} damage`;
    }
    return "";
}

// Função para verificar se uma magia causa algum efeito adicional
async function checkConditions(spell) {
    const conditionsResponse = await fetch("https://www.dnd5eapi.co/api/conditions");
    const data = await conditionsResponse.json();
    const conditions = data.results.map(condition => condition.index).filter(condition =>
        spell.desc.some(description =>
            description.toLowerCase().includes(condition.toLowerCase())
        )
    );
    return conditions.length > 0 ? ` ${conditions.join(', ')}` : "";
}

// Função principal para simular o lançamento de uma magia
async function castSpell(spellName, casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods) {
    spellName = spellName.replace(" ", "-").toLowerCase();

    const response = await fetch(`https://www.dnd5eapi.co/api/spells/${spellName}`);
    if (!response.ok) {
        throw new Error(`Não foi possível encontrar informações sobre a magia ${spellName}.`);
    }
    const spell = await response.json();

    // Lógica principal da função, agora mais curta
    const isAttack = "attack_type" in spell;
    const isSave = "dc" in spell;

    if (!isAttack && !isSave) {
        return `The ${spellName} spell does not require an attack roll or saving throw.`;
    }

    const attackRoll = isAttack ? Math.floor(Math.random() * 20) + 1 + casterProficiency + casterAbilityMod : 0;
    const savingThrow = isSave ? spell.dc.dc_type : null;
    const savingThrowRoll = isSave ? Math.floor(Math.random() * 20) + 1 + targetProficiency + targetAbilityMods[savingThrow.index] : 0;

    const result = isAttack
        ? calculateAttackOrSave(attackRoll, targetAc)
        : calculateSavingThrow(savingThrowRoll, 8 + casterProficiency + casterAbilityMod);

    const damageMessage = calculateDamage(spell);
    const conditionMessage = await checkConditions(spell);

    return `The ${spellName} spell ${result} the target${damageMessage}${conditionMessage}.`;
}

// Exemplo de uso (mantendo o mesmo do exemplo anterior)
const casterProficiency = 2;
const casterAbilityMod = 3;
const targetAc = 15;
const targetProficiency = 2;
const targetAbilityMods = { str: 2, dex: 2, con: 2, int: 2, wis: 2, cha: 2 };

castSpell("Fire Bolt", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));
castSpell("Entangle", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));
castSpell("Guidance", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));