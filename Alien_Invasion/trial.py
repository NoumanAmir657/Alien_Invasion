import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion:
    def __init__(self):
        pygame.init() #intializing components of game
        
        self.settings = Settings() #create an instance of Settings class
        self.screen = pygame.display.set_mode((self.settings.height,self.settings.width)) #set the size of regular window

        #Fullscreen settings
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion") #set the name of game
        
        self.stats = GameStats(self)
        
        self.ship = Ship(self) #passing the current instance of AlienInvasion

        self.bullets = pygame.sprite.Group() #create instance of sprite.Group class

        self.aliens = pygame.sprite.Group()

        self.sb = ScoreBoard(self)

        self._create_fleet()

        self.crash_sound = pygame.mixer.Sound("Explosion+1.wav") #save audion in self.crash_sound
        self.laser_sound = pygame.mixer.Sound("Laser.wav")
        self.ship_hit_sound = pygame.mixer.Sound("Explosion+5.wav")

        #Make play button
        self.play_button = Button(self,"Play")
        
    def run_game(self):
        while True: #while game is running
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
            
                self._update_bullets()

                self._update_aliens()
                    
            self._update_screen()
            
            
    def _check_events(self):
        for event in pygame.event.get(): #keyboard and mouse events
            
            if event.type == pygame.QUIT: #if clicked on the close window button
                pygame.quit()
                sys.exit() # then exit the game
                    
            elif event.type == pygame.KEYDOWN:
                self._check_key_down(event)
                        
            elif event.type == pygame.KEYUP:
                self._check_key_up(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


                       
    def _check_key_down(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
            
        elif event.key == pygame.K_LEFT:    
            self.ship.moving_left = True
            
        elif event.key == pygame.K_q:
            with open("High_Score.txt",'w') as hs:
                hs.write((str(self.stats.high_score)))
            
            pygame.quit()
            sys.exit()
            
        elif event.key == pygame.K_SPACE:
            
            self._fire_bullet()

            

    def _check_key_up(self,event):
         if event.key == pygame.K_RIGHT:
             self.ship.moving_right = False
         elif event.key == pygame.K_LEFT:    
             self.ship.moving_left = False


    
    def _fire_bullet(self):
        #Create new bullet and add it to bullets group
        if len(self.bullets) < self.settings.bullets_allowed: #check the number of bullets
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            pygame.mixer.Sound.play(self.laser_sound) #play audio at crash
            pygame.mixer.music.stop() #stop audio


    def _update_bullets(self):
        self.bullets.update() #move bullets on screen
        for bullet in self.bullets.copy(): #check bullet position in copy of bullet
            if bullet.rect.bottom <= 0: #check if bottom of bullet is at zero y-coordinate
                self.bullets.remove(bullet) #remove the bullet from list
        #print(len(self.bullets)) #print length of list of bullets
                
        self._check_bullet_alien_collision()
        
        


    def _check_bullet_alien_collision(self):
        #Check collision of bullets and alien
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True,
                                                True)
        
        #True and True means that both the bulleta and alien would disappear
        #from screen after collsion

        if collisions:
            pygame.mixer.Sound.play(self.crash_sound) #play audio at crash
            pygame.mixer.music.stop() #stop audio
            for aliens in collisions.values():#collision is a dictionary
                self.stats.score +=self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        #When the fleet has been destroyed
        if not self.aliens:
            self.bullets.empty() #remove the existing bullets
            self._create_fleet() #create new fleet
            self.settings.increase_speed()
            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()



    def _create_fleet(self):
        alien = Alien(self) #make an instance of alien
        
        alien_width = alien.rect.width #get the width of alien.bmp
        alien_height = alien.rect.height #get the alien.bmp height
        #print("Alien width is " + str(alien_width))

        available_space_x = self.settings.width - (2 * alien_width)
        #print(available_space_x)#subtract margins
        number_aliens_x = available_space_x // (2 * alien_width) #calculate no. of aliens
        #print(number_aliens_x)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.height - (3 * alien_height) - (ship_height)
        number_rows = available_space_y // (3 * alien_height)
                                                     
        for row in range(number_rows):
            for alien_number in range(number_aliens_x): #loop through no. of aliens
                self._create_alien(alien_number,row)             



    def _create_alien(self,alien_number,row):
        alien = Alien(self) # create alien
        
        alien_width, alien_height = alien.rect.size
        
        alien.x = alien_width + (2 * alien_width * alien_number)
        alien.rect.x = alien.x
        
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row
        
        self.aliens.add(alien) #add it to sprite list


        
    def _update_aliens(self):
        self.aliens.update() #call this method to move aliens on screen
        self._check_fleet_edges()

        #Check for alien and ship collision
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()

        #Check whether alien has hit the bottom
        self._check_aliens_bottom()    

        


    def _check_fleet_edges(self):
        #loop through sprites list of alien
        for alien in self.aliens.sprites():
            if alien.check_edges():
                #print('aaaa')
                self.change_fleet_direction()
                break


    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1    
        

    def _ship_hit(self):
        #Decrement ship
        if self.stats.ship_left > 0:
            
            pygame.mixer.Sound.play(self.ship_hit_sound) #play audio at crash
            pygame.mixer.music.stop() #stop audio
            
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            #Get rid of aliens and bullets
            self.bullets.empty()
            self.aliens.empty()

            #Create a new fleet
            self._create_fleet()
            self.ship.center_ship()

            #Pause
            sleep(0.5)
            
        else:

            pygame.mixer.Sound.play(self.ship_hit_sound) #play audio at crash
            pygame.mixer.music.stop() #stop audio
            
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

        


    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


    def _check_play_button(self,mouse_pos):
        #start a new game when player clicks Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        
        if button_clicked and not self.stats.game_active:
            self.settings.intialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #get rid of aliens
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            #hide the mouse cursor
            pygame.mouse.set_visible(False)
        
        

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        
        self.ship.blitme() #draw ship
        
        for bullet in self.bullets.sprites(): #draw bullets
            bullet.draw_bullet()
            
        self.aliens.draw(self.screen) #draw aliens

        self.sb.show_score() # draw scoreboard

        #draw button
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()  #display window



    





    

if __name__ == '__main__':
    ai = AlienInvasion() # make a game instance
    ai.run_game()
        
