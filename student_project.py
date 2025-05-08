"""
Data Structures
Student Project
Project Title: Pokédex
"""

# -- Imports -- #
# Used to request information from APIs with an API call.
import requests


# -- Functions -- #
# Used for the second stage of a Pokémon in its evolution chain
# to list off evolution requirements.
def evolutionRequirements_S2(evolution_information, min_requirement, second_stage, entry_index=0):
    """

    Args:
        evolution_information (dict): JSON variable parsed from the API call and validation
        min_requirement (str): Type of requirement (i.e., "min_level", "min_happiness")
        second_stage (int): Index of a Pokémon's second evolution path
        entry_index (int): Index for a specific version of the Pokémon's entry (default is 0 for the first version)
    """

    # If the evolution's minimum requirement exists, (above 0)
    # it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolution_details"][entry_index][min_requirement] > 0:
        print("\t\t\t" + min_requirement.replace("min_", "").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolution_details"][entry_index][min_requirement])


# Used for the third stage of a Pokémon in its evolution chain
# to list off evolution requirements.
def evolutionRequirements_S3(evolution_information, min_requirement, second_stage, third_stage, entry_index=0):
    """

    Args:
        evolution_information (dict): JSON variable parsed from the API call and validation
        min_requirement (str): Type of requirement (i.e., "min_level", "min_happiness")
        second_stage (int): Index of a Pokémon's second evolution path
        third_stage (int): Index of a Pokémon's third evolution path
        entry_index (int): Index for a specific version of the Pokémon's entry (default is 0 for the first version)
    """

    # If the evolution's minimum requirement exists, it will print it as the minimum requirement.
    if evolution_information["chain"]["evolves_to"][second_stage]["evolves_to"][third_stage]["evolution_details"][entry_index][min_requirement] > 0:
        print("\t\t\t\t" + min_requirement.replace("min_", "").title() + " Requirement:", evolution_information["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][entry_index][min_requirement])


# -- Variables -- #
# The base url for accessing PokéAPI v2.
URL = "https://pokeapi.co/api/v2/"

# The path for accessing info about a Pokémon's species entries.
SPECIES_PATH = "pokemon-species/"

# The possible entry types that can be chosen by a user.
ENTRY_TYPES = (
    "new",
    "old"
)

# The possible requirements for an evolution when calling an evolution chain function.
MIN_REQUIREMENTS = (
    "min_level",
    "min_happiness",
    "min_beauty",
    "min_affection"
)

# Acts as a whitelist to not ignore Pokémon with
# symbols/digits in their alphabetical name.
# Names are tweaked to comply with URL conventions (no spaces, apostrophes, etc.).
POKEMON_WHITELIST = (
    "nidoran-m",
    "nidoran-f",
    "mr-rime",
    "porygon2",
    "ho-oh",
    "mime-jr",
    "porygon-z",
    "jangmo-o",
    "hakamo-o",
    "kommo-o",
    "tapu-koko",
    "tapu-lele",
    "tapu-bulu",
    "tapu-fini",
    "mr-mime",
)

# Parameters for each request.
poke_params = {}

# Acts as a placeholder for choosing different entry types.
entry_type = "NONE"

# -- Introduction -- #
# Will only run at the start if the user just started the program.
# Asks for "new" or "old" as one of the user's inputs.
while entry_type.lower() not in ENTRY_TYPES:
    entry_type = input("Type \"NEW\" for newer entries, \"OLD\" for older entries: ")

if entry_type.lower() == "new":
    relevant_index = -1
else:
    relevant_index = 0

# Makes end an empty string to combine itself with the first user input.
print("\nWelcome to my Capstone Project. Type \"EXIT\" to quit. ", end="")

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
        if pokemon_name.isalpha() or pokemon_name.isdigit() or pokemon_name.lower() in POKEMON_WHITELIST:
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
            pokemon_name = input("No Pokémon exists with that set of letters and symbols/digits. ")

    # Skips displaying info if the user input is "EXIT".
    if pokemon_name != "EXIT":
        # -- Requested Info -- #
        # Displays the Pokédex Number, Pokémon Name, Pokéball Success Rate, Flavor Text Entry, and it's Evolution Chain.
        print("\nPokédex Number:", body["id"])
        print("Pokémon Name:", body["name"].title())
        print("Pokéball Success Rate (Maximum is 255):", body["capture_rate"])

        # The index uses 'relevant_index' to match the user's data preference.
        print("\nFlavor Text Entry:\n" + body["flavor_text_entries"][relevant_index]["flavor_text"])

        # Requests more info about the Pokémon's evolutions from its
        # evolution chain url provided in the species entries.
        evolution_chain_url = body["evolution_chain"]["url"]
        evolution_request = requests.get(evolution_chain_url, params=poke_params)
        evolution_body = evolution_request.json()

        # Prints out its entire evolution chain. (Interesting results for "Eevee" as the Pokémon)
        print("\nEvolution Chain")

        # -- Stage One -- #
        # Prints out the Pokémon's first evolutionary stage.
        print("\tStarts From:", evolution_body["chain"]["species"]["name"].title())

        # -- Stage Two -- #
        # Prints out each path for the Pokémon's second evolutionary stage (i for each evolution path).
        # Uses len to know how many evolutionary paths there are for that Pokémon in stage two.
        # Adds the requirement for the Pokémon to evolve into each path such as a level up or an item.
        for i in range(len(evolution_body["chain"]["evolves_to"])):
            # Following prints use 'relevant_index' to match the user's data preference
            # where it would have to specify the version of each entry to use.

            # Prints the evolution name and the general requirement to evolve.
            print("\t\tEvolves Into:", evolution_body["chain"]["evolves_to"][i]["species"]["name"].title(), "| Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][relevant_index]["trigger"]["name"].title())

            # Prepares to handle an exception if no item requirement exists.
            try:
                # Print will cause an exception unless there is an item requirement in the nested containers.
                print("\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolution_details"][relevant_index]["item"]["name"].title().replace("-", " "))

            except:
                # The exception is handled by ignoring it.
                pass

            # Checks all number-based requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
            for min_requirement in MIN_REQUIREMENTS:
                # The fourth argument uses 'relevant_index' to match the user's data preference.
                evolutionRequirements_S2(evolution_body, min_requirement, i, relevant_index)

            # -- Stage Three -- #
            # Prints out each path for the Pokémon's third evolutionary stage (j for each evolution path).
            # Uses len to know how many evolutionary paths there are for that Pokémon in stage three.
            # Adds the requirement for the Pokémon to evolve into each path such as a level up or an item.
            for j in range(len(evolution_body["chain"]["evolves_to"][i]["evolves_to"])):
                # Following prints use 'relevant_index' to match the user's data preference
                # where it would have to specify the version of each entry to use.

                # Prints the evolution name and the general requirement to evolve.
                print("\t\t\tEvolves Into:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["species"]["name"].title(), "| Requirement:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][relevant_index]["trigger"]["name"].title())

                # Prepares to handle an exception if no item requirement exists.
                try:
                    # Print will cause an exception unless there is an item requirement in the nested containers.
                    print("\t\t\t\tItem Requirement:", evolution_body["chain"]["evolves_to"][i]["evolves_to"][j]["evolution_details"][relevant_index]["item"]["name"].title().replace("-", " "))

                except:
                    # The exception is handled by ignoring it.
                    pass

                # Checks all numerical requirements in 'MIN_REQUIREMENTS' for a Pokémon, then displays each.
                for min_requirement in MIN_REQUIREMENTS:
                    # The fifth argument uses 'relevant_index' to match the user's data preference.
                    evolutionRequirements_S3(evolution_body, min_requirement, i, j, relevant_index)

        print()

    # Breaks out of the main loop if the user's input is "EXIT".
    else:
        break
