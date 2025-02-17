async function getBeasts(cr) {
    const baseUrl = "https://api.open5e.com/v1/monsters";
    const params = {
        type__iexact: "beast",
        document__slug: "wotc-srd",
        cr: cr,
    };

    const url = new URL(baseUrl);
    Object.entries(params).forEach(([key, value]) =>
        url.searchParams.append(key, value)
    );

    const response = await fetch(url);
    const data = await response.json();
    return data.results;
}

async function conjureAnimals(numberOfAnimals) {
    // Map the number of animals to their CR
    const crMap = { 1: 2, 2: 1, 4: 0.5, 8: 0.25 };
    const cr = crMap[numberOfAnimals];

    const beasts = await getBeasts(cr);

    // Permitir repetições usando random choices
    const chosenBeasts = Array.from({ length: numberOfAnimals }, () => {
        const randomIndex = Math.floor(Math.random() * beasts.length);
        return beasts[randomIndex].name;
    });

    // Ordena a lista de animais em ordem alfabética
    chosenBeasts.sort((a, b) => a.localeCompare(b));

    return chosenBeasts;
}

// Example usage:
conjureAnimals(8).then((conjuredAnimals) => {
    console.log(conjuredAnimals);
});
conjureAnimals(8).then((conjuredAnimals) => {
    console.log(conjuredAnimals);
});
conjureAnimals(8).then((conjuredAnimals) => {
    console.log(conjuredAnimals);
});
conjureAnimals(8).then((conjuredAnimals) => {
    console.log(conjuredAnimals);
});
conjureAnimals(8).then((conjuredAnimals) => {
    console.log(conjuredAnimals);
});
