import pygame, sys
from settings import *
from button import Button

pygame.init()
display = pygame.display.set_mode((1280, 720))

class Inventory:

    '''this class creates the inventory screen where the player will be able to use items to heal'''

    def __init__(self, player, display_heart):
        self.display = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, 25)
        self.button_font = pygame.font.Font(FONT, 35)
        self.running = True
        self.player = player
        self.display_heart = display_heart

        self.title_font = pygame.font.Font(FONT, 60)
        self.title = self.title_font.render("Inventory", True, "white")
        self.title_rect = self.title.get_rect(center=(640, 100))
        self.empty = self.font.render("You don't have any items in your inventory, try killing some enemies", True, "white")
        self.empty_rect = self.empty.get_rect(center=(640, 300))

        self.inventory = game_data[0]["inventory"]
        self.buttons = []
        self.items = []

        #create instances of the buttons in the inventory screen
        self.back_button = Button(None, 150, 100, "Back", self.button_font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR)
        for index, (item, amount) in enumerate(self.inventory.items()):
            self.items.append(item)
            self.buttons.append(Button(None, DIS_W // 2, 200 + 70*index, f"{item}    x{amount}", self.font, BUTTON_HOVER_COLOR, BUTTON_BASE_TEXT, MAIN_COLOR))

    def run(self):
        while self.running:
            self.display.fill(MAIN_COLOR)
            self.display.blit(self.title, self.title_rect)
            mouse = pygame.mouse.get_pos()
            self.display_heart(self.player)

            if not self.inventory:
                self.display.blit(self.empty, self.empty_rect)

            for button in self.buttons:
                button.change_color(mouse)
                button.update(self.display)

            self.back_button.change_color(mouse)
            self.back_button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.check_input(mouse):
                        self.running = False
                    for number, button in enumerate(self.buttons):
                        #if player selects an item, the item will be consumed and the amount of that item will reduce by 1
                        if button.check_input(mouse):
                            self.running = False
                            item = self.items[number]
                            self.inventory[item] -= 1
                            if self.inventory[item] == 0:
                                #if there is none of an item, the item will be deleted from the inventory
                                del self.inventory[item]
                            #the player is healed according to the health that the herb provides in the herb data
                            self.player.health += herb_data[item]
                            game_data[0]["inventory"] = self.inventory

                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_ESCAPE]:
                        self.running = False

            pygame.display.update()