import pygame, sys
from settings import *
from button import Button
from level import Level

class Menu:
    '''this class creates the main menu screen and allows the player to interact with the buttons on the screen
    to either start a new game, continue a game, or quit. it also displays the instructions for the keys'''
    def __init__(self):
        self.display = pygame.display.get_surface()
        self.title_font = pygame.font.Font(FONT, 60)
        self.font = pygame.font.Font(FONT, 35)
        self.title = self.title_font.render(TITLE, True, "white")
        self.title_rect = self.title.get_rect(center=(640, 200))

        self.text_font = pygame.font.Font(FONT, 18)

        #creates the instructions on the side of the menu screen
        self.instruction = self.font.render("Instructions:", True, "white")
        self.movement = self.text_font.render("Use WASD or the arrow keys to move", True, "white")
        self.interact = self.text_font.render("Use E to interact with objects", True, "white")
        self.attack = self.text_font.render("Use SPACE to attack enemies", True, "white")
        self.pause = self.text_font.render("Use ESC to pause the game and access your inventory", True, "white")
        self.instruction_rect = self.instruction.get_rect(topleft=(60, 240))
        self.movement_rect = self.movement.get_rect(topleft=(60,300))
        self.interact_rect = self.interact.get_rect(topleft=(60,350))
        self.attack_rect = self.attack.get_rect(topleft=(60,400))
        self.pause_rect = self.pause.get_rect(topleft=(60,450))

        self.running = True

        #create instances of the buttons in the main menu
        self.newgame_button = Button(None, 640, 320, "New Game", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)
        self.continue_button = Button(None, 640, 390, "Continue", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)
        self.quit_button = Button(None, 640, 460, "Quit", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)

        self.buttons = [self.newgame_button, self.continue_button, self.quit_button]

    def run(self):
        while True:
            mouse = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.newgame_button.check_input(mouse):
                        if len(saves)+1 > 6:
                            #checks if there are too many save files
                            raise Exception("There are too many save files")
                        save_file[0].save_data(game_data[0])
                        #runs the levels in sequence
                        for i in range(1, 21):
                            Level(game_data[0]["level"]).run()

                    if self.continue_button.check_input(mouse):
                        #asks player to choose a save file and gets current level from file
                        data_exist = get_data()
                        try:
                            while game_data[0]["level"] != 21:
                                Level(game_data[0]["level"]).run()
                        #allows player to go back to the main menu
                        except: pass
                    if self.quit_button.check_input(mouse):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.fill(MAIN_COLOR)
            self.display.blit(self.title, self.title_rect)

            self.display.blit(self.instruction, self.instruction_rect)
            self.display.blit(self.movement, self.movement_rect)
            self.display.blit(self.interact, self.interact_rect)
            self.display.blit(self.attack, self.attack_rect)
            self.display.blit(self.pause, self.pause_rect)

            for button in [self.newgame_button, self.continue_button, self.quit_button]:
                button.change_color(mouse)
                button.update(self.display)

            pygame.display.update()