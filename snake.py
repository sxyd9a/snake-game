import pygame
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

    def draw_snake(self, screen, cell_size):
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