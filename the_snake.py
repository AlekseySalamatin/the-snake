import random

import pygame as pg

# Инициализация Pygame
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_X = (GRID_WIDTH // 2) * GRID_SIZE
SCREEN_CENTER_Y = (GRID_HEIGHT // 2) * GRID_SIZE
CENTER = (SCREEN_CENTER_X, SCREEN_CENTER_Y)

# Направления движения:
DIR_UP = (0, -GRID_SIZE)
DIR_DOWN = (0, GRID_SIZE)
DIR_LEFT = (-GRID_SIZE, 0)
DIR_RIGHT = (GRID_SIZE, 0)

# Словарь противоположных направлений (для блокировки разворота в себя)
OPPOSITE_DIRECTIONS = {
    DIR_UP: DIR_DOWN,
    DIR_DOWN: DIR_UP,
    DIR_LEFT: DIR_RIGHT,
    DIR_RIGHT: DIR_LEFT
}

# Словарь соответствия клавиш направлениям движения
KEY_TO_DIRECTION = {
    pg.K_UP: DIR_UP,
    pg.K_DOWN: DIR_DOWN,
    pg.K_LEFT: DIR_LEFT,
    pg.K_RIGHT: DIR_RIGHT
}

# Цвета
BOARD_BACKGROUND_COLOR = (200, 200, 200)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 150, 0)

SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка. Для выхода из игры нажмите Esc.')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        self.position = None

    def draw_cell(self, position, color=None):
        """Отрисовывает ровно одну ячейку
        выбранным цветом на глобальном screen.
        """
        cell_color = color or self.body_color
        rect = pg.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, cell_color, rect)


class Apple(GameObject):
    """Класс яблока. Сам хранит свой цвет."""

    def __init__(self, occupied_positions, body_color=APPLE_COLOR):
        super().__init__()
        self.body_color = body_color
        self.randomize_position(occupied_positions, draw=False)

    def randomize_position(self, occupied_positions, draw=True):
        """Стирает старое яблоко цветом фона и генерирует новое."""
        if draw and self.position:
            self.draw_cell(self.position, color=BOARD_BACKGROUND_COLOR)

        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_positions:
                break

        if draw:
            self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки. Сам хранит свой цвет."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__()
        self.body_color = body_color
        self.last_tail_position = None
        self.length = 1
        self.direction = DIR_RIGHT

    def reset(self):
        """Сброс состояния со стиранием всего экрана."""
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.length = 1
        self.position = [CENTER]
        self.direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])
        self.last_tail_position = None
        self.draw_cell(self.get_head_position())

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.position[0]

    def update_direction(self, new_direction):
        """Безопасная смена направления
        с использованием словаря соответствий.
        """
        if OPPOSITE_DIRECTIONS.get(new_direction) == self.direction:
            return
        self.direction = new_direction

    def get_next_head_position(self):
        """Предсказывает, где окажется голова на следующем шаге."""
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        return ((cur_x + dir_x) % SCREEN_WIDTH,
                (cur_y + dir_y) % SCREEN_HEIGHT)

    def move(self):
        """Логика перемещения. Вычисляет новую голову и старый хвост."""
        new_head = self.get_next_head_position()

        if new_head in self.position:
            return False

        self.position.insert(0, new_head)

        if len(self.position) > self.length:
            self.last_tail_position = self.position.pop()
        else:
            self.last_tail_position = None

        return True


def handle_input(snake):
    """Обрабатывает события ввода и выхода из игры."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            new_dir = KEY_TO_DIRECTION.get(event.key)
            if new_dir:
                snake.update_direction(new_dir)


def main():
    """Игровой цикл"""
    snake = Snake()
    snake.reset()

    apple = Apple(occupied_positions=snake.position)
    apple.draw_cell(apple.position)

    while True:
        handle_input(snake)

        # Проверяем поедание яблока ДО совершения хода
        if snake.get_next_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.position)

        # Совершаем движение
        if not snake.move():
            # Самоукус
            snake.reset()
            apple.randomize_position(snake.position)
        else:
            # Стираем старый хвост цветом фона (если змейка не росла)
            if snake.last_tail_position:
                snake.draw_cell(snake.last_tail_position,
                                color=BOARD_BACKGROUND_COLOR)

            # Рисуем новую голову основным цветом змейки
            snake.draw_cell(snake.get_head_position())

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
