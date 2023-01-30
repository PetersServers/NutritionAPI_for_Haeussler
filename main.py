from api_format import *
from support_simplex import *
import random
from food_lists import *

class simplex:
    def __init__(self, man, vegan, random, num):
        print("simplex is beeing initialized".upper())
        self.man = man
        self.vegan = vegan
        self.foods = call_stored_foods(vegan=vegan, random=random,
                                       num_items=num)
        self.nutrition = call_api_data(self.foods)
        self.prices = get_prices(self.foods)
        self.optimized_food, self.cost = calculation(self.nutrition, self.prices, man)
        #test if price of food is available locally
        for food in self.foods:
            if food not in self.prices:
                raise ValueError(f"price of food {food} not stored locally")

    def calculate(self):
        return self.optimized_food

    def recalculate(self):
        print("simplex model initialized".upper())
        self.foods = random.shuffle(self.foods)
        self.optimized_food = self.optimized_food = \
            calculation(self.nutrition, self.man)
        return self.optimized_food

    def __sub__(self, other):
        self.difference = calculate_calculate_diff\
            (self.optimized_food, self.cost,other.optimized_food, other.cost)
        return self.difference

#set to vegan for testing
simplex = simplex(man=True, vegan=True, random=False, num=100)
simplex.calculate()


