import pulp
import time
import matplotlib as plt
import json



import matplotlib.pyplot as plt


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

    nutrients = list(nutrient_parts.keys())
    values = list(nutrient_parts.values())
    food_items = [f for f in food_vars if food_vars[f].value() != None and float(food_vars[f].value()) > 0]
    food_values = [food_vars[f].value() for f in food_items]
    food_dict = dict(zip(food_items, food_values))
    nutrient_parts = calculate_optimum(food_dict)

    print(nutrient_parts)

    exit()

    #optimum nutrients
    fig, ax = plt.subplots()
    bar_colors = ['b' if nut != 'price' else 'r' for nut in nutrients]
    ax.bar(nutrients, values, color=bar_colors)
    ax.set_xticks(nutrients)
    ax.set_xticklabels(nutrients, rotation=30, ha='right')
    ax.set_title(f"Nutrient Composition and Price | cheap = {cheap} | vegan = {vegan} | man = {man}")
    ax.set_ylabel("Value")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.show()

    #optimum consume

    fig, ax = plt.subplots()
    ax.set_title(f"Optimum consumption | cheap = {cheap} | vegan = {vegan} | man = {man}")
    ax.bar(food_items, food_values)
    ax.set_xlabel('Food items')
    ax.set_ylabel('Values')
    plt.xticks(rotation=0)
    plt.show()




def print_solutions(solution):
    # use food vars to finalize print functtion

    print(82 * "-")
    print("Nutrition Analysis".upper())
    for key, val in solution.items():

        if key != "price":

            print(f"the optimum comprises {val}g of {key}")

        if key == "price":

            print(82 * "-")
            print(f"optimum cost is {val}")

def calculation(foods, man,  cheap_mode):

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
