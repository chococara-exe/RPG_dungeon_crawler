import pygame, sys
import random
from queue import Queue
from settings import *
from tile import Tile
from player import Player
from enemy import Enemy
from pauseMenu import Pause
from gameOver import GameOver
from support import *
from advance import Advance
from weapon import Weapon
from dialogue import *

class Level:
    def __init__(self, level_num):
        self.display = pygame.display.get_surface()
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.interact_sprites = pygame.sprite.Group()

        #game and level information
        self.level_num = level_num
        self.level = import_csv_layout("../map/level"+str(level_num)+".csv")
        self.save_file = save_file[0]
        self.game_data = game_data[0]
        self.create_map(self.level)
        self.running = True
        self.is_advance = False

        self.font = pygame.font.Font(FONT, 35)
        self.title = self.font.render("Level " + str(level_num), True, "black")
        self.title_rect = self.title.get_rect(topleft=(10, 10))

        #saves the game every fifth level
        if level_num % 5 == 0:
            self.game_data["level"] = level_num
            self.save_file.save_data(self.game_data)

    def create_map(self, level):
        #draws the sprites onto the screen
        for indexr, row in enumerate(level):
            for indexc, col in enumerate(row):
                x = indexc * TILESIZE
                y = indexr * TILESIZE
                if col == "0":
                    object = pygame.image.load( "../graphics/rock.png").convert_alpha()
                    object = pygame.transform.scale(object, (64,64))
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], "object", object, 64)
                if col == "2":
                    self.player = Player((x, y), self.game_data["health"], [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)
                if col == "3":
                    Enemy("skeleton", (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player)
                if col == "4":
                    stair = pygame.image.load( "../graphics/stairs.png").convert_alpha()
                    self.stair = Tile((x, y), [self.visible_sprites, self.interact_sprites], "stair", stair, 32)
                if col == "5":
                    item = pygame.image.load("../graphics/sparkle.png").convert_alpha()
                    Tile((x, y), [self.visible_sprites, self.interact_sprites], "item", item, 32)

    def display_heart(self, player):
        #display the health of the player
        heart1, heart2, heart3 = player.update_health()
        self.display.blit(heart1, (1088, 0))
        self.display.blit(heart2, (1136, 0))
        self.display.blit(heart3, (1184, 0))

    def create_attack(self):
        #creates attack when the player chooses to attack
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self):
        #destroys the attack after the attack cooldown is up
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        #if the weapon collides with the enemies, it deals damage to them
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount):
        #if the player is not immune, they will take damages
        if self.player.vulnerable:
            self.player.health -= amount
            self.game_data["health"] = self.player.health
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
        if self.player.health < 1:
            #game over screen will appear if they don't have any more health
            self.running = False
            gameover = GameOver()
            gameover.run()

    def cutscene(self, file):
        #starts a cutscene if the cutscene has not been activated yet
        #the game data is saved after every cutscene
        #the activated cutscene is saved to make sure that the cutscene does not repeat
        active = game_data[0]["activated cutscenes"]
        if file not in active:
            path = f"../dialogue/{file}.json"
            active.append(file)
            dialogue_graph = parse_graph_json(open_file(path))
            dialogue = Dialogue(dialogue_graph)
            dialogue.run()
            self.save_file.save_data(self.game_data)

    def collect_item(self):
        #activates the dialogue for collecting the item
        #if all the items are collected, the level will change
        item = random.choice(items)
        items.remove(item)
        path = f"../dialogue/{item}.json"
        dialogue_graph = parse_graph_json(open_file(path))
        dialogue = Dialogue(dialogue_graph)
        dialogue.run()
        if not items:
            dialogue_graph = parse_graph_json((open_file("../dialogue/water_filter.json")))
            dialogue = Dialogue(dialogue_graph)
            dialogue.run()
            self.running = False
            game_data[0]["level"] += 1

    def interaction(self, player):
        #checks what interactable sprite the player is interacting with
        if self.interact_sprites:
            collision_sprites = pygame.sprite.spritecollide(player, self.interact_sprites, False)
            if collision_sprites:
                for target_sprite in collision_sprites:
                    if target_sprite.sprite_type == 'stair':
                        #if the player interacts with the stairs, the advance menu will ask if the player wants to move on
                        advance = Advance()
                        is_advance = advance.run()
                        if is_advance:
                            self.running = False
                            game_data[0]["level"] += 1
                    else:
                        #if the player interacts with the item sparkle, the item will be collected and the sparkle will be deleted
                        self.collect_item()
                        target_sprite.kill()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_e]:
                        self.interaction(self.player)
                    if key[pygame.K_ESCAPE]:
                        pause = Pause(self.player, self.display_heart)
                        pause.run()

            self.display.fill("black")
            self.visible_sprites.custom_draw(self.player, self.interact_sprites)
            #checks if the cutscene has already been ran and runs it if it has not
            for cutscene in cutscenes:
                if self.level_num == cutscene[0]:
                    self.cutscene(cutscene[1])
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.display.blit(self.title, self.title_rect)
            self.display_heart(self.player)
            self.player_attack_logic()
            pygame.display.update()

class YSortCameraGroup(pygame.sprite.Group):
    #draws the objects according to their y position (ie, up to down)
    def __init__(self):
        super().__init__()
        self.display = pygame.display.get_surface()
        self.half_width = self.display.get_size()[0] // 2
        self.half_height = self.display.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.floor_image = pygame.image.load("../graphics/floor.png")
        self.floor = pygame.transform.scale(self.floor_image, (TILESIZE*70, TILESIZE*60))
        self.floor_rect = self.floor.get_rect(center=(24*TILESIZE, 23*TILESIZE))


    def custom_draw(self, player, interact_sprites):
        #finds the offset of the other objects caused by the player moving
        #the player will always be at the centre of the screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #print the floor and interactable objects out separately so it is always below the object
        self.display.blit(self.floor, self.floor_rect.topleft - self.offset)
        for sprite in interact_sprites:
            self.display.blit(sprite.image, sprite.rect.topleft - self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite.sprite_type != "stair" and sprite.sprite_type != "item":
                offset_pos = sprite.rect.topleft - self.offset
                self.display.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)