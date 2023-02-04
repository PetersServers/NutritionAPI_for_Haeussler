import pulp


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



    solution = {"protein": 0, "fat": 0, "cholesterol": 0, "sodium": 0, "fiber": 0, "sugars": 0, "calcium": 0,
                 "iron": 0, "calories": 0, "price": 0}

    for f in foods:

        if food_vars[f].value() != None and float(food_vars[f].value()) > 0:

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



    print("\n"*100)


    print("simplex calcuation finished".upper())

    print("-"*82)

    return solution, foods, food_vars
