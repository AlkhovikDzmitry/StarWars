import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    '''класс для управления ресурсами и повелением игры'''

    def __init__(self):
        '''Инициализирует игру и создает игровые ресурсы'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #полноэкранный режим
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")




        #создание экземпляра для хранения игровой статисттики
        self.stats = GameStats(self)
        # создание экземпляров для хранения статистики и панель результатов
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()




        #создание кнопки play
        self.play_button = Button(self, "Play")

    def run_game(self):
        #запуск основного цикла игры
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_aliens()
                self._update_bullets()
            self._update_screen()



    def _check_events(self):
        '''обрабатывает нажатия клавиш и события мыши'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''запускае мновую тгру при нажатии кнопки'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            #указатель мыши скрывается
            pygame.mouse.set_visible(False)

            self.aliens.empty()
            self.bullets.empty()

            #создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()


    def _check_keydown_events(self, event):
        '''реагирует на нажатие клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        '''реагирует на отпускание клавиш'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        '''создание нового снаряда и включение его в группу '''
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):

        '''обновляет позиции снарядов и уничтожает старые снаряды'''
        #обновление позиций снарядов
        self.bullets.update()
        # удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        #проверка пападаний в пришельца
        #при обнаружении попадания удвлить снаряд и пришельца
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            #self.check_high_score()


        if not self.aliens:
            # уничтожкние сушествующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()



    def _update_aliens(self):
        '''обновляет позиции всех пришельцев во флоте'''
        self._check_fleet_edges()
        self.aliens.update()
        #проверка коллизий пришелец - корабль
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #проверить добрались ли пришельцы до нижнего края
        self._check_aliens_bottom()



    def _ship_hit(self):
        '''обрабатывает столкновение корабля с пришельцем'''
        #уменьшение ships_left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

        #очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

        #создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

        #пауза
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)



    def _update_screen(self):
        '''обновляет изображения на экране и отображает новый эеран'''
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)
        self.sb.show_score()

        #кнопка play отобрадается в том случае если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_buttom()

              #отображение последнего прорисованного экрана
        pygame.display.flip()


    def _create_fleet(self):
        '''создание флота втордения'''
        #создание пришельца и вычисление кол-ва пришельцев в ряду
        #Интервал между соседними пришельцами равен ширине пришельца
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        available_spase_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_spase_x // (2 * alien_width)
        '''определяем кол-во рядов, помещающтхся на экране'''
        ship_height = self.ship.rect.height
        available_spase_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_spase_y // (2 * alien_height)

        #создание флота вторжения
        for row_mumber in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_mumber)


    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''реагирует на достижение пришельцем края экрана'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''опускает весь флот и меняет направление'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        '''проверяет, добрались ли пришельцы до нижнего края'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break


if __name__ == '__main__':
    #создание и запуск экземпляра класса
    ai = AlienInvasion()
    ai.run_game()
