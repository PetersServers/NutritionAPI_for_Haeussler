
import random
from data_management import *
from faker import Faker
from check_vegan import check_vegan

def _read_categorization():
        with open("lists.txt", "r") as f:
            content = f.read()
            vegan_l = content.split("\n")[0].split("=")[1].strip().strip("[]").split(", ")
            non_vegan_l = content.split("\n")[1].split("=")[1].strip().strip("[]").split(", ")
            vegan_l = [i.replace("'", "") for i in vegan_l]
            non_vegan_l = [i.replace("'", "") for i in non_vegan_l]

        return vegan_l, non_vegan_l

def manage_lists(vegan=False):
    with open('configurable_file.txt', 'r') as f:
        grocery_list = f.readlines()

    grocery_list = [item.split(',')[0] for item in grocery_list]

    #automatically categorize the products into vegan and non vegan
    check_vegan(grocery_list)

    #read the categorization back in
    vegan_l, non_vegan_l = _read_categorization()

    for item in vegan_l[:]:
        if item not in grocery_list:
            vegan_l.remove(item)

    for item in non_vegan_l[:]:
        if item not in grocery_list:
            non_vegan_l.remove(item)
    #could specify also only non vegan products for optimization
    if vegan:
        return vegan_l
    else:
        return grocery_list



