import pygame
from settings import *

class SpriteSheet:
    '''this class creates a sprite sheet for the animations and images'''
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_frame(self, frame, row, width, height, color):
        #get a single frame from the sprite sheet
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0,0), (frame * width, row * height, width, height))
        image = pygame.transform.scale(image, (width*4, height*4))
        image.set_colorkey(color)
        return image

    def move(self, row, frames, width, height):
        #get all the frames in the row and return it in one list
        animation = []
        for i in range(frames):
            frame = self.get_frame(i, row, width, height, "black")
            animation.append(frame)
        return animation
