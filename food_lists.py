import pandas as pd
from support import *

foods = ["apple", "chicken", "salmon", "rice", "noodel", "couscous", "peas", "kebab", "broccoli", "kale"]
foods_vegan = ["apple", "pizza", "peas", "broccoli", "kale", "spinach", ]

def create_foods_list_available():
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

    with open('ingredients.txt', 'w') as file:
        for name in list_av_foods:
            file.write(name + '\n')