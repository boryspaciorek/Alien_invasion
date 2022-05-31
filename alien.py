import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """klasa opisująca kosmite"""
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        #przedstawienie obrazu obcego
        self.image=pygame.image.load('images/evil_ship.bmp')
        self.rect=self.image.get_rect()
        #umieszczenie nowego obcego w lewym górnym rogu
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height
        #dokładne położenie
        self.x=float(self.rect.x)


    def update(self):
        self.x+=(self.settings.alien_speed*self.settings.fleet_direction)
        self.rect.x=self.x

    def check_edges(self):
        if self.rect.right>self.settings.screen_width or self.rect.left<0:
            return True
