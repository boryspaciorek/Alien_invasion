from time import sleep
from random import randint

import pygame
import sys

from  game_stats import GameStats
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from background import Star
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """taka ogólna klasa do ogarniania wszystkiego"""
    def __init__(self):
        pygame.init()
        self.settings=Settings()
        # ustawienia ekranu
        self.screen=pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width=self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        self.screen_rect=self.screen.get_rect()
        #self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Inwazja obcych")

        # utworzenie egzemplarza odpowiadającego za dane statyczne
        self.stats = GameStats(self)

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self.stars=pygame.sprite.Group()
        self.create_float()
        self.create_stars()
        self.play_button=Button(self,self.screen,"Play")
        self.easy_button = Button(self, self.screen, "Easy")
        self.medium_button = Button(self, self.screen, "medium")
        self.hard_button = Button(self, self.screen, "Hard")
        self.place_lvl_button()
        self.medium_button.check_click=True
        self.sb=Scoreboard(self)
        self.sb.read_high_score("score/medium score.txt")
        self.sb.prep_high_score()


    def run_game(self):
        #petla główna która powtarza się całą gre
        while True:
            self._check_events()
            self._update_stars()
            self._update_screen()
            if self.stats.game_active:

                self.ship.update()
                self._update_bullets()
                self._update_aliens()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_game()
            #wciśniecie klawisza
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            #opuszczenie klawisza
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                self._mouse_down()

    def _mouse_down(self):
        """reakcja na klikniecie myszy"""
        mouse_pos=pygame.mouse.get_pos()
        #reakcja na klikniecie przycisku gra
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self._check_play_button()
        self._dificult_lvl(mouse_pos)

    def _dificult_lvl(self,mouse_pos):
        """odpowiada za wciśniecie jednego z przycisku poziomu trudności"""
        if self.easy_button.rect.collidepoint(mouse_pos) and not self.stats.game_active and not self.easy_button.check_click:
            self.save_score()
            self.sb.read_high_score('score/easy score.txt')
            self.easy_button.check_click=True
            self.medium_button.check_click=False
            self.hard_button.check_click=False
            self._change_lvl(0.5)
            self.sb.prep_high_score()
        if self.medium_button.rect.collidepoint(mouse_pos) and not self.stats.game_active and not self.medium_button.check_click:
            self.save_score()
            self.sb.read_high_score('score/medium score.txt')
            self.easy_button.check_click = False
            self.medium_button.check_click = True
            self.hard_button.check_click = False
            self._change_lvl(1)
            self.sb.prep_high_score()
        if self.hard_button.rect.collidepoint(mouse_pos) and not self.stats.game_active and not self.hard_button.check_click:
            self.save_score()
            self.sb.read_high_score('score/hard score.txt')
            self.easy_button.check_click = False
            self.medium_button.check_click = False
            self.hard_button.check_click = True
            self._change_lvl(1.5)
            self.sb.prep_high_score()

    def _check_play_button(self):
        """reakcja na wciśniecie przycsiku gra"""
        #zresetowanie danych statycznych gry
        self.stats.reset_stats()
        self.stats.game_active=True
        #usuniecie floty i pocisków
        self.aliens.empty()
        self.bullets.empty()
        #utworzenie nowej floty i ustawienie statku
        self.create_float()
        self.ship.center_ship()
        #pokazanie 0 punktów i 1 lvl
        self.sb.prep_score()
        self.sb.prep_lvl()
        self.settings.reset_points()
        self.sb.prep_ships()
        #ukrycie myszki
        pygame.mouse.set_visible(False)


    def _check_keydown_events(self,event):
        """zarządza wciśnietymi klawiszami"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT and self.ship.rect.x > 0:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            self.exit_game()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key==pygame.K_RETURN and not self.stats.game_active:
            self._check_play_button()
            #pokazanie wyniku 0 po włączeniu nowej rundy

    def _check_keyup_events(self,event):
        """zarządza puszczonymi klawiszami"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def fire_bullet(self):
        if self.settings.bullet_allowed>len(self.bullets):
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """aktualizowanie położenia pocisków i usuwanie tych poza granicami ekranu"""
        #aktualizowanie położenia pocisków
        self.bullets.update()
        #usuniecie pocisków poza granicami ekranu
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)
        #sprawdzenie czy jakiś pocisk trafił kosmite
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # pozbycie się pocisków i utworzenie nowej floty
            self.bullets.empty()
            self.create_float()
            self.settings.alien_speed *=self.settings.speedup_scale
            self.settings.alien_points=int(self.settings.alien_points*self.settings.score_scale)
            self.stats.lvl+=1
            self.sb.prep_lvl()

    def _update_screen(self):
        self.ship.blitme()
        # wyświetlanie ostatnio zmodyfikowanego ekranu
        pygame.display.flip()
        # odświeża ekran
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        if self.stats.game_active:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.sb.show_score()
        else:
            self.draw_buttons()

    def place_lvl_button(self):
        """ustawia gdzie mają stać przyciski"""
        #ustawienie przycisku medium
        self.medium_button.rect.midtop=self.play_button.rect.midbottom
        self.medium_button.rect.y+=50
        self.medium_button.msg_image_rect.center=self.medium_button.rect.center
        #ustawienie przycisku easy
        self.easy_button.rect.midright=self.medium_button.rect.midleft
        self.easy_button.rect.x-=20
        self.easy_button.msg_image_rect.center=self.easy_button.rect.center
        #ustawienie przycisku hard
        self.hard_button.rect.midleft = self.medium_button.rect.midright
        self.hard_button.rect.x += 20
        self.hard_button.msg_image_rect.center = self.hard_button.rect.center

    def draw_buttons(self):
        self.play_button.draw_button()
        self.easy_button.draw_button()
        self.medium_button.draw_button()
        self.hard_button.draw_button()

    def create_float(self):
        """stworzenie floty kosmitów"""
        #utworzenie jednego kosmity i obliczenie ile się zmieści w jednym rzedzie
        #odległość miedzy opcymi jest równa połowie ich szerokośći
        alien=Alien(self)
        #ustalenie szerokości miedzy kosmitami
        alien_width=alien.rect.width
        available_space_x=self.settings.screen_width-(3*alien_width)
        number_aliens_x=available_space_x // (alien_width*2)
        #utalenie wysokości miedzy kosmitami
        alien_height=alien.rect.height
        ship_height=self.ship.rect.height
        available_space_y=self.settings.screen_height-(3*alien_height)-ship_height
        number_rows=available_space_y //(alien_height*2)
        #utworzenie rzedu obcych
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number,row_number)

    def create_alien(self,alien_number,row_number):
        alien = Alien(self)
        alien_width = alien.rect.width
        alien_height = alien.rect.height
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y=alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)

    def create_stars(self):
        """tworzy tło z gwiazd"""
        for i in range(self.settings.how_much_stars):
            star=Star(self)
            self.stars.add(star)

    def _update_stars(self):
        self.stars.update()
        #sprawdzenie czy gwiazda nie znikneła poza ekran
        for star in self.stars.copy():
            if star.rect.y>self.settings.screen_height:
                self.stars.remove(star)
                #stworzenie nowej gwiazdy na górze ekranu
                star=Star(self)
                star.y=0-star.rect.height
                star.x=randint(0,self.settings.screen_width)
                self.stars.add(star)

    def _update_aliens(self):
        """uaktualnianie położenia floty"""
        self.aliens.update()
        self._check_fleet_edges()
        #wykrywanie zderzenia z graczem
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #szukanie kosmitów którzy doszli do dołu ekranu
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """reakcja gdy kosmita dojdzie do krawedzi ekranu"""
        self.screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """przesuniecie floty w dół i zmiana ich kierunku"""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1

    def _check_aliens_bottom(self):
        """sprawdzenie czy obcy dotarł do krawedzi ekranu"""
        screen_rect=self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom>=screen_rect.bottom:
                self._ship_hit()
                break

    def _ship_hit(self):
        """reakcja na uderzenie przez statek"""
        if self.stats.ship_left-1>0:
            # zmniejszenie życia
            self.stats.ship_left -= 1
            self.sb.prep_ships()
            #usuniecie kosmitów i pocisków
            self.aliens.empty()
            self.bullets.empty()
            #utworzenie nowych kosmitów
            self.create_float()
            self.ship.center_ship()
            #pauza
            sleep(1)

        else:
            sleep(1)
            self.stats.game_active=False
            self.settings.alien_speed=self.stats.alien_speed
            pygame.mouse.set_visible(True)

    def _change_lvl(self,dificult_lvl):
        self.settings.reset_speed()
        self.settings.bullet_speed*=dificult_lvl
        self.settings.ship_speed*=dificult_lvl
        self.settings.alien_speed*=dificult_lvl

    def save_score(self):
        if self.easy_button.check_click:
            self.sb.save_high_score("score/easy score.txt")
        elif self.medium_button.check_click:
            self.sb.save_high_score("score/medium score.txt")
        elif self.hard_button.check_click:
            self.sb.save_high_score("score/hard score.txt")

    def exit_game(self):
        self.save_score()
        sys.exit()



if __name__=="__main__":
    ai=AlienInvasion()
    ai.run_game()