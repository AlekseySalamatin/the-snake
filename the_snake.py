from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER_X, SCREEN_CENTER_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

# Направления движения:
UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)
LIST_OF_DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position=(SCREEN_CENTER_X, SCREEN_CENTER_Y),
        body_color=BOARD_BACKGROUND_COLOR
    ):
        # Для любого объекта класса или дочерних классов
        # position - это список кортежей
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстракция для наследования"""
        pass


class Apple(GameObject):
    """Класс яблока."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Случайная позиция яблока"""
        x = randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE
        y = randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pygame.Rect(self.position[0], self.position[1],
                           GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [self.position]
        self.length = 1
        self.direction = (GRID_SIZE, 0)  # Движение вправо по умолчанию
        self.next_direction = None

    def get_head_position(self):
        """Определение положения головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Определение следующего направления змейки"""
        if self.next_direction:
            # Запрещаем разворот на 180 градусов
            current_x, current_y = self.direction
            next_x, next_y = self.next_direction
            if (current_x * -1 != next_x) or (current_y * -1 != next_y):
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Логика движения змейки"""
        self.update_direction()
        cur_x, cur_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_x = (cur_x + dir_x) % SCREEN_WIDTH  # Проход сквозь стены
        new_y = (cur_y + dir_y) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Проверка столкновения с самим собой
        if new_head in self.positions[1:]:
            return False

        # Добавляем новый нулевой элемент,
        # удаляем последний элемент списка positions,
        # если длина змейки меньше количества элементов списка position.
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        """Возвращение начального положения при столкновении змейки с собой"""
        self.positions = [(SCREEN_CENTER_X, SCREEN_CENTER_Y)]
        self.length = 1
        choice_of_direction = choice(LIST_OF_DIRECTIONS)
        # Начало движения в случайном направлении
        self.direction = (choice_of_direction[0], choice_of_direction[1])
        self.next_direction = None

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                game_object.next_direction = RIGHT


def main():
    """Игровой цикл"""
    pygame.init()
    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        # Движение змейки
        no_collisions = snake.move()
        if not no_collisions:
            snake.reset()
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        # Поедание яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()
        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
