import pandas as pd
from api_format import *
import random
from api_format import *
import warnings

#support functions for the input of the simplex model.
#mainly works via lists

choosen_foods = ["apple", "chicken", "salmon", "rice", "noodel", "couscous", "peas", "kebab", "broccoli", "kale"]
foods_vegan = ["apple", "pizza", "peas", "broccoli", "kale", "spinach" ]

def call_stored_foods(vegan, num_items, random=False):
    if vegan:
        return foods_vegan
    if random:
        warnings.warn("script is running in random mode")
        radom_list = load_random_list(num_items)
        #print(f"the random list comprises: \n{radom_list}")
        return radom_list
    else:
        return choosen_foods


def create_foods_list_available():
    #this is a function that tries calles based on a csv file and
    # stores the calls if successfull
    list_foods = pd.read_csv("/Users/peterpichler/Downloads/ingredients.csv")
    list_foods = [i for i in list_foods["Category"]]
    list_foods = set(list_foods)
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

def load_random_list(num_items):
    with open('ingr.txt', 'r') as f:
        grocery_list = f.readlines()
    grocery_list = [item.strip() for item in grocery_list]
    random_list = random.sample(grocery_list, num_items)
    return random_list


def save_all_data_locally():
    with open('ingr.txt', 'r') as f:
        grocery_list = f.readlines()
    grocery_list = [item.strip() for item in grocery_list]
    call_api_data(grocery_list)

