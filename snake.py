import math
import time
import random
import pygame

pygame.init()
WIDTH = 500
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [[240, 240]]
        self.size = 20
        self.color = (0, 0, 0)
        self.x_change = 0
        self.y_change = 0

    def change_direction(self, key):
        if key == pygame.K_w:
            self.x_change = 0
            self.y_change = -self.size
        elif key == pygame.K_s:
            self.x_change = 0
            self.y_change = self.size
        elif key == pygame.K_a:
            self.x_change = -self.size
            self.y_change = 0
        elif key == pygame.K_d:
            self.x_change = self.size
            self.y_change = 0

    def move(self):
        for index, square in enumerate(reversed(self.body)):
            # Index if list wasn't reversed
            original_index = abs((len(self.body) - 1) - index)

            # Moving position of the head
            if index == len(self.body) - 1:
                body_x = square[0] + self.x_change
                body_y = square[1] + self.y_change
                self.body[original_index] = [body_x, body_y]
            else:
                # Each section of the body takes the coordinates of the section in front of it
                body_x = self.body[original_index - 1][0]
                body_y = self.body[original_index - 1][1]
                self.body[original_index] = [body_x, body_y]

    def draw(self, screen):
        for i, section in enumerate(self.body):
            pygame.draw.rect(screen, self.color, (section[0], section[1], self.size, self.size))

    def in_bounds(self):
        x = self.body[0][0]
        y = self.body[0][1]
        return (-20 < x < 500) and (-20 < y < 500)

    def on_food(self, food):
        snake_rect = pygame.Rect(self.body[0][0], self.body[0][1], self.size, self.size)
        return snake_rect.colliderect(food.rect)

    def grow(self):
        # New section is 20 px away from the tail section
        tail = self.body[-1]
        new_section = []
        # New section is added on in the direction that the snake is already moving
        if self.x_change != 0:
            new_section.append(tail[0] + self.size)
            new_section.append(tail[1])
        else:
            new_section.append(tail[0])
            new_section.append(tail[1] + self.size)
        self.body.append(new_section)

    def on_self(self) -> bool:
        head = self.body[0]
        for index, section in enumerate(self.body):
            if index > 0:
                if head == section:
                    return True
        return False


class Food:
    def __init__(self):
        self.size = 20
        # Chooses random coordinates that are inside the grid boxes
        self.x = random.choice([i * 20 for i in range(25)])
        self.y = random.choice([i * 20 for i in range(25)])
        # Create rect to check if the snake collides with it
        self.rect = pygame.Rect(self.x, self.y, 20, 20)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))


def draw_grid(screen):
    for i in range(25):
        for j in range(25):
            pygame.draw.line(screen, (0, 0, 0), (i * 20, j), (i * 20, 500))
            pygame.draw.line(screen, (0, 0, 0), (i, j * 20), (500, j * 20))


def display_score(screen, snake):
    score = len(snake.body) - 1
    text = f'Score: {score}'
    font = pygame.font.SysFont(None, 50)
    display_text = font.render(text, True, (0, 255, 255))
    screen.blit(display_text, (10, 10))


def update_screen(screen, snake, food):
    screen.fill((150, 150, 150))
    draw_grid(screen)
    display_score(screen, snake)
    snake.draw(screen)
    food.draw(screen)
    pygame.display.update()


def game_over(screen):
    text = 'Game Over! Press Any key to restart or Q to quit!'
    font = pygame.font.SysFont(None, 28)
    display_text = font.render(text, True, (0, 255, 255))
    screen.blit(display_text, (20, 250))
    pygame.display.update() 


def play_again():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                else:
                    return True
def main():
    snake = Snake()
    food = Food()
    while True:
        update_screen(screen, snake, food)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.KEYDOWN:
                snake.change_direction(event.key)
                
        snake.move()
        
        if not snake.in_bounds():
            break
            
        if snake.on_food(food):
            # Create a new food object when old one was eaten
            food = Food()
            snake.grow()
            continue

        if snake.on_self():
            break
        clock.tick(15)

while True:
    main()
    game_over(screen)
    time.sleep(1)
    if not play_again():
        pygame.quit()
        break

