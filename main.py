from support_simplex import *
from list_management import *
from visualize_solutions import *

#Dear Mr Häusler, we invite you, to input some food like f.e. with the estimated price per 100g
#to the configurable txt file, and let our program suggest you if you should consume it.
#you can also delete all the foods, and add your own shopping list in the format like it is in the config file
#the food suggester will then tell you what, and how much to buy, and what your expenses are

#furthermore the program will automatically store a shopping list to your desktop, if you wish

class food_suggester:
    def __init__(self, man, nutritious, vegan, save_to_desktop):

        print("simplex is beeing initialized".upper())

        self.cheap = False if nutritious else True
        self.vegan = vegan
        self.man = man
        self.nutritious = nutritious
        self.save_to_d = save_to_desktop

        self.foods = manage_lists(vegan=self.vegan)
        self.data = manage_data(self.foods)

    def calculate(self):
        self.solution, self.foods, self.food_vars = calculation(foods=self.data, cheap_mode=self.nutritious, man=self.man)

    def illustrate(self):
        print_store_solution(self.solution, self.foods, self.food_vars,
                             self.save_to_d)

        plot_nutrient_price(self.solution, self.food_vars,
                            cheap=self.cheap, vegan=self.vegan,
                            man=self.man)

def calcuate_every_option():
    #function to calculate every possible combination
    for man in [True, False]:
        for nutritious in [True, False]:
            for vegan in [True, False]:
                simplex_ = food_suggester(man=man, nutritious=nutritious, vegan=vegan)
                simplex_.calculate()
                simplex_.illustrate()

def main():
    #function for user interaction
    print("Let's find you some food suggestions according to your daily needs")
    print("please input your metrics".upper())
    man = input("Type m for man, w for woman: ")
    man = True if man.lower() == 'm' else False
    vegan = input("Are you vegan (y/n)?: ")
    vegan = True if vegan.lower() == 'y' else False
    nutritious = input("optimize by price or protein intake of daily meals (price/protein)?: ")
    nutritious = False if nutritious.lower() == 'price' else True
    save = input("store shopping list to your desktop (y/n)?: ")
    save = True if save.lower() == 'y' else False

    simplex = food_suggester(man=man, nutritious=nutritious, vegan=vegan, save_to_desktop=save)
    simplex.calculate()
    simplex.illustrate()


if __name__ == "__main__":
    main()

#calcuate_every_option()