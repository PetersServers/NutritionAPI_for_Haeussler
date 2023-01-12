import pulp
import time


def calculation(foods, man):
    print("**SIMPLEX IS CALCULATING OPTIMUM**")
    # Create a LP Maximize problem
    lp_prob = pulp.LpProblem('Nutrition Problem', pulp.LpMaximize)
    # Create variables for the amount of each food to eat
    food_vars = {f: pulp.LpVariable(f.replace(" ", "_") + "_amount", lowBound=0, cat='Continuous') for f in foods}
    # Set objective function: Maximize protein
    lp_prob += sum(foods[f].get("protein", 0) * food_vars[f] for f in foods)
    # Constraints for healthy intake for a grown man:
    # - at least 56 grams of protein
    if any(foods[f].get("protein") for f in foods):
        lp_prob += sum(foods[f]["protein"] * food_vars[f] for f in foods) >= 56 if man else 30
    if any(foods[f].get("protein") for f in foods):
        lp_prob += sum(foods[f]["protein"] * food_vars[f] for f in foods) <= 150 if man else 130
    # - at most 30% of calories from fat
    if any(foods[f].get("fat") and foods[f].get("calories") for f in foods):
        lp_prob += sum(foods[f]["fat"] * food_vars[f] for f in foods) <= 0.3 * sum(foods[f]["calories"] * food_vars[f] for f in foods)
    if any(foods[f].get("fat") for f in foods):
        lp_prob += sum(foods[f]["fat"] * food_vars[f] for f in foods) >=0
    # - at most 300 mg of cholesterol
    if any(foods[f].get("cholesterol") for f in foods):
        lp_prob += sum(foods[f]["cholesterol"] * food_vars[f] for f in foods) <= 300 if man else 200
    if any(foods[f].get("cholesterol") for f in foods):
        lp_prob += sum(foods[f]["cholesterol"] * food_vars[f] for f in foods) >= 0
    # - at most 2,300 mg of sodium
    if any(foods[f].get("sodium") for f in foods):
        lp_prob += sum(foods[f]["sodium"] * food_vars[f] for f in foods) <= 23 if man else 20
    # - at least 20 grams of fiber
    if any(foods[f].get("fiber") for f in foods):
        lp_prob += sum(foods[f]["fiber"] * food_vars[f] for f in foods) >= 20 if man else 15
    # - at most 25 grams of sugar
    if any(foods[f].get("sugars") for f in foods):
        lp_prob += sum(foods[f]["sugars"] * food_vars[f] for f in foods) <= 25 if man else 10
    # - at least 1000 mg of calcium
    if any(foods[f].get("calcium") for f in foods):
        lp_prob += sum(foods[f]["calcium"] * food_vars[f] for f in foods) >= 10 if man else 7
    if any(foods[f].get("iron") for f in foods):
        lp_prob += sum(foods[f]["iron"] * food_vars[f] for f in foods) >= 8 if man else 6
    if any(foods[f].get("calories") for f in foods):
        lp_prob += sum(foods[f]["calories"] * food_vars[f] for f in foods) >= 2800 if man else 1800
    if any(foods[f].get("calories") for f in foods):
        lp_prob += sum(foods[f]["calories"] * food_vars[f] for f in foods) <= 3500 if man else 2000
    # Solve the optimization problem
    status = lp_prob.solve()

    print(f'Status: {pulp.LpStatus[status]}')

    #Analysis of optimum

    time.sleep(2)

    nutrients = {"protein": 0, "fat": 0, "cholesterol": 0, "sodium": 0, "fiber": 0, "sugars": 0, "calcium": 0,
                 "iron": 0, "calories": 0}
    for f in foods:

        if food_vars[f].value() != None:

            print(f'{f} = {food_vars[f].value()}')
            # Create a dictionary to store the total amounts of each nutrient

            nutrients["protein"] += foods[f]["protein"] * food_vars[f].varValue
            nutrients["fat"] += foods[f]["fat"] * food_vars[f].varValue
            nutrients["cholesterol"] += foods[f]["cholesterol"] * food_vars[f].varValue
            nutrients["sodium"] += foods[f]["sodium"] * food_vars[f].varValue
            nutrients["fiber"] += foods[f]["fiber"] * food_vars[f].varValue
            nutrients["sugars"] += foods[f]["sugars"] * food_vars[f].varValue
            nutrients["calcium"] += foods[f]["calcium"] * food_vars[f].varValue
            nutrients["iron"] += foods[f]["iron"] * food_vars[f].varValue
            nutrients["calories"] += foods[f]["calories"] * food_vars[f].varValue



    print("-"*82)

            # Print the total amounts of each nutrient
    for key, val in nutrients.items():

        print(f"the optimum comprises {val}g of {key}")

    print("-" * 82)
