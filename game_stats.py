class GameStats():
    """monitorowanie danych statycznych"""

    def __init__(self,ai_game):
        self.settings=ai_game.settings
        self.reset_stats()
        #Uruchomienie gry w stanie aktywnym
        self.game_active=False
        self.high_score=0


    def reset_stats(self):
        """inicjalizacja danych statycznych które mogą się zmieniać w trakcie gry"""
        self.ship_left=self.settings.ship_limit
        self.alien_speed=self.settings.alien_speed
        self.score = 0
        self.lvl=1