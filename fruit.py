import pygame
from pygame.math import Vector2
import random

#fruit class to handle fruit placement and drawing
class FRUIT:
    def __init__(self, cell_number, cell_size):
        self.cell_number = cell_number
        self.cell_size = cell_size
        self.randomize()  #place fruit at a random location

        #load fruit image
        self.apple = pygame.image.load('Graphics/apple.png').convert_alpha()

    def draw_fruit(self, screen):
        #draw the fruit on the screen at its position
        fruit_rect = pygame.Rect(int(self.pos.x * self.cell_size), int(self.pos.y * self.cell_size), self.cell_size, self.cell_size)
        screen.blit(self.apple, fruit_rect)

    def randomize(self):
        #randomly place the fruit within the grid
        self.x = random.randint(0, self.cell_number - 1)
        self.y = random.randint(0, self.cell_number - 1)
        self.pos = Vector2(self.x, self.y)