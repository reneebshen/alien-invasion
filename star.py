'''
Created on Jun 23, 2020

@author: rb18s
'''

import pygame
from pygame.sprite import Sprite
from random import randint


class Star(Sprite):
    '''
    A class to represent a single star.
    '''

    def __init__(self, ai_game):
        '''
        Initialize the star and set starting position
        '''

        super().__init__()
        self.screen = ai_game.screen

        # Load star image and get rect
        self.image = pygame.image.load('images/star.bmp')
        self.rect = self.image.get_rect()

        # Start star at top left corner of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store devimate values for star horizontal position
        self.x = float(self.rect.x)

