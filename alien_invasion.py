'''
Created on Jun 22, 2020

@author: rb18s
'''
import sys
import pygame
from random import randint
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.play_button = Button(self, "Play")
        self.level_button = Button(self, "Choose start level")
        self.easy_button = Button(self, 'Easy')
        self.medium_button = Button(self, 'Medium')
        self.hard_button = Button(self, "Hard")

        self.stars = pygame.sprite.Group()
        self._create_sky()

    def run_game(self):
        """Start main loop for game."""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Response to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            # Move ship to right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_f or event.key == pygame.K_w:
            # Change the screen size
            self._change_screensize(event)
        elif event.key == pygame.K_q:
            # Quit by pressing q
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_buttons(self, mouse_pos):
        """Check which buttons are clicked and respond"""
        play_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if play_clicked and not self.stats.play_clicked and not self.stats.game_active:
            self.stats.play_clicked = play_clicked
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            sleep(0.3)

        elif not self.stats.game_active and self.stats.play_clicked:
            self._check_level(mouse_pos)

    def _check_level(self, mouse_pos):
        """Determine which level button was clicked"""
        easy = self.easy_button.rect.collidepoint(mouse_pos)
        med = self.medium_button.rect.collidepoint(mouse_pos)
        hard = self.hard_button.rect.collidepoint(mouse_pos)
        if easy:
            self.settings.initialize_dynamic_settings(1)
        elif med:
            self.settings.initialize_dynamic_settings(2)
            self.stats.level = self.settings.med_mult
        elif hard:
            self.settings.initialize_dynamic_settings(3)
            self.stats.level = self.settings.hard_mult
        else:
            return
        self.sb.prep_level()
        self.sb.prep_ships()
        self._start_game()

    def _start_game(self):
        """Start a new game"""
        self.stats.game_active = True

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()

        sleep(0.3)
        # Hide mouse cursor
        pygame.mouse.set_visible(False)

    def _change_screensize(self, event):
        """Change screen size to fullscreen or reg window"""
        if event.key == pygame.K_f:
            # Set game to full screen
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        elif event.key == pygame.K_w:
            # Set game back to regular window
            self.settings.reg_window()
            self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

    def _fire_bullet(self):
        """Create a new bullet and add to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets, get rid of old bullets"""
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check for any bullets that have hit aliens
        If so, get rid of bullet and alien"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """Check if aliens have reach bottom of screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""

        if self.stats.ships_left > 0:
            # Decrement ships left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of remaining aliens and bullets
            self.bullets.empty()
            self.aliens.empty()
            # Pause.
            sleep(0.5)
            # Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

        else:
            self.stats.game_active = False
            self.stats.play_clicked = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create a fleet of aliens."""
        # Make an alien and finding spacing
        # Spacing between each alien is one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Find aliens in row
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Find number of rows
        # Spacing between rows is one alien height
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height)
                            -ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create fleet
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Create an alien and place in row
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create a single alien and position it in fleet"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Placing horizontal location
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x

        # Placing vertical location
        alien.y = alien_height + (2 * alien_height * row_number)
        alien.rect.y = alien.y

        # Add alien to fleet
        self.aliens.add(alien)

    def _update_aliens(self):
        """Check if fleet is at edge.
        Update positions of all aliens in fleet"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop entire fleet and change fleet's direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_sky(self):
        """Create a sky of stars"""
        # Find spacing
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width  # - (2 * star_width)
        number_stars_x = available_space_x // (2 * star_width)

        available_space_y = self.settings.screen_height  # - (2 * star_height)
        number_rows = available_space_y // (2 * star_height)

        # Create sky
        for row in range(number_rows):
            for star_num in range(number_stars_x):
                self._create_star(star_num, row)

    def _create_star(self, star_num, row):
        """Position one star in sky and add to group"""
        star = Star(self)
        star_width, star_height = star.rect.size

        rand_x = randint(2, 5)
        star.x = (rand_x * star_width * star_num)
        star.rect.x = star.x
        rand_y = randint(2, 5)
        star.y = (rand_y * star_height * row)
        star.rect.y = star.y

        self.stars.add(star)

    def _update_screen(self):
        """Update images on screen, flip to new screen"""
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.stats.game_active:
            if not self.stats.play_clicked:
                self.play_button.draw_button()
            else:
                self.easy_button.draw_button()
                self.medium_button.draw_button()
                self.hard_button.draw_button()
                self.level_button.draw_button()
        pygame.display.flip()


if __name__ == '__main__':
    # Make game instance and run game
    ai = AlienInvasion()
    ai.run_game()
