import pygame, sys
from settings import *
from button import Button
from inventory import Inventory
from gameOver import GameOver

class Pause:

    '''this class creates a pause screen where the player can choose to resume the game or access their inventory'''

    def __init__(self, player, display_heart):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, 35)
        self.running = True
        self.player = player
        self.display_heart = display_heart

        #creates the instructions beside the buttons
        self.movement = self.font.render("Use WASD or the arrow keys to move", True, "white")
        self.interact = self.font.render("Use E to interact with objects", True, "white")
        self.attack = self.font.render("Use SPACE to attack enemies", True, "white")
        self.pause = self.font.render("Use ESC to pause the game and access your inventory", True, "white")
        self.movement_rect = self.movement.get_rect(topleft=(280,100))
        self.interact_rect = self.interact.get_rect(topleft=(280,150))
        self.attack_rect = self.attack.get_rect(topleft=(280,200))
        self.pause_rect = self.pause.get_rect(topleft=(280,250))

        #create instances of the buttons in the pause menu
        self.resume_button = Button(None, 150, 100, "Resume", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)
        self.inventory_button = Button(None, 150, 170, "Inventory", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)
        self.quit_button = Button(None, 150, 240, "Quit", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)

    def run(self):
        while self.running:
            self.display.fill(MAIN_COLOR)
            mouse = pygame.mouse.get_pos()
            self.display_heart(self.player)

            self.display.blit(self.movement, self.movement_rect)
            self.display.blit(self.interact, self.interact_rect)
            self.display.blit(self.attack, self.attack_rect)
            self.display.blit(self.pause, self.pause_rect)

            if self.player.health < 1:
                #displays game over screen if the player's health is 0
                self.running = False
                gameover = GameOver()
                gameover.run()

            for button in [self.resume_button, self.inventory_button, self.quit_button]:
                button.change_color(mouse)
                button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resume_button.check_input(mouse):
                        #allows player to resume game
                        self.running = False
                    if self.inventory_button.check_input(mouse):
                        #displays the inventory
                        Inventory(self.player, self.display_heart).run()
                    if self.quit_button.check_input(mouse):
                        pygame.quit()
                        sys.exit()

            pygame.display.update()