import pygame
from pygame.math import Vector2
from snake import SNAKE
from fruit import FRUIT

#game class to manage logic, collision, and score
class MAIN:
    def __init__(self, cell_number, cell_size):
        self.cell_number = cell_number
        self.cell_size = cell_size
        self.snake = SNAKE()
        self.fruit = FRUIT(cell_number, cell_size)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self, screen):
        self.draw_grass(screen)
        self.fruit.draw_fruit(screen)
        self.snake.draw_snake(screen, self.cell_size)
        self.draw_score(screen)

    def check_collision(self):
        #check if snake eats fruit
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        #prevent fruit from spawning on snake's body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        #check if snake hits wall
        if not 0 <= self.snake.body[0].x < self.cell_number or not 0 <= self.snake.body[0].y < self.cell_number:
            self.game_over()

        #check if snake hits itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        #reset game state
        self.snake.reset()

    def draw_grass(self, screen):
        #draw checkered grass pattern
        grass_color = (167, 209, 61)
        for row in range(self.cell_number):
            if row % 2 == 0:
                for col in range(self.cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(self.cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self, screen):
        #draw score using number of snake blocks - 3
        score_text = str(len(self.snake.body) - 3)
        font = pygame.font.Font("Font/PoetsenOne-Regular.ttf", 25)
        score_surface = font.render(score_text, True, (56,74,12))  #color of score text
        score_x = int(self.cell_size * self.cell_number - 60)
        score_y = int(self.cell_size * self.cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple = pygame.image.load('Graphics/apple.png').convert_alpha()
        apple_rect = apple.get_rect(midright=(score_rect.left - 6, score_rect.centery))

        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)