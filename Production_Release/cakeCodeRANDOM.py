import requests
import http.client
import json
import random
import webbrowser

API_KEY = "8016f8c8famshb3db0bbb5863459p1c5631jsn2f4c8a9abce8"

# Function 1: Get list of cakes
def get_cake_list():
    url = "https://the-birthday-cake-db.p.rapidapi.com/"

    headers = {
        "x-rapidapi-host": "the-birthday-cake-db.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            cakes = response.json()
            return cakes
        else:
            print("Error: Could not get cake list.")
            return []

    except:
        print("Error: Something went wrong while getting the cake list.")
        return []

# Function 2: Get recipe details by cake ID
def get_recipe_details(recipe_id):
    conn = http.client.HTTPSConnection("the-birthday-cake-db.p.rapidapi.com")

    headers = {
        "x-rapidapi-host": "the-birthday-cake-db.p.rapidapi.com",
        "x-rapidapi-key": API_KEY
    }

    try:
        endpoint = "/" + str(recipe_id)
        conn.request("GET", endpoint, headers=headers)

        res = conn.getresponse()
        data = res.read()

        if res.status == 200:
            recipe = json.loads(data.decode("utf-8"))
            return recipe
        else:
            print("Error: Could not get recipe details.")
            return {}

    except:
        print("Error: Problem getting recipe details.")
        return {}

    finally:
        conn.close()

# Function 3: Display list of cakes
def display_cake_list(cakes):
    print("\nAvailable Cakes:")

    for i in range(len(cakes)):
        cake_name = cakes[i].get("title")
        print(str(i + 1) + ". " + cake_name)

    print("\nType a number to choose a cake.")
    print("Or type random to see a random cake's recipe.")
    

# Function 4: Let user choose a cake by ID or random
def get_user_choice(cakes):
    while True:
        user_input = input("\nEnter a number or type random or q to quit: ")
        if user_input.lower() == "q":
            print("Thank you for using our program!")
            return None
        
        if user_input.lower() == "random":
            random_cake = random.choice(cakes)
            print("\nRandom Cake Selected!")
            return random_cake
    
        try:
            choice = int(user_input)

            if 1 <= choice <= len(cakes):
                return cakes[choice - 1]
            
            else:
                print("Please choose a number from the list.")

        except:
            print("Invalid input. Please enter a number or type random.")


# Function 5: Display the recipe
def display_recipe(recipe):
    print("\nCake information:")
    
    cake_number = recipe.get("id")
    print("\nid:", cake_number)
    
    cake_name = recipe.get("title")
    print("\nSelected Cake:", cake_name)

    cake_difficulty = recipe.get("difficulty")
    print("\nDifficulty:", cake_difficulty)
    
    portion_size = recipe.get("portion")
    print("\nPortion:", portion_size)

    time_to_make = recipe.get("time")
    print("\nTime to make:", time_to_make)

    description = recipe.get("description")
    print("\nCake Description:", description)

    print("\nIngredients:")
    ingredients = recipe.get("ingredients")

    if type(ingredients) == list and len(ingredients) > 0:
        for item in ingredients:
            print("-", item)
    else:
        print("No ingredients available.")

    print("\nInstructions:")
    instructions = recipe.get("method") or recipe.get("instructions")

    if type(instructions) == list and len(instructions) > 0:
        for i in range(len(instructions)):
            print(str(i + 1) + ".", instructions[i])
    elif type(instructions) == str and instructions != "":
        print(instructions)
    else:
        print("No instructions available.")

    print("\nHappy baking! Hope you enjoy!")

# Function #6 User can get pull up image of cake if they wish
def open_cake_image(recipe):
    # Get the image URL from the recipe api
    image_url = recipe.get("image")

    if image_url:
        print("\nOpening cake image in your browser...")
        webbrowser.open(image_url)
    else:
        print("\nNo image available for this cake.")

# Main program
def main():
    print("Welcome to the Cake Recipe Program!")

    cakes = get_cake_list()

    if len(cakes) == 0:
        print("No cakes found. Program ending.")
        return

    display_cake_list(cakes)

    selected_cake = get_user_choice(cakes)
    
#If user quit
    if selected_cake is None:
        print("Program ended.")
        return

    # If recipe does not show 
    recipe_id = selected_cake.get("id")

    if recipe_id is None:
        print("Error: Could not find the recipe ID for that cake.")
        print("Cake data:", selected_cake)
        return

    recipe = get_recipe_details(recipe_id)

    if len(recipe) == 0:
        print("No recipe details were returned.")
        return

    display_recipe(recipe)


# Ask the user if they want to see the image. And to rerun the program or to quit

    while True:
        choice = input("\nWould you like to see a picture of this cake? (yes/no): ")

        if choice.lower() == "yes":
            open_cake_image(recipe)
            break
        elif choice.lower() =="no":
            print("Ok, no worries! Enjoy!")
            break
        else:
            print("Not a valid input. Please type yes or no")

    while True:
        choice = input("\nWould you like to view another cake recipe? (yes or no): ")
        if choice.lower() == "yes":
            main()
            break
        elif choice.lower() == "no":
            print("Thank you for using our program!")
            break
        else:
            print("Invalid input. Please type yes or no")

main()