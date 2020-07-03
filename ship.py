'''
Created on Jun 22, 2020

@author: rb18s
'''

import pygame
from pygame import transform
from pygame.sprite import Sprite


class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize ship and set starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.image = pygame.transform.scale(self.image, (40, 67))
        self.rect = self.image.get_rect()

        # Start each new ship at bottom center of screen
        self.center_ship()

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update ship's position based on movement flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def center_ship(self):
        """Center ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw ship at its current location"""
        self.screen.blit(self.image, self.rect)
