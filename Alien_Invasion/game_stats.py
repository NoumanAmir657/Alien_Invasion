class GameStats:

    def __init__(self,ai_game):
        #Intialize stats
        self.settings = ai_game.settings
        self.game_active = False #game is active/running
        with open("High_Score.txt") as hs:
            self.high_score = int(hs.read())
            
        #self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
