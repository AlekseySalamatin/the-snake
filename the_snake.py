# Пожалуйста, прочитайте readme

from random import choice, randint

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
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Словарь противоположных направлений (для блокировки разворота в себя)
OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}

# Цвета
BOARD_BACKGROUND_COLOR = (200, 200, 200)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 150, 0)

SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка. Для выхода из игры нажмите Esc.')
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=CENTER, body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки (переопределяется в дочерних классах)."""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        super().__init__()
        self.body_color = body_color
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Случайная позиция яблока, не занятая змейкой."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        rect = pg.Rect(self.position[0], self.position[1],
                       GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(position=CENTER)
        self.body_color = body_color
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Определение положения головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Определение следующего направления змейки."""
        if self.next_direction:
            if OPPOSITE_DIRECTIONS.get(self.next_direction) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Логика движения змейки."""
        self.update_direction()
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (cur_x + dir_x) % SCREEN_WIDTH
        new_y = (cur_y + dir_y) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        if new_head in self.positions:
            return False

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        """Возвращение начального положения при столкновении змейки с собой."""
        self.positions = [CENTER]
        self.length = 1
        self.direction = choice(DIRECTIONS)
        self.next_direction = None

    def draw(self):
        """Отрисовка всех сегментов змейки."""
        for position in self.positions:
            rect = pg.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pg.draw.rect(screen, self.body_color, rect)


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            elif event.key == pg.K_UP:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    """Игровой цикл."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        handle_keys(snake)

        if not snake.move():
            snake.reset()
            apple.randomize_position(snake.positions)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Отрисовка кадра
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
