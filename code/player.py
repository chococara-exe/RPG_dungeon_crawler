import pygame
from settings import *
from entity import Entity
from spriteSheet import SpriteSheet

class Player(Entity):
    '''this class is a child class of the entity class and is used to create the player in the game. it allows the
    player to move and interact with other sprites. the player is able to get damaged and have '''
    def __init__(self, pos, health, groups, obstacle_sprites, create_attack, destroy_attack):
        super().__init__(groups)
        self.spritesheet = SpriteSheet("../graphics/character.png")
        self.image = self.spritesheet.get_frame(0, 0, 32, 32, "black")
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-110, -100)
        self.obstacle_sprites = obstacle_sprites
        self.sprite_type = "player"

        #player information
        self.direction = pygame.math.Vector2()
        self.speed = 8
        self.health = health
        self.attack = 0.5
        self.inventory = save_file[0].load_save()["inventory"]

        #player animation
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        #player cooldown
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 1000


        #player weapons
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]

    def import_player_assets(self):
        self.animations = {
            "down_idle": self.spritesheet.move(0, 4, 32, 32),
            "left_idle": self.spritesheet.move(1, 4, 32, 32),
            "right_idle": self.spritesheet.move(2, 4, 32, 32),
            "up_idle": self.spritesheet.move(3, 4, 32, 32),
            "down": self.spritesheet.move(4, 4, 32, 32),
            "left": self.spritesheet.move(5, 4, 32, 32),
            "right": self.spritesheet.move(6, 4, 32, 32),
            "up": self.spritesheet.move(7, 4, 32, 32),
            "down_attack": self.spritesheet.move(8, 1, 32, 32),
            "left_attack": self.spritesheet.move(9, 1, 32, 32),
            "right_attack": self.spritesheet.move(10, 1, 32, 32),
            "up_attack": self.spritesheet.move(11, 1, 32, 32),
        }


    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        #the player will flicker if it was just attacked and is immune to attacks
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        #gets the damage dealt to the enemy
        base_damage = self.attack
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def get_status(self):
        #gets where the player is currently facing, if the player is moving and if the player is attacking
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')


    def input(self):
        #gets the input from the user to move and attack
        if not self.attacking:
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] or key[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif key[pygame.K_DOWN] or key[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if key[pygame.K_LEFT] or key[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            elif key[pygame.K_RIGHT] or key[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            else:
                self.direction.x = 0

            if key[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

    def update_health(self):
        #update the health that is being displayed on the screen
        sheet = SpriteSheet("../graphics/game_GUI.png")
        if self.health == 2:
            heart1, heart2, heart3 = sheet.get_frame(13, 0, 16, 16, "black"), sheet.get_frame(13, 0, 16, 16, "black"), sheet.get_frame(15, 0, 16, 16, "black")
        elif self.health == 1:
            heart1, heart2, heart3 = sheet.get_frame(13, 0, 16, 16, "black"), sheet.get_frame(15, 0, 16, 16, "black"), sheet.get_frame(15, 0, 16, 16, "black")
        else:
            heart1, heart2, heart3 = sheet.get_frame(13, 0, 16, 16, "black"), sheet.get_frame(13, 0, 16, 16, "black"), sheet.get_frame(13, 0, 16, 16, "black")
        return heart1, heart2, heart3

    def cooldowns(self):
        #checks if the attack and vulnerable cooldowns are up and changes whether the player can attack or be attacked
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False
                self.destroy_attack()

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)