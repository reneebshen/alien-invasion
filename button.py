'''
Created on Jun 24, 2020

@author: rb18s
'''

import pygame.font


class Button:
    '''
    A class to manage buttons
    '''

    def __init__(self, ai_game, msg):
        '''
        Initialize button attributes
        '''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        self._set_properties(msg)

        # Button message prepped once
        self._prep_msg(msg)

    def _set_properties(self, msg):
        """Set button properties based on msg and build rect"""
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 30)
        self.width, self.height = 150, 40

        if msg == 'Play':
            self.width, self.height = 200, 50
            self.button_color = (153, 0, 76)
            self.font = pygame.font.SysFont(None, 48)

            # Build botton rect object and center it.
            vertical_modifier = 0
        elif msg == 'Choose start level':
            self.width, self.height = 300, 40
            self.button_color = (153, 0, 76)

            vertical_modifier = -(self.height * 2.5)
        elif msg == 'Easy':
            self.button_color = (0, 0, 204)
            vertical_modifier = -(self.height)
        elif msg == 'Medium':
            self.button_color = (0, 204, 0)
            vertical_modifier = self.height * 0.5
        elif msg == 'Hard':
            self.button_color = (204, 0, 0)
            vertical_modifier = 2 * self.height

        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.y += vertical_modifier

    def _prep_msg(self, msg):
        """Turn msg intro rendered image and center text on button"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and the draw message
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
