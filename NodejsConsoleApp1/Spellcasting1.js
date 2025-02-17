async function castSpell(spellName, casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods) {
    // Replace spaces with dashes and convert to lower case
    spellName = spellName.replace(" ", "-").toLowerCase();

    // Get the spell details
    const response = await fetch(`https://www.dnd5eapi.co/api/spells/${spellName}`);
    const spell = await response.json();

    // Check if the spell requires an attack roll
    if ("attack_type" in spell) {
        // Make the attack roll
        const attackRoll =
            Math.floor(Math.random() * 20) + 1 + casterProficiency + casterAbilityMod;

        // Check if the attack hits
        if (attackRoll >= targetAc) {
            result = "hits";
        } else {
            result = "misses";
        }
        return `The ${spellName} spell ${result} the target with an attack roll of ${attackRoll}.`;
    }
    // Check if the spell requires a saving throw
    else if ("dc" in spell) {
        // Get the type of saving throw
        const savingThrow = spell.dc.dc_type;

        // Make the saving throw
        const savingThrowRoll =
            Math.floor(Math.random() * 20) +
            1 +
            targetProficiency +
            targetAbilityMods[savingThrow.index];

        // Check if the saving throw is successful
        if (savingThrowRoll >= 8 + casterProficiency + casterAbilityMod) {
            result = "successfully makes";
        } else {
            result = "fails";
        }
        return `The target ${result} the ${savingThrow.name} saving throw with a roll of ${savingThrowRoll}.`;
    }
}

// Example usage:
const casterProficiency = 2;
const casterAbilityMod = 3;
const targetAc = 15;
const targetProficiency = 2;
const targetAbilityMods = { str: 1, dex: 2, con: 3, int: 4, wis: 5, cha: 6 };

castSpell("Fire Bolt", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));

castSpell("Entangle", casterProficiency, casterAbilityMod, targetAc, targetProficiency, targetAbilityMods).then((result) => console.log(result));