import time
import pygame
#import unittest
import random
from TextWrap import *
import PygameUI
#import gc
import math
import copy
import names # People's names.

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
            x = PygameUI.List(['Item %s' % str(i) for i in range(20)], (200, 224, 200))
            x.frame = pygame.Rect(Menu.scene.frame.w // 2, 10, 150, 170)
            x.frame.w = x.container.frame.w
            x.selected_index = 1
            x.border_width = 1
            x.container.draggable = True
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
        self.transit_mode = 0 # Default index=0, which is walking.
        self.selected_house_idx = 0         # House index, default=0
        self.selected_house = 'Staying with Friends' # House title, default='Staying with Friends'
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
            self.inventory.add_item('Food','random')
            self.inventory.add_item('Cash','random')
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
            self.inventory.add_item('Food','random')
            self.inventory.add_item('Cash','random')
            # Location
            self.location = Location()
    
    def born(self):
        print self.name, ' is alive!'
    def died(self):
        print self.name, ' is dead!'
      
class Inventory:
    def __init__(self):
        self.max_items = 999
        self.items = [] # Array of items.
        self.all_choices = [
            'Food','Pie','Garden','Lottery Ticket','New Car','Old Car',
            'Urban House','Suburban House','Rural House','Cash',
            'First Aid Kit','Bicycle','Seeds','Clothing','Transit Pass',
            'Speed Boat'
        ]
        self.is_store = False
        
    def item_count(self):
        #Iterates throught self.items and returns a list of all items in array with number of uses left
        storage = []
        for item in self.items:
            storage.append(item.item_type + ': ' + item.show_amount())
        return storage
    
    def item_count_buy(self):
        #Iterates throught self.items and returns a list of all items in array with number of uses left
        storage = []
        for item in self.items:
            storage.append(item.item_type + ': ' + item.show_amount() + ' $' + item.calculate_purchase_cost())
        return storage
    
    def item_count_sell(self):
        #Iterates throught self.items and returns a list of all items in array with number of uses left
        storage = []
        for item in self.items:
            storage.append(item.item_type + ': ' + item.show_amount() + ' $' + item.calculate_resale_cost())
        return storage
    
    def list_housing_types(self):
        '''Iterates through self.items and returns a list of all items
        that are considered housing types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in item.housing_types:
                storage.append(item.item_type + ': ' + item.show_amount())
        return storage
    
    def list_transit_types(self):
        '''Iterates through self.items and returns a list of all items
        that are considered transit types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in item.transit_types:
                storage.append(item.item_type + ': ' + item.show_amount())
        return storage
    
    def num_items(self):
        # Returns the number of items in the inventory
        return len(self.items)
    
    def add_item(self, item_type = None,remaining_uses = None):
        '''Add an item to this inventory.
        
        If item_type is None then add a random item.
        
        If item_type is not None then add item of this type.
        
        Does the item already exist in the inventory?
        If so, then add the item's stats.
        '''
        if item_type != None:
            new_item = Item(item_type)
            if remaining_uses == 'random':
                if item_type == 'Cash':
                    amount = random.randint(0,10000)
                    new_item.amount = amount
                elif item_type == 'Food':
                    amount = random.randint(0,100)
                    new_item.amount = amount
            else: #remaining_uses != None:
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
            # Add to existing item.
            if existing_item.grouped_item is False:    # Single item.
                # Always add another single item.
                self.items.append( new_item )
            else:                                       # Grouped item.
                if self.is_store:   # Store inventory (unbundle store inventory)
                    self.items.append( new_item )
                else:               # Character
                    existing_item.amount += new_item.amount
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
    
    def shabbitize(self, shabbiness):
        '''Make this inventory shabby.
        
        Always floor the shabbiness. So that 1 pie never become 0 pies.
        
        So Food=110; Food-=ceil(110*.99)=[110-109]=1.
        
        :param shabbiness: The shabbiness ratio, expressed between 0 and 0.99.
        :type shabbiness: float.
        '''
        if shabbiness > 0:
            for item in self.items:
                rand_shabby = random.randint(20, 100) / 100.0 # Make the shabbiness vary some, between 20%-100% of current shabbiness.
                if item.grouped_item is True:   # Grouped
                    item.amount -= math.floor(item.amount * shabbiness * rand_shabby)
                else:                           # Single
                    item.remaining_uses -= math.floor(item.remaining_uses * shabbiness * rand_shabby)
        
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
    all_items = {           # Cost, Resale, Amount, Remaining Use (None=Grouped)
        'Food':             [10,0.8,10, None], # 10 food cost $10; while life=9 food per day.
        'Pie':              [1,0,1, None],
        'Garden':           [200,0.5,10, None],
        'Lottery Ticket':   [10,0.4,1, None],
        'New Car':          [20000,0.5,1,100],
        'Old Car':          [10000,0.4,1,60],
        'Speed Boat':       [20000,0.4,1,40],
        'Urban House':      [400000,0.7,1,100],
        'Suburban House':   [200000,0.5,1,90],
        'Rural House':      [100000,0.8,1,80],
        'Cash':             [0,0,1,None], #?
        'First Aid Kit':    [10,0.6,2,None],
        'Bicycle':          [100,0.8,1,40],
        'Racing Bicycle':   [400,0.8,1,40],
        'Seeds':            [2,0.5,20,None],
        'Clothing':         [200,0.4,20,None], # 20 shirts for $10 per shirt = $200.
        'Transit Pass':     [100,0.6,1,40],
    }
    transit_types = [ # Array of transit modes
        'New Car',
        'Old Car',
        'Speed Boat',
        'Bicycle',
        'Racing Bicycle',
        'Transit Pass',
    ]
    housing_types = [ # Array of transit modes
        'Staying with Friends',
        'Urban House',
        'Suburban House',
        'Rural House',
    ]
    transit_attributes = {  # Speed, Karma, Influence, Butterfly, Health Bonus
                            # KIB based on CO2 emissions.
        'New Car':          [9,-1,-1,-1,0],
        'Old Car':          [8,0,-1,-1,0],
        'Speed Boat':       [5,-1,1,-1,0],
        'Bicycle':          [5,1,1,1,0.2],
        'Racing Bicycle':   [7,1,1,1,0.2],
        'Transit Pass':     [7,1,1,1,0.1],
        'Walking':          [2,1,1,1,0.2],
    }
    def __init__(self, item_type = None):
        self.item_type = item_type
        self.purchase_cost = 0
        self.resale_cost = 0 # A ratio of original cost, between zero to one.
        self.amount = 0
        self.original_amount = 0
        self.remaining_uses = None
        self.max_remaining_uses = None  # To show how much is left.
        self.grouped_item = True        # Default is grouped.
        self.set_item(item_type)
            
    def use_item(self, item_type):
        '''To implement.
        This will somehow use the item.
        Deincroment remaining_uses, along with in game effect.'''
        
        pass
    
    def sell_item(self):
        '''To implement.
        Sells the item based on either its remaining uses or amount remaining.
        '''
        pass
    
    def calculate_purchase_cost(self):
        '''Returns the purchase cost of the item or group of items.
        
        The cost is always rounded up.
        
        This is the same as self.calculate_resale_cost except
        the seller never pays the resale ratio.
        That is, the seller always sells as though the item were
        in new condition, minus whatever amount has been used.
        
        :return: The purchase cost of this item.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return str(math.ceil(self.purchase_cost * (self.amount / self.original_amount)))
        else:                 # Single item (% remaining)
            return str(math.ceil(self.purchase_cost * (self.remaining_uses / self.max_remaining_uses)))
            
    def calculate_resale_cost(self):
        '''Returns the sell cost of the item or group of items.
        
        The cost is always rounded down. So if an item is only
        worth $0.80 then it is really worth $0.
        
        In the case of grouped items this is:
            floor: [ self.resale_cost * (self.amount / self.original_amount) ]
        
        In the case of single items this is:
            floor: [ self.resale_cost * (self.remaining_uses / self.max_remaining_uses) ]
            
        :return: The sell cost of this item.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return str(math.floor(self.purchase_cost * self.resale_cost * (self.amount / self.original_amount)))
        else:                 # Single item (% remaining)
            return str(math.floor(self.purchase_cost * self.resale_cost * (self.remaining_uses / self.max_remaining_uses)))
    
    def show_amount(self):
        '''
        :return: The display value.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return str(self.amount)
        else:                 # Single item (% remaining)
            return str(math.ceil(100*(self.remaining_uses / self.max_remaining_uses)))+'%'
        
    def set_item(self, item_type):
        '''K=1 Karma, I=1 Influence, B=1 Butterfly
        
        Alert levels: red, yellow, no_color
        
        Food: Basic amount=10 uses, 3 uses/day;
            If Food=0: HP-=1/day
            If 0, alert_user( red "...need to find food! ...so hon-gry!" )
        
        Garden: Basic amount=10 uses, -1garden/use, -2hours/use, +6 Food/use, Strength+=0.1/use, (+K,+I,+B)
        
        Bicycle: 0.5x time travel, -1 use/mile travel, Strength+=0.1, (+K+I+B)
        
        Walking(?): 0.25x time travel, Strength+=0.1, (+K+I+B)
        
        Clothing: -1 use/day;
            If Clothing=0: -1Charisma/day, (-I)
            If 0, alert_user( yellow "...need to find clothes!" )
        
        Transit Pass: 1x time travel, -1 use/mile travel, (+K+I+B)
        
        Car: 1x time travel, -1 use/mile travel, (-1K-1B)
        
        House: -1 use/day;
            If Houses=0: -1Charisma, (-1I)
            If 0, alert_user( no_color "...sure would be nice to have a roof to sleep under!" )
        
        ================================================================
            
        How about "single items" versus "grouped items".
        So house, car, bike ... are single items.
        Food, garden, lottery tickets, cash, first aid kit ... are grouped.
        
        Single use items have remaining_use that declines.
        
        Grouped use items have num_in_group that declines.
        
        So 1000 food:
            food.amount = 1000
            food.amount -= 3 per day
            food.remaining_use = None
            
        So two bikes:
            one bike:       bike.remaining_use = 20
                            bike.amount = 1
            another bike:   bike.remaining_use = 20
                            bike.amount = 1
        
        :rtype: None
        :raises TypeError: If item_type is not in self.all_items
        '''
        try:
            n = self.all_items[item_type]
            self.purchase_cost = n[0]
            self.resale_cost = n[1]
            self.amount = n[2]
            self.original_amount = n[2]
            self.remaining_uses = n[3]
            self.max_remaining_uses = n[3]
            if self.remaining_uses is None:
                self.grouped_item = True # Set self.grouped_item
            else:
                self.grouped_item = False
            # If transit item...
        except:
            raise TypeError
            
class GameState:
    def __init__(self,testevents = None):
        global game_state # Reference the global game state variable to this object.
        game_state = self
        self.game = Game()
        self.events_loop = EventsLoop(testevents) # Starts with opening menu.

class Store:
    '''
    Each store is located in a urban, suburban, or rural location.
    
    Then based on this, each store has a distance to park, to urban
    house, to suburban house, and to rural house.
    
    If urban,       distance=rand_float(0,2.0),
                    sub=dist+rand_float(0,4.0),
                    rur=dist+rand_float(0,8.0)
    If suburban,    distance=rand_float(0,4.0),
                    urb=dist+rand_float(0,4.0),
                    rur=dist+rand_float(0,8.0)
    If rural,       distance=rand_float(0,8.0),
                    urb=dist+rand_float(0,4.0),
                    sub=dist+rand_float(0,4.0)
    '''
    grocery_types = [   'Bodega',   'Mini-Market',  'Supermarket',
                        'Market',   'Delicatessen', 'Fishmonger',
                        'Butcher',  'Convenience Store',
                        'Mom-and-Pop',              'Corner Store']
    store_locations = [
        'urban', 'suburban', 'rural'
    ]
    
    def __init__(self):
        self.distance = random.randint(0, 4)
        self.distance = random.randint(0, 4)
        self.store_location = self.store_locations[ random.randint(0, 2) ]
        self.distance = None
        self.distances() # Set distances
        self.inventory = Inventory()
        self.inventory.is_store = True # Set so that inventory is unbundled.
        # Give store a shabbiness-gaudiness value.
        #  0 is low shabbiness.
        #  0.99 is highly shabby.
        self.shabby = random.randint(0, 99) / 100.0
        for i in range(40):
            self.inventory.add_item()
        self.inventory.shabbitize(self.shabby)
        self.grocery_type = self.grocery_types[ random.randint(0, len(self.grocery_types)-1) ]
        self.name = names.NAMES_LIST[ random.randint(0, len(names.NAMES_LIST)-1) ] + "'s " + self.grocery_type
    
    def distances(self):
        if self.store_location == 'urban':
            x = random.uniform(0.0,2.0)
            self.distance = {
                'Urban House':      x,
                'Suburban House':   x+random.uniform(0.0,4.0),
                'Rural House':      x+random.uniform(0.0,8.0),
                'Staying with Friends':      x+random.uniform(0.0,1.0),
            }
        elif self.store_location == 'suburban':
            x = random.uniform(0.0,4.0)
            self.distance = {
                'Urban House':      x+random.uniform(0.0,4.0),
                'Suburban House':   x,
                'Rural House':      x+random.uniform(0.0,4.0),
                'Staying with Friends':      x+random.uniform(0.0,1.0),
            }
        else: # Assume rural
            x = random.uniform(0.0,8.0)
            self.distance = {
                'Urban House':      x+random.uniform(0.0,8.0),
                'Suburban House':   x+random.uniform(0.0,4.0),
                'Rural House':      x,
                'Staying with Friends':      x+random.uniform(0.0,1.0),
            }
        # Round distances to the nearest tenth.
        self.distance['Urban House'] = round(self.distance['Urban House'], 1)
        self.distance['Suburban House'] = round(self.distance['Suburban House'], 1)
        self.distance['Rural House'] = round(self.distance['Rural House'], 1)
        self.distance['Staying with Friends'] = round(self.distance['Staying with Friends'], 1)
        
    def distance_from_house(self):
        '''
        game_state.game.character.selected_house is a string
        that is character's current housing.
        '''
        d = self.distance[ game_state.game.character.selected_house ]    
        return str(d)
    
class CharacterHUD:
    def __init__(self, current_menu):
        self.current_menu = current_menu
        self.warning_change_house = 'Warning: Changing housing takes one hour to complete!'
        
        # Character attributes
        x = PygameUI.List([game_state.game.character.name, 'Hp: ' + str(game_state.game.character.health),'Str: ' + str(game_state.game.character.strength),
                           'Char: ' + str(game_state.game.character.charisma),'Int: ' + str(game_state.game.character.intelligence),
                           'Job: ' + game_state.game.character.job, 'Income: $' + str(game_state.game.character.income),
                           'Sanity: ' + str(game_state.game.character.sanity)], (255,120,71))
        x.frame = pygame.Rect(4, 4, 150, Menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 0
        x.container.draggable = False #Change to True is needs to be draggable 
        current_menu.scene.add_child(x)

        # Character items
        x = PygameUI.List(game_state.game.character.inventory.item_count(), (255,120,71))
        x.frame = pygame.Rect(Menu.scene.frame.w -154, 4, 150, Menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 0
        x.container.draggable = False #Change to True is needs to be draggable 
        current_menu.scene.add_child(x)
        
        # Selected mode of housing.
        # Title.
        lbl = PygameUI.Label('Housing:')
        lbl.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -200, 150, 20)
        current_menu.scene.add_child(lbl)
        # List of available transit types.
        x = PygameUI.List(['Staying with Friends']+game_state.game.character.inventory.list_housing_types(), (200, 224, 200))
        x.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -180, 150, 80)
        #~ x.frame.w = x.container.frame.w
        x.frame.w = 150
        x.selected_index = game_state.game.character.selected_house_idx # selected mode, default = Staying with Friends
        x.border_width = 1
        x.container.draggable = True
        # What to do on change mode? (i.e. clicked)
        x.callback_function = self.click_housing
        current_menu.scene.add_child(x)
        
        # Selected mode of transit.
        # Title.
        lbl = PygameUI.Label('Transit Mode:')
        lbl.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -100, 150, 20)
        current_menu.scene.add_child(lbl)
        # List of available transit types.
        x = PygameUI.List(['Walking']+game_state.game.character.inventory.list_transit_types(), (200, 224, 200))
        x.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -80, 150, 80)
        #~ x.frame.w = x.container.frame.w
        x.frame.w = 150
        x.selected_index = game_state.game.character.transit_mode # selected mode, default = walking
        x.border_width = 1
        x.container.draggable = True
        # What to do on change mode? (i.e. clicked)
        x.callback_function = self.click_transit
        current_menu.scene.add_child(x)
    
    def click_housing(self, selected_index, selected_value):
        '''Update game_state.game.character.selected_house_idx and
        game_state.game.character.selected_house.
        
        Make an alert here saying that it will take X hours to move.
        Default=1. Based on transit?
        
        Or just automatically subtract 1 always.
        And then if 0 hours remain change back to previous
        selected index.
        '''
        # Alert...
        self.current_menu.scene.show_alert(self.warning_change_house)
        
        game_state.game.character.selected_house_idx = selected_index
        if selected_value == 'Staying with Friends':
            game_state.game.character.selected_house = 'Staying with Friends'
        elif 'Urban House' in selected_value:
            game_state.game.character.selected_house = 'Urban House'
        elif 'Suburban House' in selected_value:
            game_state.game.character.selected_house = 'Suburban House'
        elif 'Rural House' in selected_value:
            game_state.game.character.selected_house = 'Rural House'
        else:
            # Raise?
            pass
    
    def click_transit(self, selected_index, selected_value):
        '''Update game_state.game.character.transit_mode
        '''
        game_state.game.character.transit_mode = selected_index
        
class StoreScreenSelect(Menu):
    def __init__(self):
        self.menu_name = '...'
        location = game_state.game.locations_handler.location
        store = location.stores[ location.active_store_idx ]
        
        # Title for list.
        lbl = PygameUI.Label('Click to Buy')
        lbl.frame = pygame.Rect((Menu.scene.frame.w // 2)-200, 100, 400, Menu.scene.frame.h -220)
        self.scene.add_child(lbl)
        # List of items for sale.
        x = PygameUI.List(store.inventory.item_count_buy(), (200, 224, 200))
        x.frame = pygame.Rect((Menu.scene.frame.w // 2)-200, 140, 400, Menu.scene.frame.h -220)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 1
        x.container.draggable = True
        self.scene.add_child(x)
        
        # Title for list.
        lbl = PygameUI.Label('Click to Sell')
        lbl.frame = pygame.Rect((Menu.scene.frame.w // 2), 100, 400, Menu.scene.frame.h -220)
        self.scene.add_child(lbl)
        # List of items to sell.
        x = PygameUI.List(game_state.game.character.inventory.item_count_sell(), (200, 224, 200))
        x.frame = pygame.Rect((Menu.scene.frame.w // 2), 140, 400, Menu.scene.frame.h -220)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 1
        x.container.draggable = True
        self.scene.add_child(x)
        
        # HUD
        CharacterHUD(self)
        
        self.keypressArray = [
             DayScreen
        ]
        self.titlesArray = ['Back to Day'] # Just back to day, no "Back to Store List" 
        self.process_event = True
        self.body = {
            'text': 'Welcome to '+store.name+'!',
            'font_size': 40,
            'top': 10,
            'height': 80
        }
    
    def process_events(self,chosen_position):
        '''Reset location.active_store_idx before leaving.
        '''
        location = game_state.game.locations_handler.location
        location.active_store_idx = None
        pass
            
class StoreScreen(Menu):
    '''Class StoreScreen. This shows the stores in the character's current
    location. Then the user chooses to go to a specific store.
    '''
    def __init__(self):
        self.menu_name = '...'
        location = game_state.game.locations_handler.location
        self.keypressArray = [ StoreScreenSelect for x in range(len(location.stores)) ] + [ DayScreen ]
        self.titlesArray = location.menu_values() + ['Back to Day']
        self.process_event = True
        
        # HUD
        CharacterHUD(self)
    
    def process_events(self,chosen_position):
        '''Subtract the mileage from the hours.
        Also, validate that character has enough resources to make this
        trip. (Need to implement.)
        '''
        location = game_state.game.locations_handler.location
        if len(location.stores) -1  < chosen_position:
            return
        location.active_store_idx = chosen_position
        pass

class Location:
    def __init__(self):
        self.location_name = 'Town of Anywhere'
        self.connected_regions = []
        self.stores = [
            Store() for i in range(random.randint(1,4))
        ]
        self.active_store_idx = None # Index of store being visited.

    def menu_values(self):
        temp_array = []
        for store in self.stores:
            temp_array.append(store.name + ': ' + str(store.distance_from_house()) + ' miles')
        return temp_array
    
class Locations:
    '''https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States'''
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
    locations = [ Location() for i in range(0,8) ]
    def __init__(self):
        # Start in random location.
        self.location = self.locations[ random.randint(0, len(self.locations)-1) ]
    def random_location(self):
        '''Not implemented.
        '''
        pass

class Event:
    def __init__(self, event_text, bonuses={}, story_text='', base_duration=0,
                 duration_rand_min=0, duration_rand_max=0):
        self.event_text = event_text
        self.story_text = story_text
        self.bonuses = bonuses
        self.base_duration = base_duration
        self.duration = None # Dynamic
        self.months_remaining = None # Dynamic
        self.duration_rand_min = duration_rand_min
        self.duration_rand_max = duration_rand_max
        
    def process(self):
        '''Process event. Each time the event happens months_remaining -= 1.
        
        Each bonus of the event does one of the following:
            1) update day hours remaining;
            2) update or add an inventory item;
            3) or, change one of the character's attributes, such as hp.
        '''
        c = game_state.game.character
        for key, value in self.bonuses.iteritems():
            if key == "hours":
                game_state.game.current_day.day_hours += value
            elif key in c.inventory.all_choices:
                c.inventory.add_item(str(key),int(value))
            else:
                n = getattr(c,str(key))
                setattr(c,str(key),n+value)
        self.months_remaining -= 1
        # If self.months_remaining <= 0 ...
        # Then ...
    
    def generate_duration(self):
        '''Generate the duration of this event. It is between
        [base_duration + duration_rand_min] and [base_duration + duration_rand_max].
        Then set months_remaining to be duration.
        '''
        self.duration = self.base_duration + random.randint(self.duration_rand_min, self.duration_rand_max)
        self.months_remaining = self.duration
        
class Events:
    events_array = [
        Event(  'Tsunami', {"health":-1,"sanity":-1},
                "...story...",
                2, 0, 1),
        Event(  'Win Lottery', {"Cash":10000,"sanity":1},
                "...story...",
                1, 0, 0),
        Event(  'Extreme Pollution', {"health":-1,"sanity":-1},
                "...story...",
                4, 0, 4),
        Event(  'Nuclear War', {"health":-2,"sanity":-5},
                "...story...",
                6, 0, 6),
        Event(  'Curfew', {"hours":-4,"sanity":-1},
                "...story...",
                2, 0, 1),
        Event(  'Marshall Law', {"hours":-4,"sanity":-2,"income":-5000},
                "...story...",
                4, 0, 8),
        Event(  'Zombie Apocalypse', {"hours":-4,"sanity":-2,"income":-5000},
                "...story...",
                4, 0, 8),
        Event(  'Power Sleep', {"hours":2,"sanity":2},
                "...story...",
                1, 0, 0),
        Event(  'Find Good Stuff', {"Food":5,"Cash":1000,"sanity":1},
                "...story...",
                1, 0, 0),
    ]
    #~ events_dict = {}
    
    def __init__(self):
        self.inactive_events = []
        self.active_events = []
        pass
    
    def events_values(self):
        '''Returns an array of titles of current inactive events.
        
        :return: Array of titles of current inactive events
        :rtype: array
        '''
        events_temp = []
        for event in self.inactive_events:
            events_temp.append(event.event_text)
        return events_temp
        
    def random_event(self):
        '''Add a random event to inactive_events.'''
        num = random.randint(0,len(Events.events_array)-1) 
        event = copy.deepcopy(Events.events_array[num])
        # Generate event duration.
        event.generate_duration()
        # Add to inactive events
        # Shallow copy?
        self.inactive_events.append(event)
        
    def toggle_event(self, event):
        '''Move an event from self.inactive_event to self.active_event.
        Assumption: Once an event is activated it stays active until
        it runs out. Then it is removed altogether.
        
        :param event: The event to toggle.
        :type event: Event
        '''
        self.active_events.append(event)
        for k,v in enumerate(self.inactive_events):
            if v == event:
                del self.inactive_events[k]
        
class EventScreen(Menu): 
    def __init__(self):
        self.menu_name = '...'
        self.events_values = game_state.game.events_handler.events_values()
        self.keypressArray = [
             DayScreen for x in range(len(game_state.game.events_handler.inactive_events)+1)
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
        '''Define this menu's process_events function.

        This will be called just before changing to the next menu.
        
        Updates the game based on the event chosen by the user.
        
        If the user does not choose an event then return immediately to the
        DayScreen. Otherwise, mark the event as active so that it processes
        from now on during StoryScreen (new month).
        
        Also, process the event for the first time starting now.
        
        :param chosen_position: The position of the menu selected by user.
        :type chosen_position: int
        :return: Does not return a value.
        '''
        if len(self.events_values) -1  < chosen_position:
            return
        event = game_state.game.events_handler.inactive_events[chosen_position]
        event.process()
        # Go from inactive to active.
        game_state.game.events_handler.toggle_event(event)
            
class Game:
    day_counter = 0
    current_year = 2017
    month_counter = 1
    month_day = 1
    term_count = 1
    locations_handler = Locations()
    events_handler = Events()
    #~ events = []
    #~ event_dict = {"Tsunami": {"health":-1,"sanity":-1},
                          #~ "Win Lottery": {"Cash":10000,"sanity":1,},
                          #~ "Extreme Pollution": {"health":-1,"sanity":-1},
                          #~ "Nuclear War": {"health":-2,"sanity":-5},
                          #~ "Curfew": {"hours":-4,"sanity":-1},
                          #~ "Marshall Law": {"income":-5000,"hours":-4,"sanity":-2,},
                          #~ "Power Sleep": {"hours":2,"sanity":2},
                          #~ "Find Good Stuff": {"Food":5,'Cash':1000,"sanity":1},
                          #~ }
    def __init__(self):
        self.current_day = None #self.Day()
        self.character = None #Character('random') creates charecter on start menu becasue its an error.
        #self.character = Character('random')
        #self.score = ...  # will be calculated on game over
            
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

        x = PygameUI.List(game_state.game.character.inventory.item_count(), (255,120,71))
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
        
        # Add HUD
        CharacterHUD(self)
        
        if game_state.game.day_counter % 48 != 0:
            
            self.keypressArray = [
                EventScreen,
                StoryScreen, #Reset Game.Day.day_hours back to 16
                StoreScreen,
                StoryScreen #Work -> -8 on the Game.Day.day_hours
                
            ]
            self.titlesArray = [
                'Events: ' + str(len(game_state.game.events_handler.inactive_events)),
                'Next Day', 
                'Store', 
                'Work', 
            ]
        else:
            self.keypressArray = [
                ElectionDay, #Reset Game.Day.day_hours back to 16
                StoreScreen,
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
        # Do a random event
        game_state.game.events_handler.random_event()

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
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((255,120,71)) #Color of the background of window
    GameState([0,1] + [ x*0 for x in range(1000)])

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
#else: #used for testing #To run this code do import Trumpocalypse in python shell

