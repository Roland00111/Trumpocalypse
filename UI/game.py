try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    print 'Import pygame sdl2 error.'
    pass
    
import pygame, sys, os
from pygame.locals import *
from classes import *

def main():
    pygame.init()
    pygame.display.set_caption('PyGame Snake')

    window = pygame.display.set_mode((854, 480))
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 20)

    game = SnakeGame(window, screen, clock, font)

    while game.run(pygame.event.get()):
        pass

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
