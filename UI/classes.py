#classes.py - 3/22/2013

import pygame, random
from pygame.locals import *
import config as cf


# Gams speed
STARTING_FPS = 4
FPS_INCREMENT_FREQUENCY = 80


# Direction constants
DIRECTION_UP    = 1
DIRECTON_DOWN   = 2
DIRECTION_LEFT  = 3
DIRECTION_RIGHT = 4


# World size
WORLD_SIZE_X = 35
WORLD_SIZE_Y = 20


# Snake and food attributes
SNAKE_START_LENGTH = 4
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)


# Snake class
class Snake:

    # Initializes a Snake object
    def __init__(self, x, y, startLength):
        self.startLength = startLength
        self.startX = x
        self.startY = y
        self.reset()

    # Resets snake back to its original state
    def reset(self):
        self.pieces = []
        self.direction = 1

        for n in range(0, self.startLength):
            self.pieces.append((self.startX, self.startY + n))

    # Changes the direction of the snake
    def changeDirection(self, direction):
        # Moving in the opposite direction of current movement is not allowed
        if self.direction == 1 and direction == 2: return
        if self.direction == 2 and direction == 1: return
        if self.direction == 3 and direction == 4: return
        if self.direction == 4 and direction == 3: return

        self.direction = direction

    # Returns the head piece of the snake
    def getHead(self):
        return self.pieces[0]

    # Returns the tail piece of the snake
    def getTail(self):
        return self.pieces[len(self.pieces) - 1]

    # Updates snake by moving blocks in direction of movement
    def update(self):
        (headX, headY) = self.getHead()
        head = ()

        # Create new piece that is the new head of the snake
        if self.direction == 1: head = (headX, headY - 1)
        elif self.direction == 2: head = (headX, headY + 1)
        elif self.direction == 3: head = (headX - 1, headY)
        elif self.direction == 4: head = (headX + 1, headY)

        # Remove tail of the snake and add a new head
        self.pieces.insert(0, head)
        self.pieces.pop()

    # Adds a new piece to the end of the snake
    def grow(self):
        (tx, ty) = self.getTail()
        piece = ()

        if self.direction == 1: piece = (tx, ty + 1)
        elif self.direction == 2: piece = (tx, ty - 1)
        elif self.direction == 3: piece = (tx + 1, ty)
        elif self.direction == 4: piece = (tx - 1, ty)

        self.pieces.append(piece)

    # Are two pieces of the snake occupying the same block?
    def collidesWithSelf(self):
        """
        # Because of the way new pieces are added when the snake grows, eating a
        # new food block could cause the snake to die if it's in a certain position. 
        # So instead of checking if any of the spots have two pieces at once, the new
        # algorithm only checks if the position of the head piece contains more than one block.

        for p in self.pieces:
            if len(self.pieces) - len([c for c in self.pieces if c != p]) > 1: return True
        return False
        """

        return len([p for p in self.pieces if p == self.getHead()]) > 1


# SnakeGame class
class SnakeGame:

    # Initializes SnakeGame object with pre-initialized objects and configuration settings
    def __init__(self, window, screen, clock, font):
        self.window = window
        self.screen = screen
        self.clock = clock
        self.font = font

        self.fps = STARTING_FPS
        self.ticks = 0
        self.playing = True
        self.score = 0

        self.nextDirection = DIRECTION_UP
        self.sizeX = WORLD_SIZE_X
        self.sizeY = WORLD_SIZE_Y
        self.food = []
        self.snake = Snake(WORLD_SIZE_X / 2, WORLD_SIZE_Y / 2, SNAKE_START_LENGTH)

        self.addFood()

    # Adds a new piece of food to a random block
    def addFood(self):
        fx = None
        fy = None

        while fx is None or fy is None or (fx, fy) in self.food:
            fx = random.randint(1, self.sizeX)
            fy = random.randint(1, self.sizeY)

        self.food.append((fx, fy))

    # Handles input from keyboard
    def input(self, events):
        for e in events:
            if e.type == QUIT:
                return False

            elif e.type == KEYUP:
                if   e.key == K_w: self.nextDirection = 1
                elif e.key == K_s: self.nextDirection = 2
                elif e.key == K_a: self.nextDirection = 3
                elif e.key == K_d: self.nextDirection = 4
                elif e.key == K_SPACE and not self.playing: 
                    self.reset()

        return True

    # Update gamestate -- update snake and check for death
    def update(self):
        self.snake.changeDirection(self.nextDirection)
        self.snake.update()

        # If snake hits a food block, then consume the food, add new food and grow the snake
        for food in self.food: 
            if self.snake.getHead() == food:
                self.food.remove(food)
                self.addFood()
                self.snake.grow()
                self.score += len(self.snake.pieces) * 50

        # If snake collides with self or the screen boundaries, then game over
        (hx, hy) = self.snake.getHead()
        if self.snake.collidesWithSelf() or hx < 1 or hy < 1 or hx > self.sizeX or hy > self.sizeY:
            self.playing = False

    # Resets the game
    def reset(self):
        cf.arcade_game=False
        pygame.event.post(cf.gs.first_game_event)


    # Draws snake and food objects to the screen
    def draw(self):
        self.screen.fill((45, 45, 45))

        (width, height) = self.window.get_size()
        blockWidth = int(width / self.sizeX)
        blockHeight = int(height / self.sizeY)

        # Draw pieces of snake
        for (px, py) in self.snake.pieces: 
            pygame.draw.rect(self.screen, SNAKE_COLOR, (blockWidth * (px-1), blockHeight * (py-1), blockWidth, blockHeight))

        # Draw food objects
        image = pygame.image.load('24x24trump.jpg')
        for (fx, fy) in self.food:
            #pygame.draw.rect(self.screen, FOOD_COLOR, (blockWidth * (fx-1), blockHeight * (fy-1), blockWidth, blockHeight))
        
            self.screen.blit(image,(blockWidth * (fx-1), blockHeight * (fy-1), blockWidth, blockHeight))
        pygame.display.flip()

    # Draws the death message to the screen
    def drawDeath(self):
        self.screen.fill((255, 0, 0))
        self.screen.blit(self.font.render("Game over! Press Space to go back to day", 1, (255, 255, 255)), (200, 150))
        self.screen.blit(self.font.render("Your score is: %d" % self.score, 1, (255, 255, 255)), (340, 180))
        pygame.display.flip()

    # Run the main game loop
    def run(self, events):
        if not self.input(events): return False

        if self.playing: 
            self.update()
            self.draw()
        else: self.drawDeath()

        self.clock.tick(self.fps)

        self.ticks += 1
        if self.ticks % FPS_INCREMENT_FREQUENCY == 0: self.fps += 1

        return True
