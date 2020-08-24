import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_game):
        
        super().__init__()
        self.screen = ai_game.screen

        self.settings = ai_game.settings

        #Load the alien image
        self.image = pygame.image.load('Images/alien.bmp') #load image of alien
        self.rect = self.image.get_rect() #get alien rect
        
        
        #Start each new alien at the top-left of screen
        self.rect.x = self.rect.width 
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)


    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction) 
        self.rect.x = self.x

        
    def check_edges(self):
        screen_rect = self.screen.get_rect()

        #check whether the alien is at edge
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        else:
            return False

