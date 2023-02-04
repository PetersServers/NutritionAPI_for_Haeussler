import requests
from config import api_key
from config import *
import json
import warnings
from data_support import *

def _call_validate_data(food_name):
    #validates if all necessary data for food item
    #to be valid is present in the response
    response = call_api(food_name)
    price = validate_price(food_name)
    serving_size = validate_serving(response)
    return response, price, serving_size

def _normalize_data(food_dict, price):
    #
    food_dict = normalize_item_data(food_dict, price)
    food_dict = normalize_ensure_values(food_dict)
    food_dict = normalize_format_dict(food_dict)
    return food_dict

def manage_data(food_list):
    # main function of data management
    #makes the api call, and manages the locally saved data
    try:
        with open("nutrition_data.json", "r") as f:
            food_dict = json.load(f)
            print("some data not found locally".upper())
    # if file not found create new data dict
    except FileNotFoundError:
        food_dict = {}
    for food_name in food_list:
        if food_name not in food_dict:
            try:
                response, price, serving_size = _call_validate_data(food_name)
            except:
                delete_line_from_file(food_name)
                print(f'{food_name} is invalid, '
                      f'deprecated data is removed')
                continue

            food_dict[food_name] = {
                "nutrients": response["labelNutrients"],
                "servingSize": {"value": serving_size}}

            food_dict[food_name] = _normalize_data(food_dict[food_name], price)

    with open("nutrition_data.json", "w") as f:
        json.dump(food_dict, f, indent=4)

    # Return only the items in food_dict where the key is found in food_list
    return {key: value for key, value in food_dict.items() if key in food_list}



