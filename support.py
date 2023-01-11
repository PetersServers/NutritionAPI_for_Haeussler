import requests
from config import api_key
from config import *


def get_all_foods():
    pass
    query = "*"
    page_size = "50"
    page_number = "1"
    url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={api_key}&query={query}&pageSize={page_size}&pageNumber={page_number}"
    response = requests.get(url)
    data = response.json()
    print(data)


def get_response(food_name):
    pass
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


def get_food_values(nutrient_data, food_name):
    pass
    food_dict = {}
    for key, value in nutrient_data.items():
        if key == "labelNutrients":
            dict = value
            #print(food_name.upper)
            for _ in dict.items():
                food_dict[f"{food_name}"] = dict.items()
                return food_dict

#######################################################################################################################

def format_dict(original_dict):
    for food in original_dict:
        print(f"preprocessing data for {food}".upper())
        for key in desired_keys:
            if key not in original_dict[food]:
                original_dict[food].update({key: 0})
    return original_dict


def get_food_list_values(food_list):
    original_dict = {}
    for food_name in food_list:
        url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={api_key}&query={food_name}"
        response = requests.get(url)
        # Get the food ID from the API response
        food_data = response.json()
        food_id = food_data['foods'][0]['fdcId']
        # Make an API request to get the nutrient data for the food
        url = f"https://api.nal.usda.gov/fdc/v1/{food_id}?api_key={api_key}"
        response = requests.get(url)
        original_dict[food_name] = response.json()["labelNutrients"]
        new_dict = {food: {nutrient: original_dict[food].get(nutrient, {}).get("value", None) for nutrient in
                           original_dict[food]} for food in original_dict}
    return format_dict(new_dict)



