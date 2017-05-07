import config as cf
import pygame
import random
import PygameUI
import math
import copy
import eventsloop as EVENTSLOOP
from TextWrap import *
from pygame.locals import *
import game
import sys
import ToGame as TOGAME

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()
                
class GameState:
    '''There is only one GameState instance. This is created when the
    program is first started. A global variable cf.gs is 
    made to reference this instance. Thus throughout the program
    it is possible to reference this instance.
    The GameState instance creates an instance of the Game class
    and then it creates an instance of the EventsLoop class.
    Passing in a list of keypress indexes (integers) allows the
    program to simulate a game by hitting the "Enter Key" on specified
    menu items.
    There is a reset function that is called when the character dies.
    This resets a number of important variables in the Game class
    and then creates a new Game class instance.
    '''
    def __init__(self,testevents = None):
        # Reference the global game state variable to this object.
        cf.gs = self
        self.game = TOGAME.Game()
        # Starts with opening menu.
        self.events_loop = EVENTSLOOP.EventsLoop(testevents) 
    
    def reset(self):
        ''' Takes self meaning the game as a parameter and resets the
        time.
        '''
        TOGAME.Game.day_counter = 0
        TOGAME.Game.current_year = 2017
        TOGAME.Game.month_counter = 1
        TOGAME.Game.month_day = 1
        TOGAME.Game.term_count = 1
        self.game = TOGAME.Game()

# Sample unittest test case.
#class TestGame(unittest.TestCase):
#    def test1(self):
#        print 'xxx'

def run_tests():
    '''This is where tests are run.
    In the python shell run `import Trumpocalypse.py`.
    Then run Trumpocalypse.run_tests() to run this code.
    :param: None.
    :rtype: Does not a return value.
    :raises: None.
    '''
    import sys
    cf.surface = pygame.display.set_mode((854,480))
    GameState([0,1] + [ x*0 for x in range(1000)])

if __name__ == '__main__':
    '''First you have to make an object of a *Menu class.
    *init take 2 arguments. list of fields and destination surface.
    Then you have a 4 configuration options:
    *set_colors will set colors of menu (text, selection, background)
    *set_fontsize will set size of font.
    *set_font take a path to font you choose.
    *move_menu is quite interseting. It is only option which you can use before 
    and after *init statement. When you use it before you will move menu from 
    center of your surface. When you use it after it will set constant coordinates. 
    Uncomment every one and check what is result!
    *draw will blit menu on the surface. Be carefull better set only -1 and 1 
    arguments to move selection or nothing. This function will return actual 
    position of selection.
    *get_postion will return actual position of seletion. '''
    # Pygame.init just initializes all pygame modules.
    # This is unnecessary because we initialize only the modules
    # we need whenever necessary.
    # DO NOT USE THIS:
    #   pygame.init()
    cf.surface = pygame.display.set_mode((854,480), HWSURFACE|DOUBLEBUF|RESIZABLE)
    GameState()
