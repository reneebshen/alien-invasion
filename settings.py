'''
Created on Jun 22, 2020

@author: rb18s
'''


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize game's static settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (255, 240, 255)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (247, 38, 59)
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        self.easy_mult = 1
        self.med_mult = 3
        self.hard_mult = 6

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self, level=1):
        """Initialize settings that change throughout game"""
        # Easy 1, Med 2, Hard, 3
        self.ship_speed = 1.0
        self.bullet_speed = 1.5
        self.alien_speed = 0.5
        self.alien_points = 50
        if level == 2:
            self.increase_speed(self.med_mult)
        elif level == 3:
            self.increase_speed(self.hard_mult)

        # fleet direction 1 means right' -1 means left
        self.fleet_direction = 1

        # Scoring

    def increase_speed(self, mult=1):
        """Increase speed settings and alien point values for levels"""
        self.ship_speed *= (self.speedup_scale ** mult)
        self.bullet_speed *= (self.speedup_scale ** mult)
        self.alien_speed *= (self.speedup_scale ** mult)

        self.alien_points = int(self.alien_points * (self.score_scale ** mult))

    def reg_window(self):
        """Return screen size to regular window"""
        self.screen_width = 1200
        self.screen_height = 700
