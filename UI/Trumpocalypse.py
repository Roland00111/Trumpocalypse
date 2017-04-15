import config as cf
import time
import pygame
import random
from TextWrap import *
import PygameUI
import math
import copy
import names # People's names.
import items as ITEMS # Items dictionary.
import jobs as JOBS #Potential jobs
import events as EVENTS
import menu as MENU

from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()
    

# A global variable for pygameui (menu custom fields)
down_in = None 
CharacterDictionary = None

def plus_minus():
    '''Return a random +1 or -1.
    
    :rtype: int.
    '''
    return random.random()*2 - 1

def euclidean(p1, p2):
    '''Determine euclidean distance between two points.
    Pretty straightforward: http://stackoverflow.com/a/4169284/2178774.
    
    :param list p1: A list with first element=x, second=y.
    :param list p2: A list with first element=x, second=y.
    :return: Euclidean distance between points.
    :rtype: int.
    '''
    return math.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2)

    
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
            self.cm = GameOverScreen()
    
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
                    global down_in
                    down_in = self.cm.scene.hit(event.pos)
                    if (down_in is not None and
                        not isinstance(down_in, PygameUI.Scene)):
                        down_in.mouse_down(event.button,
                            down_in.from_window_point(event.pos))
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
                    if down_in == up_in:
                        down_in.mouse_up(event.button,
                            down_in.from_window_point(event.pos))
                    down_in = None
            elif event.type == pygame.MOUSEMOTION:
                if down_in is not None and down_in.draggable:
                    if down_in.parent is not None:
                        (down_in.parent.
                        child_dragged(down_in, event.rel))
                    down_in.dragged(event.rel)
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
            
class Character:
    ''' This class contains a default character and two hard coded
    characters for testing purposes. 
    '''
    def __init__ (self, create_type):
        ''' Default character '''
        self.name = 'Default'
        self.health = 3
        self.strength = 3
        self.gender = 'male'
        self.age = 40
        self.charisma = 3
        self.intelligence = 3
        self.sanity = 30
        self.inventory = Inventory() # Give character an inventory.
        self.reset_modes() # Set transit and housing type.
        self.location = None # Will be set later.
        self.is_dead = False# Set to True when health=0 to end game
        self.game_over = False  # Set by EventsLoop
        if create_type == 'random':
            self.randomGenerate()
            pass

    def earn_money ( self, num_hours ):
        '''Earn money.
        Round amount to the nearest tenth.
        
        :param num_hours: The number of hours worked.
        :type num_hours: int or float.
        :return: Amount of money earned.
        :rtype: float.
        '''
        amount = round(self.job.income * (num_hours / 8), 1)
        self.inventory.add_item('Cash', amount)
        return amount
    
    def reset_modes(self):
        '''Reset transit and housing type to original values.
        '''
        # Transit index, default=0 (walking).
        self.transit_mode_idx = 0
        # Transit title, default='Walking'
        self.transit_mode = 'Walking'
        # House index, default=0
        self.selected_house_idx = 0
        # House title, default='Staying with Friends'
        self.selected_house = 'Staying with Friends'    
        
    def randomGenerate(self):
        ''' Eventually this will completly randomize what you get but
        for now this contains two characters that are chosen at
        randomly for the purpose of testing. This function also adds
        the characters starting items randomly.
        '''
        num = random.randint(0,1)
        if num == 0:
            self.name = 'Bill'
            self.health = 3
            self.strength = 5
            self.gender = 'male'
            self.age = 69
            self.charisma = 3
            self.intelligence = 1
            #self.income = 10000
            self.sanity = 30
            # Add some random items.
            #To add item insert string of item (item_type) see Item
            #class, else it's random.
            self.inventory.add_item() 
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item('Food','random')
            self.inventory.add_item('Cash','random')
            # Location
            self.location = (cf.gs.game.locations.
                             random_location())
            self.job = self.location.random_job()
            print(self.location.location_name) #DDDDDDDDDD
        elif num == 1:
            self.name = 'Linda'
            self.health = 3
            self.strength = 1
            self.gender = 'female'
            self.age = 40
            self.charisma = 4
            self.intelligence = 5
            
            #self.income = 20000
            self.sanity = 30
            # Add some random items.
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item('Food','random')
            self.inventory.add_item('Cash','random')
            # Location
            self.location=cf.gs.game.locations.random_location()
            self.job = self.location.random_job()
    
    def born(self):
        print (self.name, ' is alive!')
    def died(self):
        print (self.name, ' is dead!')
      
class Inventory:
    ''' This class deals with everything related to the inventory of
    the character.
    '''
    def __init__(self):
        ''' Holds starting data and will get modified to hold the
        contents of the inventory.
        '''
        self.max_items = 999
        self.items = [] # Array of items.
        self.sorted_items = { # Sorted items
            'housing':[],
            'transit':[],
            'other':[],
            'cash':None, # Will be cash item.
            'food':None, # Will be food item.
        }
        self.is_store = False
    def house_degrade(self,ratio):
        ''' Decraments house uses by aratio for cases where an event
        might cause you to loose 50% of your house for example.
        '''
        for house in self.sorted_items['housing']:
            house.remaining_uses *= ratio
            
    def item_count(self):
        ''' Iterates throught self.items and returns a list of all
        items in array with number of uses left.
        '''
        storage = []
        for item in self.items:
            storage.append({'item':item, 'value': item.item_type +
                            ': ' + item.show_amount()})
        return storage
    
    def item_count_buy(self):
        '''Return a list of items available to buy and their buy price.
        Do not allow buying of cash.
        '''
        storage = []
        for item in self.items:
            if item.item_type == 'Cash':
                continue
            storage.append({'item':item, 'value': item.item_type +
                            ': ' + item.show_amount() + ' $' +
                            str(item.calculate_purchase_cost())})
        return storage
    
    def item_count_sell(self):
        '''Return a lits of items available to sell and their
        sell price.
        Do not allow selling of cash.
        '''
        storage = []
        for item in self.items:
            if item.item_type == 'Cash':
                continue
            storage.append({'item':item, 'value': item.item_type +
                            ': ' + item.show_amount() + ' $' +
                            str(item.calculate_resale_cost())})
        return storage
    
    def list_housing_types(self):
        '''Iterates through self.items and returns a list of all items
        that are considered housing types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in ITEMS.n['housing_types']:
                storage.append({'item':item, 'value': item.item_type +
                                ': ' + item.show_amount()})
        return storage
    
    def list_transit_types(self):
        '''Iterates through self.items and returns a list of all items
        that are considered transit types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in ITEMS.n['transit_types']:
                storage.append({'item':item, 'value': item.item_type +
                                ': ' + item.show_amount()})
        return storage
    
    def num_items(self):
        ''' Returns the number of items in the inventory'''
        return len(self.items)
    
    def use_item(self, item, amount):
        '''Try to use an item in the inventory.
        Returns True if the item was used, False otherwise.
        
        :param item: An Item instance.
        :type item: Item.
        :param amount: The amount to use.
        :type amount: float or int.
        '''
        item = self.contains_item(item.item_type)
        if item is False: # Inventory does not contain item.
            return False
        if item.grouped_item is False:  # single item
            item.remaining_uses -= amount
            if item.remaining_uses <= 0:
                self.remove_item(item)
            return True
        else:                           # grouped item
            item.amount -= amount
            if item.amount <= 0:
                self.remove_item(item)
            return True
        
    def use_transit(self, distance):
        ''' This is called whenever you travel some whwere like to
        work or to the store. The function then decrements the uses
        on the proper form of transportation.
        '''
        c = cf.gs.game.character
        mode = c.transit_mode
        if mode != 'Walking':
            idx = c.transit_mode_idx - 1
            # Minus one as walking is not in this list...
            t_item = self.sorted_items['transit'][idx]
            print 'remaining uses:',t_item.remaining_uses
            print 'distance:',distance
            t_item.remaining_uses -= distance
            if t_item.remaining_uses <= 0:
                self.remove_item(t_item)
                # Reset transit type.
                # (This also resets housing type.)
                c.reset_modes()
        
    def remove_item(self, item):
        '''Remove an item from this inventory.
        Item is removed from self.items and self.sorted_items.
        '''
        self.items.remove(item)
        # Remove from sorted items.
        if item.item_type in ITEMS.n['transit_types']:
            self.sorted_items['transit'].remove(item)
        elif item.item_type in ITEMS.n['housing_types']:
            self.sorted_items['housing'].remove(item)
        elif item.item_type == 'Cash':
            self.sorted_items['cash'].amount -= item.amount
        elif item.item_type == 'Food':
            self.sorted_items['food'].amount -= item.amount        
        else:
            self.sorted_items['other'].remove(item)
        
    def multiply_item(self, item_type = None, item_multiplier = None):
        '''Multiply an item by a multiplier.
        Typically this would be called multiply_item('Food', 0.5).
        Which, if the character has food, reduces Food by 50%.
        
        :param str item_type: The type of item.
        :param float item_multiplier: The item amount multiplier.
        '''
        item = self.contains_item(item_type)
        if item:
            if item.grouped_item is False:  # single item
                item.remaining_uses *= item_multiplier 
            else:                           # grouped item
                item.amount *= item_multiplier
                    
    def add_item(self, item_type = None, item_amount = None):
        '''Add an item to this inventory.
        If item_type is None then add a random item.
        If item_type is not None then add item of this type.
        Does the item already exist in the inventory?
        If so, then add the item's stats.
        item_amount:
            if new_item.grouped_item is False: # single item
                new_item.remaining_uses = item_amount 
            else:                               # grouped item
                new_item.amount = item_amount 
        '''
        if item_type != None:
            new_item = Item(item_type)
            if item_amount == 'random':
                if item_type == 'Cash':
                    a = random.randint(0,10000)
                    new_item.amount = a
                elif item_type == 'Food':
                    a = random.randint(0,100)
                    new_item.amount = a
            else:
                if new_item.grouped_item is False: # single item
                    new_item.remaining_uses = item_amount 
                else:                              # grouped item
                    new_item.amount = item_amount
            self.update_or_add_item(new_item)
        else:
            # A random item.
            n = random.randint(0, ITEMS.n['num_items']-1)
            rand_item = Item( ITEMS.n['all_choices'][n] )
            self.update_or_add_item(rand_item)
    
    def sorted_append(self, new_item):
        '''This function ensures that when an item is added to an
        inventory, the same item is also added to sorted_items.
        sorted_items is a dictionary which organizes the items
        in the inventory by type (transit, housing, cash, food, and
        other) for easy access.
        '''
        if new_item.item_type in ITEMS.n['transit_types']:
            self.sorted_items['transit'].append(new_item)
        elif new_item.item_type in ITEMS.n['housing_types']:
            self.sorted_items['housing'].append(new_item)
        elif new_item.item_type == 'Cash':
            self.sorted_items['cash'] = new_item
        elif new_item.item_type == 'Food':
            self.sorted_items['food'] = new_item
        else:
            self.sorted_items['other'].append(new_item)
            
    def update_or_add_item(self, new_item):
        ''' Updates or adds an item to the inventory.
        '''
        existing_item = self.contains_item(new_item.item_type)
        if existing_item != False:
            # Add to existing item.
            if existing_item.grouped_item is False:     # Single item.
                # Always add another single item.
                self.items.append( new_item )
                self.sorted_append( new_item )
            else:                        # Grouped item.
                # Store inventory (unbundle store inventory grouped
                # items).
                if self.is_store:   
                    self.items.append( new_item )
                    self.sorted_append( new_item )
                else:               # Character
                    existing_item.amount += new_item.amount
        else:
            self.items.append( new_item )
            self.sorted_append( new_item )
    
    def contains_item(self, item_type):
        '''Returns the item in the inventory if it exists.
        Otherwise returns False.
        This takes O(n) time as it searches entire list.
        '''
        for existing_item in self.items:
            if existing_item.item_type == item_type:
                return existing_item
        # Still here? Then the item is not in the inventory.
        return False
    
    def shabbitize(self, shabbiness):
        '''Make this inventory shabby.
        Always floor the shabbiness. So that 1 pie never become 0
        pies.
        So Food=110; Food-=ceil(110*.99)=[110-109]=1.
        :param shabbiness:
            The shabbiness ratio, expressed between 0 and 0.99.
        :type shabbiness: float.
        '''
        if shabbiness > 0:
            for item in self.items:
                # Make the shabbiness vary some,
                # between 20%-100% of current shabbiness.
                rand_shabby = random.randint(20, 100) / 100.0 
                if item.grouped_item is True:   # Grouped
                    item.amount -= math.floor(item.amount *
                                             shabbiness * rand_shabby)
                else:                           # Single
                    item.remaining_uses -= math.floor(item.
                    remaining_uses * shabbiness * rand_shabby)
        
class Item:
    '''
    For transit:
    Remaining Uses: The number of miles traveled before the item is
        deleted from character's inventory.
    '''
    def __init__(self, item_type = None):
        self.item_type = item_type
        self.purchase_cost = 0
        # A ratio of original cost, between zero to one.
        self.resale_cost = 0 
        self.amount = 0
        self.original_amount = 0
        self.remaining_uses = None
        self.max_remaining_uses = None  # To show how much is left.
        self.grouped_item = True        # Default is grouped.
        self.coordinates = {}           # For mapped items.
        self.set_item(item_type)
        
    def use_item(self, item_type):
        '''To implement.
        This will somehow use the item.
        Deincroment remaining_uses, along with in game effect.
        '''
        
        pass
    
    def sell_item(self):
        '''To implement.
        Sells the item based on either its remaining uses or amount
        remaining.
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
            return math.ceil(self.purchase_cost * (self.amount /
                                                self.original_amount))
        else:                 # Single item (% remaining)
            return math.ceil(self.purchase_cost * (self.
                        remaining_uses / self.max_remaining_uses))
            
    def calculate_resale_cost(self):
        '''Returns the sell cost of the item or group of items.
        The cost is always rounded down. So if an item is only
        worth $0.80 then it is really worth $0.
        In the case of grouped items this is:
            floor: [ self.resale_cost * (self.amount /
            self.original_amount) ]
        In the case of single items this is:
            floor: [ self.resale_cost * (self.remaining_uses /
            self.max_remaining_uses) ]
            
        :return: The sell cost of this item.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return math.floor(self.purchase_cost * self.resale_cost *
                              (self.amount / self.original_amount))
        else:                 # Single item (% remaining)
            return math.floor(self.purchase_cost * self.resale_cost *
                     (self.remaining_uses / self.max_remaining_uses))
    
    def show_amount(self):
        '''
        :return: The display value.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return str(self.amount)
        else:                 # Single item (% remaining)
            return str(math.ceil(100*(self.remaining_uses /
                                self.max_remaining_uses)))+'%'
        
    def set_item(self, item_type):
        '''Single use items have remaining_use that declines.
        Grouped use items have num_in_group that declines.
    
        :raises TypeError: If item_type is not in ITEMS.n['stats'].
        '''
        try:
            n = ITEMS.n['stats'][item_type]
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
            # If housing item...
            if item_type in ITEMS.n['housing_types']:
                if item_type == 'Urban House':
                    self.coordinates['x'] = (random.uniform(0.0,2.0) *
                                             plus_minus())
                    self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                             plus_minus())
                elif item_type == 'Suburban House':
                    self.coordinates['x'] = (random.uniform(2.0,8.0) *
                                             plus_minus())
                    self.coordinates['y'] = (random.uniform(2.0,8.0) *
                                             plus_minus())
                elif item_type == 'Rural House':
                    self.coordinates['x'] = (random.uniform(8.0,20.0)*
                                             plus_minus())
                    self.coordinates['y'] = (random.uniform(8.0,20.0)*
                                             plus_minus())
        except:
            raise TypeError
            
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
        #~ global cf.gs
        #~ print 'cf.gs:',cf.gs
        cf.gs = self
        #~ print 'cf.gs:',cf.gs
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
        ''' Give store a shabbiness-gaudiness value:
        0 is low shabbiness, 0.99 is highly shabby.
        '''
        self.store_location = self.store_locations[ random.randint
                                                    (0, 2) ]
        self.coordinates = {} # 0=x, 1=y
        self.distances() # Set distances
        self.inventory = Inventory()
        # Set so that inventory is unbundled.
        self.inventory.is_store = True 
        self.shabby = random.randint(0, 99) / 100.0
        for i in range(40):
            self.inventory.add_item()
        self.inventory.shabbitize(self.shabby)
        self.grocery_type = self.grocery_types[ random.randint(0,
                                        len(self.grocery_types)-1) ]
        self.name = names.NAMES_LIST[ random.randint(0,
            len(names.NAMES_LIST)-1) ] + "'s " + self.grocery_type
    
    def distances(self):
        '''Set store location based on location type.
        Note: Random choice provides random between + and - number:
        https://docs.python.org/2/library/random.html#random.choice
        '''
        if self.store_location == 'urban':
            self.coordinates['x'] = (random.uniform(0.0,2.0) *
                                     plus_minus())
            self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                     plus_minus())
        elif self.store_location == 'suburban':
            self.coordinates['x'] = (random.uniform(2.0,8.0) *
                                     plus_minus())
            self.coordinates['y'] = (random.uniform(2.0,8.0) *
                                     plus_minus())
        else: # Assume rural
            self.coordinates['x'] = (random.uniform(8.0,20.0) *
                                     plus_minus())
            self.coordinates['y'] = (random.uniform(8.0,20.0) *
                                     plus_minus())
    
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
        return round(euclidean(c1, [c2['x'], c2['y']]), 1)


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
                                     plus_minus())
            self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                     plus_minus())
        elif self.area == 'suburban':
            self.coordinates['x'] = (random.uniform(2.0,8.0) *
                                     plus_minus())
            self.coordinates['y'] = (random.uniform(2.0,8.0) *
                                     plus_minus())
        else: # Assume rural
            self.coordinates['x'] = (random.uniform(8.0,20.0) *
                                     plus_minus())
            self.coordinates['y'] = (random.uniform(8.0,20.0) *
                                     plus_minus())
    
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
        return round(euclidean(c1, [c2['x'], c2['y']]), 1)

class CharacterHUD:
    ''' This class takes care of everything you see on the main day
    screen.
    '''
    def __init__(self, current_menu):
        self.current_menu = current_menu
        self.warning_change_house = ('Warning: Changing housing '+
                                     'takes one hour to complete!')
        self.warning_cannot_change_house = ('Warning: Changing '+
                'housing is only allowed at home (home screen)!')
        self.warning_not_enough_hours = ('Warning: Not enough day '+
                                'hours remaining to change housing!')
        cf.gs.game.character_hud = self # Add to global.
       
        # Draw
        self.elements = []
        self.draw_elements()
        
    def draw_elements(self):
        ''' This displays everything on the main day screen.
        '''
        # Remove old (on update)
        if len(self.elements) > 0:
            for e in self.elements:
                self.current_menu.scene.remove_child(e)
        self.elements = []
        
        # Character attributes
        x = PygameUI.List([
                {'item':None, 'value':cf.gs.game.character.name},
                {'item':None, 'value':'Hp: ' +
                 str(cf.gs.game.character.health)},
                {'item':None, 'value':'Str: ' +
                 str(cf.gs.game.character.strength)},
                {'item':None, 'value':'Char: ' +
                 str(cf.gs.game.character.charisma)},
                {'item':None, 'value':'Int: ' +
                 str(cf.gs.game.character.intelligence)},
                {'item':None, 'value':'Job: ' +
                 cf.gs.game.character.job.title},
                {'item':None, 'value':'Loc: ' + (cf.gs.game.
                character.location.location_name)},
                {'item':None, 'value':'Income: $' +
                 str(cf.gs.game.character.job.income)},
                {'item':None, 'value':'Sanity: ' +
                 str(cf.gs.game.character.sanity)}
            ], (255,120,71)
        )
        x.frame = pygame.Rect(
            4, 4, 150, self.current_menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        #~ x.selected_index = 1
        x.border_width = 0
        #Change to True is needs to be draggable 
        x.container.draggable = False 
        self.current_menu.scene.add_child(x)
        self.elements.append(x)

        # Character items
        x = PygameUI.List(cf.gs.game.character.inventory.
                          item_count(), (255,120,71))
        #Left quite a gap at end so it is easy on the eyes when list
        #is full
        x.frame = pygame.Rect(
            self.current_menu.scene.frame.w -154, 4, 150,
            self.current_menu.scene.frame.h - 230) 
        x.frame.w = x.container.frame.w
        #~ x.selected_index = 1
        x.border_width = 0
        #Change to True is needs to be draggable 
        x.container.draggable = True 
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        
        # Selected mode of housing.
        # Title.
        x = PygameUI.Label('Housing:')
        x.frame = pygame.Rect(
            self.current_menu.scene.frame.w -154,
            self.current_menu.scene.frame.h -200, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of available transit types.
        self.select_housing = PygameUI.List(
            [{'item':None,'value':'Staying with Friends'}]+
            cf.gs.game.character.inventory.list_housing_types()
        )
        self.select_housing.frame = pygame.Rect(
            self.current_menu.scene.frame.w-154,
            self.current_menu.scene.frame.h -180, 150, 80)
        self.select_housing.frame.w = 150
        # selected mode, default = Staying with Friends
        self.select_housing.selected_index = (cf.gs.game.
                                        character.selected_house_idx)
        self.select_housing.border_width = 1
        self.select_housing.container.draggable = True
        # What to do on change mode? (i.e. click)
        self.select_housing.callback_function = self.click_housing
        self.current_menu.scene.add_child(self.select_housing)
        self.elements.append(self.select_housing)
        
        # Selected mode of transit.
        # Title.
        x = PygameUI.Label('Transit Mode:')
        x.frame = pygame.Rect(
            self.current_menu.scene.frame.w -154,
            self.current_menu.scene.frame.h -100, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of available transit types.
        x = PygameUI.List(
            [{'item':None,'value':'Walking'}]+cf.gs.game.
            character.inventory.list_transit_types()
        )
        x.frame = pygame.Rect(
            self.current_menu.scene.frame.w -154,
            self.current_menu.scene.frame.h -80, 150, 80)
        x.frame.w = 150
        # selected mode, default = walking
        x.selected_index = cf.gs.game.character.transit_mode_idx
        x.border_width = 1
        x.container.draggable = True
        # What to do on change mode? (i.e. click)
        x.callback_function = self.click_transit
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        
    def click_housing(self, selected_index, selected_value,
                      selected_item):
        '''Update cf.gs.game.character.selected_house_idx and
        cf.gs.game.character.selected_house.
        Make an alert here saying that it will take X hours to move.
        Default=1. Based on transit?
        Or just automatically subtract 1 always.
        And then if 0 hours remain change back to previous
        selected index.
        '''
        # If the selected house is the same as current house,
        # then do nothing.
        if (selected_index == cf.gs.game.character.
            selected_house_idx and
            selected_value == cf.gs.game.character.
            selected_house):
            return
        # If not DayScreen then do nothing.
        # But show warning.
        if self.current_menu.menu_name != 'DayScreen':
            self.current_menu.alert(self.warning_cannot_change_house,
                                    ['OK'], self.click_no_change)
            return
        # If hours remaining = 0 then do nothing.
        # But show warning.
        if cf.gs.game.current_day.day_hours < 1:
            self.current_menu.alert(self.warning_not_enough_hours,
                                    ['OK'], self.click_no_change)
            return
        # Force user to confirm change.
        self.current_menu.alert(self.warning_change_house,
        ['Yes, change housing.', 'No, stay put.'], self.click_alert)
        
    def test_list(self, selected_index, selected_value,
                  selected_item):
        '''This tests adding a list element to an alert box.
        self.current_menu.alert('Test alert.', ['OK'],
        self.click_ok_button, [{'item':self,'value':'meh'}],
        self.test_list)
        Either the OK button or the List is clickable.
        Clicking either one dismisses the alert, calling the relevent
        callback function (click_ok_button or test_list)
        '''
        print selected_index
        print selected_value
        print selected_item
        
    def click_transit(self, selected_index, selected_value,
                      selected_item):
        '''Update cf.gs.game.character.transit_mode
        '''
        cf.gs.game.character.transit_mode_idx = selected_index
        cf.gs.game.character.transit_mode = (selected_value.
                                                  split(':')[0])
    
    def click_no_change(self, confirm):
        '''Reset index of housing list.
        '''
        self.select_housing.selected_index = (cf.gs.game.
                                        character.selected_house_idx)
        return
        
    def click_alert(self, confirm):
        '''Handle alert button click.
        :param boolean confirm:
        True if first button clicked, False if second button clicked.
        '''
        if confirm is True: # 'Yes, change...'
            cf.gs.game.character.selected_house_idx = (self.
                                        select_housing.selected_index)
            v = self.select_housing.selected_value
            if v == 'Staying with Friends':
                cf.gs.game.character.selected_house = ('Staying'+
                                                    ' with Friends')
            else:
                cf.gs.game.character.selected_house = (v.
                                                        split(':')[0])
            # Reduce day hours.
            cf.gs.game.mod_hours(-1) 
            self.current_menu.update_body() # update menu
        elif confirm is False: # 'No, stay...'
            # Reset index of housing list.
            self.select_housing.selected_index = (cf.gs.game.
                                        character.selected_house_idx)
        else: # Pass
            pass

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
            Store() for i in range(random.randint(1,4))
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
                                    uniform(0.0, 20.0) * plus_minus())
        self.friend_location['coordinates'][1] = (random.
                                    uniform(0.0, 20.0) * plus_minus())
        
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
                cf.gs.game.character.health -= 1
                cf.gs.game.character.sanity -= 1

            
            elif (cf.gs.game.character.selected_house == ('Staying with Friends')):
                cf.gs.game.character.sanity -= 1
                

                #if sanity dips under zero at the end of the day it hurts
                #your health
            elif (cf.gs.game.character.sanity <=0):
                cf.gs.game.character.sanity = 5
                cf.gs.game.character.health -=1

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
    cf.surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    GameState([0,1] + [ x*0 for x in range(1000)])

if __name__ == '__main__':
    import sys
    
    cf.surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
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

