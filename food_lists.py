import pandas as pd
from support import *
import random


choosen_foods = ["apple", "chicken", "salmon", "rice", "noodel", "couscous", "peas", "kebab", "broccoli", "kale"]
foods_vegan = ["apple", "pizza", "peas", "broccoli", "kale", "spinach" ]


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
            get_food_list_values([i])
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

