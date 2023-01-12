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
        print(self.nutrition)
        self.optimized_food = calculation(self.nutrition, man)

    def calculate(self):
        return self.optimized_food

    def recalculate(self):
        print("simplex model initialized".upper())
        self.foods = random.shuffle(self.foods)
        self.optimized_food = self.optimized_food = \
            calculation(self.nutrition, self.man)
        return self.optimized_food


#simplex = simplex(man=True, vegan=False, random=True, num=200)
#simplex.calculate()




