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
import character as CHARACTER
import sys
import inventory as INVENTORY
import game
import classes

class Menu:
    '''Original code for the menu class is from:
        @author: avalanchy (at) google mail dot com
        @version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14;
            MS Windows XP SP3
       @date: 2012-04-08
        @license: This document is under GNU GPL v3
        README on the bottom of document.
        @font: from http://www.dafont.com/coders-crux.font
              more about license you can find in data/coders-crux/license.txt
    '''
    # Default=False. Set to a function to process.
    process_before_unload = False 
    lista = []
    by = []
    FontSize = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface #how surface game is on is generated
    QuanityOfLista = 0 #initalizer
    BackgroundColor = (255,215,194)#color of background of menu itself)
    TextColor =  (0, 0, 0)#changed to black for readability
    SelectionColor = (255,120,71) #(153,102,255)
    PositionSelection = 0 #initalizer
    Position = (0,0) #set as initalizer
    menu_width = 0 
    menu_height = 0
    keypressArray = []
    titlesArray = []
    # To be filled in by menu classes that need buttons, selects,
    #inputs, and number inputs
    custom_fields = []
    scene = PygameUI.Scene()        # For utilizing pygameui
    body = False                    # This is for main text area.
    menu_name = '...' # Default menu name.
    
    #####################################################
    # A few generic warning messages.
    #####################################################
    warn_no_event = (
        'Warning: No event selected!\n'+
        'You must select an event to activate!')
    warn_ask_health_pack = (
        'Warning: You are about to die!\n'+
        'Would you like to use some health packs?')
    warn_ignore_health_pack = (
        'Warning: Why did you choose not to use a health pack!?\n'+
        'Now you died!')
    warn_no_health_pack = 'Warning: No more health packs!\nYou died!'
    warn_event_active = 'Warning: The event is already activated!'
        
    class Field:
        ''' Saves some variables for future use of methods.'''
        test = ''
        Field = pygame.Surface
        Field_rect = pygame.Rect
        Selection_rect = pygame.Rect

    def move_menu(self, top, left):
        '''
        Starting point for pygame window, parameters are the location
        coordinates for the top, and the left most side of the window.
        '''
        self.Position = (top,left) 

    def set_colors(self, text, selection, background):
        '''
        Sets the text color, color of anything while it is
        selected, and the background color for screens.
        '''
        self.BackgroundColor = background
        self.TextColor =  text
        self.SelectionColor = selection
        
    def set_fontsize(self,font_size):
        ''' Sets the font size taking an integer'''
        self.FontSize = font_size
        
    def set_font(self, path):
        '''Sets font type, takes the path to the font as parameter'''
        self.font_path = path
        
    def get_position(self):
        '''
        Gets the position location for many screens, no parameters
        allows the system to understand which button was chosen
        '''
        return self.PositionSelection
    
    def init(self, lista, dest_surface, height_top=0):
        '''
        This super fake init function is called to generate the
        different items you can select.
        '''
        self.Position = (0,0) # Must be 0,0 each time Menu is redrawn
        self.lista = lista
        self.dest_surface = dest_surface
        self.Quanity = len(self.lista)
        self.CreateStructure(height_top)        
        
    def draw(self,move=0):
        ''' Draw function for every menu that gets called anytime a
            menu changes.
        '''
        if move:
            self.PositionSelection += move 
            if self.PositionSelection == -1:
                self.PositionSelection = self.Quanity - 1
            self.PositionSelection %= self.Quanity
        dm = (self.menu_width*cf.rx, self.menu_height*cf.ry)
        menu = pygame.Surface(dm)
        menu.fill(self.BackgroundColor)
        Selection_rect = self.by[self.PositionSelection].Selection_rect
        pygame.draw.rect(menu,self.SelectionColor,Selection_rect)

        for i in xrange(self.Quanity):
            menu.blit(self.by[i].Field, self.by[i].Field_rect)
        self.dest_surface.blit(menu, self.Position)
        return self.PositionSelection

    def CreateStructure(self, height_top):
        ''' Creates the structure for where all the items that can be
            selected are placed.
        '''
        shift = 0
        self.menu_height = 0
        tmp_fontsz = int(self.FontSize*cf.rcombined)
        self.font = pygame.font.Font(self.font_path, tmp_fontsz)
        for i in xrange(self.Quanity):
            self.by.append(self.Field())
            self.by[i].text = self.lista[i]
            self.by[i].Field = self.font.render(self.by[i].text, 1,
                                                self.TextColor)

            self.by[i].Field_rect = self.by[i].Field.get_rect()
            shift = int(tmp_fontsz * 0.2)

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
        x = self.dest_surface.get_rect().centerx-self.menu_width/2
        y = self.dest_surface.get_rect().centery-self.menu_height/2
        y = y + height_top # Add top offset
        mx, my = self.Position
        self.Position = ((x+mx)*cf.rx, (y+my)*cf.ry)
    
    def alert(self, message, buttons, callback_function=None,
              choice_list=None, choice_list_callback=None):
        '''Helper function to show alert using PygameUI scene.
        There is only one alert allowed at a time.
        See class Alert for parameter details.
        '''
        self.scene.show_alert(message, buttons, callback_function,
                              choice_list, choice_list_callback)

    class CustomField:
        def __init__(self, field_type, field_content, field_label,
                     field_event_hooks):
            '''Testing. Not fully implemented.
            :param str field_type: 'list', 'button', 'input', or
                'number' (also input but limits to numbers)
            :param list field_content:
                Based on parameter field_type.
                If field == 'list':
                    A list of strings for list.
                If field == 'button':
                    One element, string for button text.
                If field == 'input':
                    One element, string for input's current value.
                If field == 'number':
                    One element, int for number field current value.
            :param str field_label: A label to put beside the field.
            :param list field_event_hooks:
                List of dict events, where each dict event has a `type`
                and `callback_function`.
            '''
            self.field_type         = field_type
            self.field_content      = field_content
            self.field_label        = field_label
            self.field_event_hooks  = field_event_hooks
            # Sample: Add a select to the scene.
            self.select()
            
        def select(self):
            '''Testing.
            This is named select because Python already has a list()
            function.
            There is probably a callback function here for events.
            There could be a label passed into CustomField
            that is added to the left of each list.
            Is it possible to add this with the Label class?
            '''
            x = PygameUI.List([{'item':None,'value':'Item %s'%str(i) }
                               for i in range(20)])
            x.frame = pygame.Rect(Menu.scene.frame.w // 2, 10, 150, 170)
            x.frame.w = x.container.frame.w
            x.selected_index = 1
            x.border_width = 1
            x.container.draggable = True
            Menu.scene.add_child(x)

            x = PygameUI.TextField()
            x.frame = pygame.Rect(10, 50, 150, 30)
            Menu.scene.add_child(x)
         
    def remove_pui_children(self):
        '''Remove scene children one at a time.
        For each iteration of while loop remove one child from the
        scene.
        '''
        while self.scene.children:
            for child in self.scene.children:
                self.scene.remove_child(child)
                break

    def draw_menu_body(self):
        '''
        calculates where to put box and text then draws it
        '''
        # Calculate x offset
        w = self.scene.frame.w - 160 - 160
        xoff = self.dest_surface.get_rect().centerx - w/2 
        # Draw a box background.
        pygame.draw.rect(cf.surface, (255,60,71),
            pygame.Rect(xoff, self.body['top'], w,
            self.body['height']), 10) 
        # There is a slight offset from the text
        # and the box. The box needs to contain the text.
        # So the text is going to be slightly smaller.
        # How about 8 pixels???? neccesary?
        rect = pygame.Rect((xoff+8,self.body['top']+8,
                w-8,300-8)) # left,top,width,height
        font = (pygame.font.Font
            ('data/coders_crux/coders_crux.ttf',
            self.body['font_size']))
        drawText(cf.surface, self.body['text'], (0,0,0), rect,
                 font, aa=False, bkg=None)
    
    ############################################################
    # These are a few generic functions:
    # click_died
    # click_use_first_aid
    ############################################################
    def click_died(self, confirm):
        '''User clicked "OK". So end the game.
        In EventsLoop this will immediately jump
        to GameOverScreen, assuming also of course
        that health <= 0.
        :param boolean confirm: Confirm is always true in this case.
        '''
        cf.gs.game.character.health = 0
        cf.gs.game.character.is_dead = True
        pygame.event.post(cf.gs.first_game_event)

    def click_use_first_aid(self, confirm):
        '''User clicked "Use first aid packs" or
        "Do not use first aid packs".
        If "Do not use" end the game. Else try using first aid packs
        until there are no more remaining or until the character's
        health > 0.
        :param boolean confirm: True if "Use" is pressed,
            False if "Do not" is pressed.
        '''
        c = cf.gs.game.character
        ci = c.inventory
        if confirm is False:
            self.alert(self.warn_ignore_health_pack, ['OK'],
                       self.click_died)
        else:
            n = 0
            while (c.health <= 0 and
                ci.use_item(INVENTORY.Item('First Aid Kit'), 1) is True
            ):
                c.modifyHealth(1)
                n += 1
            if c.health <= 0:
                self.alert(self.warn_no_health_pack, ['OK'],
                           self.click_died)
            else:
                if n == 1:
                    m = "You're still alive thanks to a health pack!"
                else:
                    m = ("You're still alive thanks to those "
                        +str(n)+' health packs!')
                self.alert(m, ['OK'])
                
class WorkScreen(Menu):
    ''' This will knock 8 hours off the day and possibly more or less
    depending on the work event
    '''
    def __init__(self):
        self.menu_name = 'WorkScreen'
        #Need to have work option removed when going back to DayScreen
        self.keypressArray = [
                DayScreen, 
            ]
        self.titlesArray = [
               'Back to Day',
            ]
        #This points to job name which is a str.
        #Then tries to do .work()
        work_text = cf.gs.game.character.job.work() 
        
        self.body = {
            'text': work_text,
            'font_size': 32,
            'top': 20,
            'height': 300
        }

class StoreScreenSelect(Menu):
    ''' This class deals with everything about the store '''
    def __init__(self):
        ''' This is a menu class so the init function sets up the
        buttons and what they will look like.
        '''
        self.menu_name = '...'
        location = cf.gs.game.character.location
        # To get store.
        self.store = location.stores[ location.active_store_idx ]
        self.warning_not_enough_cash = ('Oops... that item costs '+
                                        'too much money!')
        
        CharacterHUD(self) # HUD
        
        #~ self.elements = [] # Lists
        self.buy_list = None
        self.sell_list = None
        self.draw_store_lists()
        
        self.keypressArray = [
             DayScreen
        ]
        # Just back to day, no 'Back to Store List' 
        self.titlesArray = ['Back to Day'] 
        self.body = {
            'text': 'Welcome to '+self.store.name+'!',
            'font_size': 40,
            'top': 10,
            'height': 80
        }
    
    def draw_list(self, draw_type):
        if draw_type == 'buy':
            # Remove old
            if self.buy_list != None:
                self.scene.remove_child(self.buy_list)
            # List of items for sale.
            x = PygameUI.List(self.store.inventory.item_count_buy())
            x.frame = pygame.Rect(
                    (Menu.scene.frame.w // 2)-200, 140, 400,
                    Menu.scene.frame.h -220)
            x.frame.w = x.container.frame.w
            x.border_width = 1
            x.container.draggable = True
            x.callback_function = self.click_buy
            self.scene.add_child(x)
            #~ self.elements.append(x)
            self.buy_list = x
        elif draw_type == 'sell':
            # Remove old
            if self.sell_list != None:
                self.scene.remove_child(self.sell_list)
            # List of items to sell.
            x = PygameUI.List(cf.gs.game.character.inventory.
                              item_count_sell())
            x.frame = pygame.Rect(
                    (Menu.scene.frame.w // 2), 140, 400,
                    Menu.scene.frame.h -220)
            x.frame.w = x.container.frame.w
            x.border_width = 1
            x.container.draggable = True
            x.callback_function = self.click_sell
            self.scene.add_child(x)
            #~ self.elements.append(x)
            self.sell_list = x
        
    def draw_store_lists(self):
        ''' This displays the items that are for sale in the store.
        '''
        # Title for list.
        x = PygameUI.Label('Click to Buy')
        x.frame = pygame.Rect((Menu.scene.frame.w // 2)-200, 100, 400,
                              Menu.scene.frame.h -220)
        self.scene.add_child(x)
        # Title for list.
        x = PygameUI.Label('Click to Sell')
        x.frame = pygame.Rect((Menu.scene.frame.w // 2), 100, 400,
                              Menu.scene.frame.h -220)
        self.scene.add_child(x)
        # Add lists
        self.draw_list('buy')
        self.draw_list('sell')
        
    def process_before_unload(self,chosen_position):
        '''Reset location.active_store_idx before leaving.
        :param int chosen_position:
            The position of the menu selected by user.
        :return:
            Return True if it is okay to continue, False if it is not.
        :rtype: boolean.
        '''
        location = cf.gs.game.character.location
        location.active_store_idx = None
        return True
        
    def click_buy(self, selected_index, selected_value,
                  selected_item, child):
        '''Try to buy the clicked item.
            Variables:
                Character cash: (cf.gs.game.character.inventory.
                sorted_items['cash'])
                Cost of item: item.calculate_purchase_cost()
                update_or_add function (?)
        It is probably necessary for
                now to reset character's selected housing and transit,
                at least for simplicity (reset_modes).
        '''
        c = cf.gs.game.character
        c.reset_modes()
        cost = selected_item.calculate_purchase_cost()
        cash = c.inventory.sorted_items['cash'].amount
        if cash < cost:
            self.alert(self.warning_not_enough_cash, ['OK'],
                       self.click_no_change)
            return
        # Enough cash, so...
        c.inventory.sorted_items['cash'].amount -= cost
        c.inventory.update_or_add_item(selected_item)
        self.store.inventory.remove_item(selected_item)
        # Redraw lists.
        self.draw_list('sell')
        # Redraw HUD
        cf.gs.game.character_hud.draw_elements()
        # Remove child
        self.buy_list.remove_selected(child)
        
    def click_sell(self, selected_index, selected_value,
                   selected_item, child):
        '''Sell the clicked item.
        It is probably necessary for now to reset character's selected
        housing and transit, at least for simplicity (reset_modes).
        '''
        c = cf.gs.game.character
        c.reset_modes()
        cost = selected_item.calculate_resale_cost()
        c.inventory.sorted_items['cash'].amount += cost
        c.inventory.remove_item(selected_item)
        self.store.inventory.update_or_add_item(selected_item)
        # Redraw lists.
        self.draw_list('buy')
        # Redraw HUD
        cf.gs.game.character_hud.draw_elements()
        # Remove child
        self.sell_list.remove_selected(child)
        
    def click_no_change(self, confirm):
        '''Do nothing.
        '''
        pass

class StoreScreen(Menu):
    '''
    Class StoreScreen. This shows the stores in the character's
    current location. Then the user chooses to go to a specific store.
    '''
    def __init__(self):
        self.menu_name = '...'
        location = cf.gs.game.character.location
        self.keypressArray = [ StoreScreenSelect
            for x in range(len(location.stores)) ] + [ DayScreen ]
        self.titlesArray = location.menu_values() + ['Back to Day']
        # HUD
        CharacterHUD(self)
    
    def process_before_unload(self, chosen_position):
        '''Go to the store or back home.
        If store, validate that travel constraints are met (time).
        Ceiling the travel time (20 minutes = one hour).
        Set location.active_store_idx to chosen store.
            Variables:  Num day hours remaining:
                            cf.gs.game.current_day.day_hours
                        Distance x 2 of store (round-trip):
                            (cf.gs.game.character.location.
                            stores[ chosen_position ].
                            distance_from_house())
                        Current mode of transit:
                            mode = (cf.gs.game.character.
                                    transit_mode)
                            speed = (ITEMS.n['transit_attributes']
                            [ mode ][0])
            Time = (2 * Distance) / Speed.
            E.g.   (2 * 5 miles ) / 30mph = 20 minutes.
        :param int chosen_position:
            The position of the menu selected by user.
        :return:
            Return True if it is okay to continue, False if it is not.
        :rtype: boolean.
        '''
        location = cf.gs.game.character.location
        if len(location.stores) -1  < chosen_position: # To DayScreen.
            return True
        #-----------------
        # Validate travel.
        #-----------------
        distance = 2 * (location.stores[ chosen_position ].
                        distance_from_house())
        mode = cf.gs.game.character.transit_mode
        speed = ITEMS.n['transit_attributes'][ mode ][0]
        travel_time = math.ceil(distance / speed)
        # No store.
        if cf.gs.game.current_day.day_hours < travel_time: 
            store_name = location.stores[ chosen_position ].name
            m = ('Warning: There is not enough time visit '+
                 store_name+'.\nThe trip takes '+str(travel_time)+
                 ' hours but only '+str(cf.gs.game.current_day.
                                        day_hours)+' hours remain!')
            self.alert(m, ['OK'], None)
            return False
        else:
            # Subtract hours.
            cf.gs.game.mod_hours(-travel_time)
            # Subtract travel cost.
            cf.gs.game.character.inventory.use_transit(distance)
        # To store.
        location.active_store_idx = chosen_position
        return True
        
#No longer being called, replace None in the self alert
    #above to die when going to store with no time
    def click_no_change(self, confirm):
        '''This tests whether setting character health to 
        zero actually results in game over.
        '''
        cf.gs.game.character.health = 0
        cf.gs.game.character.is_dead = True
        pygame.event.post(cf.gs.first_game_event)
        
class GameOverScreen(Menu):
    '''
    This menu when directed to creates the game over screen and
    calls the score to be calculated and replaces highscore if
    the new one is better. 
    '''
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
             OpeningMenu,
             Close
        ]
        self.titlesArray = ['Start Over', 'Quit']
        #Calculate the score, then open and read current highscore
        finalScore = cf.gs.game.tally_score()
        high_score_file = open("high_score.txt", "r")
        highScore = high_score_file.readline()
        high_score_file.close()
        
        if finalScore > (int(highScore)):
            #Replace with new highscore
            text = ('Congratulations, new Highscore! \n '
                    +'Your score:'+str(finalScore))
            
            high_score_file = open('high_score.txt', 'w')
            high_score_file.write(str(finalScore))
            high_score_file.close()
                    
        elif finalScore <= (int(highScore)):
            text = ('Game Over, better luck next time! \n '
                    +'Your score:'+str(finalScore)+' \n '
                    +'HighScore:'+str(highScore))
            
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        # Reset game
        cf.gs.reset()
        
class EventScreen(Menu): 
    def __init__(self):
        self.menu_name = '...'
        self.events_values = cf.gs.game.events.events_values()
        self.keypressArray = [
            DayScreen,
            DayScreen,
        ]
        self.titlesArray = ['Active Event','Go Back To Day']
        text = 'Select an event to continue...'
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        # Some variables specific to this screen.
        self.selected_event = None
        self.left_list = None
        self.right_list = None
        self.draw_lists()
        self.draw_labels()
        
    def draw_labels(self):
        """Draw labels on the left and right."""
        x = PygameUI.Label('Inactive Events')
        x.frame = pygame.Rect(4, 4, 150, 30)
        self.scene.add_child(x)
        
        x = PygameUI.Label('Active Events')
        x.frame = pygame.Rect(Menu.scene.frame.w-150, 4, 150, 30)
        self.scene.add_child(x)
        
    def draw_list(self, side):
        """Function to draw left and right event lists."""
        g = cf.gs.game.events
        if side == 'left':
            self.scene.remove_child(self.left_list)
            x = PygameUI.List(
                g.show_inactive_events(), (200, 224, 200),
                self.click_event_list1
                )
            x.frame = pygame.Rect(4, 4+30, 150, Menu.scene.frame.h -8-30)
            #~ x.frame.w = x.container.frame.w
            x.border_width = 1
            x.container.draggable = True
            self.scene.add_child(x)
            self.left_list = x
        elif side == 'right':
            self.scene.remove_child(self.right_list)
            x = PygameUI.List(
                g.show_active_events(), (200, 224, 200),
                self.click_event_list2
                )
            x.frame = pygame.Rect(Menu.scene.frame.w -154, 4+30, 150, Menu.scene.frame.h -8-30)
            #~ x.frame.w = x.container.frame.w
            x.border_width = 1
            x.container.draggable = True
            self.scene.add_child(x)
            self.right_list = x
            
    def draw_lists(self):
        """Function to draw left and right event lists."""
        self.selected_event = None # Reset the selected event
        self.draw_list('left')
        self.draw_list('right')

    def click_event_list1(self, selected_index,
        selected_value, selected_item, child):
        '''
        This will show the events text after you click the event
        '''
        self.draw_list('right') # Redraw right list.
        self.selected_event = selected_item
        self.body['text'] = (selected_item.story_text+'\n'+
            'Months Remaining: '+str(selected_item.months_remaining)
        )

    def click_event_list2(self, selected_index,
        selected_value, selected_item, child):
        '''
        This will show the events text after you click the event
        '''
        self.draw_list('left') # Redraw left list.
        self.selected_event = selected_item
        self.body['text'] = (selected_item.story_text+'\n'+
            'Months Remaining: '+str(selected_item.months_remaining)
        )

    def process_before_unload(self,chosen_position):
        '''
        The user pressed "Activate Event".
        '''
        if chosen_position == 0:
            # Has the user clicked on a list yet?
            #selected_event is in Event Class, how do I ref it?
            if self.selected_event is None:
                self.alert(self.warn_no_event, ['OK'])
                return False # Stay on EventScreen
            # Clicked on something.
            # Is it active?
            if self.selected_event.activated is True:
                self.alert(self.warn_event_active, ['OK'])
                return False # Stay on EventScreen
            # The event is not activated.
            # Activate event.
            cf.gs.game.events.toggle_event(self.selected_event)
            # Check character.health.
            c = cf.gs.game.character
            if c.health >= 1:
                return True # Back to DayScreen
            elif c.health <= 0:
                self.alert(self.warn_ask_health_pack,
                        [ 'Use some health packs.',
                        'Do not use any health packs.' ],
                        self.click_use_first_aid)
                return False # Stay on EventScreen
        elif chosen_position == 1:
            # User pressed Go Back to Day.
            # In this case simply return True.
            # This will go back to DayScreen.
            return True

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
        text = ''
        self.body = {
            'text': text,
            'font_size': 32,
            'top': -100,
            'height': 0
        }
        
        self.select_value(100,200,0) #button creation click does not work yet though
        self.select_value(200,200,0)
        
        x = PygameUI.List([{'item':None,'value':'Item %s'%str(i) }
                            for i in range(20)])
        x.frame = pygame.Rect(Menu.scene.frame.w // 2, 10, 150, 170)
        x.frame.w = x.container.frame.w
        x.selected_index = 1
        x.border_width = 1
        x.container.draggable = True
        Menu.scene.add_child(x)

        x = PygameUI.TextField()
        x.frame = pygame.Rect(10, 50, 150, 30)
        Menu.scene.add_child(x)
##        self.CustomField( # Something along the lines of.........
##            'list',
##            ['Choice 1', 'Choice 2', 'Choice 3'],
##            'Make a 'good' choice:',
##            { MOUSEBUTTONUP: self.select_on_mouseup }
##        )
        #~ self.CustomField( # Something along the lines of.........
            #~ 'button',
            #~ 'Some Button',
            #~ False,
            #~ { MOUSEBUTTONUP: self.button_on_mouseup }
        #~ )
    
    #def select_on_mouseup(self, event):
        #print ('This is called when selecting a choice from the '+
         #      'select field!')
        
    def select_value(self,left,top,attrib_value):
        '''
        Increment/decrement button drawing takes parameters of the
        left side, top side, and the value for the attribute
        '''
        plus = PygameUI.Button('+')
        plus.frame = pygame.Rect(left, top, 27, 30)
        Menu.scene.add_child(plus)

        value = PygameUI.Label()
        value.frame = pygame.Rect(left, top+50, 27, 30)
        value.text = str(attrib_value)
        Menu.scene.add_child(value)

        minus = PygameUI.Button('-')
        minus.frame = pygame.Rect(left, top+100 ,27, 30)
        Menu.scene.add_child(minus)
        
class CreateCharacterAutomatic(Menu):
    '''The user wants to create an automatic character.
    Set cf.gs.game.character to a random character instance:
    Character('random').
    Display the character's state with CharacterHUD(self). Allow the
    user to start the game or go back to create a new character.
    '''
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
        cf.gs.game.character = CHARACTER.Character('random')
        
        name= cf.gs.game.character.name
        health=str(cf.gs.game.character.health)
        strength=str(cf.gs.game.character.strength)
        gender=cf.gs.game.character.gender
        age=str(cf.gs.game.character.age)
        charisma=str(cf.gs.game.character.charisma)
        intelligence=str(cf.gs.game.character.intelligence)
        job = cf.gs.game.character.job.title
        income = str(cf.gs.game.character.job.income)
        sanity = str(cf.gs.game.character.sanity)
        location = cf.gs.game.character.location.location_name
        
        CharacterHUD(self)
        
        self.body = {
            'text': ('Name: '+name+'\nLocation: '+location+'\n'+'Health: '+health+'\n'+
                     'Strength: '+strength+'\n'+'Gender: '+gender+
                     '\n'+'Age: '+age+'\n'+'Charisma: '+charisma+
                     '\n'+'Intelligence: '+intelligence + '\n' +
                     'Job: ' +job+ '\n' + 'Income: $'+income+'\n'+
                     'Sanity: ' +sanity),'font_size': 32,'top': 40,
            'height': 300
        }

class SnakeScreen(Menu):
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
            DayScreen,
        ]

        self.titlesArray = [
            'Back to Day',
           
        ]
        window=cf.surface
        screen=pygame.display.get_surface()
        clock=pygame.time.Clock()
        font=pygame.font.Font('freesansbold.ttf', 20)
        cf.arcade_game =game.SnakeGame(window,screen,clock,font)
        
        cf.snake_score=0
        
class ArcadeScreen(Menu):
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
            SnakeScreen, #Have to call a class on the keypress array
            DayScreen,
        ]

        self.titlesArray = [
            'Play the Snake game use WASD',
            'Back to Day',
           
        ]

    def process_before_unload(self, chosen_position):
        """Validate there are enough hours left to play the game."""
        if chosen_position == 1:
            # Go back to day screen
            return True
        # Chosen position == 0.
        # The user wants to play the game.
        # Is there enough day hours left to play?
        if cf.gs.game.current_day.day_hours < 1:
            # Alert: Not enough hours left.
            # Alert is: Message, Buttons, Callback_Function
            # Then return False to stay here.
            self.alert(
                ('Warning: There are not enough hours left to play!\n'
                'Try again tomorrow.'), ['OK'])
            return False
        elif cf.gs.game.current_day.day_hours >= 1:
            # Remove one hour from the day.
            # Then return True to leave here and go to the game.
            cf.gs.game.mod_hours(-1)
            return True
        
class HighScores(Menu):
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
            OpeningMenu,
            ResetHighScore, #Have to call a class on the keypress array
            Close,
        ]

        high_score_file = open('high_score.txt', 'r+')
        high_score = high_score_file.read().replace('\n', '')
        high_score_file.close()

        self.titlesArray = [
            'Main Menu',
            'Reset Highscore',
            'Quit',
           
        ]
        a=str(high_score)
 
        Text='Highscore:'+a
        self.body = {
            'text': Text,
            'font_size': 44,
            'top': 240,
            'height': 44
        }
    
    def get_high_score():
        '''
        Opens a hard coded location of a text file, reads it saves it
        and then closes the file returning the high score
        '''
        high_score_file = open('high_score.txt', 'r+')
        highScoreStr = high_score_file.read()
        high_score = high_score_file.read().replace('\n', '')
        high_score_file.close()
        return highScoreStr

class ResetHighScore(Menu): #Idea... what if above when they hit reset highscore
                            #it brings them to a page asking if they are sure
    '''
    Coming to this screen resets your highscore
    '''
    def __init__(self):
        high_score_file = open('high_score.txt', 'w')
        high_score_file.write(str(0))
        high_score_file.close()

        self.keypressArray = [
            HighScores, #Have to call a class on the keypress array
            OpeningMenu,
            
        ]

        self.body = {
            'text': 'Your highscore has been reset to zero!',
            'font_size': 44,
            'top': 140,
            'height': 70
        }

        self.titlesArray = [
            'Back to Highscores',
            'Main Menu',
        ]
        
class DayScreen(Menu):
    def __init__(self):
        self.menu_name = 'DayScreen'
        # Add HUD
        CharacterHUD(self)
        if cf.gs.game.day_counter % 48 != 0:
            self.keypressArray = [
                EventScreen,
                StoryScreen,#Reset Game.Day.day_hours back to 16
                ArcadeScreen,
                StoreScreen,
                WorkScreen #Work -> -8 on the Game.Day.day_hours
            ]
            self.titlesArray = [
                'Events: ' + str(len(cf.gs.game.events.
                                     inactive_events)),
                'Next Month',
                'Arcade',
                'Store', 
                'Work', 
            ]
        else:
            self.keypressArray = [
                ElectionDay, #Reset Game.Day.day_hours back to 16
                StoreScreen,
                #WorkScreen #Work -> -8 on the Game.Day.day_hours
                
            ]
            self.titlesArray = [
                'Vote', 
                'Store', 
                #'Work', 
            ]
        #This displays a text box showing how many hours left in your
        #day to spend
        text = ('Term Number: ' + str(cf.gs.game.term_count) +
                ' \nDay is: ' + str(cf.gs.game.current_day.
                generated_date)+ ' \n' +' \nHours Left: ' +
                str(cf.gs.game.current_day.day_hours)) 
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 20,
            'height': 250
        }
    
    def update_body(self):
        '''
        Call this function to update text in the body.
        '''
        text = ('Term Number: ' + str(cf.gs.game.term_count) +
                ' \nDay is: ' + str(cf.gs.game.current_day.
                generated_date)+ ' \n' +' \nHours Left: ' + str(cf.gs.
                game.current_day.day_hours)) #This displays a text box
                     #showing how many hours left in your day to spend
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 20,
            'height': 250
        }
        
    def process_before_unload(self, chosen_position):
        '''
        Leave the DayScreen after user presses EnterKey.
        
        :param int chosen_position:
            The position of the menu selected by user.
        :return:
            Return True if it is okay to continue, False if it is not.
        :rtype: boolean.
        '''
        if chosen_position != 4: # Anything but work
            return True
        #----------------------
        # Validate work travel.
        #----------------------
        job = cf.gs.game.character.job
        distance = 2 * (job.distance_from_house())
        mode = cf.gs.game.character.transit_mode
        speed = ITEMS.n['transit_attributes'][ mode ][0]
        travel_time = math.ceil(distance / speed)
        # No store.
        if cf.gs.game.current_day.day_hours < travel_time: 
            m = ('Warning: There are not enough hours left to make it '+
                 'to work!'+
                 '\nThe trip takes '+str(travel_time)+
                 ' hours but only '+str(cf.gs.game.current_day.
                                        day_hours)+' hours remain!')
            self.alert(m, ['OK'])
            return False
        else:
            # Subtract hours.
            cf.gs.game.mod_hours(-travel_time)
            # Subtract travel cost.
            cf.gs.game.character.inventory.use_transit(distance)
            return True
        
class ElectionDay(Menu): #Use on 48,96 .... +=48
    '''
    This screen brings you to election day ever 4 years to decide if
    you want to end the game or continue takes the menu as a param
    '''
    def __init__(self):
        cf.gs.game.day_counter += 1
        cf.gs.game.month_counter += 1
        cf.gs.game.locations.update_friend_location()
        cf.gs.game.events.process_inactive_events()
        cf.gs.game.events.random_event()
        cf.gs.game.current_day = cf.gs.game.Day() #Game.Day()
        cf.gs.game.current_day.eod_mods()
        cf.gs.game.current_day.gen_date()
        self.menu_name = '...'
        
        self.keypressArray = [
            DayScreen,
            EndGame, # Need to add class, build when highscore point
                     #system is in place
        ]
        self.titlesArray = [
            'Vote For Trump (Continue Playing)',
            'Vote For Anyone Else (End)',
        ]
        text = cf.gs.game.current_day.story_text
        
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        # Check character health.
        if cf.gs.game.character.health < 1:
            self.alert(self.warn_ask_health_pack,
                [ 'Use some health packs.',
                'Do not use any health packs.' ],
                self.click_use_first_aid)
                
class StoryScreen(Menu):
    '''StoryScreen is the screen where new days occur.
    This causes a few actions to take place:
        1) Update friend's location;
        2) Generate a random event;
        3) Increment day counter and month counter;
        4) Create a new Day() instance.
    When creating a new Day() instance end of day modifications takes
    place.
    '''
    def __init__(self):
        self.menu_name = '...'
        self.keypressArray = [
            DayScreen 
        ]
        self.titlesArray = [
            'Start Day',
        ]
        # Run end of month events.
        cf.gs.game.day_counter += 1
        cf.gs.game.month_counter += 1
        cf.gs.game.locations.update_friend_location()
        cf.gs.game.events.process_inactive_events()
        cf.gs.game.events.random_event() # Do a random event
        cf.gs.game.current_day = cf.gs.game.Day()
        cf.gs.game.current_day.eod_mods()
        cf.gs.game.current_day.gen_date()
        # Set body text.
        text = cf.gs.game.current_day.story_text
        self.body = {
            'text': text,
            'font_size': 32,
            'top': 60,
            'height': 250
        }
        # Check character health.
        if cf.gs.game.character.health < 1:
            self.alert(self.warn_ask_health_pack,
                [ 'Use some health packs.',
                'Do not use any health packs.' ],
                self.click_use_first_aid)
            
class CreateCharacter(Menu):
    '''
    This is the menu in which you decide which character creation you
    would like to go to, or return to the main menu.
    '''
    def __init__(self):
        # some things in self are in the parent class.
        self.menu_name = '...'
        self.keypressArray = [
            CreateCharacterManual,
            CreateCharacterAutomatic,
            OpeningMenu,
        ]
        self.titlesArray = [
            'Manual',
            'Auto',
            'Main Menu',
        ]
        
class OpeningMenu(Menu):
    '''
    The beginning main menu which draws everything for you.
    '''
    def __init__(self):
    # What does this do?: Menu.__init__(self)
        self.menu_name = '...'
        self.om = True
        
        self.keypressArray = [
            CreateCharacter,
            OptionsMenu, # OptionsFunction #Using this for testing rn 
            HighScores,
            Close, # QuitFunction
            
        ]
        self.titlesArray = [
            'Start',
            'Options',
            'Highscore',
            'Quit'
        ]
        
class OptionsMenu(Menu):
    """An options menu that shows lots of options.
    Options such as volume control, music on and off,
    music file selection, and difficulty level.
    """
    
    def __init__(self):
        """Initialize the menu."""
        self.menu_name = '...'
        
        self.keypressArray = [
            OpeningMenu,
        ]
        self.titlesArray = [
            'Main Menu'
        ]
        # Toggle music on and off.
        # Setting is config.music_on.
        self.add_button(True)
    
    def remove_button(self):
        """Remove old buton (on update)."""
        self.scene.remove_child(self.toggle_button_el)
        
    def add_button(self, first_run = False):
        """Add a button that toggles music config setting.
        Do not start or stop the music when first arriving
        at this menu.
        
        :param boolean first_run:
            On the first run do not toggle the config setting.
        """
        if cf.music_on is True:
            m = 'Off'
            if first_run is False:
                cf.start_music('spoopy.wav')
        elif cf.music_on is False:
            m = 'On'
            if first_run is False:
                cf.stop_music()
        x = PygameUI.Button('Turn Music '+m,self.click_music)
        x.frame = pygame.Rect(0, 100, 270, 30)
        self.scene.add_child(x)
        w = x.frame.w
        xoff = cf.surface.get_rect().centerx-w/2
        x.frame = pygame.Rect(xoff, 100, 270, 30)
        self.toggle_button_el = x
        
    def click_music(self, button):
        """Handle the click on the music toggle button.
        
        :param button: This is the clicked PygameUI button.
        """
        if cf.music_on is True:
            cf.music_on = False
        elif cf.music_on is False:
            cf.music_on = True
        # Remove old button.
        self.remove_button()
        # Re-add the button.
        self.add_button()
        
class Close(Menu):
    def __init__(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()
        
class EndGame(Menu):
    def __init__(self):
        self.titlesArray = [
            'Test',
        ]
        
class CharacterHUD:
    ''' This class takes care of everything you see on the main day
    screen.
    This is not a Menu class but is implemented only by Menu classes.
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
        '''
        This displays everything on the main day screen.
        '''
        # Remove old (on update)
        if len(self.elements) > 0:
            for e in self.elements:
                self.current_menu.scene.remove_child(e)
        self.elements = []
        if cf.gs.game.character.health<=0:
            temp_font_size=64
        else:
            temp_font_size=int(48/cf.gs.game.character.health+0.01)
        # Character attributes
        x = PygameUI.List([
                {'item':None, 'value':cf.gs.game.character.name},
                {'item':None, 'value':'Hp: ' +
                 str(cf.gs.game.character.health),'color':(255,0,0),
                 'font_size':temp_font_size},{'item':None,
                 'value':'Str: ' + str(cf.gs.game.character.strength)},
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
            ], (255,215,194)
        )
        x.frame = pygame.Rect(
            4, 4, 150, self.current_menu.scene.frame.h -8)
        x.frame.w = x.container.frame.w
        x.border_width = 0
        #Change to True is needs to be draggable 
        x.container.draggable = False 
        self.current_menu.scene.add_child(x)
        self.elements.append(x)

        # Character items
        ci = cf.gs.game.character.inventory
        x = PygameUI.List(ci.show_main_items(), (255,215,194))
        #Left quite a gap at end so it is easy on the eyes when list
        #is full
        x.frame = pygame.Rect(
            self.current_menu.scene.frame.w -154, 4, 150,
            self.current_menu.scene.frame.h - 230) 
        x.frame.w = x.container.frame.w
        x.border_width = 0
        #Change to True is needs to be draggable 
        x.container.draggable = True 
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        
        # Selected mode of housing.
        x = PygameUI.Label('Housing:')
        x.frame = pygame.Rect(
            self.current_menu.scene.frame.w -154,
            self.current_menu.scene.frame.h -200, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of available transit types.
        self.select_housing = PygameUI.List(
            [{'item':None,'value':'Staying with Friends'}]+
            cf.gs.game.character.inventory.list_housing_types())
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
        
        # DayScreen Notices
        x = PygameUI.Label('Notices:')
        x.frame = pygame.Rect(4,
            self.current_menu.scene.frame.h -200, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of notices.
        x = PygameUI.List(cf.gs.game.notices.display(), (255,215,194)) 
        x.frame = pygame.Rect(4,
            self.current_menu.scene.frame.h -180, 150, 180)
        x.frame.w = 150
        x.border_width = 1
        x.container.draggable = True
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        
        # DayScreen Warnings
        x = PygameUI.Label('Warnings:')
        x.frame = pygame.Rect(4,
            self.current_menu.scene.frame.h -300, 150, 20)
        self.current_menu.scene.add_child(x)
        self.elements.append(x)
        # List of warnings.
        x = PygameUI.List(self.list_warnings(), (255,215,194))
        x.frame = pygame.Rect(4,
            self.current_menu.scene.frame.h -280, 150, 80)
        x.frame.w = 150
        x.border_width = 1
        x.container.draggable = True
        self.current_menu.scene.add_child(x)
        self.elements.append(x)        
        
    def list_warnings(self):
        """Return a list of helpful warnings."""
        lwarn = []
        r = (220,0,0) # Red
        w = (244,234,244) # White
        g = (144,238,144) # Green
        w = (255,255,255) # White
        c = cf.gs.game.character
        ci = c.inventory
        f = ci.sorted_items['food'].amount
        if f > 0 and f < 10:
            lwarn.append(
            {'item':None,'value':'Low food!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        elif f <= 0:
            lwarn.append(
            {'item':None,'value':'0 food: HP -1!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
            lwarn.append(
            {'item':None,'value':'0 food: Sanity -1!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        h = cf.gs.game.character.selected_house
        if h == 'Staying with Friends':
            lwarn.append(
            {'item':None,'value':'No house: Sanity -1!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        if c.health == 1:
            lwarn.append(
            {'item':None,'value':'Low health!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        elif c.health <= 0:
            lwarn.append(
            {'item':None,'value':'0 health!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        if len(cf.gs.game.events.inactive_events) == 5:
            lwarn.append(
            {'item':None,'value':'5 events: Activating!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        if c.sanity > 0 and c.sanity < 10:
            lwarn.append(
            {'item':None,'value':'Low sanity!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        elif c.sanity <= 0:
            lwarn.append(
            {'item':None,'value':'0 sanity!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        cash = ci.sorted_items['cash'].amount
        if cash > 0 and cash < 4000:
            lwarn.append(
            {'item':None,'value':'Low cash!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        elif cash <= 0:
            lwarn.append(
            {'item':None,'value':'0 cash: Sanity-=1!',
            'selected_bgcolor':r,'bgcolor':r,'font_size':20,'color':w})
        if len(lwarn) == 0:
            lwarn.append(
            {'item':None,'value':'Green means go!',
            'selected_bgcolor':g,'bgcolor':g,'font_size':20})
        return lwarn
        
    def click_housing(self, selected_index, selected_value,
                      selected_item, child):
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
                  selected_item, child):
        """This tests adding a list element to an alert box.
        
        self.current_menu.alert('Test alert.', ['OK'],
        self.click_ok_button, [{'item':self,'value':'meh'}],
        self.test_list)
        Either the OK button or the List is clickable.
        Clicking either one dismisses the alert, calling the relevent
        callback function (click_ok_button or test_list)
        """
        print selected_index
        print selected_value
        print selected_item
        
    def click_transit(self, selected_index, selected_value,
                      selected_item, child):
        '''
        Update cf.gs.game.character.transit_mode
        '''
        cf.gs.game.character.transit_mode_idx = selected_index
        cf.gs.game.character.transit_mode = (selected_value.
                                                  split(':')[0])
    
    def click_no_change(self, confirm):
        '''
        Reset index of housing list.
        '''
        self.select_housing.selected_index = (cf.gs.game.
                                        character.selected_house_idx)
        return
        
    def click_alert(self, confirm):
        '''
        Handle alert button click.
        :param boolean confirm:
        True if first button clicked, False if second button clicked.
        '''
        c = cf.gs.game.character
        if confirm is True: # 'Yes, change...'
            c.selected_house_idx = self.select_housing.selected_index
            v = self.select_housing.selected_value
            if v == 'Staying with Friends':
                c.selected_house = 'Staying with Friends'
            else:
                c.selected_house = v.split(':')[0]
            # Reduce day hours.
            cf.gs.game.mod_hours(-1) 
            self.current_menu.update_body() # update menu
            # Redraw CharacterHUD to refresh Warnings List.
            self.draw_elements()
        elif confirm is False: # 'No, stay...'
            # Reset index of housing list.
            self.select_housing.selected_index = c.selected_house_idx
        else: # Pass
            pass
