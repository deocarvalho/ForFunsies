async function castSpell(spellName, casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods) {
    spellName = spellName.replace(" ", "-").toLowerCase();


    const response = await fetch(`https://www.dnd5eapi.co/api/spells/${spellName}`);
    const spell = await response.json();


    let result = "";


    if ("attack_type" in spell) {
        const attackRoll = Math.floor(Math.random() * 20) + 1 + casterProficiency + casterAbilityMod;


        if (attackRoll >= targetAc) {
            result = "hits";
        } else {
            result = "misses";
        }

    } else if ("dc" in spell) {
        const savingThrow = spell.dc.dc_type;
        const savingThrowRoll = Math.floor(Math.random() * 20) + 1 + targetProficiency + targetAbilityMods[savingThrow.index];


        if (savingThrowRoll >= 8 + casterProficiency + casterAbilityMod) {
            result = "successfully makes";
        } else {
            result = "does not affect";
        }

    } else {
        return `The ${spellName} spell does not require an attack roll or saving throw.`;
    }


    let damageMessage = "";
    if (result === "hits" || result === "fails") {
        if ("damage" in spell && "level" in spell) {
            if ("damage_at_slot_level" in spell.damage) {
                var damageDice = spell.damage.damage_at_slot_level[spell.level];
            } else {
                var damageDice = spell.damage.damage_at_character_level[1];
            }
            const [numDice, diceType] = damageDice.split("d").map(Number);
            let damageRoll = 0;
            for (let i = 0; i < numDice; i++) {
                damageRoll += Math.floor(Math.random() * diceType) + 1;
            }
            const damageType = spell.damage.damage_type.name;

            damageMessage = ` and deals ${damageRoll} ${damageType} damage`;
        }
    }

    const conditionsResponse = await fetch("https://www.dnd5eapi.co/api/conditions");
    const data = await conditionsResponse.json();
    const conditions = data.results.map(condition => condition.index).filter(condition =>
        spell.desc.some(description =>
            description.toLowerCase().includes(condition.toLowerCase())
        )
    );

    let conditionMessage = "";
    if (conditions.length > 0) {
        conditionMessage = ` ${conditions.join(', ')}`;
    }

    return `The ${spellName} spell ${result} the target${damageMessage}${conditionMessage}.`;
}

const casterProficiency = 2;
const casterAbilityMod = 3;
const targetAc = 15;
const targetProficiency = 2;
const targetAbilityMods = { str: 2, dex: 2, con: 2, int: 2, wis: 2, cha: 2 };

castSpell("Fire Bolt", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));

castSpell("Entangle", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));

castSpell("Guidance", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));
