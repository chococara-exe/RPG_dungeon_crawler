import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    '''this class is used to create non-entity sprites to blit on the map'''
    def __init__(self, pos, groups, sprite_type, image, size):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = pygame.Surface((size, size))
        self.image.blit(image, (0,0))
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.image.set_colorkey("black")
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
