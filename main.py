import os
import sys
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, app, tile_type, pos_x, pos_y):
        super().__init__(app.tiles_group, app.all_sprites)
        if tile_type == 'empty':
            self.image = app.load_image('fon_v_igre.png')

        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x, app.tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, app, pos_x, pos_y):
        super().__init__(app.player_group, app.all_sprites)
        self.image = app.load_image("mar.png")
        self.rect = self.image.get_rect().move(
            app.tile_width * pos_x + 15, app.tile_height * pos_y + 5)

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        if x == 0 and y == 0:
            self.kill()


class App:
    def __init__(self):
        pygame.init()
        self.width, self.height = 550, 550
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Mario')
        self.fps = 0
        pygame.key.set_repeat(200, 70)
        self.all_sprites = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.hero = None
        self.tile_width = self.tile_height = 50
        self.player, self.level_x, self.level_y = self.generate_level(self.load_level('level_1.txt'))

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, name, colorkey=None):
        fullname = os.path.join('data', name)
        # если файл не существует, то выходим
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()
        image = pygame.image.load(fullname)
        if colorkey is not None:
            image = image.convert()
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
        return image

    def run_game(self):
        run = True
        self.game_over = 0
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.pause_screen()
                if event.type == pygame.KEYDOWN:
                    key = pygame.key.get_pressed()
                    if key[pygame.K_DOWN] or key[pygame.K_s]:
                        self.player.update(0, 5)
                    if key[pygame.K_LEFT] or key[pygame.K_a]:
                        self.player.update(-5, 0)
                    if key[pygame.K_RIGHT] or key[pygame.K_d]:
                        self.player.update(5, 0)
                    if key[pygame.K_UP] or key[pygame.K_w]:
                        self.player.update(0, -5)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    self.game_over += 1
                if self.game_over == 5:
                    self.player.update(0, 0)
                    self.end_screen()
                    run = False
            # update

            # render
            self.screen.fill(pygame.Color('blue'))
            self.tiles_group.draw(self.screen)
            self.player_group.draw(self.screen)
            # изменяем ракурс камеры
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start_screen(self):
            intro_text = ["ЗАСТАВКА", "", "", "",
                          "ИСПОЛЬЗУЙТЕ СТРЕЛОЧКИ ДЛЯ ДВИЖЕНИЯ", "",
                          "ЛУЧШИЙ СЧЁТ", "", "", "", "", "", "", "",
                          "НАЖМИТЕ ЧТОБЫ ИГРАТЬ"]

            fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
            self.screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                self.screen.blit(string_rendered, intro_rect)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    elif event.type == pygame.KEYDOWN or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                        self.run_game()  # начинаем игру
                pygame.display.flip()
                self.clock.tick(self.fps)

    def pause_screen(self):
            intro_text = ["ПАУЗА", "", "", "",
                          "", "",
                          "", "", "", "", "", "", "",
                          "НАЖМИТЕ Esc ЧТОБЫ ПРОДОЛЖИТЬ",
                          "НАЖМИТЕ Backspace ЧТОБЫ ВЫЙТИ"]

            fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
            self.screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                self.screen.blit(string_rendered, intro_rect)

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.run_game()  # начинаем игру
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        self.player.update(0, 0)
                        self.player, self.level_x, self.level_y = self.generate_level(self.load_level('level_1.txt'))
                        self.start_screen()
                pygame.display.flip()
                self.clock.tick(self.fps)

    def end_screen(self):
            intro_text = ["ЗАСТАВКА", "", "", "",
                          "ВАШ СЧЁТ", "",
                          "ЛУЧШИЙ СЧЁТ", "", "", "", "", "", "",
                          "НАЖМИТЕ Esc ЧТОБЫ ВЫЙТИ",
                          "НАЖМИТЕ ЧТОБЫ НАЧАТЬ СНАЧАЛА"]

            fon = pygame.transform.scale(self.load_image('fon.jpg'), (self.width, self.height))
            self.screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 50
            for line in intro_text:
                string_rendered = font.render(line, 1, pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                self.screen.blit(string_rendered, intro_rect)
            self.player, self.level_x, self.level_y = self.generate_level(self.load_level('level_1.txt'))

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                    elif event.type == pygame.KEYDOWN and not event.key == pygame.K_ESCAPE or \
                            event.type == pygame.MOUSEBUTTONDOWN:
                        self.run_game()  # начинаем игру
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.start_screen()
                pygame.display.flip()
                self.clock.tick(self.fps)

    def load_level(self, filename):
        filename = "data/" + filename
        # читаем уровень, убирая символы перевода строки
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]

        # и подсчитываем максимальную длину
        max_width = max(map(len, level_map))

        # дополняем каждую строку пустыми клетками ('.')
        return list(map(lambda x: x.ljust(max_width, '.'), level_map))

    def generate_level(self, level):
        new_player, x, y = None, None, None
        for y in range(len(level)):
            for x in range(len(level[y])):
                if level[y][x] == '.':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '#':
                    Tile(self, 'empty', x, y)
                elif level[y][x] == '@':
                    Tile(self, 'empty', x, y)
                    new_player = Player(self, x, y)
        # вернем игрока, а также размер поля в клетках
        return new_player, x, y


if __name__ == '__main__':
    app = App()
    app.start_screen()
    app.run_game()
