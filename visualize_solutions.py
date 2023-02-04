import time
import matplotlib as plt
import json
from data_support import normalize_ensure_values
import matplotlib.pyplot as plt
import numpy as np
import datetime
import os


def calculate_optimum(food_amounts):
    with open("nutrition_data.json", "r") as f:
        food_dict = json.load(f)
    optimum_dict = {}
    for food, amount in food_amounts.items():
        optimum_dict[food] = {}
        food_data = food_dict[food]['nutrients']
        for nutrient, value in food_data.items():
            optimum_dict[food][nutrient] = value * amount

    return optimum_dict


def plot_nutrient_price(nutrient_parts, food_vars, vegan, cheap, man):
    plt.style.use('seaborn-darkgrid')
    color_style = "viridis_r"  # 'prism' auch nice

    # create dynamic titles
    classification_food = "vegan" if vegan else "non vegan"
    classification_gender = "man" if man else "woman"
    classification_prices = "cost minimization" if cheap else "protein maximization"

    # preprocess values
    nutrients = list(nutrient_parts.keys())
    nutrients = [i for i in nutrients if i != "price"]
    values = list(nutrient_parts.values())
    values.remove(values[len(values) - 1])
    food_items = [f for f in food_vars if food_vars[f].value() != None and float(food_vars[f].value()) > 0]
    food_values = [food_vars[f].value() for f in food_items]
    food_dict = dict(zip(food_items, food_values))
    nutrient_parts = calculate_optimum(food_dict)
    nutrient_parts = normalize_ensure_values(nutrient_parts)
    date_time = datetime.datetime.now()

    # nutrients optimum
    title = "Nutrient Composition optimum"
    fig, ax = plt.subplots()
    cmap = plt.get_cmap(f"{color_style}")
    bar_colors = [cmap(i / len(nutrients)) if nut != 'price' else 'r' for i, nut in enumerate(nutrients)]
    ax.bar(nutrients, values, color=bar_colors)
    ax.set_xticks(nutrients)
    ax.set_xticklabels(nutrients, rotation=30, ha='right')
    plt.suptitle(f"{title}")
    plt.title(f"Parameters: {classification_prices}, {classification_food}, "
              f"{classification_gender}", fontsize=10)
    ax.set_ylabel("Value")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()

    # optimum consumption food in 100g units
    title = "Optimum consumption in 100g"
    fig, ax = plt.subplots()
    cmap = plt.get_cmap(f"{color_style}")
    bar_colors = [cmap(i / len(food_items)) for i, food in enumerate(food_items)]
    ax.bar(food_items, food_values, color=bar_colors)
    plt.suptitle(f"{title}")
    plt.title(f"Parameters: {classification_prices}, {classification_food}, "
              f"{classification_gender}", fontsize=10)
    ax.set_xlabel('Food items')
    ax.set_ylabel('Values')
    plt.xticks(rotation=0)
    # plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()

    # price comparison
    title = "Optimum food expenses"
    cmap = plt.get_cmap(f"{color_style}")
    food_prices = [nutrient_parts[food]['price'] for food in nutrient_parts]
    food_names = list(nutrient_parts.keys())
    num_bars = len(food_prices)
    colors = cmap(np.linspace(0, 1, num_bars))
    plt.bar(food_names, food_prices, color=colors)
    plt.xlabel('Food Name')
    plt.ylabel('Price')
    plt.suptitle(f'{title}')
    plt.title(f"Parameters: {classification_prices}, {classification_food}, "
              f"{classification_gender}", fontsize=10)
    # plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()

    # nutrients comparison layered
    nutrient_parts = {
        food: {nutrient: value for nutrient, value in nutrients.items() if nutrient not in ['price', 'transFat']}
        for food, nutrients in nutrient_parts.items()}

    title = "Nutrients in optimum layered"
    cmap = plt.get_cmap(f"{color_style}")
    colors = [cmap(i / len(nutrient_parts)) for i, food in enumerate(nutrient_parts)]
    for i, (food, nutrients) in enumerate(nutrient_parts.items()):
        plt.bar(nutrients.keys(), nutrients.values(), color=colors[i], label=food)
        plt.legend()
    plt.suptitle(f"{title}")
    plt.title(f"Parameters: {classification_prices}, {classification_food}, "
              f"{classification_gender}", fontsize=10)
    plt.xticks(rotation=30, fontsize=8)
    # plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()


def print_store_solution(solution, foods, food_vars, save_to_desktop=False):

    print("optimal food suggestions".upper())
    for f in foods:
        if food_vars[f].value() != None and float(food_vars[f].value()) > 0:
            # print the optimum amount and store it in a dict for later calcuations
            print(f'{f} = {food_vars[f].value()}')
    print("-"*82)
    print("nutriotional analysis".upper())
    for key, val in solution.items():
        if key != "price" and key != "calories":
            if key in ["sodium", "fiber", "cholesterol", "calcium", "iron"]:
                print(f"the optimum comprises {round(val, 2)} mg of {key}")
                continue
            else:
                print(f"the optimum comprises {round(val, 2)} g of {key}")
        if key == "calories":
            print(f"the optimum comprises {round(val, 2)} {key}")
        if key == "price":
            print(82 * "-")
            print("COST ANALYSIS")
            print(f"optimum cost is {round(val, 2)}")

    if save_to_desktop:
        if os.name == 'nt':
            desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        else:
            desktop = os.path.expanduser("~/Desktop")
        filename = os.path.join(desktop, "shopping_list.txt")

        # open file and write the content to it
        with open(filename, "w") as file:
            # optimal consumption analysis
            file.write("-" * 82 + "\n")
            file.write("optimal food suggestions".upper() + "\n")
            for f in foods:
                if food_vars[f].value() != None and float(food_vars[f].value()) > 0:
                    # print the optimum amount and store it in a dict for later calcuations
                    file.write(f'{f} = {food_vars[f].value()}' + "\n")

            print("\n")
            print("shopping list has been stored locally as shopping_list.txt")

