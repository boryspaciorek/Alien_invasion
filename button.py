import pygame.font

class Button():

    def __init__(self,ai_game,screen,msg):
        """inicjalizacja atrybutów przycisku"""
        self.screen=screen
        self.screen_rect=ai_game.screen.get_rect()

        # zdefiniowanie wartości przycisków
        self.button_color = (0, 100, 250)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # komunikat wyświetlany przez przycisk
        self._prep_msg(msg)

        #zdefiniowanie wymiarów przycisku
        self.width=self.msg_image_rect.width+100
        self.height=50

        #utworzenie prostokąta przycisku
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen_rect.center

        self.msg_image_rect.center = self.rect.center
        #przycisk po kliknieciu
        self.click_color=(0,0,250)
        self.msg_image_click=self.font.render(msg,True,self.text_color,self.click_color)
        self.check_click=False

    def _prep_msg(self,msg):
        """umieszczenie komunikatu na przycisku i wyśrodkowanie tekstu"""
        #zamiana tekstu na obraz
        self.msg_image=self.font.render(msg,True,self.text_color,self.button_color)
        #stworzenie prostokątu wiadomości
        self.msg_image_rect=self.msg_image.get_rect()


    def draw_button(self):
        """wyświetlenie pustego przycisku a nastepnie komunikatu na nim"""
        if self.check_click:
            self.screen.fill(self.click_color, self.rect)
            self.screen.blit(self.msg_image_click, self.msg_image_rect)

        else :
            self.screen.fill(self.button_color,self.rect)
            self.screen.blit(self.msg_image,self.msg_image_rect)