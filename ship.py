import pygame

class Ship():
    '''класс управления кораблем'''
    def __init__(self, ai_game):
        '''инициализируем корабль и щадаем его начальную позицию'''
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        #Загружаем изображение корабля
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #каждый новый корабль появляется у нижнего края
        self.rect.midbottom = self.screen_rect.midbottom

        #сохранение вещественной координаты цунтра коробля
        self.x = float(self.rect.x)

        #Флаги перемещения кораблем
        self.moving_right = False
        self.moving_left = False
    def update(self):
        '''обновляет позицию корабля с учетом флага'''
        #обновляется атрибут x, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        #обновление атрибута rect на основании self.x
        self.rect.x = self.x

    def blitme(self):
        '''рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''размещает корабль в центре нижней стороны'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)