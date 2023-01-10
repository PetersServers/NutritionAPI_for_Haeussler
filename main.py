import requests
from config import api_key


def get_response(food_name):
    url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={api_key}&query={food_name}"
    response = requests.get(url)
    # Get the food ID from the API response
    food_data = response.json()
    food_id = food_data['foods'][0]['fdcId']
    # Make an API request to get the nutrient data for the food
    url = f"https://api.nal.usda.gov/fdc/v1/{food_id}?api_key={api_key}"
    response = requests.get(url)
    nutrient_data = response.json()
    return nutrient_data


def print_nutrient_data(nutrient_data, food_name):
    for key, value in nutrient_data.items():
        if key == "labelNutrients":
            dict = value
            print(food_name.upper)
            for key, val in dict.items():

                print(key, val)


food_name = "pizza"

nutrient_data = get_response(food_name)
print_nutrient_data(nutrient_data, food_name)

