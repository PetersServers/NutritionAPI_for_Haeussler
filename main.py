from data_management import *
from support_simplex import *
import random
from list_management import *

#write a pandas vis for result and use webdriver to analyze if food is vegan or not

#everything that is in json is evaluated, have to check why

class simplex:
    def __init__(self, man, nutritious, vegan):

        print("simplex is beeing initialized".upper())

        self.cheap = False if nutritious else True
        self.vegan = vegan
        self.man = man
        self.nutritious = nutritious

        self.foods = manage_lists(vegan=self.vegan)
        print(self.foods)
        self.data = manage_data(self.foods)

    def calculate(self):

        self.solution, self.food_vars = calculation(foods=self.data, cheap_mode=self.nutritious, man=self.man)

    def illustrate(self):
        plot_nutrient_price(self.solution, self.food_vars,
                            cheap=self.cheap, vegan=self.vegan,
                            man=self.man)

#set to vegan for testing
simplex = simplex(man=True, nutritious=False, vegan=True)
simplex.calculate()
simplex.illustrate()


