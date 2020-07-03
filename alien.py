'''
Created on Jun 23, 2020

@author: rb18s
'''

import pygame
from pygame.sprite import Sprite
from pygame import transform


class Alien(Sprite):
    '''
    A class to represent a single alien in the fleet.
    '''

    def __init__(self, ai_game):
        '''
        Initialize the alien and set starting position.
        '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load alien image and get rect
        self.image = pygame.image.load('images/alien.bmp')
        self.image = pygame.transform.scale(self.image, (50, 52))
        self.rect = self.image.get_rect()

        # Start an alien at top left corner of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store decimal values for alien horizontal position
        self.x = float(self.rect.x)

    def update(self):
        """Move alien to the right"""

        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
