import pygame
from settings import Settings
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self,ai_game): #instance of AlienIncasion class passed to ship

        super().__init__()
        self.screen = ai_game.screen #to access the screen of AlienInvasion
        
        self.settings = ai_game.settings
        
        self.screen_rect = ai_game.screen.get_rect() #get the rectangle of screen

        self.image = pygame.image.load('Images/ship.bmp') #load the image of ship
        self.rect = self.image.get_rect() # get rectangle of ship
        
        # to draw at midbottom the rect attribute of screen and ship should match
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False #flag value
        self.moving_left = False #flag value

    def update(self):
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.rect.x += self.settings.ship_speed #move ship towards right by one pixel
            if self.moving_left and self.rect.left > 0:
                self.rect.x -= self.settings.ship_speed

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
                
        
        
    def blitme(self):
        self.screen.blit(self.image,self.rect) #show ship on screen
        
        
