import time
import pygame
import unittest
import random
from TextWrap import *
import PygameUI
import gc

from pygame.locals import *


if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

game_state = None # A global variable to be accessible by all classes throughout the game.
down_in = None # A global variable for pygameui (menu custom fields)
CharacterDictionary = None


class Menu:
    '''
    Original code for the menu class is from:
        @author: avalanchy (at) google mail dot com
        @version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
        @date: 2012-04-08
        @license: This document is under GNU GPL v3
        README on the bottom of document.
        @font: from http://www.dafont.com/coders-crux.font
              more abuot license you can find in data/coders-crux/license.txt
    '''
    process_event = False
    lista = []
    by = []
    FontSize = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface #how surface game is on is generated
    QuanityOfLista = 0 #initalizer
    #BackgroundColor = (51,51,51)
    BackgroundColor = (255,120,71)#color of background of menu itself (currently Trumps skin color :))
    TextColor =  (255, 255, 153)
    SelectionColor = (153,102,255)
    PositionSelection = 0 #initalizer
    Position = (0,0) #set as initalizer
    menu_width = 0 
    menu_height = 0
    keypressArray = []
    titlesArray = []
    custom_fields = []              # To be filled in by menu classes that need buttons, selects, inputs, and number inputs
    scene = PygameUI.Scene()        # For utilizing pygameui
    body = False                    # This is for main text area.
    
     
    def __init__(self):
        pass
        
    class Field:
        test = ''
        Field = pygame.Surface
        Field_rect = pygame.Rect
        Selection_rect = pygame.Rect

    def move_menu(self, top, left):
        self.Position = (top,left) 

    def set_colors(self, text, selection, background):
        self.BackgroundColor = background
        self.TextColor =  text
        self.SelectionColor = selection
        
    def set_fontsize(self,font_size):
        self.FontSize = font_size
        
    def set_font(self, path):
        self.font_path = path
        
    def get_position(self):
        return self.PositionSelection
    
    def init(self, lista, dest_surface, height_top=0):
        self.Position = (0,0) # Must be 0,0 each time Menu is redrawn
        self.lista = lista
        self.dest_surface = dest_surface
        self.Quanity = len(self.lista)
        self.CreateStructure(height_top)        
        
    def draw(self,move=0):
        if move:
            self.PositionSelection += move 
            if self.PositionSelection == -1:
                self.PositionSelection = self.Quanity - 1
            self.PositionSelection %= self.Quanity
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.BackgroundColor)
        Selection_rect = self.by[self.PositionSelection].Selection_rect
        pygame.draw.rect(menu,self.SelectionColor,Selection_rect)

        for i in xrange(self.Quanity):
            menu.blit(self.by[i].Field,self.by[i].Field_rect)
        self.dest_surface.blit(menu,self.Position)
        return self.PositionSelection

    def CreateStructure(self, height_top):
        shift = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.FontSize)
        for i in xrange(self.Quanity):
            self.by.append(self.Field())
            self.by[i].text = self.lista[i]
            self.by[i].Field = self.font.render(self.by[i].text, 1, self.TextColor)

            self.by[i].Field_rect = self.by[i].Field.get_rect()
            shift = int(self.FontSize * 0.2)

            height = self.by[i].Field_rect.height
            self.by[i].Field_rect.left = shift
            self.by[i].Field_rect.top = shift+(shift*2+height)*i

            width = self.by[i].Field_rect.width+shift*3
            height = self.by[i].Field_rect.height+shift*3            
            left = self.by[i].Field_rect.left-shift
            top = self.by[i].Field_rect.top-shift

            self.by[i].Selection_rect = (left,top ,width, height)
            if width > self.menu_width:
                    self.menu_width = width
            self.menu_height += height
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        y = y + height_top # Add top offset
        mx, my = self.Position
        self.Position = (x+mx, y+my) 
    
    class CustomField:
        def __init__(self, field_type, field_content, field_label, field_event_hooks):
            '''
            field_type = string: 'list', 'button', 'input', 'number' (also input but limited to #s)
            field_content = array of strings: for list; string: button text, input default value, number default value
            field_label = string, a label to put beside the field
            field_event_hooks = array, an array of dict events, each dict event has a `type` and `callback_function`
            '''
            self.field_type         = field_type
            self.field_content      = field_content
            self.field_label        = field_label
            self.field_event_hooks  = field_event_hooks
            # Sample: Add a select to the scene.
            self.select()
            
        def select(self):
            # This is named select because Python already has a list() function.
            # There is probably a callback function here for events.
            # There could be a label passed into CustomField
            # that is added to the left of each list.
            # Is it possible to add this with the Label class?
            x = PygameUI.List(['Item %s' % str(i) for i in range(20)])
            x.frame = pygame.Rect(Menu.scene.frame.w // 2, 10, 150, 170)
            x.frame.w = x.container.frame.w
            x.selected_index = 1
            Menu.scene.add_child(x)

            x = PygameUI.TextField()
            x.frame = pygame.Rect(10, 50, 150, 30)
            Menu.scene.add_child(x)
 
            ###
            # Here is where a label for the select() element would go.
            ###
        
        def button(self):
            pass
         
        def input_box(self):
            pass
        
        def number(self):
            # What if the number field is instead just a list() field?
            pass
    
    #def __del__(self):
    #    print "__del__", self

class EventsLoop:
    '''
    Note the pygame.time.wait(0) call. This reduces CPU
    usage from 100% to negligible!
    This is noted at this URL:
    https://www.gamedev.net/topic/518494-pygame-eating-up-my-cpu/#entry4368408
    The author states:
    "Giving up any remainder of the timeslice is the key to
    lowering CPU usage, which is done by sleeping - or,
    in the case of PyGame, calling time.wait()."
            
    Sample body text: menu.body = {
        text: 'Some Main Text',
        font_size: 32,
        top: 40,
        height: 300
    }
    '''
    current_menu = None
    
    def __init__(self,testevents = None): # , text = False, size=22,top=40,boxHeight=300
        self.current_menu = OpeningMenu() # Starts on opening menu. Then changes.
        event_loop = True
        recurse_test = 0
        while event_loop:
            chosen_position = None # Reset on each loop
            cm = self.current_menu # A quick shortcut
            ########################Used for Testing###############################
            if testevents != None:
                while testevents:
                    cm = self.current_menu # A quick shortcut
                    chosen_position = testevents.pop(0)
                    #print chosen_position
                    while cm.scene.children:
                    # This does work to remove Scene() children.
                        for child in cm.scene.children:
                    # Grab one child and remove it.
                            cm.scene.remove_child(child)
                            break
                    surface.blit(cm.scene.draw(), (0, 0))
                    # Draw other menu content
                    if cm.body is False:
                        # Draw non-body menu
                        cm.init(cm.titlesArray, surface)
                        cm.draw()
                    else:
                        # Draw menu plus body
                        cm.init(cm.titlesArray, surface, 200)
                        cm.draw()
                        x = cm.dest_surface.get_rect().centerx - 150 #300 - self.menu_width / 2  Calculate the x offset
                        pygame.draw.rect(surface, (255,60,71), pygame.Rect(x, cm.body['top'], 300, cm.body['height']), 10) # Draw a box background.
                                                   #Box color
                        # There is a slight offset from the text and the box.
                        # The box needs to contain the text. So the text is
                        # going to be slightly smaller. How about 8 pixels?
                        rect = pygame.Rect((x+8,cm.body['top']+8,300-8,300-8)) # left,top,width,height
                        font = pygame.font.Font('data/coders_crux/coders_crux.ttf',cm.body['font_size'])
                        drawText(surface, cm.body['text'], (130,130,130), rect, font, aa=False, bkg=None)
                    pygame.display.update()
                    #print cm.keypressArray[chosen_position]
                    #print cm.keypressArray
                    self.current_menu = cm.keypressArray[chosen_position]()
                return
            #####################################################################
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    print(str(event.unicode))
                    if event.key == K_UP:
                        cm.draw(-1) #here is the Menu class function
                    elif event.key == K_DOWN:
                        cm.draw(1) #here is the Menu class function
                    elif event.key == K_RETURN:
                        chosen_position = cm.get_position()
                        break
                    elif event.key == K_ESCAPE:
                        pass
                        #pygame.display.toggle_fullscreen() # Toggle full screen #Apparently only works when running X11
                        #pygame.display.set_mode((800,600),pygame.FULLSCREEN) #Mess up the screen (at least with my laptop)
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONUP: #pygame.MOUSEBUTTONUP
                        '''
                        http://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
                        '''
                        pos = pygame.mouse.get_pos()
                        (pressed1,pressed2,pressed3) = pygame.mouse.get_pressed()
                        print 'Mouse click: ', pos, pygame.mouse.get_pressed()
                        # This will check if a Rect was clicked:
                        #~ if Rectplace.collidepoint(pos)& pressed1==1:
                            #~ print("You have opened a chest!")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    global down_in
                    down_in = cm.scene.hit(event.pos)
                    if down_in is not None and not isinstance(down_in, PygameUI.Scene):
                        down_in.mouse_down(event.button, down_in.from_window_point(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP:
                    up_in = cm.scene.hit(event.pos)
                    if down_in == up_in:
                        down_in.mouse_up(event.button, down_in.from_window_point(event.pos))
                    down_in = None
                elif event.type == pygame.MOUSEMOTION:
                    if down_in is not None and down_in.draggable:
                        if down_in.parent is not None:
                            down_in.parent.child_dragged(down_in, event.rel)
                        down_in.dragged(event.rel)
                elif event.type == pygame.KEYDOWN:
                    cm.scene.key_down(event.key, event.unicode)
                elif event.type == pygame.KEYUP:
                    cm.scene.key_up(event.key)
                # Draw the pygameui input boxes
                surface.blit(cm.scene.draw(), (0, 0))
                # Draw other menu content
                if cm.body is False:
                    # Draw non-body menu
                    cm.init(cm.titlesArray, surface)
                    cm.draw()
                else:
                    # Draw menu plus body
                    cm.init(cm.titlesArray, surface, 200)
                    cm.draw()
                    x = cm.dest_surface.get_rect().centerx - 150 #300 - self.menu_width / 2  Calculate the x offset
                    pygame.draw.rect(surface, (255,60,71), pygame.Rect(x, cm.body['top'], 300, cm.body['height']), 10) # Draw a box background.
                                               #Box color
                    # There is a slight offset from the text and the box.
                    # The box needs to contain the text. So the text is
                    # going to be slightly smaller. How about 8 pixels?
                    rect = pygame.Rect((x+8,cm.body['top']+8,300-8,300-8)) # left,top,width,height
                    font = pygame.font.Font('data/coders_crux/coders_crux.ttf',cm.body['font_size'])
                    drawText(surface, cm.body['text'], (130,130,130), rect, font, aa=False, bkg=None)
                pygame.display.update()
            if chosen_position is not None:
                # There is a chosen position.
                # Change to a new menu class.
        # The following does not work to remove Scene() children:
        #   del self.current_menu
        #   self.scene.__del__()
                while cm.scene.children:
            # This does work to remove Scene() children.
                    for child in cm.scene.children:
                # Grab one child and remove it.
                        cm.scene.remove_child(child)
                        break
        # Go to the next menu.
                if cm.process_event == True:
                    cm.process_events(chosen_position)
                self.current_menu = cm.keypressArray[chosen_position]()
            pygame.time.wait(0)

class Character:
    def __init__ (self, create_type):
        self.name = 'Default'
        self.health = 3
        self.strength = 3
        self.gender = 'male'
        self.age = 40
        self.charisma = 3
        self.intelligence = 3
        self.sanity = 30
        self.inventory = Inventory() # Give character an inventory.
        if create_type == 'random':
            self.randomGenerate()
            pass
        #~ self.location = self.Location() # This works...
    #~ # Subclasses of Character? Eg Location...
    #~ # This works...
    #~ class Location:
        #~ def __init__(self):
            #~ print 'test'
    
    def randomGenerate(self):
        num = random.randint(0,1)
        global CharacterDictionary
        if num == 0:
            self.name = 'Bill'
            self.health = 3
            self.strength = 5
            self.gender = 'male'
            self.age = 69
            self.charisma = 3
            self.intelligence = 1
            self.job = 'Plumber'
            self.income = 10000
            self.sanity = 30
            # Add some random items.
            self.inventory.add_item() #To add item insert string of item (item_type) see Item class, else it's random
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            # Location
            self.location = Location()
            
        elif num == 1:
            self.name = 'Linda'
            self.health = 3
            self.strength = 1
            self.gender = 'female'
            self.age = 40
            self.charisma = 4
            self.intelligence = 5
            self.job = 'CEO'
            self.income = 20000
            self.sanity = 30
            # Add some random items.
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            # Location
            self.location = Location()
    
    def born(self):
        print self.name, ' is alive!'
    def died(self):
        print self.name, ' is dead!'

class Location:
    '''https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States'''
    def __init__(self):
        self.environment_bonus = 1
        self.all_locations = [
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
        # Default location is random.
        self.name = self.all_locations[ random.randint(0,8) ] # Any of 0,1,2,3,4,5,6,7,8
        
class Inventory:
    def __init__(self):
        self.max_items = 999
        self.items = [] # Array of items.
        self.all_choices = [
            'Food','Pie','Garden','LotteryTicket','NewCar','OldCar',
            'UrbanHouse','SuburbanHouse','RuralHouse','Cash','Food',
        ]
    def item_count(self):
        #Iterates throught self.items and returns a list of all items in array with number of uses left
        storage = []
        for item in self.items:
            storage.append(item.item_type + ': ' + str(item.remaining_uses))
        return storage
    
    def num_items(self):
        # Returns the number of items in the inventory
        return len(self.items)
    def add_item(self, item_type = None,remaining_uses = None):
        # Add an item to this inventory.
        # If item_type is None then add a random item.
        # If item_type is not None then add item of this type.
        # Does the item already exist in the inventory?
        # If so, then add the item's stats.    
        if item_type != None:
            new_item = Item(item_type)
            if remaining_uses != None:
                new_item.remaining_uses = remaining_uses
            self.update_or_add_item(new_item)
        else:
            # A random item.
            n = random.randint(0, len(self.all_choices)-1)
            rand_item = Item( self.all_choices[n] )
            self.update_or_add_item(rand_item)
    def update_or_add_item(self, new_item):
        existing_item = self.contains_item(new_item.item_type)
        if existing_item != False:
            # Add to the remaining uses.
            existing_item.remaining_uses += new_item.remaining_uses
        else:
            self.items.append( new_item )
    def contains_item(self, item_type):
        # Returns the item in the inventory if it exists.
        # Otherwise returns False.
        # This takes O(n) time as it searches entire list.
        for existing_item in self.items:
            if existing_item.item_type == item_type:
                return existing_item
        # Still here? Then the item is not in the inventory.
        return False
        
class Item:
    '''
    Example items:
        There is a NewCar item in the inventory with e.g. 100 uses.
        There is a Food in the inventory with e.g. 10 uses.
    
    Purchase and resale amounts:
    1) Buy: Remaining Uses * Purchase Cost
        E.g. Buy Food with 4 uses left and purchase cost=10.
        So 4 * 10 = $40.
    2) Sell: Remaining Uses * Resale Cost
        E.g. Sell Food with 4 uses left and resale cost=8.
        So 4 * 8 = $32.
    
    Each purchase of an item just adds to the total remaining_uses.
        
    Inventory quick display (right side bar).
        How about...
        Any number of new cars will shows as "NewCar: 100" (for one car)
            ...or "NewCar: 200" (for two cars)
            ...or "NewCar: 300" (for three cars)
            ... and so on
        One food with 100 uses shows as "Food: 100"
            ...or "Food: 200" (two purchases of food)
            ...or "Food: 300" (three purchases of food)
            ... and so on
    ''' 
    def __init__(self, item_type = None):
        self.item_type = item_type
        self.purchase_cost = 1
        self.resale_cost = 0
        self.remaining_uses = 1
        self.set_item(item_type)
            
    def use_item(self, item_type):
        '''This will somehow use the item...'''
        ''' Deincroment remaining_uses, along with in game effect'''
        
        pass
        
    def set_item(self, item_type):
        if item_type == 'Food':
            self.purchase_cost = 10 
            self.resale_cost = 8
            self.remaining_uses = 10 
        elif item_type == 'Pie':
            self.purchase_cost = 1
            self.resale_cost = 0
            self.remaining_uses = 1
        elif item_type == 'Garden':
            self.purchase_cost = 200
            self.resale_cost = 100
            self.remaining_uses = 10
        elif item_type == 'LotteryTicket':
            self.purchase_cost = 10
            self.resale_cost = 4
            self.remaining_uses = 1
        elif item_type == 'NewCar':
            self.purchase_cost = 20000
            self.resale_cost = 10000
            self.remaining_uses = 100
        elif item_type == 'OldCar':
            self.purchase_cost = 10000
            self.resale_cost = 4000
            self.remaining_uses = 60
        elif item_type == 'UrbanHouse':
            self.purchase_cost = 40000
            self.resale_cost = 40000
            self.remaining_uses = 100
        elif item_type == 'SuburbanHouse':
            self.purchase_cost = 20000
            self.resale_cost = 20000
            self.remaining_uses = 50
        elif item_type == 'RuralHouse':
            self.purchase_cost = 10000
            self.resale_cost = 10000
            self.remaining_uses = 20
        elif item_type == 'Cash':
            self.purchase_cost = 0
            self.resale_cost = 0
            self.remaining_uses = 0
        else:
            # The item does not exist which must be a bug.
            # Raise an error.
            raise TypeError
            

class GameState:
    def __init__(self,testevents = None):
        global game_state # Reference the global game state variable to this object.
        game_state = self
        self.game = Game()
        # Old starting method was:
    #   self.current_screen = OpeningMenu()
        self.events_loop = EventsLoop(testevents) # Starts with opening menu.
        
class EventScreen(Menu): 
    def __init__(self):
        #game_state.game.current_day = game_state.game.Day() #Game.Day()
        self.menu_name = '...'
        self.events_values = game_state.game.events_values()
        self.keypressArray = [
             DayScreen for x in range(len(self.events_values)+1)
        ]
        self.titlesArray = self.events_values + ['Back to Day']
        text = ""
        #For some reason font size 32 looks a lot better than 30 or 34 
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        self.process_event = True
    def process_events(self,chosen_position):
        if len(self.events_values) -1  < chosen_position:
            return 
        event = game_state.game.event_dict[self.events_values[chosen_position]]
        c = game_state.game.character
        for key, value in event.iteritems():
            print key
            print value
            print getattr(c,"health")
            print c.sanity
            if key == "hours":
                game_state.game.current_day.day_hours += value
            elif key in c.inventory.all_choices:
                c.inventory.add_item(str(key),int(value))
            else:
                print 'Going to try changing char attribute'
                n = getattr(c,str(key))
                setattr(c,str(key),n+value)
            #else:
                #Needs fixing
                #pass

            #Need to add remove func
                
            
class Game:
    day_counter = 0
    current_year = 2017
    month_counter = 1
    month_day = 1
    term_count = 1
    events = []
    event_dict = {"Tsunami": {"health":-1,"sanity":-1},
                          "Win Lottery": {"Cash":10000,"sanity":1,},
                          "Extreme Pollution": {"health":-1,"sanity":-1},
                          "Nuclear War": {"health":-2,"sanity":-5},
                          "Curfew": {"hours":-4,"sanity":-1},
                          "Marshall Law": {"income":-5000,"hours":-4,"sanity":-2,},
                          "Power Sleep": {"hours":2,"sanity":2},
                          "Find Good Stuff": {"Food":5,'Cash':1000,"sanity":1},
                          }
    def __init__(self):
        self.current_day = None #self.Day()
        self.character = None #Character('random') creates charecter on start menu becasue its an error.
        #self.character = Character('random')
        #self.score = ...  # will be calculated on game over
    def events_values(self):
        events_temp = []
        for event in self.events:
            events_temp.append(event.event_text)
        return events_temp
            
        
    
    class Event:
        def __init__(self):
            #self.event_type = None
            self.event_text = ""
            self.story_text = ""
            self.random_event()
        def random_event(self):
            num = random.randint(0,len(Game.event_dict)-1) 
            self.event_text = Game.event_dict.keys()[num]
        def remove_event():
            
        
            
            
    class Day:
        day_hours = 16
        generated_date = 0
        inauguration_day = "January 20th" #Only needed to be used once, every other time you can use generated_date find it at the bottom of this class

        def __init__(self):
            self.day_hours = 16
        
        def gen_date(self):
            g = game_state.game
            print 'New day'
            if g.day_counter == 1:
                self.story_text = "Today is " + Game.Day.inauguration_day + " \ninauguration day, Trump is being sworn into office by Chief Justice John Roberts"         
            elif g.day_counter % 48 == 0:
                g.term_count += 1
                self.story_text = "Today is the Election day, Trump is up for Relection"
            else:
                self.story_text = 'This is  new Day bros'
            
            if g.month_counter % 12 == 1 and g.day_counter != 1:
                g.current_year += 1
            if g.month_counter + 1 == 13:
                x=12
                month_day = 31
            else:
                x=g.month_counter + 1
                month_day = 1 #Needed because when Game.month_counter == 12 it would go back a year, because it would be 12/?/2017 to 1/?/2017 and get confused
                              # This implementation of month_day works as I tested it   
            self.generated_date = self.randomDate(str(g.month_counter) + "/1/" + str(g.current_year),
                                                   str((x)) + "/" + str(month_day) +"/" + str(g.current_year),
                                                   random.random())
            
            #Fix game day counter incromentation 
            if g.month_counter == 12:
                g.month_counter = 0
            print g.day_counter
           
            
            
        def strTimeProp(self,start, end, format, prop):
            # Taken From : http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
            # By: Tom Alsberg
            """Get a time at a proportion of a range of two formatted times.

            start and end should be strings specifying times formated in the
            given format (strftime-style), giving an interval [start, end].
            prop specifies how a proportion of the interval to be taken after
            start.  The returned time will be in the specified format.
            """

            stime = time.mktime(time.strptime(start, format))
            etime = time.mktime(time.strptime(end, format)) - 1
            print stime
            print etime
            ptime = stime + prop * (etime - stime)

            return time.strftime(format, time.localtime(ptime))


        def randomDate(self,start, end, prop):
            return self.strTimeProp(start, end, '%m/%d/%Y', prop)
        
class CreateCharacterManual(Menu): #Not in effect yet
    def __init__(self):
        '''Eg spend 20 points
        intelligence, charisma, sanity, cash
        '''
        self.menu_name = '...'
        self.keypressArray = [
            StoryScreen,
            CreateCharacter,
        ]
        self.titlesArray = [
            'Continue To Location',
            'Back To Previous Page'
        ]
        self.CustomField( # Something along the lines of.........
            'list',
            ['Choice 1', 'Choice 2', 'Choice 3'],
            'Make a "good" choice:',
            { MOUSEBUTTONUP: self.select_on_mouseup }
        )
        #~ self.CustomField( # Something along the lines of.........
            #~ 'button',
            #~ 'Some Button',
            #~ False,
            #~ { MOUSEBUTTONUP: self.button_on_mouseup }
        #~ )
    
    def select_on_mouseup(self, event):
        print 'This is called when selecting a choice from the select field!'
        #~ print event
        #~ pos = pygame.mouse.get_pos()
        #~ (pressed1,pressed2,pressed3) = pygame.mouse.get_pressed()
        #~ print 'Mouse click: ', pos, pygame.mouse.get_pressed()
    
class CreateCharacterAutomatic(Menu):
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
            StoryScreen,
            CreateCharacter,
        ]

        self.titlesArray = [
            'Begin Your Adventure',
            'Back To Previous Page',
           
        ]
        game_state.game.character = Character('random')
        
        name= game_state.game.character.name
        health=str(game_state.game.character.health)
        strength=str(game_state.game.character.strength)
        gender=game_state.game.character.gender
        age=str(game_state.game.character.age)
        charisma=str(game_state.game.character.charisma)
        intelligence=str(game_state.game.character.intelligence)
        job = game_state.game.character.job
        income = str(game_state.game.character.income)
        sanity = str(game_state.game.character.sanity)

        x = PygameUI.List(game_state.game.character.inventory.item_count())
        x.frame = pygame.Rect(Menu.scene.frame.w -154, 4, 150, Menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 0
        x.container.draggable = False #Change to True is needs to be draggable 
        self.scene.add_child(x)
        
        self.body = {
            'text': ("Name: "+name+" \n"+"Health: "+health+" \n"+"Strength: "+strength+" \n"
              +"Gender: "+gender+" \n"+"Age: "+age+" \n"+"Charisma: "+charisma+" \n"+"Intelligence: "
              +intelligence + " \n" + "Job: " +job+ " \n" + "Income: $"+income+" \n"+"Sanity: " +sanity),
            'font_size': 32,
            'top': 40,
            'height': 300
        }
        
class HighScores(Menu):
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
            OpeningMenu,
            ResetHighScore,
            Close,
        ]

        high_score_file = open("high_score.txt", "r+")
        high_score = high_score_file.read().replace('\n', '')
        high_score_file.close()

        
        self.titlesArray = [
            'Main Menu',
            'Reset Highscore',
            'Quit',
           
        ]
        a=str(high_score)
 
        Text="Highscore:"+a
        self.body = {
            'text': Text,
            'font_size': 44,
            'top': 240,
            'height': 44
        }
    
    def get_high_score():
        high_score_file = open("high_score.txt", "r+")
        high_score = high_score_file.read().replace('\n', '')
        high_score_file.close()
    
    def save_high_score():
        pass

class ResetHighScore(Menu):
    def __init__(self):
        high_score_file = open("high_score.txt", "w")
        high_score_file.write(str(0))
        high_score_file.close()
        HighScores()

class DayScreen(Menu):
    def __init__(self):
        print game_state.game.current_day
        print game_state.game.current_day.generated_date
        x = PygameUI.List([game_state.game.character.name, 'Hp: ' + str(game_state.game.character.health),'Str: ' + str(game_state.game.character.strength),
                           'Char: ' + str(game_state.game.character.charisma),'Int: ' + str(game_state.game.character.intelligence),
                           'Job: ' + game_state.game.character.job, 'Income: $' + str(game_state.game.character.income),
                           'Sanity: ' + str(game_state.game.character.sanity)])
        x.frame = pygame.Rect(4, 4, 150, Menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 0
        x.container.draggable = False #Change to True is needs to be draggable 
        self.scene.add_child(x)

        x = PygameUI.List(game_state.game.character.inventory.item_count())
        x.frame = pygame.Rect(Menu.scene.frame.w -154, 4, 150, Menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 0
        x.container.draggable = False #Change to True is needs to be draggable 
        self.scene.add_child(x)

        if game_state.game.day_counter % 48 != 0:
            
            self.keypressArray = [
                EventScreen,
                StoryScreen, #Reset Game.Day.day_hours back to 16
                StoryScreen,#Store -> -2 on the Game.Day.day_hours (maybe)
                StoryScreen #Work -> -8 on the Game.Day.day_hours
                
            ]
            self.titlesArray = [
                'Events: ' + str(len(game_state.game.events)),
                'Next Day', 
                'Store', 
                'Work', 
            ]
        else:
            self.keypressArray = [
                ElectionDay, #Reset Game.Day.day_hours back to 16
                StoryScreen,#Store -> -2 on the Game.Day.day_hours (maybe)
                StoryScreen #Work -> -8 on the Game.Day.day_hours
                
            ]
            self.titlesArray = [
                'Vote', 
                'Store', 
                'Work', 
            ]
        text = ("Term Number: " + str(game_state.game.term_count) + " \nDay is: " + str(game_state.game.current_day.generated_date)
        + " \n" +" \nHours Left: " + str(game_state.game.current_day.day_hours)) #This displays a text box showing how many hours left in your day to spend
        #For some reason font size 32 looks a lot better than 30 or 34
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 20,
            'height': 300
        }
        

class ElectionDay(Menu): #Use on 48,96 .... +=48
    def __init__(self):
        game_state.game.current_day = game_state.game.Day() #Game.Day()
        self.menu_name = '...'
        
        self.keypressArray = [
            DayScreen,
            EndGame, # Need to add class, build when highscore point system is in place
        ]
        self.titlesArray = [
            'Vote For Trump (Continue Playing)',
            'Vote For Anyone Else (End)',
        ]
        text = game_state.game.current_day.story_text
        #For some reason font size 32 looks a lot better than 30 or 34 
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }

class StoryScreen(Menu):
    def __init__(self):
        
        game_state.game.day_counter += 1
        game_state.game.month_counter += 1
        game_state.game.current_day = game_state.game.Day() #Game.Day()
        game_state.game.current_day.gen_date()
        self.menu_name = '...'
        
        self.keypressArray = [
            DayScreen 
        ]
        self.titlesArray = [
            'Start Day',
        ]
        text = game_state.game.current_day.story_text
        #For some reason font size 32 looks a lot better than 30 or 34 
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        game_state.game.events.append(game_state.game.Event())

class CreateCharacter(Menu):
    """
    ...
    """
    def __init__(self):
        # some things in self are in the parent class.
        self.menu_name = '...'
        self.keypressArray = [
            CreateCharacterManual,
            CreateCharacterAutomatic,
        ]
        self.titlesArray = [
            'Manual',
            'Auto',
        ]

class OpeningMenu(Menu):
    """
    ...
    """
    def __init__(self):
    # What does this do?: Menu.__init__(self)
        self.menu_name = '...'
        self.keypressArray = [
            CreateCharacter,
            StoryScreen, # OptionsFunction #Using this for testing rn 
            HighScores,
            Close, # QuitFunction
        ]
        self.titlesArray = [
            'Start',
            'Options',
            'Highscore',
            'Quit'
        ]

    def box(self):
        print 'Box'

class Close(Menu):
    def __init__(self):
        pygame.display.quit()
        sys.exit()
class EndGame(Menu):
    def __init__(self):
        self.titlesArray = [
            'Test',
        ]
class TestGame(unittest.TestCase):
    def test1(self):
        print 'xxx'

if __name__ == "__main__":
    import sys
    
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((255,120,71)) #Color of the background of window
#    pygame.display.toggle_fullscreen() # Toggle full screen #Apparently only works when running X11
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
    GameState()
    #unittest.main()
else: #used for testing #To run this code do import Trumpocalypse in python shell
    #Needed for testing
    import sys
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((255,120,71)) #Color of the background of window
    #test = [ x for x in range(1000)]
    #print test
    GameState([ x*0 for x in range(1000)])

