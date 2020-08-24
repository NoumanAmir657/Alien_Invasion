import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    def __init__(self,ai_game): #ai_game is an instance of AlienInvasion
        
        super().__init__() #inheritance from Sprite class
        
        self.screen = ai_game.screen
        
        self.settings = ai_game.settings
        
        self.color = self.settings.bullet_color

        #Create a rect of bullet at (0,0)
        self.rect = pygame.Rect(0,0,self.settings.bullet_width,
                                       self.settings.bullet_height)
        
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed #bullet moves up
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)    
        
