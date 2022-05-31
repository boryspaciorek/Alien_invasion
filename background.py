import pygame
from pygame.sprite import Sprite
from settings import Settings
from random import randint
class Star(Sprite):
    def __init__(self,game):
        super().__init__()
        self.image=pygame.image.load("images/star2.bmp")
        self.rect=self.image.get_rect()
        self.settings=Settings()
        self.rect.x=randint(0,game.settings.screen_width)
        self.rect.y = randint(0, game.settings.screen_height )
        self.y=float(self.rect.y)

    def update(self):
        self.y+=self.settings.star_speed
        self.rect.y=self.y