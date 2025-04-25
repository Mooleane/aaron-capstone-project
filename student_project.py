"""
Data Structures
Student Project
Project Title: Pokédex
"""

# -- Imports -- #
# Used for requesting information from API's with an API call.
import requests


# -- Functions -- #
# Used for the second stage of a Pokémon in its evolution chain
# to list off evolution requirements.
def evolutionRequirements(evolution_information, min_requirement, second_stage, entry_index=0):
    # If the evolution's minimum requirement exists, (above 0)
    # it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolution_details"][entry_index][min_requirement] > 0:
        print("\t\t\t" + min_requirement.replace("min_", "").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolution_details"][entry_index][min_requirement])


# Used for the third stage of a Pokémon in its evolution chain
# to list off evolution requirements.
def evolutionRequirements2(evolution_information, min_requirement, second_stage, third_stage, entry_index=0):
    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolves_to"][third_stage]["evolution_details"][entry_index][min_requirement] > 0:
        print("\t\t\t\t" + min_requirement.replace("min_", "").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][entry_index][min_requirement])


# -- Variables -- #
# The base url for accessing PokéAPI v2.
URL = "https://pokeapi.co/api/v2/"

# The path for accessing info about a Pokémon's species entries.
SPECIES_PATH = "pokemon-species/"

# The possible requirements for an evolution when calling an evolution chain function.
MIN_REQUIREMENTS = ("min_level", "min_happiness", "min_beauty", "min_affection")

# Parameters for each request.
poke_params = {}

# -- Introduction -- #
# Will only run at the start if the user just started the program.
# Makes end an empty string to combine itself with the first user input.
print("Welcome to the Pokédex. Type \"EXIT\" to quit. ", end="")

# -- Main Loop -- #
# Will keep running until the user types "EXIT" to break the loop.
while True:
    # -- User Input -- #
    pokemon_name = input("Please enter a Pokémon's Name or Pokédex Number: ")

    # -- User Input Verification -- #
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

    # Skips displaying info if the user input is "EXIT".
    if pokemon_name != "EXIT":
        # -- Requested Info -- #
        # Displays the Pokédex Number, Pokémon Name, Type, Pokéball Success Rate, Flavor Text Entry, and it's Evolution Chain.
        print("\nPokédex Number:", body["id"])
        print("Pokémon Name:", body["name"].title())
        print("Pokéball Success Rate (Maximum is 255):", body["capture_rate"])

        print("\nFlavor Text Entry:", body["flavor_text_entries"][0]["flavor_text"].replace("\n", " "))

        # Requests more info about the Pokémon evolution from its
        # evolution chain url provided in the species entries.
        evolution_chain_url = body["evolution_chain"]["url"]
        evolution_request = requests.get(evolution_chain_url, params=poke_params)
        evolution_body = evolution_request.json()

        # Prints out its entire evolution chain. (Interesting results for "Eevee" as the Pokémon)
        print("\nEvolution Chain")

        # Prints out the Pokémon's first evolutionary stage.
        print("\tStarts From:", evolution_body["chain"]["species"]["name"].title())

        # Prints out each path for the Pokémon's second evolutionary stage (i for each evolution path).
        # Uses len to know how many evolutionary paths there are for that Pokémon in stage two.
        # Adds the requirement for the Pokémon to evolve into each path such as a level up or an item.
        for i in range(len(evolution_body["chain"]["evolves_to"])):
            # Loops through each evolution entry for that Pokémon in search of an
            # "item" key with an existing "name" key and value that contains the item requirement.
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

            # Prints out each path for the Pokémon's third evolutionary stage (j for each evolution path).
            # Uses len to know how many evolutionary paths there are for that Pokémon in stage three.
            # Adds the requirement for the Pokémon to evolve into each path such as a level up or an item.
            for j in range(len(evolution_body["chain"]["evolves_to"][i]["evolves_to"])):
                # Loops through each evolution entry for that Pokémon in search of an
                # "item" key with an existing "name" key and value that contains the item requirement.
                for z in range(len(evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"])):
                    # Tries validating itself with an if statement to see if it runs into an error/no item or contains the item.
                    try:
                        if evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][z]["item"]["name"]:
                            # This variable refers to the first most relevant evolution entry from PokéAPI v2 that contains an item requirement
                            item_entry_index = z
                            # These two prints are based off the same entry with the item requirement.
                            print("\t\tEvolves Into:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["species"]["name"].title(), "| Requirement:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][item_entry_index]["trigger"]["name"].title())
                            print("\t\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][item_entry_index]["item"]["name"].title().replace("-", " "))

                            # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
                            for min_requirement in MIN_REQUIREMENTS:
                                # The optional fifth argument which determines the entry being displayed
                                # is replaced with the same entry with the item requirement.
                                evolutionRequirements(evolution_body, min_requirement, i, j, item_entry_index)

                            # Breaks since it does need to print more about the evolution name, requirement type, and requirements.
                            break

                    except:
                        # Skips changing or displaying any unnecessary info.
                        pass

                # This runs when it evaluates there is no item requirements at all.
                else:
                    # This version of the print uses its first evolution entry from PokéAPI v2.
                    print("\t\t\tEvolves Into:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["species"]["name"].title(), "| Requirement:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][0]["trigger"]["name"].title())

                    # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
                    for min_requirement in MIN_REQUIREMENTS:
                        evolutionRequirements(evolution_body, min_requirement, i, j)

        print()

    # Breaks out of the main loop if the user's input is "EXIT".
    else:
        break
