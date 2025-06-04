import pygame, sys, random
from pygame.math import Vector2

#snake class to handle snake's body, movement, and rendering
class SNAKE:
    def __init__(self):
        #snake starts with 3 body segments
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        #initial movement direction (right)
        self.direction = Vector2(0,0)
        #flag to indicate if a new block should be added
        self.new_block = False

        #load in every graphic representing parts of a snake
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        #import snake eating sound
        self.crunch_sound = pygame.mixer.Sound("Sound/crunch.wav")


    def draw_snake(self):
        self.update_head_graphics() #update head orientation based on movements
        self.update_tail_graphics() #update tail orientation based on movements

        #draw each block of the snake on the screen
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)  #calculate the pixel x-position of the block
            y_pos = int(block.y * cell_size)  #calculate the pixel y-position of the block
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)  #Create a rectangle for drawing

            if index == 0:
                #head of the snake
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                #tail of the snake
                screen.blit(self.tail, block_rect)
            else:
                #middle part of the snake (body segments)
                previous_block = self.body[index + 1] - block  #Vector from current to next block
                next_block = self.body[index - 1] - block      #Vector from current to previous block

                if previous_block.x == next_block.x:
                    #the segment is vertically aligned (same x-axis)
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    #the segment is horizontally aligned (same y-axis)
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    #the segment is a corner piece
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        #top-left corner (coming from right or down)
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        #bottom-left corner (coming from right or up)
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        #top-right corner (coming from left or down)
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        #bottom-right corner (coming from left or up)
                        screen.blit(self.body_br, block_rect)


    def update_head_graphics(self):
        #update head graphic based on the direction of movement
        head_relation = self.body[1] - self.body[0]  #compare head with next segment
        if head_relation == Vector2(1,0): self.head = self.head_left    #moving left
        if head_relation == Vector2(-1,0): self.head = self.head_right  #moving right
        if head_relation == Vector2(0,1): self.head = self.head_up      #moving up
        if head_relation == Vector2(0,-1): self.head = self.head_down   #moving down

    def update_tail_graphics(self):
        #update tail graphic based on the direction of movement
        tail_relation = self.body[-2] - self.body[-1]  #compare tail with next segment
        if tail_relation == Vector2(1,0): self.tail = self.tail_left    #moving left
        if tail_relation == Vector2(-1,0): self.tail = self.tail_right  #moving right
        if tail_relation == Vector2(0,1): self.tail = self.tail_up      #moving up
        if tail_relation == Vector2(0,-1): self.tail = self.tail_down   #moving down




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

    def play_crunch_sound(self):
        self.crunch_sound.play() #trigger snake crunching sound 

    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)] #reset snake to intial start position
        self.direction = Vector2(0,0) #reset snake direction


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
        screen.blit(apple,fruit_rect)

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
        self.check_fail()

    def draw_elements(self):
        #draw all game elements
        self.draw_grass()
        self.fruit.draw_fruit()         
        self.snake.draw_snake() 
        self.draw_score()

    def check_collision(self):
        #check if snake's head has collided with the fruit
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()  #relocate fruit
            self.snake.add_block()  #grow snake
            self.snake.play_crunch_sound() #snake crunching apple sound

        #ensure fruit doesn't appear on a part of the snake's body
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        #check if snake hits the wall
        if not 0 <= self.snake.body[0].x < cell_num or not 0 <= self.snake.body[0].y < cell_num:
            self.game_over()
    
        #check if snake collides with itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        self.snake.reset() #restart game for user

    def draw_grass(self):
        grass_color = (167, 209, 61)  #a greenish color for the grass

        for row in range(cell_num):
            for col in range(cell_num):
                #this condition creates a checkerboard pattern:
                #only draw on cells where the sum of row and col is even
                if (row + col) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, grass_color, grass_rect)
    
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)  #current score
        score_surface = game_font.render(score_text, True, (56, 74, 12))  #render text
        score_x = int(cell_size * cell_num - 60)
        score_y = int(cell_size * cell_num - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))  #text position
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))  #apple icon position
        bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width+score_rect.width+6,apple_rect.height) #score background position

        pygame.draw.rect(screen,(167,209,61),bg_rect) #draw score background
        screen.blit(score_surface, score_rect)  #draw score
        screen.blit(apple, apple_rect)  #draw apple icon
        pygame.draw.rect(screen,(56, 74, 12),bg_rect,2) #draw frame around score





#initialize pygame/constants
pygame.mixer.pre_init(44100,-16,2,512) #handle sound delay
pygame.init()
cell_size = 38  #size of each cell (square)
cell_num = 16   #number of cells in the grid (width and height)
screen = pygame.display.set_mode((cell_num * cell_size, cell_num * cell_size))  #game window
clock = pygame.time.Clock()  #clock to control frame rate
apple = pygame.image.load("Graphics/apple.png").convert_alpha() #load in the apple graphic for usage
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)


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
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    #draw game background and all elements
    screen.fill((175,215,70))  #fill background with green
    main_game.draw_elements()
    pygame.display.update()    #refresh display
    clock.tick(60)             #limit loop to 60 frames per second