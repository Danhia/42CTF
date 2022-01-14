from random import choice, randint

colors = ['blue', 'red', 'yellow', 'green', 'black', 'white', 'purple', 'orange', 'brown', 'fuchsia', 'gold', 'pink', 'cyan', 
    'magenta', 'pearl']

animals = ['tiger', 'bee', 'dog', 'cat', 'otter', 'lizard', 'horse', 'mouse', 'butterfly', 'dolphin', 'elephant', 'falcon', 'goat'
    'cow', 'lion', 'ostrich']

def get_random_name():
    return choice(colors) + choice(animals) + str(randint(0, 100))