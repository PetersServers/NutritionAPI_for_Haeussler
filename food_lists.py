import pandas as pd
from api_format import *
import random
from api_format import *
import warnings
from configurable_lists import *
from faker import Faker
import vegan
#support functions for the input of the simplex model.
#mainly works via lists

#all vegan foods from ingr.txt
foods_vegan = vegan.vegan_l

def call_stored_foods(vegan, num_items, random=False):
    #function that returns lists based on specifications
    if vegan:
        return foods_vegan
    elif type(num_items) == str and random:
        random = False
    elif num_items == "all":
        return load_all()
    elif random:
        return load_random_list(num_items)
    else:
        return choosen_foods


def get_prices(foods):
    prices = {}
    with open("ingr_price.txt", 'r') as file:
        for line in file:
            food, eur, cent = line.strip().split(',')
            price = eur + '.' + cent
            print(price)
            price = float(price)
            if food in foods:
                prices[food] = price
    return prices


def _create_foods_list_available(list_foods):
    #function that tests if certain foods in a list are available in api data
    list_av_foods = []
    for i in list_foods:
        i = str(i).lower()
        try:
            call_api_data([i])
            list_av_foods.append(i)
            print(f"{i} available")
        except:
            print(f"{i} not available")
            continue

    with open('ingr.txt', 'w') as file:
        for name in list_av_foods:
            file.write(name + '\n')

def _generate_food_list(num):
    #function that can be used to generate food list
    #to backtest it against api
    #to save data locally in json
    faker = Faker()
    # Create an empty list to store the food items
    food_items = []
    for _ in range(num):
        food_items.append(faker.food().ingredient())
    food_items = set(food_items)
    _create_foods_list_available(food_items)


def load_random_list(num_items):
    #function that returns a random list of
    #the foods that we have saved in the local
    #txt file
    with open('ingr.txt', 'r') as f:
        grocery_list = f.readlines()
    grocery_list = [item.strip() for item in grocery_list]
    random_list = random.sample(grocery_list, num_items)
    return random_list

def load_all():
    #crates a list of all food items
    with open('ingr.txt', 'r') as f:
        grocery_list = f.readlines()
    grocery_list = [item.strip() for item in grocery_list]
    return grocery_list

def store_txt_json_locally():
    #depracated code
    with open('ingr.txt', 'r') as f:
        grocery_list = f.readlines()
    grocery_list = [item.strip() for item in grocery_list]
    call_api_data(grocery_list)

