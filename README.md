# Purpose/Problem Statement
This [program](student_project.py) gives the user essential information about a Pokémon as if it were the Pokédex. 

Useful for those who are stuck on how to obtain a Pokémon, or don't know what else to do with it.
# Target Audience
Fans or Players of Pokémon. 
# Solution + Limitations
Neat tips about a Pokémon can be requested by the user to ensure they know about it's general background, and what to do with it as a player in a digestable amount of time. It would be nice if the image of the Pokémon could be provided as well, alongside the official Pokédex entry instead of only the Pokemon's flavor text (usually found on cards). That would give the user more than enough insight on what the Pokémon is and does.
# Key Features / Key Components
When running the program, a prompt is given to enter the valid name of a Pokémon or just their Pokédex number.

```python
pokemon_name = input("Please enter a Pokémon's Name or Pokédex Number: ")
```

Once entered, information about the Pokémon is validated and retrieved through the API, "PokéAPI v2," with a fair rate limit (no parameters needed to be changed).

## The API call and the validation steps

```python
    # The input loop will stop if the user wants to
    # quit the program by typing "EXIT".
    while pokemon_name != "EXIT":
        # Verifies the user input is either alphabetical for the Pokémon Name
        # or the user input has a digit for the Pokédex Number.
        if pokemon_name.isalpha() or pokemon_name.isdigit():
            # Requests more info about the Pokémon from it's species entries.
            # The input for 'pokemon_name' is lowered and added to 'URL + SPECIES_PATH'
            # to get info about that specific Pokémon with url capitalization consistency.
            request = requests.get(URL + SPECIES_PATH + pokemon_name.lower(), params=poke_params)
            body = request.json()
            
            # Checks if the request was OK (200).
            if request.status_code == 200:
                # Continues getting the requested info if the request is OK.
                body = request.json()
                # Moves onto displaying the info by breaking out of the while loop.
                break
                
            # Checks if there are too many requests (429).
            elif request.status_code == 429:
                pokemon_name = input("PokéAPI v2 is receiving too many requests. Try again later. ")
                
            # Assumes the Pokémon was invalid due to the request failing.
            elif request.status_code == 404:
                pokemon_name = input("Please enter a valid Pokémon. ")
                
            # Warns the user about a different request status code
            else:
                pokemon_name = input("Error: Status Code", request.status_code)

        # Assumes the input was invalid due to not being entirely alphabetical or numerical.
        else:
            pokemon_name = input("Please enter a valid input (no symbols). ")
```

## 

Player-important info such as the Pokémon's Pokéball success rate, and its evolution requirements for different paths will be displayed. Additionally, its first flavor text entry will be shown for basic insights (not every entry is in English).

## Printing data retrieved from the API's json variable

```python
print("Pokéball Success Rate (Maximum is 255):", body["capture_rate"])
```

# Technical Challenges + Future Plans
A challenge during the creation of this project was displaying the requirements for each evolutionary stage of a Pokémon, mostly due to the complexity of PokéAPI v2 requests. Number-based requirements are retrieved through the API's data via a function in-order to account for most Pokémon, but still leaves room for incorrect evolution requirements displayed in the output due to each evolution entry possibly having multiple versions from the PokéAPI v2 datasets.

## The Numerical Requirements

```python
# The possible requirements for an evolution when calling an evolution chain function.
MIN_REQUIREMENTS = ("min_level", "min_happiness", "min_beauty", "min_affection")
```

## The Functions

```python
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

## Printing each available evolution requirement

```python
            # If the evolution requirement uses an item, it will print out the evolution item requirement.
            if "use-item" in evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["trigger"]["name"]:
                # Uses .replace to fill in any hyphens with spaces to improve readability.
                print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["item"]["name"].title().replace("-", " "))
                
            # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
            for min_requirement in MIN_REQUIREMENTS:
                evolutionRequirements(evolution_body, min_requirement, i)
```

## The prints with "Eevee" as the Pokémon

```
Evolution Chain
    Starts From: Eevee
        Evolves Into: Vaporeon | Requirement: Use-Item
            Item Requirement: Water Stone
        Evolves Into: Jolteon | Requirement: Use-Item
            Item Requirement: Thunder Stone
        Evolves Into: Flareon | Requirement: Use-Item
            Item Requirement: Fire Stone
        Evolves Into: Espeon | Requirement: Level-Up
            Happiness Requirement: 160
        Evolves Into: Umbreon | Requirement: Level-Up
            Happiness Requirement: 160
        Evolves Into: Leafeon | Requirement: Level-Up # ? There seems to be incorrect requirements for this path and the one after since it is meant to be the Leaf stone and Ice stone respectively.
        Evolves Into: Glaceon | Requirement: Level-Up # ?
        Evolves Into: Sylveon | Requirement: Level-Up
            Affection Requirement: 2
```

With more time, I could include a rundown of the Pokémon's stats, abilities, and type influences. That would give players more preperation when interacting with a specific Pokémon. 
# Project Timeline
At our internship, we were first introduced to the creation of a project involving API calls and decided which APIs to use. 

I chose PokéAPI v2, and searched through its documentation for ideas. 

After some brainstorming, I decided to recreate the Pokédex (mainly its evolution information). 

About 1-2 days were spent in school to implement its main features such as displaying general insights about a Pokémon and its evolution paths. 

When the project's main deadline and revision deadlines were over, I showed the project to a few others.

A day was spent at my internship to implement peer suggestions such as displaying the evolution requirements of Pokémon.

Another opportunity arose to recycle this project for our internship's culminating project, where I intend to polish and optimize its features.

# Updates
The system for printing the item requirements of an evolution path has changed to use the very first version of a PokéAPI v2 entry that is not None nor outputs an error (uses 'try' to test for an item or an error/no item, 'except' to skip the error/no item, and 'pass' to output nothing about the error).

## Before

```python
            # If the evolution requirement uses an item, it will print out the evolution item requirement.
            if "use-item" in evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["trigger"]["name"]:
                # Uses .replace to fill in any hyphens with spaces to improve readability.
                print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["item"]["name"].title().replace("-", " "))
```

This used to miss out on any item requirements if the first PokéAPI v2 entry [0] did not store an "item" key with an existing "name" key and value but the ones after it did, since PokéAPI v2 uses a dictionary of lists for different iterations/versions of the evolution entry for a Pokémon (this also applies to flavor text entries as it can go from the oldest to newest versions). 

## After

```python
            for z in range(len(evolution_body["chain"]["evolves_to"][i]["evolution_details"])):
                    # Tries to print to see if it runs into an error or displays the item before skipping to any next iteration.
                    try:
                        print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][z]["item"]["name"].title().replace("-", " "))
                    except:
                        # Skips changing or displaying any unnecessary info.
                        pass
```

The for z in range loop goes through the dictionary of lists to print the first iteration/version of the Pokémon's evolution entry that contains the "item" key with an existing "name" key and value that contains the item requirement.

# Tools and Resources Used
* Python - The programming language used for the project.
* TechSmart - The primary IDE used when coding this project.
* PokéAPI v2 - The API this project was based around, including all of its documentation.
