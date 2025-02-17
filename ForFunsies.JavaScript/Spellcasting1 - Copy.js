async function castSpell(spellName, casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods) {
    // 1. Formatar o nome da magia para a API
    spellName = spellName.replace(" ", "-").toLowerCase();

    // 2. Buscar os dados da magia na API
    const response = await fetch(`https://www.dnd5eapi.co/api/spells/${spellName}`);
    const spell = await response.json();

    // 3. Inicializar a variável que armazenará o resultado da magia
    let result = "";

    // 4. Verificar o tipo de rolagem (ataque ou salvaguarda)
    if ("attack_type" in spell) {
        // 4.1. Rolagem de ataque
        const attackRoll = Math.floor(Math.random() * 20) + 1 + casterProficiency + casterAbilityMod;

        // 4.2. Comparar a rolagem com a CA do alvo
        if (attackRoll >= targetAc) {
            result = "hits"; // Acerto
        } else {
            result = "misses"; // Erro
        }

    } else if ("dc" in spell) {
        // 4.3. Rolagem de salvaguarda
        const savingThrow = spell.dc.dc_type; // Tipo de salvaguarda (Força, Destreza, etc.)
        const savingThrowRoll = Math.floor(Math.random() * 20) + 1 + targetProficiency + targetAbilityMods[savingThrow.index];

        // 4.4. Comparar a rolagem com a CD da magia
        if (savingThrowRoll >= 8 + casterProficiency + casterAbilityMod) {
            result = "successfully makes"; // Sucesso na salvaguarda
        } else {
            result = "fails"; // Falha na salvaguarda
        }

    } else {
        // 4.5. Magia sem rolagem
        return `The ${spellName} spell does not require an attack roll or saving throw.`;
    }

    // 5. Calcular o dano (se aplicável)
    let damageMessage = "";
    if (result === "hits" || result === "fails") { // Se a magia acertou ou a salvaguarda falhou
        if ("damage" in spell) { // Se a magia causa dano
            if (spell.damage.damage_at_slot_level) {
                var damageDice = spell.damage.damage_at_slot_level[0]; // Dado de dano da magia
            } else if (spell.damage.damage_at_character_level) {
                var damageDice = spell.damage.damage_at_character_level[0]; // Dado de dano da magia
            }
            const damageType = spell.damage.damage_type.name; // Tipo de dano da magia
            const damageRoll = rollDice(damageDice); // Rolar o dado de dano
            const totalDamage = damageRoll + casterAbilityMod; // Adicionar o modificador de habilidade do lançador
            damageMessage = ` and deals ${totalDamage} ${damageType} damage`; // Mensagem de dano
        }
    }

    // 6. Verificar condições (se aplicável)
    let conditionMessage = "";
    if ("conditions" in spell && spell.conditions.length > 0) { // Se a magia impõe condições
        const conditions = spell.conditions.map(condition => condition.name).join(", "); // Lista de condições
        conditionMessage = ` and imposes the ${conditions} condition`; // Mensagem de condição
    }

    // 7. Construir a mensagem de resultado final
    return `The ${spellName} spell ${result} the target${damageMessage}${conditionMessage}.`;
}

// Função auxiliar para rolar dados
function rollDice(diceString) {
    if (diceString === undefined) {
        return 0; // Retorna 0 se a string de dados for undefined
    }
    const [numDice, diceType] = diceString.split("d").map(Number);
    let total = 0;
    for (let i = 0; i < numDice; i++) {
        total += Math.floor(Math.random() * diceType) + 1;
    }
    return total;
}

// Example usage:
const casterProficiency = 2;
const casterAbilityMod = 3;
const targetAc = 15;
const targetProficiency = 2;
const targetAbilityMods = { str: 1, dex: 2, con: 3, int: 4, wis: 5, cha: 6 };

castSpell("Fire Bolt", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));

castSpell("Entangle", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));