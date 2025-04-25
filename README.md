# Purpose/Problem Statement
This [program](student_project.py) gives the user essential information about a Pokémon as if it were the Pokédex. 

Useful for those who are stuck on how to obtain a Pokémon, or don't know what else to do with it.
# Target Audience
Fans or Players of Pokémon. 
# Solution + Limitations
Neat tips about a Pokémon can be requested by the user to ensure they know about its general background, and what to do with it as a player in a digestable amount of time. It would be nice if the image of the Pokémon could be provided as well, alongside the official Pokédex entry instead of only the Pokémon's flavor text (usually found on cards). That would give the user more than enough insight on what the Pokémon is and does.
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
A challenge during the creation of this project was displaying the requirements for each evolutionary stage of a Pokémon, mostly due to the complexity of PokéAPI v2 requests. Number-based requirements are retrieved through the API's data via a function in-order to account for most Pokémon, but still leaves room for incorrect evolution requirements displayed in the output due to each evolution entry (list) possibly having multiple versions from the PokéAPI v2 data.

## The Numerical Requirements

```python
# The possible requirements for an evolution when calling an evolution chain function.
MIN_REQUIREMENTS = ("min_level", "min_happiness", "min_beauty", "min_affection")
```

## The First and Second Stage Functions

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

## Printing each Evolution Requirement

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
        Evolves Into: Leafeon | Requirement: Level-Up # ? Meant to be the item requirements of a "Leaf Stone".
        Evolves Into: Glaceon | Requirement: Level-Up # ? Meant to be the item requirements of a "Ice Stone".
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

* # Fixed evolution item requirements not properly displaying

The system for printing the item requirements of an evolution path has changed to use the very first version of a PokéAPI v2 evolution entry (list) that is not None nor outputs an error (uses 'try' to test for an item or an error/no item, 'except' to skip the error/no item, and 'pass' to output nothing about the error).

## Printing the Very First Evolution Item Requirements (Before)

```python
            # If the evolution requirement uses an item, it will print out the evolution item requirement.
            if "use-item" in evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["trigger"]["name"]:
                # Uses .replace to fill in any hyphens with spaces to improve readability.
                print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["item"]["name"].title().replace("-", " "))
```

This used to miss out on any item requirements if the first PokéAPI v2 evolution entry (index 0) did not store an "item" key with an existing "name" key and value but the ones after it did, since PokéAPI v2 uses a dictionary of lists for different versions of the evolution entry for a Pokémon (this also applies to flavor text entries as it can go from the oldest to newest versions). 

## Printing the First Available Evolution Item Requirements (After)

```python
            for z in range(len(evolution_body["chain"]["evolves_to"][i]["evolution_details"])):
                    # Tries to print to see if it runs into an error or displays the item before skipping to any next iteration.
                    try:
                        print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][z]["item"]["name"].title().replace("-", " "))
                    except:
                        # Skips changing or displaying any unnecessary info.
                        pass
```

The for z in range loop goes through the dictionary of lists to print the first iterated version of the Pokémon's evolution entry that contains the "item" key with an existing "name" key and value that contains the item requirement.

* # Tweaked the evolution requirement functions to use the first passed argument

The first parameter of the evolution requirement functions, 'evolution_information', retrieves the evolution data (dictionary) parsed from a JSON request for PokéAPI v2. The original function body did not refer to this parameter, but instead assumed the parsed variable was 'evolution_body'. Each function body has been changed with the replacement of 'evolution_body" to 'evolution_information' as what the parameter indicates is the parsed evolution data (the function still expects 'evolution_body', a.k.a the API evolution data to be passed for 'evolution_information').

## The First and Second Stage Functions (Before)

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

The variable 'evolution_body' is present two times within each function body.

## The First and Second Stage Functions (After)

```python
# Used for the second stage of a Pokémon in its evolution chain to list off evolution requirements.
def evolutionRequirements(evolution_information, min_requirement, second_stage):
    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolution_details"][0][min_requirement] > 0:
        print("\t\t\t" + min_requirement.replace("min_","").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolution_details"][0][min_requirement])
        
# Used for the third stage of a Pokémon in its evolution chain to list off evolution requirements.
def evolutionRequirements2(evolution_information, min_requirement, second_stage, third_stage):
    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolves_to"][third_stage]["evolution_details"][0][min_requirement] > 0:
        print("\t\t\t\t" + min_requirement.replace("min_","").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][0][min_requirement])
```

Both functions now use the parameter 'evolution_information' for the parsed variable instead of 'evolution_body' when referring to the API evolution data.

## Updated prints with Eevee as the Pokémon

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
        Evolves Into: Leafeon | Requirement: Level-Up # Meant to be "Use-Item"
            Item Requirement: Leaf Stone # Correct
        Evolves Into: Glaceon | Requirement: Level-Up # Meant to be "Use-Item"
            Item Requirement: Ice Stone # Correct
        Evolves Into: Sylveon | Requirement: Level-Up
            Affection Requirement: 2
```

* # Reworked evolution requirements to display proper requirements

The system for printing both evolution item requirements and numerical evolution requirements have changed. Instead of 'try' being used to print the first available item requirement, it will validate and assign it to the variable 'item_entry_index' instead. It will use that to output the proper evolution requirement type, item requirement, and numerical requirements, all from the same PokéAPI v2 evolution entry (list).

## Printing the First Available Evolution Item Requirements (Before)

```python
            for z in range(len(evolution_body["chain"]["evolves_to"][i]["evolution_details"])):
                    # Tries to print to see if it runs into an error or displays the item before skipping to any next iteration.
                    try:
                        print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][z]["item"]["name"].title().replace("-", " "))
                    except:
                        # Skips changing or displaying any unnecessary info.
                        pass
```

This only helps with displaying the item requirement, completely ignoring the pretense of the requirement type also needing to be the use of an item.

## Printing the First Available Evolution Requirements (After)

```python
            for z in range(len(evolution_body["chain"]["evolves_to"][i]["evolution_details"])):
                # Tries validating itself with an if statement to see if it runs into an error/no item or contains the item.
                try:
                    if evolution_body["chain"]["evolves_to"][i]["evolution_details"][z]["item"]["name"]:
                        # This variable refers to the first most relevant evolution entry from PokéAPI v2 that contains an item requirement
                        item_entry_index = z

                        # These two prints are based off the same entry with the item requirement.
                        print("\t\tEvolves Into:", evolution_body["chain"]["evolves_to"][i]["species"]["name"].title(), "| Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][item_entry_index]["trigger"]["name"].title())
                        print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][item_entry_index]["item"]["name"].title().replace("-", " "))

                        # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
                        for min_requirement in MIN_REQUIREMENTS:
                            # The optional fourth argument which determines the entry being displayed
                            # is replaced with the same entry with the item requirement.
                            evolutionRequirements(evolution_body, min_requirement, i, item_entry_index)

                        # Breaks since it does need to print more about the evolution name, requirement type, and requirements.
                        break

                except:
                    # Skips changing or displaying any unnecessary info.
                    pass

            # This runs when it evaluates there is no item requirements at all.
            else:
                # This version of the print uses its first evolution entry from PokéAPI v2.
                print("\t\tEvolves Into:", evolution_body["chain"]["evolves_to"][i]["species"]["name"].title(), "| Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0]["trigger"]["name"].title())

                # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
                for min_requirement in MIN_REQUIREMENTS:
                    evolutionRequirements(evolution_body, min_requirement, i)
```

Each evolutionary stage has the display of their requirements tied to one for else loop. If there is no item requirement after every iteration, it will display the very first PokéAPI v2 evolution entry (index 0) requirements instead. This also needed the functions to be changed to include a default parameter value to determine the specific evolution entry to retrieve the requirements from (in the scenario where an evolution item requirement is contained after the first iteratated entry among the evolution entries), defaulting to 0 for the very first PokéAPI v2 evolution entry.

## The First Stage Function (Before)

```python
# Used for the second stage of a Pokémon in its evolution chain to list off evolution requirements.
def evolutionRequirements(evolution_information, min_requirement, second_stage):
    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_body["chain"]["evolves_to"][second_stage]["evolution_details"][0][min_requirement] > 0:
        print("\t\t\t" + min_requirement.replace("min_","").title() + " Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][0][min_requirement])
```

This only considers the very first evolution entry (index 0) for the numerical requirements nested within a specific entry (list) nested within the key-value pair of "evolution_details".

## The First Stage Function (After)

```python
# Used for the second stage of a Pokémon in its evolution chain to list off evolution requirements.
def evolutionRequirements(evolution_information, min_requirement, second_stage, entry_index=0):
    # If the evolution's minimum requirement exists (above 0),
    # it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolution_details"][entry_index][min_requirement] > 0:
        print("\t\t\t" + min_requirement.replace("min_", "").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolution_details"][entry_index][min_requirement])
```

Every time 0 was previously used to find the corresponding evolution entry when called, it uses the default entry_index parameter instead.

## Fixed prints with Eevee as the Pokémon

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
        Evolves Into: Leafeon | Requirement: Use-Item # Correct
            Item Requirement: Leaf Stone
        Evolves Into: Glaceon | Requirement: Use-Item # Correct
            Item Requirement: Ice Stone
        Evolves Into: Sylveon | Requirement: Level-Up
            Affection Requirement: 2
```

# Tools and Resources Used
* Python - The programming language used for the project.
* TechSmart - The primary IDE used when coding this project.
* PokéAPI v2 - The API this project was based around, including all of its documentation.
