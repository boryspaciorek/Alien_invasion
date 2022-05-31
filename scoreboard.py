import pygame.font
import json
from pygame.sprite import Group
from ship import Ship
class Scoreboard():

    def __init__(self,ai_game):
        self.ai_game=ai_game
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen_rect
        self.settings=ai_game.settings
        self.stats=ai_game.stats
        #ustawienie czcionki
        self.text_color=(100,100,100)
        self.font=pygame.font.SysFont(None,48)
        #stworzenie obrazu napisu
        self.prep_score()
        self.prep_high_score()
        self.prep_lvl()
        self.prep_ships()

    def prep_ships(self):
        self.ships=Group()
        for ship_number in range(self.stats.ship_left):
            ship=Ship(self.ai_game)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)

    def prep_score(self):
        """konwertuje wynik i umiesza go u góry ekranu"""
        rounded_score=round(self.stats.score,-1)
        score_str="{:,}".format(rounded_score)
        self.score_image=self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        self.score_rect=self.score_image.get_rect()
        self.score_rect.right=self.screen_rect.right-20
        self.score_rect.top=20

    def prep_high_score(self):
        """konwertuje najwyższy wynik i umiesza go u góry ekranu"""
        high_score=round(self.stats.high_score,-1)
        high_score_str="{:,}".format(high_score)
        self.high_score_image=self.font.render(high_score_str,True,self.text_color,self.settings.bg_color)
        self.high_score_rect=self.score_image.get_rect()
        self.high_score_rect.centerx=self.screen_rect.centerx
        self.high_score_rect.top=self.score_rect.top


    def show_score(self):
        """pokazuje wyniki"""
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_image_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """sprawdza czy wynik jest wiekszy od najwiekszego"""
        if self.stats.score>self.stats.high_score:
            self.stats.high_score=self.stats.score
            self.prep_high_score()

    def prep_lvl(self):
        lvl_str=str(self.stats.lvl)
        self.level_image=self.font.render(lvl_str,True,self.text_color,self.settings.bg_color)
        self.level_image_rect=self.level_image.get_rect()
        self.level_image_rect.right=self.score_rect.right
        self.level_image_rect.top=self.score_rect.bottom+10

    def save_high_score(self,file):
        """zapisanie najwyższego wyniku"""
        record=0
        with open(file,'r') as in_file:
            record=in_file.read()
        record=int(record)
        if record < self.stats.high_score:
            with open(file,'w') as out_file:
                out_file.write(str(self.stats.high_score))

    def read_high_score(self,file):
        """odczytanie najwyższego wyniku"""
        with open(file,'r') as f:
            self.stats.high_score=f.read()
        self.stats.high_score=int(self.stats.high_score)
        print(type(self.stats.high_score))

