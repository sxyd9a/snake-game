import pygame
import sys
from main_game import MAIN

pygame.mixer.pre_init(44100,-16,2,512) #handle sound delay
pygame.init()

#constants
cell_size = 38
cell_number = 16
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

#initialize the main game object
main_game = MAIN(cell_number, cell_size)

#setup timer event for controlling snake movement speed
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  #150 milliseconds per move

#main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != pygame.Vector2(0, 1):
                main_game.snake.direction = pygame.Vector2(0, -1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != pygame.Vector2(-1, 0):
                main_game.snake.direction = pygame.Vector2(1, 0)
            if event.key == pygame.K_DOWN and main_game.snake.direction != pygame.Vector2(0, -1):
                main_game.snake.direction = pygame.Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction != pygame.Vector2(1, 0):
                main_game.snake.direction = pygame.Vector2(-1, 0)

    #render everything
    screen.fill((175, 215, 70))  #background color
    main_game.draw_elements(screen)
    pygame.display.update()
    clock.tick(60)