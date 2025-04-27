import random
from time import time
from game import Game

if __name__ == '__main__':
    random.seed(int(time() % 100))
    game = Game()
    game.run()