from config import *
import requests


'''data normalization functions'''


def normalize_ensure_values(food_data):
    #ensures that all values that the simplex operaion needs is present
    for food in food_data:
        food_data[food] = {key: value for key, value in food_data[food].items() if key in desired_keys}
        for key in desired_keys:
            if key not in food_data[food]:
                food_data[food].update({key: 0})
    return food_data

def normalize_item_data(food_data, price_per_size):
    # calculate values for 100g + add price per 100g
    factor = 100 / food_data["servingSize"]["value"]
    for key, value in food_data['nutrients'].items():
        if key not in ['price', 'servingSize']:
            food_data['nutrients'][key]['value'] *= factor
    food_data.pop("servingSize")
    food_data["nutrients"]["price"] = {'value': price_per_size}
    return food_data

def normalize_format_dict(dictionary):
    #reformats the dictioary to match the needed format for the simplex
    new_dict = {}
    for key, value in dictionary.items():
        if isinstance(value, dict):
            if 'value' in value:
                new_dict[key] = value['value']
            else:
                new_dict[key] = normalize_format_dict(value)
        else:
            new_dict[key] = value
    return new_dict

'''call data and check if crucial data is present'''

def validate_serving(response):
    #validates the serving
    return response["servingSize"]

def validate_price(food_item):
    #validates the price
    with open("configurable_file.txt", "r") as f:
        for line in f:
            item, price = line.strip().split(',')
            if item == food_item:
                return float(price)
        raise ValueError(" price not stored")


def _delete_line(text, item_to_delete):
    # deletes lines from config file that can not be used for analysis
    lines = text.split("\n")
    new_lines = [line for line in lines if not line.startswith(item_to_delete + ",")]
    return "\n".join(new_lines)

def delete_line_from_file(item_to_delete):
    #deletes lines from config file that can not be used for analysis
    with open("configurable_file.txt", "r") as file:
        text = file.read()
    new_text = _delete_line(text, item_to_delete)
    with open("configurable_file.txt", "w") as file:
        file.write(new_text)


def call_api(food_name):
    #calls the food data from udsa
    print(f"{food_name.upper()} data is fetched and compressed: ", end=" ")
    url = f"https://api.nal.usda.gov/fdc/v1/search?api_key={api_key}&query={food_name}"
    response = requests.get(url)
    print("**", end="")
    # Get the food ID from the API response
    food_data = response.json()
    food_id = food_data['foods'][0]['fdcId']
    url = f"https://api.nal.usda.gov/fdc/v1/{food_id}?api_key={api_key}"
    response = requests.get(url)
    print("**")
    return response.json()


