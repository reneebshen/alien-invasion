'''
Created on Jun 22, 2020

@author: rb18s
'''

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    '''
    A class to manage bullets fired from ship
    '''

    def __init__(self, ai_game):
        '''
        Create a bullet object at ship's current position
        '''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0,0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullet position as decimal value
        self.y = float(self.rect.y)

    def update(self):
        """Move bullet up screen"""
        # Update decimal position of bullet
        self.y -= self.settings.bullet_speed
        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
