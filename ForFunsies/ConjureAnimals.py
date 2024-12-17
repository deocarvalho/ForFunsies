import requests
import random

def get_beasts(cr):
    base_url = "https://api.open5e.com/v1/monsters"
    params = {"type__iexact": "beast", "document__slug": "wotc-srd", "cr": cr}
    response = requests.get(base_url, params=params)
    beasts = response.json()['results']
    return beasts

def conjure_animals(number_of_animals):
    # Map the number of animals to their CR
    cr_map = {1: 2, 2: 1, 4: 0.5, 8: 0.25}
    cr = cr_map[number_of_animals]
    
    beasts = get_beasts(cr)
    chosen_beasts = random.sample(beasts, number_of_animals)
    return [beast['name'] for beast in chosen_beasts]

# Example usage:
conjured_animals = conjure_animals(2)
print(conjured_animals)
