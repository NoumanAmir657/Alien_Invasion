import pygame
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats


        # Font settings for score board
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        #Prepare the intial score image
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        #Turn the score into a rendered image.
         score_str = str(self.stats.score)
         self.score_image = self.font.render(score_str, True,
         self.text_color, self.settings.bg_color)
        #Display the score at the top right of the screen.
         self.score_rect = self.score_image.get_rect()
         self.score_rect.right = self.screen_rect.right - 30
         self.score_rect.top = 20


    def prep_high_score(self):
        high_score = round(self.stats.high_score, -1) #round score to nearest 10
        #high_score_str = "{:,}".format(high_score)
        high_score_str = str(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                        self.text_color, self.settings.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top


    def prep_level(self):
        #Turn the level into a rendered image.
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                        self.text_color, self.settings.bg_color)
        #Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        #self.level_rect.right = self.score_rect.right - 300
        #self.level_rect.bottom = self.score_rect.bottom
        self.level_rect.left = self.screen_rect.left + 30
        self.level_rect.top = 20


    def prep_ships(self):
        self.ships = Group() #make a instance of Group class
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 100 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            


    def check_high_score(self):
        #Check to see if there's a new high score.
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def show_score(self):
        #Draw score to the screen.
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
        
