import pulp
import time
import matplotlib as plt
import json
from data_support import normalize_ensure_values
import matplotlib.pyplot as plt
import numpy as np
import datetime

#remove price and create price graph for all values in the optimum (already datenbasis bc calculate optimum)
#make existant graphs more fancy



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
    color_style = "viridis_r" #'prism' auch nice

    #create dynamic titles
    classification_food = "vegan" if vegan else "non vegan"
    classification_gender = "man" if man else "woman"
    classification_prices = "cost minimization" if cheap else "protein maximization"

    #preprocess values
    nutrients = list(nutrient_parts.keys())
    nutrients = [i for i in nutrients if i != "price"]
    values = list(nutrient_parts.values())
    values.remove(values[len(values)-1])
    food_items = [f for f in food_vars if food_vars[f].value() != None and float(food_vars[f].value()) > 0]
    food_values = [food_vars[f].value() for f in food_items]
    food_dict = dict(zip(food_items, food_values))
    nutrient_parts = calculate_optimum(food_dict)
    nutrient_parts = normalize_ensure_values(nutrient_parts)
    date_time = datetime.datetime.now()


    #nutrients optimum
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
    #plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()

    #optimum consumption food in 100g units
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
    #plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()


    #price comparison
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
    #plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()

    #nutrients comparison layered
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
    #plt.savefig(f"/Users/peterpichler/Desktop/pics_simplex/{title} - {date_time}.png")
    plt.show()


def print_solutions(solution):
    # use food vars to finalize print functtion

    print(82 * "-")
    print("Nutrition Analysis".upper())
    for key, val in solution.items():

        if key != "price":


            if key in ["sodium", "fiber", "cholesterol", "calcium", "iron"]:
                print(f"the optimum comprises {round(val, 2)} mg of {key}")
                continue
            print(f"the optimum comprises {round(val, 2)} g of {key}")

        else:
            print(82 * "-")
            print(f"optimum cost is {round(val, 2)}")

def calculation(foods, man, cheap_mode):

    # Create a LP Problem
    lp_prob = pulp.LpProblem('Food Optimization Problem', pulp.LpMinimize if not cheap_mode else pulp.LpMaximize)
    # Create variables for the amount of each food to eat
    food_vars = {f: pulp.LpVariable(f.replace(" ", "_") + "_amount", lowBound=0, cat='Integer') for f in foods}

    lp_prob += sum(food_vars[f] for f in foods) == 10 #not working

    # Set objective function: Minimize cost or Maximize protein
    lp_prob += (sum(foods[f]['nutrients']['price'] * food_vars[f] for f in foods) if not cheap_mode
                else sum(foods[f]['nutrients'].get("protein", 0) * food_vars[f] for f in foods))
    # Constraints for healthy intake for a grown man:
    # - at least 50 grams of protein
    if any(foods[f]['nutrients'].get("protein") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["protein"] * food_vars[f] for f in foods) >= 50
    # - maximum amount of fat 78
    if any(foods[f]['nutrients'].get("fat") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["fat"] * food_vars[f] for f in foods) <= 78
    # - at most 300 mg of cholesterol
    if any(foods[f]['nutrients'].get("cholesterol") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["cholesterol"] * food_vars[f] for f in foods) <= 300
    # - at most 2,300 mg of sodium
    if any(foods[f]['nutrients'].get("sodium") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["sodium"] * food_vars[f] for f in foods) <= 2300
    # - at least 28 grams of fiber
    if any(foods[f]['nutrients'].get("fiber") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["fiber"] * food_vars[f] for f in foods) >= 28
    # - at most 50 grams of sugar
    if any(foods[f]['nutrients'].get("sugars") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["sugars"] * food_vars[f] for f in foods) <= 50
    # - at least 1300 mg of calcium
    if any(foods[f]['nutrients'].get("calcium") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["calcium"] * food_vars[f] for f in foods) >= 1300
    if any(foods[f]['nutrients'].get("iron") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["iron"] * food_vars[f] for f in foods) >= 18 if man else 27
    if any(foods[f]['nutrients'].get("calories") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["calories"] * food_vars[f] for f in foods) <= 2000
    if any(foods[f]['nutrients'].get("calories") for f in foods):
        lp_prob += sum(foods[f]['nutrients']["calories"] * food_vars[f] for f in foods) >= 1800
    # Solve the optimization problem
    status = lp_prob.solve()

    #print(f'Status: {pulp.LpStatus[status]}')

    print("-" * 82)
    print("optimal food suggestions".upper())

    solution = {"protein": 0, "fat": 0, "cholesterol": 0, "sodium": 0, "fiber": 0, "sugars": 0, "calcium": 0,
                 "iron": 0, "calories": 0, "price": 0}

    for f in foods:

        if food_vars[f].value() != None and float(food_vars[f].value()) > 0:

            #print the optimum amount and store it in a dict for later calcuations
            print(f'{f} = {food_vars[f].value()}')

            # Create a dictionary to store the total amounts of each nutrient
            solution["protein"] += foods[f]['nutrients']["protein"] * food_vars[f].varValue
            solution["fat"] += foods[f]['nutrients']["fat"] * food_vars[f].varValue
            solution["cholesterol"] += foods[f]['nutrients']["cholesterol"] * food_vars[f].varValue
            solution["sodium"] += foods[f]['nutrients']["sodium"] * food_vars[f].varValue
            solution["fiber"] += foods[f]['nutrients']["fiber"] * food_vars[f].varValue
            solution["sugars"] += foods[f]['nutrients']["sugars"] * food_vars[f].varValue
            solution["calcium"] += foods[f]['nutrients']["calcium"] * food_vars[f].varValue
            solution["iron"] += foods[f]['nutrients']["iron"] * food_vars[f].varValue
            solution["calories"] += foods[f]['nutrients']["calories"] * food_vars[f].varValue
            solution["price"] += foods[f]['nutrients']['price'] * food_vars[f].varValue

    print_solutions(solution)



    return solution, food_vars
