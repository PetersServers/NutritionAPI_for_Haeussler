from support import *
from support_simplex import *
import random

class simplex:
    def __init__(self, man, vegan):
        print("simplex is beeing initialized".upper())
        self.man = man
        self.vegan = vegan
        self.foods = call_stored_foods(vegan=vegan)
        self.nutrition = get_food_list_values(self.foods)
        self.optimized_food = calculation(self.nutrition, man)


    def calculate(self):
        return self.optimized_food

    def recalculate(self):
        print("simplex model initialized".upper())
        self.foods = random.shuffle(self.foods)
        self.optimized_food = self.optimized_food = \
            calculation(self.nutrition, self.man)
        return self.optimized_food

create_foods_list_available()
exit()
simplex = simplex(man=True, vegan=True)
optimal_diet = simplex.calculate()
print_values(optimal_diet)
optimal_diet = simplex.recalculate()
print_values(optimal_diet)




