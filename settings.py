import pygame

class Settings():
    '''класс для хранения всех настроек игры'''
    def __init__(self):
        '''инициализируем настройки игры'''
        #параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)



        #настройки корабля
        self.ship_speed = 1.5
        self.ship_limit = 3

        #параметры снаряда
        self.bullet_speed = 2
        self.bullet_width = 4
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        #параметры пришельцев
        self.alien_speed = 0.3
        self.fleet_drop_speed = 10
        #self.fleet_direction = 1


        #темп ускорения игры
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

        #темп роста стоимости пришельца
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        #инициализируем настройки, изменяющиеся в ходе игры
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0
        self.fleet_direction = 1

        #подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        ''' увеличивает настройки скорости'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


