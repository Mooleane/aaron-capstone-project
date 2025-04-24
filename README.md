# Purpose/Problem Statement
This program gives the user essential information about a Pokémon as if it were the Pokédex. Useful for those who are stuck on how to catch a Pokémon, or don't know what else to do with it.
# Target Audience
Fans or Players of Pokémon. 
# Solution + Limitations
Neat tips about a Pokémon can be requested by the user to ensure they know about it's general background, and what to do with it as a player. It would be nice if the image of the Pokémon could be retrieved as well, alongside the official Pokédex entry instead of only the Pokemon's flavor text (usually found on cards). That would give the user more than enough insight on what the Pokémon is and does in a short amount of time.
# Key Features / Key Components
When running the program, a prompt is given to enter a the valid name of a Pokémon or just their Pokédex number.

```
pokemon_name = input("Please enter a Pokémon's Name or Pokédex Number: ")
```

Once entered, information about the Pokémon is retrieved and looped through the API, "PokéAPI v2," with a fair rate limit.

```
            # Requests more info about the Pokémon from it's species entries.
            # The input for 'pokemon_name' is lowered and added to 'URL + species_path'
            # to get info about that specific Pokémon with url capitalization consistency.
            request = requests.get(URL + SPECIES_PATH + pokemon_name.lower(), params=poke_params)
            body = request.json()
```

Player-important info such as the Pokémon's Pokéball success rate, and its evolution requirements for different paths (especially Eevee) will be displayed. Additionally, its Card entry will be shown for basic insights.

```
# Retrieves the Pokéball Success Rate of the Pokémon through its listed "capture_rate" from the API.
print("Pokéball Success Rate (Maximum is 255):", body["capture_rate"])
```

# Technical Challenges + Future Plans
A difficulty during the creation of this project was figuring out how to display the requirements for each evolutionary stage of a Pokémon. Number-based requirements are looped through the API's data via a function in-order to account for most Pokémon, but still leaves room for miscellaneous evolution requirements.

## The Numerical Requirements

```
# The possible requirements for an evolution, when calling an evolution chain function.
MIN_REQUIREMENTS = ("min_level", "min_happiness", "min_beauty", "min_affection")
```

## The Functions

```
# Used for the second stage of a Pokémon in its evolution chain to list off evolution requirements.
def evolutionRequirements(evolution_information, min_requirement, second_stage):
    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_body["chain"]["evolves_to"][second_stage]["evolution_details"][0][min_requirement] > 0:
        print("\t\t\t" + min_requirement.replace("min_","").title() + " Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0][min_requirement])
        
# Used for the third stage of a Pokémon in its evolution chain to list off evolution requirements.
def evolutionRequirements2(evolution_information, min_requirement, second_stage, third_stage):
    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_body["chain"]["evolves_to"][second_stage]["evolves_to"][third_stage]["evolution_details"][0][min_requirement] > 0:
        print("\t\t\t\t" + min_requirement.replace("min_","").title() + " Requirement:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][0][min_requirement])
```

## The evolution requirements of the Pokémon

```
            # If the evolution requirement uses an item, it will print out the evolution item requirement.
            if "use-item" in evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["trigger"]["name"]:
                # Uses .replace to fill in any hyphens with spaces to improve readability.
                print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["item"]["name"].title().replace("-", " "))
                
            # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
            for min_requirement in MIN_REQUIREMENTS:
                evolutionRequirements(evolution_body, min_requirement, i)
```

If given more time, I would have included a rundown of the Pokémon's stats, abilities, and type influences. That would give players the preperation they need when interacting with a specific Pokémon.
# Project Timeline
At our internship, we were first introduced to the creation of a project involving API calls and decided which APIs to use. After I chose PokéAPI v2, I got to work skimming through its documentation for ideas. After some brainstorming, I decided to recreate the Pokédex (mainly its evolution functions). About 1-2 days were spent in school to implement its main features such as displaying general insights about a Pokémon and its evolution paths. Another day was spent at my internship to implement peer suggestions such as displaying the evolution requirements of Pokémon.
# Tools and Resources Used
TechSmart - The primary IDE used to code.
PokéAPI v2 - The API this project was based around.
