from support_simplex import *
from list_management import *

#add suptitle and title to the remaining 2 graphs

class simplex:
    def __init__(self, man, nutritious, vegan):

        print("simplex is beeing initialized".upper())

        self.cheap = False if nutritious else True
        self.vegan = vegan
        self.man = man
        self.nutritious = nutritious

        self.foods = manage_lists(vegan=self.vegan)
        self.data = manage_data(self.foods)

    def calculate(self):
        self.solution, self.food_vars = calculation(foods=self.data, cheap_mode=self.nutritious, man=self.man)

    def illustrate(self):
        plot_nutrient_price(self.solution, self.food_vars,
                            cheap=self.cheap, vegan=self.vegan,
                            man=self.man)


def calcuate_every_option():
    for man in [True, False]:
        for nutritious in [True, False]:
            for vegan in [True, False]:
                simplex_ = simplex(man=man, nutritious=nutritious, vegan=vegan)
                simplex_.calculate()
                simplex_.illustrate()

calcuate_every_option()

