import config as cf
import time
import pygame
import random
import PygameUI
import math
import copy
import items as ITEMS # Items dictionary.
import jobs as JOBS #Potential jobs
import events as EVENTS
import menu as MENU
import store as STORE
import locations as LOCATIONS
import eventsloop as EVENTSLOOP
from TextWrap import *
from pygame.locals import *
import game
import sys

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
        self.game = Game()
        # Starts with opening menu.
        self.events_loop = EVENTSLOOP.EventsLoop(testevents) 
    
    def reset(self):
        ''' Takes self meaning the game as a parameter and resets the
        time.
        '''
        Game.day_counter = 0
        Game.current_year = 2017
        Game.month_counter = 1
        Game.month_day = 1
        Game.term_count = 1
        self.game = Game()

class Game:
    '''Each game starts in January of 2017, in the first term
    of Donald Trump's presidency. Each game has a Jobs() instance,
    a Locations() instance, and an Events() instance.
    Each game starts without an instance of a Character().
    The user adds a Character() instance during Automatic or 
    Manual character creation.
    '''
    day_counter = 0
    current_year = 2017
    month_counter = 1
    month_day = 1
    term_count = 1
    def __init__(self):
        self.jobs = JOBS.Jobs()
        self.current_day = None
        self.opening_menu = MENU.OpeningMenu()
        #Character('random') creates charecter on start menu becasue
        #its an error.
        self.character = None 
        self.locations = LOCATIONS.Locations()
        self.events = EVENTS.Events()#Events() #EVENTS.Events()
    
    def tally_score(self):
        score = 10000
        #score += item.calculate_resale_cost() or some new way?
        size = len(cf.gs.game.events.inactive_events)
        score -= (size*1000)
        print 'Tallied the score...'
        print (score)
        return score

    def mod_hours(self,hours,operation=False):
        '''The parameters are the amount of hours if its adding time
        or -hours if its taking time away and the operation.By default
        the operation is False which equates to adding if you pass
        True then it multiplies. Finally it ensures that hours is
        greater than or equal to 0.
        '''
        if operation==False:
            cf.gs.game.current_day.day_hours += hours
        if operation==True:
            cf.gs.game.current_day.day_hours *= hours
        if cf.gs.game.current_day.day_hours < 0:
            cf.gs.game.current_day.day_hours=0
        print 'mod hours done:',cf.gs.game.current_day.day_hours
        
    class Day:
        day_hours = 16
        generated_date = 0
        #Only needed to be used once, every other time you can use
        #generated_date find it at the bottom of this class
        inauguration_day = 'January 20th' 

        def __init__(self):
            '''Set day hours to 16 and run end of day modifications.
            
            Run generate date to generate today's "date" and
            accompanying story text.
            
            Note: Do not do eod_mods and gen_date in the initializer.
            This is because, for example, with eod_mods it runs
            process events which in turn makes references to
            cf.gs.game.current_day.day_hours. As this is still
            being initialized this is still referencing the
            previous day!
            So instead do this in StoryScreen.
            '''
            self.day_hours = 16
            # Does not happen here.
            #self.eod_mods()
            #self.gen_date()

        def eod_mods(self):
            '''This function checks if you have enough food to go to
            the next day unharmed. Then checks if you are staying at
            your friends house to decrement sanity. Then checks if
            your sanity has gone below 0 and if it has then it
            decrements health and sets sanity to 5. 
            '''
            food = (cf.gs.game.character.inventory.
                    sorted_items['food'])

            if (food.amount >= 3):
                food.amount -= 3
            
            elif (food.amount <3 ):
                food.amount = 0
                cf.gs.game.character.modifyHealth(-1)
                cf.gs.game.character.sanity -= 1

            if (cf.gs.game.character.selected_house == ('Staying with Friends')):
                cf.gs.game.character.sanity -= 1
                
                #if sanity dips under zero at the end of the day it hurts
                #your health
            if (cf.gs.game.character.sanity <=0):
                cf.gs.game.character.sanity = 5
                cf.gs.game.character.modifyHealth(-1)

            else:
                #Continue the events whose durations have not run out.
                pass
            #cf.gs.game.character.check_health()

            # Process events.
            # Then regenerate active events.
            a = cf.gs.game.events.active_events
            for event in a:
                event.process()
            cf.gs.game.events.regenerate_active_events()

            # If events are > 5, toggle a random event.
            i = cf.gs.game.events.inactive_events
            if len(i) > 5:
                event = random.choice(i)
                cf.gs.game.events.toggle_event(event)
                          
        def gen_date(self):
            g = cf.gs.game # A shortcut
            self.gen_story_text() # Generate today's story text
            if g.month_counter % 12 == 1 and g.day_counter != 1:
                g.current_year += 1
            if g.month_counter + 1 == 13:
                x=12
                month_day = 31
            else:
                x=g.month_counter + 1
                month_day = 1 #Needed because when Game.month_counter
                #== 12 it would go back a year, because it would be
                #12/?/2017 to 1/?/2017 and get confused 
            self.generated_date = self.randomDate(
                str(g.month_counter)+'/1/'+str(g.current_year),
                str(x)+'/'+str(month_day)+'/'+str(g.current_year),
                random.random()
            )
            
            # Reset game day counter incromentation 
            if g.month_counter == 12:
                g.month_counter = 0
        
        def gen_story_text(self):
            g = cf.gs.game # A shortcut
            if g.day_counter == 1:
                self.story_text = ('Today is ' +
                Game.Day.inauguration_day + '\ninauguration day, '+
                'Trump is being sworn into office by Chief Justice '+
                'John Roberts')
            elif g.day_counter % 48 == 0:
                g.term_count += 1
                self.story_text = ('Today is the Election day, '+
                                   'Trump is up for Relection')
            else:
                #If latest random event is a repeat, add again to the
                #text.
                event = cf.gs.game.events.last_random_event[0]
                if (cf.gs.game.events.last_random_event[1] == 1):
                    self.story_text = ('You are sitting on the couch'
                        ' watching the news while eating your '
                        'breakfast and drinking your arbitrary drink'
                        ', and the news comes on. The reporter is '
                        'raving about how life will never be the '
                        'same after...                 '
                        +event
                        + ' again!')
                else:
                    self.story_text = ('You are sitting on the couch'
                        ' watching the news while eating your '
                        'breakfast and drinking your arbitrary drink'
                        ', and the news comes on. The reporter is '
                        'raving about how life will never be the '
                        'same after...\n'
                        +event)
            
        def strTimeProp(self,start, end, format, prop):
            '''Get a time at a proportion of a range of two formatted
            times.
            The start and end should be strings specifying times formated
            in thegiven format (strftime-style), giving an interval
            [start, end].prop specifies how a proportion of the
            interval to be taken afterstart.  The returned time will
            be in the specified format.
            Taken From : http://stackoverflow.com/questions/553303/
                generate-a-random-date-between-two-other-dates
            By: Tom Alsberg
            '''
            stime = time.mktime(time.strptime(start, format))
            etime = time.mktime(time.strptime(end, format)) - 1
            ptime = stime + prop * (etime - stime)
            return time.strftime(format, time.localtime(ptime))

        def randomDate(self,start, end, prop):
            return self.strTimeProp(start, end, '%m/%d/%Y', prop)
# Sample unittest test case.
#class TestGame(unittest.TestCase):
#    def test1(self):
#        print 'xxx'

def run_tests():
    '''.. function:: run_tests()
    This is where tests are run.
    In the python shell run `import Trumpocalypse.py`.
    Then run Trumpocalypse.run_tests() to run this code.
    :param: None.
    :rtype: Does not a return value.
    :raises: None.
    '''
    import sys
    #0,6671875 and 0,(6) of HD resoultion
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
    #pygame.init()
    #0,6671875 and 0,(6) of HD resoultion
    cf.surface = pygame.display.set_mode((854,480))
    # Toggle full screen #Apparently only works when running X11
    #pygame.display.toggle_fullscreen()
    GameState()
