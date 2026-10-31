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
BORDER_COLOR = (40, 40, 40)

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

    def draw_cell(self, position, color=None):
        """Метод отрисовки одной ячейки на игровом поле."""
        draw_color = color or self.body_color
        rect = pg.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pg.draw.rect(screen, draw_color, rect)
        if draw_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Базовый метод отрисовки (переопределяется в дочерних классах)."""


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self, occupied_positions=None, body_color=APPLE_COLOR):
        super().__init__(body_color=body_color)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Случайная позиция яблока, не занятая змейкой."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color=body_color)
        self.reset()

    def get_head_position(self):
        """Определение положения головы змейки."""
        return self.positions[0]

    def update_direction(self, new_direction):
        """Определение следующего направления змейки."""
        if OPPOSITE_DIRECTIONS.get(new_direction) != self.direction:
            self.direction = new_direction

    def move(self):
        """Логика движения змейки."""
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        self.positions.insert(
            0,
            ((cur_x + dir_x) % SCREEN_WIDTH, (cur_y + dir_y) % SCREEN_HEIGHT)
        )

        self.last = (
            self.positions.pop()
            if len(self.positions) > self.length
            else None
        )

    def reset(self):
        """Возвращение начального положения змейки."""
        self.positions = [CENTER]
        self.length = 1
        self.direction = choice(DIRECTIONS)
        self.last = None  # Инициализация / сброс отрезанного сегмента
        screen.fill(BOARD_BACKGROUND_COLOR)  # Очищаем всё поле

    def draw(self):
        """Отрисовка только головы и затирание хвоста
        с помощью метода родительского класса .draw_cell
        """
        # Рисуем новую голову змейки
        self.draw_cell(self.get_head_position())

        # Стираем старый хвост цветом фона поля
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if (
            event.type == pg.QUIT
            or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
        ):
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                snake.update_direction(UP)
            elif event.key == pg.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pg.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pg.K_RIGHT:
                snake.update_direction(RIGHT)


def main():
    """Игровой цикл."""
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)

    while True:
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
