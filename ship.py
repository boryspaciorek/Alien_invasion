import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    """klasa związana z statkiem"""
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.settings=ai_game.settings
        self.screen_rect=ai_game.screen.get_rect()
        """stworzenie statku i jego hitboxa"""
        self.image=pygame.image.load('images/Nowy folder.bmp')#
        self.rect=self.image.get_rect()
        self.center_ship()
        #położenie statku jest jako zmiennoprczecinkowa liczba
        self.x=float(self.rect.x)
        #poruszanie statku
        self.moving_right = False
        self.moving_left = False

    #funkcja odpowiadająca za poruszanie się statku
    def update(self):
        if self.moving_right:
            self.x+=self.settings.ship_speed
            if self.rect.right>self.screen_rect.right:
                self.moving_right=False
        if self.moving_left:
            self.x-=self.settings.ship_speed
            if self.x<=0:
                self.moving_left=False
        self.rect.x=self.x

    #pokazywanie statku przed tłem
    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """położenie statku na środku"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x = float(self.rect.x)

