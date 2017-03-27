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
import items as ITEMS # Items dictionary.
import jobs #Potential jobs


from pygame.locals import *


if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

game_state = None # A global variable to be accessible by all classes throughout the game.
down_in = None # A global variable for pygameui (menu custom fields)
CharacterDictionary = None

def plus_minus():
    '''Return a random +1 or -1.
    
    :return: Random number, +1 or -1.
    :rtype: int.
    '''
    return random.random()*2 - 1

def euclidean(p1, p2):
    '''Determine euclidean distance between two points.
    
    Pretty straightforward: http://stackoverflow.com/a/4169284/2178774.
    
    :param list p1: A list with first element=x, second=y.
    :param list p2: A list with first element=x, second=y.
    :return: Euc. distance between points.
    :rtype: int.
    '''
    return math.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2)

class Menu:
    '''Original code for the menu class is from:
        @author: avalanchy (at) google mail dot com
        @version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
        @date: 2012-04-08
        @license: This document is under GNU GPL v3
        README on the bottom of document.
        @font: from http://www.dafont.com/coders-crux.font
              more abuot license you can find in data/coders-crux/license.txt
    '''
    process_before_unload = False # Default=False. Set to a function to process.
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
    menu_name = '...' # Default menu name.
     
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
    
    def alert(self, message, buttons, callback_function=None, choice_list=None, choice_list_callback=None):
        '''Helper function to show alert using PygameUI scene.
        
        See class Alert for parameter details.
        '''
        self.scene.show_alert(message, buttons, callback_function, choice_list, choice_list_callback)
        
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
            # Testing.....
            # This is named select because Python already has a list() function.
            # There is probably a callback function here for events.
            # There could be a label passed into CustomField
            # that is added to the left of each list.
            # Is it possible to add this with the Label class?
            x = PygameUI.List([{'item':None,'value':'Item %s' % str(i) } for i in range(20)], (200, 224, 200))
            x.frame = pygame.Rect(Menu.scene.frame.w // 2, 10, 150, 170)
            x.frame.w = x.container.frame.w
            x.selected_index = 1
            x.border_width = 1
            x.container.draggable = True
            Menu.scene.add_child(x)

            x = PygameUI.TextField()
            x.frame = pygame.Rect(10, 50, 150, 30)
            Menu.scene.add_child(x)
         
        def button(self):
            pass
         
        def input_box(self):
            pass
        
        def number(self):
            # What if the number field is instead just a list() field?
            pass

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
    
    def __init__(self,testevents = None):
        self.current_menu = OpeningMenu() # Starts on opening menu. Then changes.
        event_loop = True
        recurse_test = 0
        game_state.first_game_event=False
        while event_loop:
            chosen_position = None # Reset on each loop
            cm = self.current_menu # A quick shortcut
            ########################Used for Testing###############################
            if testevents != None:
                self.test(testevents)
                return
            #####################################################################
            for event in pygame.event.get():
                if game_state.first_game_event==False:
                    game_state.first_game_event=event

                #------------------------------------------
                # If the character's health is 0
                # then kill the character (is_dead=true).
                # Then do the game over screen.
                #------------------------------------------
                if (game_state.game.character != None and
                    game_state.game.character.health <= 0 and 
                    game_state.game.character.is_dead is True and
                    game_state.game.character.game_over is False):
                    game_state.game.character.game_over = True# Set game_over=True
                    print "why we broke"
                    while cm.scene.children:                    # Remove scene children.
                        for child in cm.scene.children:
                            cm.scene.remove_child(child)
                            break
                    self.current_menu = GameOverScreen()
                    continue
                
                if event.type == QUIT: # Quit.
                    pygame.display.quit()
                    sys.exit()
                
                #-------------------------------------------------    
                # If there is an alert then stop everything except
                # mouse down, mouse up, and quit.
                # Use continue to jump forward in event_loop.
                #-------------------------------------------------
                if cm.scene._has_alert is True and (
                    event.type == pygame.MOUSEBUTTONDOWN or
                    event.type == pygame.MOUSEBUTTONUP):
                    # Allow only cm.scene.hit(event.pos) = <PygameUI.Button object at ...>
                    # That is, only allow button presses.
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                        # Only allow elements in the alert element to
                        # receive mouse events.
                        if cm.scene._alert.hit(event.pos) == None:
                            continue
                elif cm.scene._has_alert is True:
                    surface.blit(cm.scene.draw_alert(), (0, 0)) # Make sure to draw alert
                    pygame.display.update()                     # and update, in the case of cm.process_before_unload()=False and chosen_position=True
                    continue
                
                #-----------------------------------
                # Key press events and mouse events.
                #-----------------------------------
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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        global down_in
                        down_in = cm.scene.hit(event.pos)
                        if down_in is not None and not isinstance(down_in, PygameUI.Scene):
                            down_in.mouse_down(event.button, down_in.from_window_point(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP:
                    '''
                    http://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
                    '''
                    if event.button == 1:                    
                        pos = pygame.mouse.get_pos()
                        (pressed1,pressed2,pressed3) = pygame.mouse.get_pressed()
                        print 'Mouse click: ', pos, pygame.mouse.get_pressed()
                        # PygameUI
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
                
                #---------------------------
                # Drawing stuff starts here.
                #---------------------------
                
                # Draw PygameUI.
                surface.blit(cm.scene.draw(), (0, 0))
                # Draw Menu
                if cm.body is False:                 # Draw other menu content
                    cm.init(cm.titlesArray, surface) # Draw non-body menu
                    cm.draw()
                else:
                    cm.init(cm.titlesArray, surface, 200) # Draw menu plus body
                    cm.draw()
                    x = cm.dest_surface.get_rect().centerx - 150 # Calculate x offset
                    pygame.draw.rect(surface, (255,60,71), pygame.Rect(x, cm.body['top'], 300, cm.body['height']), 10) # Draw a box background.
                                               #Box color
                    # There is a slight offset from the text and the box.
                    # The box needs to contain the text. So the text is
                    # going to be slightly smaller. How about 8 pixels?
                    rect = pygame.Rect((x+8,cm.body['top']+8,300-8,300-8)) # left,top,width,height
                    font = pygame.font.Font('data/coders_crux/coders_crux.ttf',cm.body['font_size'])
                    drawText(surface, cm.body['text'], (130,130,130), rect, font, aa=False, bkg=None)
                # Draw scene alert.
                if cm.scene._has_alert is True:
                    surface.blit(cm.scene.draw_alert(), (0, 0))
                # Update
                pygame.display.update()
            
       
            #----------------------------
            # Enter key has been pressed.
            #----------------------------
            
            if chosen_position is not None:         # If there is a chosen position, consider changing to new menu.
                if cm.process_before_unload != False:      # Run function based on current selected item.
                    result = cm.process_before_unload(chosen_position)
                    if result is False:             # If process_before_unload return false, then
                        continue                    # go to next loop (do not go to next menu!)
                while cm.scene.children:            # Remove scene children.
                    for child in cm.scene.children:
                        cm.scene.remove_child(child)
                        break
                self.current_menu = cm.keypressArray[chosen_position]() # Go to the next menu.
            
            # CPU wait.
            pygame.time.wait(0)
    
    def test(testevents):
        '''Run tests.
        
        :param list testevents: A list of keypress indexes to auto-"press".
        '''
        while testevents:
            cm = self.current_menu # A quick shortcut.
            chosen_position = testevents.pop(0)
            while cm.scene.children: # Clear children.
                for child in cm.scene.children:
                    cm.scene.remove_child(child)
                    break
            surface.blit(cm.scene.draw(), (0, 0))
            if cm.body is False:
                cm.init(cm.titlesArray, surface) # Draw non-body menu
                cm.draw()
            else:
                cm.init(cm.titlesArray, surface, 200) # Draw menu plus body
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
        self.reset_modes() # Set transit and housing type.
        self.location = None # Will be set later.
        self.is_dead = False    # Set to True when health=0 to end game
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
        amount = round(self.income * (num_hours / 8), 1)
        self.inventory.add_item('Cash', amount)
        return amount
    
    def reset_modes(self):
        '''Reset transit and housing type to original values.
        '''
        self.transit_mode_idx = 0                       # Transit index, default=0 (walking).
        self.transit_mode = 'Walking'                   # Transit title, default="Walking"
        self.selected_house_idx = 0                     # House index, default=0
        self.selected_house = 'Staying with Friends'    # House title, default="Staying with Friends"
        
    def randomGenerate(self):
        num = random.randint(0,1)
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
            self.location = game_state.game.locations.random_location()
            
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
            self.location = game_state.game.locations.random_location()
    
    def born(self):
        print self.name, ' is alive!'
    def died(self):
        print self.name, ' is dead!'
      
class Inventory:
    def __init__(self):
        '''
        Sample common function: How to quickly retrieve character's cash
        amount?
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
        
    def item_count(self):
        #Iterates throught self.items and returns a list of all items in array with number of uses left
        storage = []
        for item in self.items:
            storage.append({'item':item, 'value': item.item_type + ': ' + item.show_amount()})
        return storage
    
    def item_count_buy(self):
        '''
        Do not allow buying of cash.
        '''
        storage = []
        for item in self.items:
            if item.item_type == 'Cash':
                continue
            storage.append({'item':item, 'value': item.item_type + ': ' + item.show_amount() + ' $' + str(item.calculate_purchase_cost())})
        return storage
    
    def item_count_sell(self):
        '''
        Do not allow selling of cash.
        '''
        storage = []
        for item in self.items:
            if item.item_type == 'Cash':
                continue
            storage.append({'item':item, 'value': item.item_type + ': ' + item.show_amount() + ' $' + str(item.calculate_resale_cost())})
        return storage
    
    def list_housing_types(self):
        '''Iterates through self.items and returns a list of all items
        that are considered housing types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in ITEMS.n['housing_types']:
                storage.append({'item':item, 'value': item.item_type + ': ' + item.show_amount()})
        return storage
    
    def list_transit_types(self):
        '''Iterates through self.items and returns a list of all items
        that are considered transit types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in ITEMS.n['transit_types']:
                storage.append({'item':item, 'value': item.item_type + ': ' + item.show_amount()})
        return storage
    
    def num_items(self):
        # Returns the number of items in the inventory
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
        c = game_state.game.character
        mode = c.transit_mode
        if mode != 'Walking':
            idx = c.transit_mode_idx - 1 # Minus one as walking is not in this list...
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
        existing_item = self.contains_item(new_item.item_type)
        if existing_item != False:
            # Add to existing item.
            if existing_item.grouped_item is False:     # Single item.
                # Always add another single item.
                self.items.append( new_item )
                self.sorted_append( new_item )
            else:                                       # Grouped item.
                if self.is_store:   # Store inventory (unbundle store inventory grouped items)
                    self.items.append( new_item )
                    self.sorted_append( new_item )
                else:               # Character
                    existing_item.amount += new_item.amount
        else:
            self.items.append( new_item )
            self.sorted_append( new_item )
    
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
    For transit:
    Remaining Uses: The number of miles traveled before the item is
        deleted from character's inventory.
    '''
    def __init__(self, item_type = None):
        self.item_type = item_type
        self.purchase_cost = 0
        self.resale_cost = 0 # A ratio of original cost, between zero to one.
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
            return math.ceil(self.purchase_cost * (self.amount / self.original_amount))
        else:                 # Single item (% remaining)
            return math.ceil(self.purchase_cost * (self.remaining_uses / self.max_remaining_uses))
            
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
            return math.floor(self.purchase_cost * self.resale_cost * (self.amount / self.original_amount))
        else:                 # Single item (% remaining)
            return math.floor(self.purchase_cost * self.resale_cost * (self.remaining_uses / self.max_remaining_uses))
    
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
            If 0, alert_user( red "...need to find food!" )
        
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
       
        Single use items have remaining_use that declines.
        
        Grouped use items have num_in_group that declines.
        
        :rtype: None
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
                    self.coordinates['x'] = random.uniform(0.0,2.0) * plus_minus()
                    self.coordinates['y'] = random.uniform(0.0,2.0) * plus_minus()
                elif item_type == 'Suburban House':
                    self.coordinates['x'] = random.uniform(2.0,8.0) * plus_minus()
                    self.coordinates['y'] = random.uniform(2.0,8.0) * plus_minus()
                elif item_type == 'Rural House':
                    self.coordinates['x'] = random.uniform(8.0,20.0) * plus_minus()
                    self.coordinates['y'] = random.uniform(8.0,20.0) * plus_minus()
        except:
            raise TypeError
            
class GameState:
    def __init__(self,testevents = None):
        global game_state # Reference the global game state variable to this object.
        game_state = self
        self.game = Game()
        self.events_loop = EventsLoop(testevents) # Starts with opening menu.
    
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
        '''
        Give store a shabbiness-gaudiness value:
         0 is low shabbiness, 0.99 is highly shabby.
        '''
        self.store_location = self.store_locations[ random.randint(0, 2) ]
        self.coordinates = {} # 0=x, 1=y
        self.distances() # Set distances
        self.inventory = Inventory()
        self.inventory.is_store = True # Set so that inventory is unbundled.
        self.shabby = random.randint(0, 99) / 100.0
        for i in range(40):
            self.inventory.add_item()
        self.inventory.shabbitize(self.shabby)
        self.grocery_type = self.grocery_types[ random.randint(0, len(self.grocery_types)-1) ]
        self.name = names.NAMES_LIST[ random.randint(0, len(names.NAMES_LIST)-1) ] + "'s " + self.grocery_type
    
    def distances(self):
        '''Set store location based on location type.
        Note: Random choice provides random between + and - number:
        https://docs.python.org/2/library/random.html#random.choice
        '''
        if self.store_location == 'urban':
            self.coordinates['x'] = random.uniform(0.0,2.0) * plus_minus()
            self.coordinates['y'] = random.uniform(0.0,2.0) * plus_minus()
        elif self.store_location == 'suburban':
            self.coordinates['x'] = random.uniform(2.0,8.0) * plus_minus()
            self.coordinates['y'] = random.uniform(2.0,8.0) * plus_minus()
        else: # Assume rural
            self.coordinates['x'] = random.uniform(8.0,20.0) * plus_minus()
            self.coordinates['y'] = random.uniform(8.0,20.0) * plus_minus()
    
    def distance_from_house(self):
        '''Calculate the euclidean distance to the current house.
        
        Character's current housing is (string):
            game_state.game.character.selected_house
        
        :return: Distance in miles, rounded to the tenth.
        :rtype: int.
        '''
        if game_state.game.character.selected_house_idx == 0: # Friend's house
            c1 = [0,0]
        else:
            idx = game_state.game.character.selected_house_idx - 1 # Housing is always -1
            x = game_state.game.character.inventory.sorted_items[ 'housing' ][ idx ].coordinates
            c1 = [x['x'], x['y']]
        c2 = self.coordinates
        return round(euclidean(c1, [c2['x'], c2['y']]), 1)


class Jobs:
    def __init__(self):
        self.none = None

    def random_job(self):
        r = random.randint(0,len(jobs.j.keys())-1)
        x = jobs.j.values()[r]
        return Job(x['title'], x['income'], x['company'], x['area'], x['events'])

class Job:
    def __init__(self,title=None,income=None,company=None,area=None,work_events=None):
        self.title = title
        self.income = income
        self.company = company
        self.area = area
        self.work_events = work_events

    def work(self):
        self.random_dictPos = random.randint(0,len(self.work_events)-1)      
        self.hours_worked = self.work_events.values()[self.random_dictPos]
        self.money_made = game_state.game.character.earn_money( self.hours_worked)
        return (self.work_events.keys()[self.random_dictPos] + " \n" +
                + " \nWorked: " + str(self.hours_worked)
                + " \nYou made: " + str(int(self.money_made)))
        


        

class CharacterHUD:
    def __init__(self, current_menu):
        self.current_menu = current_menu
        self.warning_change_house = 'Warning: Changing housing takes one hour to complete!'
        self.warning_cannot_change_house = 'Warning: Changing housing is only allowed at home (home screen)!'
        self.warning_not_enough_hours = 'Warning: Not enough day hours remaining to change housing!'
        game_state.game.character_hud = self # Add to global.
        
        # Draw
        self.elements = []
        self.draw_elements()
    
    def draw_elements(self):
        '''
        '''
        # Remove old (on update)
        if len(self.elements) > 0:
            for e in self.elements:
                self.current_menu.scene.remove_child(e)
        self.elements = []
        
        # Character attributes
        x = PygameUI.List([
                {'item':None, 'value':game_state.game.character.name},
                {'item':None, 'value':'Hp: ' + str(game_state.game.character.health)},
                {'item':None, 'value':'Str: ' + str(game_state.game.character.strength)},
                {'item':None, 'value':'Char: ' + str(game_state.game.character.charisma)},
                {'item':None, 'value':'Int: ' + str(game_state.game.character.intelligence)},
                {'item':None, 'value':'Job: ' + game_state.game.character.job},
                {'item':None, 'value':'Income: $' + str(game_state.game.character.income)},
                {'item':None, 'value':'Sanity: ' + str(game_state.game.character.sanity)}
            ], (255,120,71)
        )
        x.frame = pygame.Rect(4, 4, 150, Menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        #~ x.selected_index = 1
        x.border_width = 0
        x.container.draggable = False #Change to True is needs to be draggable 
        self.current_menu.scene.add_child(x)
        self.elements.append(x)

        # Character items
        x = PygameUI.List(game_state.game.character.inventory.item_count(), (255,120,71))
        x.frame = pygame.Rect(Menu.scene.frame.w -154, 4, 150, Menu.scene.frame.h - 230) #Left quite a gap at end so it is easy on the eyes when list is full
        x.frame.w = x.container.frame.w
        #~ x.selected_index = 1
        x.border_width = 0
        x.container.draggable = True #Change to True is needs to be draggable 
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        
        # Selected mode of housing.
        # Title.
        x = PygameUI.Label('Housing:')
        x.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -200, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of available transit types.
        self.select_housing = PygameUI.List(
            [{'item':None,'value':'Staying with Friends'}]+game_state.game.character.inventory.list_housing_types(),
            (200, 224, 200)
        )
        self.select_housing.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -180, 150, 80)
        self.select_housing.frame.w = 150
        self.select_housing.selected_index = game_state.game.character.selected_house_idx # selected mode, default = Staying with Friends
        self.select_housing.border_width = 1
        self.select_housing.container.draggable = True
        # What to do on change mode? (i.e. click)
        self.select_housing.callback_function = self.click_housing
        self.current_menu.scene.add_child(self.select_housing)
        self.elements.append(self.select_housing)
        
        # Selected mode of transit.
        # Title.
        x = PygameUI.Label('Transit Mode:')
        x.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -100, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of available transit types.
        x = PygameUI.List(
            [{'item':None,'value':'Walking'}]+game_state.game.character.inventory.list_transit_types(),
            (200, 224, 200)
        )
        x.frame = pygame.Rect(Menu.scene.frame.w -154, Menu.scene.frame.h -80, 150, 80)
        x.frame.w = 150
        x.selected_index = game_state.game.character.transit_mode_idx # selected mode, default = walking
        x.border_width = 1
        x.container.draggable = True
        # What to do on change mode? (i.e. click)
        x.callback_function = self.click_transit
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        
    def click_housing(self, selected_index, selected_value, selected_item):
        '''Update game_state.game.character.selected_house_idx and
        game_state.game.character.selected_house.
        
        Make an alert here saying that it will take X hours to move.
        Default=1. Based on transit?
        
        Or just automatically subtract 1 always.
        And then if 0 hours remain change back to previous
        selected index.
        '''
        # If the selected house is the same as current house,
        # then do nothing.
        if (selected_index == game_state.game.character.selected_house_idx and
            selected_value == game_state.game.character.selected_house):
            return
        # If not DayScreen then do nothing.
        # But show warning.
        if self.current_menu.menu_name != 'DayScreen':
            self.current_menu.alert(self.warning_cannot_change_house, ['OK'], self.click_no_change)
            return
        # If hours remaining = 0 then do nothing.
        # But show warning.
        if game_state.game.current_day.day_hours < 1:
            self.current_menu.alert(self.warning_not_enough_hours, ['OK'], self.click_no_change)
            return
        # Force user to confirm change.
        self.current_menu.alert(self.warning_change_house, ['Yes, change housing.', 'No, stay put.'], self.click_alert)
        
    def test_list(self, selected_index, selected_value, selected_item):
        '''This tests adding a list element to an alert box.
        
        self.current_menu.alert('Test alert.', ['OK'], self.click_ok_button, [{'item':self,'value':'meh'}], self.test_list)
        
        Either the OK button or the List is clickable.
        Clicking either one dismisses the alert, calling the relevent
        callback function (click_ok_button or test_list)
        '''
        print selected_index
        print selected_value
        print selected_item
        
    def click_transit(self, selected_index, selected_value, selected_item):
        '''Update game_state.game.character.transit_mode
        '''
        game_state.game.character.transit_mode_idx = selected_index
        game_state.game.character.transit_mode = selected_value.split(':')[0]
    
    def click_no_change(self, confirm):
        '''Reset index of housing list.
        '''
        self.select_housing.selected_index = game_state.game.character.selected_house_idx
        return
        
    def click_alert(self, confirm):
        '''Handle alert button click.
        
        :param boolean confirm: True if first button clicked, False if second button clicked.
        '''
        if confirm is True: # "Yes, change..."
            game_state.game.character.selected_house_idx = self.select_housing.selected_index
            v = self.select_housing.selected_value
            if v == 'Staying with Friends':
                game_state.game.character.selected_house = 'Staying with Friends'
            else:
                game_state.game.character.selected_house = v.split(':')[0]
            game_state.game.current_day.day_hours -= 1 # Reduce day hours.
            self.current_menu.update_body() # update menu
        elif confirm is False: # "No, stay..."
            # Reset index of housing list.
            self.select_housing.selected_index = game_state.game.character.selected_house_idx
        else: # Pass
            pass

class WorkScreen(Menu):
    ''' This will knock 8 hours off the day and possibly more or less depending on the work event'''
    
    def __init__(self):
        self.menu_name = 'WorkScreen'
            
        self.keypressArray = [
                DayScreen, #Need to have work option removed when going back to DayScreen
            ]
        self.titlesArray = [
               'Back to Day',
            ]
            
        work_text = Job().work() #This points to job name which is a str
                                                         #Then tries to do .work()  
        
        self.body = {
            'text': work_text,
            'font_size': 32,
            'top': 20,
            'height': 300
        }

        game_state.game.current_day.day_hours -= self.hours_worked
        
class StoreScreenSelect(Menu):
    def __init__(self):
        self.menu_name = '...'
        location = game_state.game.character.location
        self.store = location.stores[ location.active_store_idx ]    # To get store.
        self.warning_not_enough_cash = 'Oops... that item costs too much money!'
        
        # HUD
        CharacterHUD(self)
        
        # Lists
        self.elements = []
        self.draw_store_lists()
        
        self.keypressArray = [
             DayScreen
        ]
        self.titlesArray = ['Back to Day'] # Just back to day, no "Back to Store List" 
        self.body = {
            'text': 'Welcome to '+self.store.name+'!',
            'font_size': 40,
            'top': 10,
            'height': 80
        }
    
    def draw_store_lists(self):
        # Remove old elements, if they exist (on update lists).
        if len(self.elements) != 0:
            for l in self.elements:
                self.scene.remove_child(l)
        self.elements = []
        
        # Title for list.
        x = PygameUI.Label('Click to Buy')
        x.frame = pygame.Rect((Menu.scene.frame.w // 2)-200, 100, 400, Menu.scene.frame.h -220)
        self.scene.add_child(x)
        self.elements.append(x)
        # List of items for sale.
        x = PygameUI.List(self.store.inventory.item_count_buy(), (200, 224, 200))
        x.frame = pygame.Rect((Menu.scene.frame.w // 2)-200, 140, 400, Menu.scene.frame.h -220)
        x.frame.w = x.container.frame.w
        x.border_width = 1
        x.container.draggable = True
        x.callback_function = self.click_buy
        self.scene.add_child(x)
        self.elements.append(x)
        
        # Title for list.
        x = PygameUI.Label('Click to Sell')
        x.frame = pygame.Rect((Menu.scene.frame.w // 2), 100, 400, Menu.scene.frame.h -220)
        self.scene.add_child(x)
        self.elements.append(x)
        # List of items to sell.
        x = PygameUI.List(game_state.game.character.inventory.item_count_sell(), (200, 224, 200))
        x.frame = pygame.Rect((Menu.scene.frame.w // 2), 140, 400, Menu.scene.frame.h -220)
        x.frame.w = x.container.frame.w
        x.border_width = 1
        x.container.draggable = True
        x.callback_function = self.click_sell
        self.scene.add_child(x)
        self.elements.append(x)
        
    def process_before_unload(self,chosen_position):
        '''Reset location.active_store_idx before leaving.
        
        :param int chosen_position: The position of the menu selected by user.
        :return: Return True if it is okay to continue, False if it is not.
        :rtype: boolean.
        '''
        location = game_state.game.character.location
        location.active_store_idx = None
        return True
        
    def click_buy(self, selected_index, selected_value, selected_item):
        '''Try to buy the clicked item.
        
            Variables:
                Character cash: game_state.game.character.inventory.sorted_items['cash']
                Cost of item: item.calculate_purchase_cost()
                update_or_add function (?)
        
        It is probably necessary for
                now to reset character's selected housing and transit,
                at least for simplicity (reset_modes).
        '''
        game_state.game.character.reset_modes()
        cost = selected_item.calculate_purchase_cost()
        cash = game_state.game.character.inventory.sorted_items['cash'].amount
        print 'cost',cost
        print 'cash',cash
        if cash < cost:
            self.alert(self.warning_not_enough_cash, ['OK'], self.click_no_change)
            return
        # Enough cash, so...
        game_state.game.character.inventory.sorted_items['cash'].amount -= cost
        game_state.game.character.inventory.update_or_add_item(selected_item)
        self.store.inventory.remove_item(selected_item)
        # Redraw lists.
        self.draw_store_lists()
        # Redraw HUD
        game_state.game.character_hud.draw_elements()
    
    def click_sell(self, selected_index, selected_value, selected_item):
        '''Sell the clicked item.
        
        It is probably necessary for
                now to reset character's selected housing and transit,
                at least for simplicity (reset_modes).
        '''
        game_state.game.character.reset_modes()
        cost = selected_item.calculate_resale_cost()
        game_state.game.character.inventory.sorted_items['cash'].amount += cost
        game_state.game.character.inventory.remove_item(selected_item)
        self.store.inventory.update_or_add_item(selected_item)
        # Redraw lists.
        self.draw_store_lists()
        # Redraw HUD
        game_state.game.character_hud.draw_elements()
        
    def click_no_change(self, confirm):
        '''Do nothing.
        '''
        pass


    
class StoreScreen(Menu):
    '''Class StoreScreen. This shows the stores in the character's current
    location. Then the user chooses to go to a specific store.
    '''
    def __init__(self):
        self.menu_name = '...'
        location = game_state.game.character.location
        self.keypressArray = [ StoreScreenSelect for x in range(len(location.stores)) ] + [ DayScreen ]
        self.titlesArray = location.menu_values() + ['Back to Day']
        
        # HUD
        CharacterHUD(self)
    
    def process_before_unload(self, chosen_position):
        '''Go to the store or back home.
        
        If store, validate that travel constraints are met (time).
        Ceiling the travel time (20 minutes = one hour).
        
        Set location.active_store_idx to chosen store.
        
            Variables:  Num day hours remaining:
                            game_state.game.current_day.day_hours
                        Distance x 2 of store (round-trip):
                            game_state.game.character.location.stores[ chosen_position ].distance_from_house()
                        Current mode of transit:
                            mode = game_state.game.character.transit_mode
                            speed = ITEMS.n['transit_attributes'][ mode ][0]
            
            Time = (2 * Distance) / Speed.
            E.g.   (2 * 5 miles ) / 30mph = 20 minutes.
        
        :param int chosen_position: The position of the menu selected by user.
        :return: Return True if it is okay to continue, False if it is not.
        :rtype: boolean.
        '''
        location = game_state.game.character.location
        if len(location.stores) -1  < chosen_position: # To DayScreen.
            return True
        
        #-----------------
        # Validate travel.
        #-----------------
        distance = 2 * location.stores[ chosen_position ].distance_from_house()
        mode = game_state.game.character.transit_mode
        speed = ITEMS.n['transit_attributes'][ mode ][0]
        travel_time = math.ceil(distance / speed)
        if game_state.game.current_day.day_hours < travel_time: # No store.
            store_name = location.stores[ chosen_position ].name
            m = ('Warning: There is not enough time visit '+store_name+'.\nThe trip takes '+
                str(travel_time)+' hours but only '+str(game_state.game.current_day.day_hours)+' hours remain!')
            self.alert(m, ['OK'], self.click_no_change)
            return False
        else:
            # Subtract hours.
            game_state.game.current_day.day_hours -= travel_time
            # Subtract travel cost.
            game_state.game.character.inventory.use_transit(distance)
                
        # To store.
        location.active_store_idx = chosen_position
        return True
        
    def click_no_change(self, confirm):
        #--------
        # This tests whether setting character health to 
        # zero actually results in game over... which it does.
        #--------
        game_state.game.character.health = 0
        game_state.game.character.is_dead = True
        pygame.event.post(game_state.event)
        
        #--------
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
    def __init__(self):
        self.locations = [ Location() for i in range(0,8) ]
        pass
        
    def random_location(self):
        '''Return a random location instance.
        
        :return: A random location instance.
        :rtype: location.
        '''
        return self.locations[ random.randint(0, len(self.locations)-1) ]

class Event:
    '''
    '''
    def __init__(self, event_text, bonuses={}, bonuses_by_ratio={}, story_text='', base_duration=0,
                 duration_rand_min=0, duration_rand_max=0):
        '''
        :param str event_text: Event title.
        :param dict bonuses: Event bonuses.
        :param dict bonuses_by_ratio: Event bonuses using a multiplier ('Cash':0.2 means the character is left with 20% of current cash).
        :param str story_text: A long-worded story for the event.
        :param int base_duration: Base number of months.
        :param int duration_rand_min: Random min. added number of months.
        :param int duration_rand_max: Random max. added number of months.
        '''
        self.event_text = event_text
        self.story_text = story_text
        self.bonuses = bonuses
        self.bonuses_by_ratio = bonuses_by_ratio
        self.base_duration = base_duration
        self.duration = None # Dynamic
        self.months_remaining = None # Dynamic
        self.duration_rand_min = duration_rand_min
        self.duration_rand_max = duration_rand_max
        self.activated = False # Will be changed to True at some point.
        
    def process(self):
        '''Process event. Each time the event happens months_remaining -= 1.
        
        Each bonus of the event does one of the following:
            1) update day hours remaining;
            2) update or add an inventory item;
            3) or, change one of the character's attributes, such as hp.
        '''
        c = game_state.game.character
        for key, value in self.bonuses.iteritems():
            if key == "hours":                      # Hours
                game_state.game.current_day.day_hours += value
            elif key in ITEMS.n['all_choices']:    # Inventory
                c.inventory.add_item(str(key),int(value))
            else:                                   # Character attribute
                n = getattr(c,str(key))
                setattr(c,str(key),n+value)
        for key, value in self.bonuses_by_ratio.iteritems():
            if key == "hours":
                game_state.game.current_day.day_hours *= value
            elif key in ITEMS.n['all_choices']:
                c.inventory.multiply_item(str(key),float(value))
            else:
                n = getattr(c,str(key))
                setattr(c,str(key),n*value)
        # Decrement months.
        self.months_remaining -= 1
        # Make sure it is presently active.
        self.activated = True
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
        #"life will never be the same after..."
        # Max event length ~24 characters bigger breaks the nl character.
        Event(  'A Tsunami', {"health":-1,"sanity":-1}, {},
                "...story...",
                2,0,1), #duration,duration_rand_min, duration_rand_max all in months
        Event(   'You Won the Lottery!', {"Cash":10000,"sanity":1}, {},
                "...story...",
                1,0,0),
        Event(  'Extreme Pollution', {"health":-1,"sanity":-1}, {},
                "...story...",
                4,0,4),
        Event(  'Nuclear War', {"health":-2,"sanity":-5}, {},
                "...story...",
                6,0,6),
        Event(  'Curfew', {"hours":-4,"sanity":-1}, {},
                "...story...",
                2,0,1),
        Event(  'Marshall Law', {"hours":-4,"sanity":-2,"income":-5000}, {},
                "...story...",
                4,0,8),
        Event(  'Zombie Apocalypse', {"hours":-4,"sanity":-2,"income":-5000}, {},
                "...story...",
                4,0,8),
        Event(  'You Power Sleep', {"hours":2,"sanity":2}, {},
                "...story...",
                1,0,0),
        Event(  'Find Supply Cache', {"Food":5,"Cash":1000,"sanity":1}, {},
                "...story...",
                1,0,0),
        Event(  'Puppies!!',{"Cash":-1000, "sanity":10}, {},
                "...story...",
                1,0,0),
        Event(  'Tax Collector',{"Cash":100, "sanity":10}, {"Cash":0.90}, # Removes $100, then sets cash to 90%.
                "...story...",
                1,0,1),
    ]
    
    def __init__(self):
        self.inactive_events = []
        self.active_events = []
        pass
    
    def events_values(self):
        '''Returns a list of titles of current inactive events.
        
        :return: List of titles of current inactive events
        :rtype: list.
        '''
        events_temp = []
        for event in self.inactive_events:
            events_temp.append(event.event_text)
        return events_temp
        
    def random_event(self):
        '''Add a random event to inactive_events.'''
        num = random.randint(0,len(Events.events_array)-1) 
        event = copy.deepcopy(Events.events_array[num]) # copy v. deepcopy =same
        # Generate event duration.
        event.generate_duration()
        # Add to inactive events
        # Shallow copy?
        print 'event in self.inactive_events? ',event in self.inactive_events
        self.inactive_events.append(event)
        
    def toggle_event(self, event):
        '''Move an event from self.inactive_event to self.active_event.
        Assumption: Once an event is activated it stays active until
        it runs out. Then it is removed altogether.
        
        Fire the event for the first time (event.process).
        
        :param event: The event to toggle.
        :type event: Event.
        '''
        self.active_events.append(event)
        for k,v in enumerate(self.inactive_events):
            if v == event:
                del self.inactive_events[k]
        # Run the event.
        event.process()

class GameOverScreen(Menu): 
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
             OpeningMenu,
             Close
        ]
        self.titlesArray = ['Start Over', 'Quit']
        # Tally score (implement)
        game_state.game.tally_score()
        text = 'Buh-bye!'
        #For some reason font size 32 looks a lot better than 30 or 34 
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        # Reset game
        game_state.reset()
        
class EventScreen(Menu): 
    def __init__(self):
        self.menu_name = '...'
        self.events_values = game_state.game.events.events_values()
        self.keypressArray = [
             DayScreen for x in range(len(game_state.game.events.inactive_events)+1)
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
    
    def process_before_unload(self,chosen_position):
        '''Define this menu's process_before_unload function.

        This will be called just before changing to the next menu.
        
        Updates the game based on the event chosen by the user.
        
        If the user does not choose an event then return immediately to the
        DayScreen. Otherwise, mark the event as active so that it processes
        from now on during StoryScreen (new month).
        
        Also, process the event for the first time starting now.
        
        :param int chosen_position: The position of the menu selected by user.
        :return: Return True if it is okay to continue, False if it is not.
        :rtype: boolean.
        '''
        if len(self.events_values) -1  < chosen_position:
            return
        event = game_state.game.events.inactive_events[chosen_position]
        # Go from inactive to active.
        game_state.game.events.toggle_event(event)
        return True
            
class Game:
    day_counter = 0
    current_year = 2017
    month_counter = 1
    month_day = 1
    term_count = 1
    def __init__(self):
        self.jobs = Jobs()
        self.current_day = None
        self.character = None #Character('random') creates charecter on start menu becasue its an error.
        self.locations = Locations()
        self.events = Events()
    
    def tally_score(self):
        print 'Tally the score...'
        
    class Day:
        day_hours = 16
        generated_date = 0
        inauguration_day = "January 20th" #Only needed to be used once, every other time you can use generated_date find it at the bottom of this class

        def __init__(self):
            self.day_hours = 16
            self.eod_mods()
            self.gen_date()

        def eod_mods(self):
            #
            food = game_state.game.character.inventory.sorted_items['food']
            if (food.amount >= 3):
                food.amount -= 3
            else:
                food.amount = 0
                game_state.game.character.health -= 1

            ##
            ##
            #game_state.game.character.check_health()
        
        def gen_date(self):
            
            g = game_state.game
            print 'New day'
            if g.day_counter == 1:
                self.story_text = "Today is " + Game.Day.inauguration_day + " \ninauguration day, Trump is being sworn into office by Chief Justice John Roberts"         
            elif g.day_counter % 48 == 0:
                g.term_count += 1
                self.story_text = "Today is the Election day, Trump is up for Relection"
            else:
                self.story_text = ('You are sitting on the couch watching the news while eating your breakfast and'
                                   +' drinking your arbitrary drink, and the news comes on. The reporter is raving about how life will never be the same after...                 '
                                   +(game_state.game.events.inactive_events[-1].event_text))
            
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
        
        CharacterHUD(self)
        #~ x = PygameUI.List(game_state.game.character.inventory.item_count(), (255,120,71))
        #~ x.frame = pygame.Rect(Menu.scene.frame.w -154, 4, 150, Menu.scene.frame.h -8)
        #~ x.frame.w = x.container.frame.w
        #~ x.selected_index = 1
        #~ x.border_width = 0
        #~ x.container.draggable = False #Change to True is needs to be draggable 
        #~ self.scene.add_child(x)
        
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
        self.menu_name = 'DayScreen'
        
        # Add HUD
        CharacterHUD(self)
        
        if game_state.game.day_counter % 48 != 0:
            
            self.keypressArray = [
                EventScreen,
                StoryScreen, #Reset Game.Day.day_hours back to 16
                StoreScreen,
                WorkScreen #Work -> -8 on the Game.Day.day_hours
                
            ]
            self.titlesArray = [
                'Events: ' + str(len(game_state.game.events.inactive_events)),
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
    
    def update_body(self):
        '''Call this function to update text in the body.
        '''
        text = ("Term Number: " + str(game_state.game.term_count) + " \nDay is: " + str(game_state.game.current_day.generated_date)
        + " \n" +" \nHours Left: " + str(game_state.game.current_day.day_hours)) #This displays a text box showing how many hours left in your day to spend
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 20,
            'height': 300
        }

class ElectionDay(Menu): #Use on 48,96 .... +=48
    def __init__(self):
        game_state.game.day_counter += 1
        game_state.game.month_counter += 1
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
        # Do a random event
        game_state.game.events.random_event()
        game_state.game.day_counter += 1
        game_state.game.month_counter += 1
        
        game_state.game.current_day = game_state.game.Day() #Game.Day()
        
        #~ if game_state.game.character.health == 0:
            #~ self.do_end_screen()
            #~ return
        
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

