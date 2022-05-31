class Settings():
    def __init__(self):
        #ustawienia ekranu
        self.screen_width=153
        self.screen_height=800
        self.bg_color=(2,2,10)
        #ustawienia statku
        self.ship_speed=2
        self.ship_limit=3
        #ustawienia pocisku
        self.bullet_speed=1.5
        self.bullet_width=3.5
        self.bullet_height=25
        self.bullet_color=(100,100,100)
        self.bullet_allowed=2
        #ustawienia tła
        self.how_much_stars=25
        self.star_speed=0.1
        #ustawienia kosmitów
        self.alien_speed=1.6
        self.fleet_drop_speed=10
        #porusza się w prawo gdy jest 1 i w lewo gdy -1
        self.fleet_direction=1
        #zmiana szybkości gry
        self.speedup_scale=1.1
        #normalna predkość
        self.normal_ship_spd=2
        self.normal_bullet_spd=1.5
        self.normal_alien_spd=1.6
        #punkty
        self.normal_alien_points=50
        self.alien_points = self.normal_alien_points
        self.score_scale=1.5

    def reset_speed(self):
        """resetuje predkość"""
        self.bullet_speed=self.normal_bullet_spd
        self.ship_speed=self.normal_ship_spd
        self.alien_speed=self.normal_alien_spd

    def reset_points(self):
        self.alien_points=self.normal_alien_points
