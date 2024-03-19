import pygame, sys
from settings import *
from button import Button


class GameOver:

    '''this class creates a game over screen that will be displayed if the player dies. the player will have the option to try again'''

    def __init__(self):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, 35)
        self.running = True

        self.title_font = pygame.font.Font(FONT, 60)
        self.title = self.title_font.render('Game Over', True, "white")
        self.title_rect = self.title.get_rect(center=(640, 200))

        #create instances of the buttons in the game over screen
        self.tryagain_button = Button(None, DIS_W // 2, DIS_H // 2 + 20, "Try Again", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, "black")
        self.quit_button = Button(None, DIS_W // 2, DIS_H // 2 + 100, "Quit", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, "black")


    def run(self):
        while self.running:
            self.display.fill("black")
            self.display.blit(self.title, self.title_rect)
            mouse = pygame.mouse.get_pos()

            for button in [self.tryagain_button, self.quit_button]:
                button.change_color(mouse)
                button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.tryagain_button.check_input(mouse):
                        #opens the save menu for the player to load a save if they want to try again
                        data_exist = get_data()
                        if data_exist:
                            self.running = False
                    if self.quit_button.check_input(mouse):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()