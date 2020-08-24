class Settings:
    def __init__(self):
        
        #Screen Settings
        self.height = 1200   #1200
        self.width = 900   #900
        self.bg_color = (230,230,230)
        
        #Ship Settings
        
        self.ship_limit = 3

        #Bullets Settings
        self.bullet_height = 15
        self.bullet_width = 6 #
        
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #Alien Settings
        
        self.fleet_drop_speed = 20 #drop speed of fleet

        self.speedup_scale = 1.1

        self.intialize_dynamic_settings()
        

    def intialize_dynamic_settings(self):

        self.ship_speed = 2  #2
        self.bullet_speed = 3
        self.alien_speed = 8  #1.5
        self.fleet_direction = 1 # 1 is for right and -1 for left movement
        #Scoring
        self.alien_points = 50


    def increase_speed(self):
        #Increase speed settings.
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        
