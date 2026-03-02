import pygame,sys, random
from pygame.math import Vector2

pygame.init()
title_font = pygame.font.Font(None, 50)
score_font = pygame.font.Font(None, 40)

blue_color = (0, 0, 139)
yellow_color = (225, 225, 0)

cell_size = 30
number_of_cell = 25

off_set = 75

class food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)

    def draw(self):
        food_rect = pygame.Rect(off_set + self.position.x * cell_size, off_set + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cell - 1)
        y = random.randint(0, number_of_cell - 1)
        return Vector2(x, y)

    def generate_random_pos(self, snake_body):

        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

class snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
        self.add_segment = False

    def draw(self):
        for segment in self.body:
            segment_rect = (off_set + segment.x * cell_size, off_set + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, yellow_color, segment_rect, 0, 6)

    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
           self.add_segment = False
        else:
            self.body = self.body[:-1]

    def reset(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)


class game:
    def __init__(self):
        self.snake = snake()
        self.food = food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0

    def draw(self):
        self.food.draw()
        self.snake.draw()

    def update(self):
        if self.state == "RUNNING":
          self.snake.update()
          self.check_collision_with_food()
          self.check_collision_with_edges()
          self.check_collision_with_tail()

    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
           self.food.position = self.food.generate_random_pos(self.snake.body)
           self.snake.add_segment = True
           self.score += 1

    def check_collision_with_edges(self):
        if self.snake.body[0] .x == number_of_cell or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cell or self.snake.body[0].y == -1:
            self.game_over()

    def game_over(self):
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0

    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()

screen = pygame.display.set_mode((2*off_set + cell_size*number_of_cell, 2*off_set + cell_size*number_of_cell))

pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

game = game()
food_surface = pygame.image.load("Graphics/food.png")

snake_update = pygame.USEREVENT
pygame.time.set_timer(snake_update, 200)

while True:
    for event in pygame.event.get():
        if event.type == snake_update:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game.state == "STOPPED":
                game.state = "RUNNING"
            if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
               game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                game.snake.direction = Vector2(1, 0)

    screen.fill(blue_color)
    pygame.draw.rect(screen, yellow_color,
    (off_set -5, off_set-5, cell_size*number_of_cell+10, cell_size*number_of_cell+10), 5)
    game.draw()
    title_surface = title_font.render("Snake", True, yellow_color)
    score_surface = score_font.render(str(game.score), True, yellow_color)
    screen.blit(title_surface, (off_set-5, 20))
    screen.blit(score_surface, (off_set-5, off_set + cell_size*number_of_cell + 10))

    pygame.display.update()
    clock.tick(60)