import requests
from config import api_key
from config import *
import json

#api, local storage and formatting of response

def ensure_values(original_dict):
    for food in original_dict:
        for key in desired_keys:
            if key not in original_dict[food]:
                original_dict[food].update({key: 0})
    return original_dict

def call_api_data(food_list):
    try:
        with open("nutrition_data_formatted.json", "r") as f:
            original_dict = json.load(f)
            print("some data not found locally".upper())
    except FileNotFoundError:
        original_dict = {}
    for food_name in food_list:
        print(f"Searching for local data for: {food_name}".upper())
        if food_name not in original_dict:
            print(f"{food_name.upper()} data is fetched and compressed: ", end=" ")
            url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={api_key}&query={food_name}"
            response = requests.get(url)
            print("**", end = "")
            # Get the food ID from the API response
            food_data = response.json()
            food_id = food_data['foods'][0]['fdcId']
            # Make an API request to get the nutrient data for the food
            url = f"https://api.nal.usda.gov/fdc/v1/{food_id}?api_key={api_key}"
            response = requests.get(url)
            print(url)
            print("**")
            original_dict[food_name] = response.json()["labelNutrients"]
            # add the serving size to the dictionary
            try:
                serv = response.json()["servingSize"]
                original_dict[food_name]["servingSize"] = serv
                print(original_dict[food_name])
            except:
                continue
        #check if serving size is included change values  not
        if 'servingSize' not in original_dict[food_name]:
            url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={api_key}&query={food_name}"
            response = requests.get(url)

            # Get the food ID from the API response
            food_data = response.json()
            food_id = food_data['foods'][0]['fdcId']
            url = f"https://api.nal.usda.gov/fdc/v1/{food_id}?api_key={api_key}"
            response = requests.get(url)
            try:
                serv = response.json()["servingSize"]
                #add the serving size to the dictionary
                original_dict[food_name]["servingSize"] = serv
            except:
                continue



    # Save the response to the local json file
    with open("nutrition_data_formatted.json", "w") as f:
        json.dump(original_dict, f, indent=4) #indent the json file to make it more readable
    #normalizes the nutritional values to per 100g
    original_dict = {food: original_dict[food] for food in original_dict if food in food_list}
    new_dict = {food: {nutrient: original_dict[food].get(nutrient, {}).get("value", None) / original_dict[food].get("servingSize") * 100 for nutrient in original_dict[food] if nutrient != 'servingSize'} for food in original_dict}
    return ensure_values(new_dict)


#######################################################################################################################
#old code just for testing

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





