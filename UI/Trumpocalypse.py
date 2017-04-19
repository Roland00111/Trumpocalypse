import config as cf
import time
import pygame
import random
from TextWrap import *
import PygameUI
import math
import copy
import items as ITEMS # Items dictionary.
import jobs as JOBS #Potential jobs
import events as EVENTS
import menu as MENU
import store as STORE

from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()
    
class EventsLoop:
    '''
    This loop is running continuously to check for any time a key on
    the keyboard is pressed or a mouse button is pressed.
    As well as drawing the next menu by creating a new Menu() class
    for the specified keypress index when a menu item is selected.
    To reduce CPU usage from 100% the loop utilizes a 
    call to pygame.time.wait(0).
    This is noted at this URL:
        https://www.gamedev.net/topic/
        518494-pygame-eating-up-my-cpu/#entry4368408
    The author states:
        "Giving up any remainder of the timeslice is the key to
        lowering CPU usage, which is done by sleeping - or,
        in the case of PyGame, calling time.wait()."
    When the game is first started an initial Menu instance is started
    using OpeningMenu(). OpeningMenu is just one of the many classes
    that inherit from the Menu class.
    '''
    current_menu = None
    test_events = None
    
    def __init__(self,test_events = None):
        '''This starts the continuosly running loop.
                
        :param list test_events:
            A list of keypress indexes to auto-"press".
        '''
        pygame.display.set_caption('Trumpocalypse!')
        # Start on opening menu. Then changes.
        self.cm = MENU.OpeningMenu() # Current menu reference
        self.test_events = test_events
        event_loop = True
        recurse_test = 0
        cf.gs.first_game_event=False
        while event_loop:
            self.process_pygame_events()
            # CPU wait.
            pygame.time.wait(0)
    
    def check_character_alive(self):

        '''If the character's health is 0 then kill the character
        (is_dead=true). Then do the game over screen.
        '''

        if (cf.gs.game.character != None and
            cf.gs.game.character.health <= 0 and 
            cf.gs.game.character.is_dead is True and
            cf.gs.game.character.game_over is False):
            # Set game_over=True
            cf.gs.game.character.game_over = True
            self.cm.remove_pui_children()
            self.cm = MENU.GameOverScreen()
    
    def set_first_game_event(self, event):
        if cf.gs.first_game_event==False:
            print("setting first game event")
            cf.gs.first_game_event=event
    
    def pui_has_alert(self, event):
        '''If there is an alert then stop everything except
        mouse down, mouse up, and quit.
        Use continue to jump forward in event_loop.
        '''

        if self.cm.scene._has_alert is True and (
            event.type == pygame.MOUSEBUTTONDOWN or
            event.type == pygame.MOUSEBUTTONUP):
            # Allow only
            #   self.cm.scene.hit(event.pos) =
            #   <PygameUI.Button object at ...>
            #   That is, only allow button presses.
            if event.type == (pygame.MOUSEBUTTONDOWN or
                              event.type == pygame.MOUSEBUTTONUP):
                # Only allow elements in the alert element to
                # receive mouse events.
                if self.cm.scene._alert.hit(event.pos) == None:
                    return True
        elif self.cm.scene._has_alert is True:
            # Make sure to draw alert
            cf.surface.blit(self.cm.scene.draw_alert(), (0, 0))
            # and update, in the case of
            #self.cm.process_before_unload()=False and
            #chosen_position=True
            pygame.display.update()
            return True
        # If the code is down here then there is no alert.
        # Allow the event to be processed.
        return False
        
    def process_pygame_events(self):
        ''' This function contains our main while loop that is
        constantly checking for keyboard and mouse button presses.
        '''
        chosen_position = None # Reset on each loop
        ########################Used for Testing##################
        if self.test_events != None:
            self.test()
            return
        ##########################################################
        for event in pygame.event.get():
            # Set first game event
            self.set_first_game_event(event)
            # Check character is alive
            self.check_character_alive()
            # Check quit event
            if event.type == QUIT:
                pygame.display.quit()
                sys.exit()
            # Check alert status
            if self.pui_has_alert(event):
                continue
            
            #-----------------------------------
            # Key press events and mouse events.
            #-----------------------------------
            if event.type == KEYDOWN:
                print(str(event.unicode))
                if event.key == K_UP:
                    self.cm.draw(-1)
                elif event.key == K_DOWN:
                    self.cm.draw(1)
                elif event.key == K_RETURN:
                    chosen_position = self.cm.get_position()
                    break
                elif event.key == K_ESCAPE:
                    pass
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    cf.down_in
                    cf.down_in = self.cm.scene.hit(event.pos)
                    if (cf.down_in is not None and
                        not isinstance(cf.down_in, PygameUI.Scene)):
                        cf.down_in.mouse_down(event.button,
                            cf.down_in.from_window_point(event.pos))
            elif event.type == pygame.MOUSEBUTTONUP:
                '''
                http://stackoverflow.com/questions/10990137/
                pygame-mouse-clicking-detection
                '''
                if event.button == 1:                    
                    pos = pygame.mouse.get_pos()
                    (pressed1,pressed2,pressed3) = (pygame.mouse.
                                                    get_pressed())
                    print ('Mouse click: ', pos,
                           pygame.mouse.get_pressed())
                    # PygameUI
                    up_in = self.cm.scene.hit(event.pos)
                    if cf.down_in == up_in:
                        cf.down_in.mouse_up(event.button,
                            cf.down_in.from_window_point(event.pos))
                    cf.down_in = None
            elif event.type == pygame.MOUSEMOTION:
                if cf.down_in is not None and cf.down_in.draggable:
                    if cf.down_in.parent is not None:
                        (cf.down_in.parent.
                        child_dragged(cf.down_in, event.rel))
                    cf.down_in.dragged(event.rel)
            elif event.type == pygame.KEYDOWN:
                self.cm.scene.key_down(
                    event.key, event.unicode)
            elif event.type == pygame.KEYUP:
                self.cm.scene.key_up(event.key)
            
            #---------------------------
            # Drawing stuff starts here.
            #---------------------------
            
            # Draw PygameUI.
            cf.surface.blit(self.cm.scene.draw(), (0, 0))
            # Draw Menu
            if self.cm.body is False:
                self.cm.init(self.cm.titlesArray, cf.surface) 
                self.cm.draw()
            else:
                # Draw menu plus body
                self.cm.init(self.cm.titlesArray, cf.surface, 200) 
                self.cm.draw()
                self.cm.draw_menu_body()
            # Draw scene alert.
            if self.cm.scene._has_alert is True:
                cf.surface.blit(self.cm.scene.draw_alert(), (0, 0))
            # Update
            pygame.display.update()
   
        #----------------------------
        # Enter key has been pressed.
        #----------------------------
        if chosen_position is not None:
            # If there is a chosen position, consider changing
            #to new menu.
            # Run function based on current selected item.
            if self.cm.process_before_unload != False:
                result = self.cm.process_before_unload(chosen_position)
                if result is False:
                    # If process_before_unload returns false, then
                    # stop processing now (do not go to next menu!)
                    return        
            # Remove scene children
            self.cm.remove_pui_children()
            # Go to the next menu.
            self.cm = (self.cm.keypressArray
                                 [chosen_position]()) 

    def test():
        '''Run tests.
        '''
        while self.test_events:
            chosen_position = self.test_events.pop(0)
            self.cm.remove_pui_children()
            cf.surface.blit(self.cm.scene.draw(), (0, 0))
            if self.cm.body is False:
                self.cm.init(self.cm.titlesArray, cf.surface) # Draw non-body menu
                self.cm.draw()
            else:
                # Draw menu plus body
                self.cm.init(self.cm.titlesArray, cf.surface, 200) 
                self.cm.draw()
                #300 - self.menu_width / 2  Calculate the x offset
                x = self.cm.dest_surface.get_rect().centerx - 150
                # Draw a box background.
                pygame.draw.rect(cf.surface, (255,60,71), pygame.Rect(x,
                self.cm.body['top'], 300, self.cm.body['height']), 10) 
                                           #Box color
                # There is a slight offset from the text and the box.
                # The box needs to contain the text. So the text is
                # going to be slightly smaller. How about 8 pixels?
                                             # left,top,width,height
                rect = pygame.Rect((x+8,self.cm.body['top']+8,300-8,300-8))
                font = (pygame.font.Font
                ('data/coders_crux/coders_crux.ttf',
                 self.cm.body['font_size']))
                drawText(cf.surface, self.cm.body['text'], (0,0,0), rect,
                         font, aa=False, bkg=None)
            pygame.display.update()
            self.cm = self.cm.keypressArray[chosen_position]()
            
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
        self.events_loop = EventsLoop(testevents) 
    
    def reset(self):
        Game.day_counter = 0
        Game.current_year = 2017
        Game.month_counter = 1
        Game.month_day = 1
        Game.term_count = 1
        self.game = Game()
    
class Jobs:
    '''Handler for jobs in the game. Each game has one instance
    of the Jobs class. The Jobs class currently has one function,
    which is to provide a random Job class instance when appropriate.
    The jobs list is stored in jobs.py.
    '''
    def __init__(self):
        pass
    def random_job(self):
        r = random.randint(0,len(JOBS.j.keys())-1)
        x = JOBS.j.values()[r]
        return Job(x['title'], x['income'], x['company'], x['area'],
                   x['events'])

class Job:
    ''' Deals with anythinng that deals with the characters job'''
    def __init__(self,title=None,income=None,company=None,area=None,
                 work_events=None):
        ''' Sets default things related to the characters job '''
        self.title = title
        self.income = income
        self.company = company
        self.area = area
        self.work_events = work_events
        self.coordinates = {}
        #self.distances_call = 
        self.distances()

    def work(self):
        ''' this is called when the character goes to work so it
        decrements time and increases there cash.
        '''
        self.random_dictPos = random.randint(0,
                                            len(self.work_events)-1)
        
        self.hours_worked = (self.work_events.values()
                              [self.random_dictPos])
        if self.hours_worked > cf.gs.game.current_day.day_hours:
            self.hours_worked = cf.gs.game.current_day.day_hours
        cf.gs.game.mod_hours(-self.hours_worked)
        print self.hours_worked
        self.money_made = (cf.gs.game.character.
                           earn_money( self.hours_worked))
        print self.money_made

        return (self.work_events.keys()[self.random_dictPos] + ' \n'
                + ' \nWorked: ' + str(self.hours_worked)
                + ' \nYou made: '+ str(self.money_made))

    def distances(self):
        '''Set store location based on location type.
        Note: Random choice provides random between + and - number:
        https://docs.python.org/2/library/random.html#random.choice
        '''
        if self.area == 'urban':
            self.coordinates['x'] = (random.uniform(0.0,2.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                     cf.plus_minus())
        elif self.area == 'suburban':
            self.coordinates['x'] = (random.uniform(2.0,8.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(2.0,8.0) *
                                     cf.plus_minus())
        else: # Assume rural
            self.coordinates['x'] = (random.uniform(8.0,20.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(8.0,20.0) *
                                     cf.plus_minus())
    
    def distance_from_house(self):
        '''Calculate the euclidean distance to the current house.
        Character's current housing is (string):
            cf.gs.game.character.selected_house
        
        :return: Distance in miles, rounded to the tenth.
        :rtype: int.
        '''
        # Friend's house
        if cf.gs.game.character.selected_house_idx == 0: 
            c1 = (cf.gs.game.locations.
                  friend_location['coordinates'])
        else:
            # Housing is always -1
            idx = cf.gs.game.character.selected_house_idx - 1 
            x = (cf.gs.game.character.inventory.
                 sorted_items['housing'][ idx ].coordinates)
            c1 = [x['x'], x['y']]
        c2 = self.coordinates
        return round(cf.euclidean(c1, [c2['x'], c2['y']]), 1)

class Location:
    '''Provide the player with a location. Each location has 1-4
    Store instance. Each location has a region name (passed in).
    Each location has 10-20 associated Job instances.
    Each location has an active_store_idx which specifies which
    store the player is current visiting (None if no store).
    '''
    def __init__(self,location_name):
        '''
        :param str location_name: A location name.
        '''
        self.location_name = location_name
        self.connected_regions = []
        self.stores = [
            STORE.Store() for i in range(random.randint(1,4))
        ]
        self.active_store_idx = None # Index of store being visited.
   
    def random_job(self):
        ''' Assigns a random job '''
        r = random.randint(0, 10)
        self.jobs = [ cf.gs.game.jobs.random_job()
                      for i in range(0, 10+r) ]
        
        r = random.randint(0, len(self.jobs)-1)
        return self.jobs[ r ]

    def menu_values(self):
        temp_array = []
        for store in self.stores:
            temp_array.append(store.name + ': ' +
                        str(store.distance_from_house()) + ' miles')
        return temp_array
    
class Locations:
    '''
    Handler for locations in the game. Each game has one instance
    of the Locations class. The Locations class instance has a list of
    Location class instances for each of the eight locations.
    The Locations class also has a friend_location attribute which
    specifies the X,Y coordinates of the friend's location.
    The friend_location attribute changes daily so that when 
    "staying with a friend" each day the player is starting from
    a new location (see StoryScreen).
    The list of regions is from:
    https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States
    '''
    all_locations = [ #prototype
        'Middle Atlantic',
        'New England',
        'South Atlantic',
        'East South Central',
        'East North Central',
        'West North Central',
        'West South Central',
        'Mountain',
        'Pacific'
    ]
    def __init__(self):
        self.locations = [ Location(name) for name in self.all_locations ]
        self.friend_location = { 'coordinates': [ 0, 0 ] }
        pass
    
    def update_friend_location(self):
        '''This function sets the 0th and 1st element of
        self.friend_location to a random float, -20.0 to 20.0.
        '''
        self.friend_location['coordinates'][0] = (random.
                                    uniform(0.0, 20.0) * cf.plus_minus())
        self.friend_location['coordinates'][1] = (random.
                                    uniform(0.0, 20.0) * cf.plus_minus())
        
    def random_location(self):
        '''
        :return: A random location instance.
        :rtype: location.
        '''
        return self.locations[random.randint(0,len(self.locations)-1)]

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
        self.jobs = Jobs()
        self.current_day = None
        #Character('random') creates charecter on start menu becasue
        #its an error.
        self.character = None 
        self.locations = Locations()
        self.events = EVENTS.Events()#Events() #EVENTS.Events()
    
    def tally_score(self):
        '''This function is called when the game is over.
        It will tally the score of the game.
        '''
        print 'Tally the score...'

    def mod_hours(self,hours,operation=False):
        '''Modifies hours. Ensures that hours is greater than or equal
        to 0.
        '''
        if operation==False:
            cf.gs.game.current_day.day_hours += hours
        if operation==True:
            cf.gs.game.current_day.day_hours *= hours
        if cf.gs.game.current_day.day_hours < 0:
            cf.gs.game.current_day.day_hours=0
        
    class Day:
        day_hours = 16
        generated_date = 0
        #Only needed to be used once, every other time you can use
        #generated_date find it at the bottom of this class
        inauguration_day = 'January 20th' 

        def __init__(self):
            '''Set day hours to 16. Run end of day modifications.
            Run generate date to generate today's "date" and
            accompanying story text.
            '''
            self.day_hours = 16
            self.eod_mods()
            self.gen_date()

        def eod_mods(self):
            #
            food = (cf.gs.game.character.inventory.
                    sorted_items['food'])

            
            
            if (food.amount >= 3):
                food.amount -= 3
            
            elif (food.amount <3 ):
                food.amount = 0
                cf.gs.game.character.lose_health(1)
                cf.gs.game.character.sanity -= 1

            
            elif (cf.gs.game.character.selected_house == ('Staying with Friends')):
                cf.gs.game.character.sanity -= 1
                

                #if sanity dips under zero at the end of the day it hurts
                #your health
            elif (cf.gs.game.character.sanity <=0):
                cf.gs.game.character.sanity = 5
                cf.gs.game.character.lose_health(1)

            else:
                #Continue the events whose durations have not run out.
                pass
            
            ##
            ##
            #cf.gs.game.character.check_health()
                          
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
    import sys
    #0,6671875 and 0,(6) of HD resoultion
    cf.surface = pygame.display.set_mode((854,480))
    # Toggle full screen #Apparently only works when running X11
    #pygame.display.toggle_fullscreen()
    GameState()

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
    

