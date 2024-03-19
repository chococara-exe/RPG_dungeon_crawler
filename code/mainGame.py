import pygame
from settings import *
from mainMenu import Menu

class Game:

    '''this class is used to create an instance of the game so that the player can play the game'''

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.display = pygame.display.set_mode((DIS_W, DIS_H))
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.running = True

    def main(self):
        while self.running:
            self.display.fill((0, 0, 0))
            self.clock.tick(FPS)
            self.menu.run()

            pygame.display.update()

#runs the python file if the python file is the main file
if __name__ == '__main__':
    game = Game()
    game.main()