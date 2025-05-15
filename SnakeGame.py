import pygame, sys, random
from pygame.math import Vector2

#snake class to handle snake's body, movement, and rendering
class SNAKE:
    def __init__(self):
        #snake starts with 3 body segments
        self.body = [Vector2(5,10), Vector2(6,10), Vector2(7,10)]
        #initial movement direction (right)
        self.direction = Vector2(1,0)
        #flag to indicate if a new block should be added
        self.new_block = False

    def draw_snake(self):
        #draw each block of the snake on the screen
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183,111,122), block_rect)

    def move_snake(self):
        if self.new_block == True:
            #move snake forward and grow by keeping all segments
            body_copy = self.body[:]  
            body_copy.insert(0, body_copy[0] + self.direction)  #add a new head in the direction
            self.body = body_copy[:]  #update snake body
            self.new_block = False
        else:
            #move snake forward in current direction by removing tail
            body_copy = self.body[:-1]  #remove the tail segment
            body_copy.insert(0, body_copy[0] + self.direction)  #add a new head in the direction
            self.body = body_copy[:]  #update snake body

    def add_block(self):
        #trigger snake to grow in the next move
        self.new_block = True

#fruit class to handle fruit position and rendering
class FRUIT:
    def __init__(self):
        #generate random position for fruit on grid
        self.randomize()

    def draw_fruit(self):
        #draw fruit on screen at its grid position
        x_pos = int(self.x * cell_size)
        y_pos = int(self.y * cell_size)
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, (126,166,114), fruit_rect)

    def randomize(self):
        #assign a new random grid position to the fruit
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        #update snake's position and check for collisions
        self.snake.move_snake()
        self.check_collision()

    def draw_elements(self):
        #draw all game elements: fruit and snake
        self.fruit.draw_fruit()         
        self.snake.draw_snake() 

    def check_collision(self):
        #check if snake's head has collided with the fruit
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()  #relocate fruit
            self.snake.add_block()  #grow snake


#initialize pygame/constants
pygame.init()
cell_size = 25  #size of each cell (square)
cell_num = 20   #number of cells in the grid (width and height)
screen = pygame.display.set_mode((cell_num * cell_size, cell_num * cell_size))  #game window
clock = pygame.time.Clock()  #clock to control frame rate

main_game = MAIN()

#pygame event for updating game logic
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)  #trigger SCREEN_UPDATE every 150ms

#game loop -
while True:
    #event loop to handle inputs and timed events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #exit the game
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            #move snake on every SCREEN_UPDATE event
            main_game.update()
        if event.type == pygame.KEYDOWN: #move snake depending on pressed key
            if event.key == pygame.K_UP:
                main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                main_game.snake.direction = Vector2(-1,0)

    #draw game background and all elements
    screen.fill((175,215,70))  #fill background with green
    main_game.draw_elements()
    pygame.display.update()    #refresh display
    clock.tick(60)             #limit loop to 60 frames per second