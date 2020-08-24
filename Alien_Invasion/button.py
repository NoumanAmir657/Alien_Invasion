import pygame.font

class Button:

    def __init__(self,ai_game,msg):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimension of height and width
        self.width , self.height = 200 , 50
        self.button_color = (0,0,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None,48) #48 is the size of font


        #Build the button's rect object and center it
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center


        #button msg
        self._prep_msg(msg)


    def _prep_msg(self,msg):
        #turn msg into a rendered image
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color) #True is for antialiasing on or off
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
