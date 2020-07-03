'''
Created on Jun 24, 2020

@author: rb18s
'''


class GameStats:
    '''
    Track statistics for Alien Invasion
    '''

    def __init__(self, ai_game):
        '''
        Initialize statistics.
        '''
        self.settings = ai_game.settings
        self.reset_stats()
        self.play_clicked = False
        self.game_active = False
        self.high_score_file = 'text_files/high_score.txt'
        with open(self.high_score_file) as high_score:
            self.high_score = int(high_score.read())

    def reset_stats(self):
        """Initialize statistics that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
