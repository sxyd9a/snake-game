import pygame, sys, random
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.x = random.randint(0,cell_num - 1)
        self.y = random.randint(0,cell_num - 1)
        self.pos = Vector2(self.x,self.y) #position of fruit

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x*cell_size, self.pos.y*cell_size, cell_size, cell_size)
        pygame.draw.rect(screen,(126,166,114),fruit_rect) #place rect on screen


pygame.init()
cell_size = 25
cell_num = 20
screen = pygame.display.set_mode((cell_num*cell_size, cell_num*cell_size)) #display window size
clock = pygame.time.Clock()

fruit = FRUIT()

while True: #game loop

    for event in pygame.event.get(): #event loop
        if event.type == pygame.QUIT: #close game
            pygame.quit()
            sys.exit()
    screen.fill((175,215,70)) #fill screen with specified RGB (0-255)
    fruit.draw_fruit()
    #draw all game elements
    pygame.display.update()
    clock.tick(60) #run game loop at 60 fps