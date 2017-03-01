
import time
import pygame
import unittest
import random
from TextWrap import *
import PygameUI

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
    custom_fields = []  # To be filled in by menu classes that need buttons, selects, inputs, and number inputs
    scene = PygameUI.Scene()     # For utilizing pygameui
    
    
     
    
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
            ###
            # Here is where a label for the select() element would go.
            ###
        
        def button(self):
            pass
         
        def input(self):
            pass
        
        def number(self):
            # What if the number field is instead just a list() field?
            pass
        
    def keypressFunction(self, text = False, size=22,top=40,boxHeight=300):
        #~ print self # Prints "<__main__.OpeningMenu instance at 0x7f5bb2a99d40>" or "<__main__.CreateCharacter instance at 0x7f5bb2a99ef0>"
        while 1:
            for event in pygame.event.get():
                ########
                # This would be where the iteration for CustomField events takes place
                # pseudo-code:
                # for field in self.custom_fields:
                #    for event_hook, callback_function in field.field_event_hooks.iteritems():
                #        if event.type == event_hook:
                #            # Parentheses here execute the function. The event is passed as an argument to the function.
                #            callback_function(event)
                ########
                if event.type == KEYDOWN:
                    print(str(event.unicode))
                    if event.key == K_UP:
                        self.draw(-1) #here is the Menu class function
                    elif event.key == K_DOWN:
                        self.draw(1) #here is the Menu class function
                    elif event.key == K_RETURN:
                        if self.get_position() == 0: #here is the Menu class function
                            self.keypressArray[0]()
                            return
                        elif self.get_position() == 1:
                            self.keypressArray[1]()
                            return
                        elif self.get_position() == 2:
                            self.keypressArray[2]()
                            return
                        elif self.get_position() == 3: #HERE is where you need to add the look to the next screen!!!!!!
                            self.keypressArray[3]()
                            return
                        elif self.get_position() == 4: #HERE is where you need to add the look to the next screen!!!!!!
                            self.keypressArray[4]()
                            return
                        elif self.get_position() == 5: #HERE is where you need to add the look to the next screen!!!!!!
                            self.keypressArray[5]()
                            return
                        
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
                    down_in = self.scene.hit(event.pos)
                    if down_in is not None and not isinstance(down_in, PygameUI.Scene):
                        down_in.mouse_down(event.button, down_in.from_window_point(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP:
                    up_in = self.scene.hit(event.pos)
                    if down_in == up_in:
                        down_in.mouse_up(event.button, down_in.from_window_point(event.pos))
                    down_in = None
                elif event.type == pygame.MOUSEMOTION:
                    if down_in is not None and down_in.draggable:
                        if down_in.parent is not None:
                            down_in.parent.child_dragged(down_in, event.rel)
                        down_in.dragged(event.rel)
                elif event.type == pygame.KEYDOWN:
                    self.scene.key_down(event.key, event.unicode)
                elif event.type == pygame.KEYUP:
                    self.scene.key_up(event.key)
                # Draw the pygameui input boxes
                surface.blit(self.scene.draw(), (0, 0))
                # Draw other menu content
                if text is False:
                    self.init(self.titlesArray, surface)
                    self.draw()
                else:
                    self.init(self.titlesArray, surface, 200)
                    self.draw()
                    x = self.dest_surface.get_rect().centerx - 150#300 - self.menu_width / 2  Calculate the x offset
                    pygame.draw.rect(surface, (255,60,71), pygame.Rect(x, top, 300, boxHeight), 10) # Draw a box background.
                    # There is a slight offset from the text and the box.
                    # The box needs to contain the text. So the text is
                    # going to be slightly smaller. How about 8 pixels?
                    rect = pygame.Rect((x+8,top+8,300-8,300-8)) # left,top,width,height
                    font = pygame.font.Font('data/coders_crux/coders_crux.ttf',size)
                    drawText(surface, text, (130,130,130), rect, font, aa=False, bkg=None)
                pygame.display.update()

class Character:
    def __init__ (self, create_type):
        self.name = 'Default'
        self.health = 3
        self.strength = 3
        self.gender = 'male'
        self.age = 40
        self.charisma = 3
        self.intelligence = 3
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
            CharacterDictionary = {'Name':self.name,
                                   'Health':self.health,
                                   'Strength':self.strength,
                                   'Gender':self.gender,
                                   'Age':self.age,
                                   'Charisma':self.charisma,
                                   'Intelligence':self.intelligence
                                   }
            
            
        elif num == 1:
            self.name = 'Linda'
            self.health = 3
            self.strength = 1
            self.gender = 'female'
            self.age = 40
            self.charisma = 4
            self.intelligence = 5
            CharacterDictionary = {'Name':self.name,
                                   'Health':self.health,
                                   'Strength':self.strength,
                                   'Gender':self.gender,
                                   'Age':self.age,
                                   'Charisma':self.charisma,
                                   'Intelligence':self.intelligence
                                   }
        
            
    
    def born(self):
        print self.name, ' is alive!'
    def died(self):
        print self.name, ' is dead!'

class GameState:
    def __init__(self):
        global game_state # Reference the global game state variable to this object.
        game_state = self
        self.game = Game()
        # self.current_screen references the 
        # current screen function that is trapped in its events while
        # loop. E.g. when OpeningMenu() moves onto CreateCharacter()
        # then self.current_screen references 
        # the currently running CreateCharacter() class.
        # ...maybe.
        self.current_screen = OpeningMenu() # Start the events while loop.

class Game:
    day_counter = 1
    current_year = 2017
    def __init__(self):
        self.current_day = self.Day()
        self.terms_to_play = 1 # 1, 2, 999
        #self.character = Character('random') creates charecter on start menu becasue its an error.
        
        #self.score = ...  # will be calculated on game over

    class Day:
        def __init__(self):
            if Game.day_counter == 1:
                self.story_text = "Today is \nthe inauguration day and Trump is being sworn into office by Chief Justice John Roberts"
                #Don't put space after \n
            print self.randomDate(str(Game.day_counter) + "/1/" + str(Game.current_year) + " 1:00 AM",
                                  str((Game.day_counter+1)) + "/1/" + str(Game.current_year) + " 1:00 AM",
                                  random.random())
                                    #counter % 12, if == 1 incroment Game.current_year....
            
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
            return self.strTimeProp(start, end, '%m/%d/%Y %I:%M %p', prop)
        
class CreateCharacterManual(Menu):
    def __init__(self):
        '''Eg spend 20 points
        intelligence, charisma, sanity, cash
        '''
        self.menu_name = '...'
        self.keypressArray = [
            Close,
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
        # Call the parent's keypress handler
        self.keypressFunction()
    
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
        self.character = Character('random')
        
        name=CharacterDictionary['Name']
        health=str(CharacterDictionary['Health'])
        strength=str(CharacterDictionary['Strength'])
        gender=CharacterDictionary['Gender']
        age=str(CharacterDictionary['Age'])
        charisma=str(CharacterDictionary['Charisma'])
        intelligence=str(CharacterDictionary['Intelligence'])
 
        Text="Name: "+name+" \n"+"Health: "+health+" \n"+"Strength: "+strength+" \n"+"Gender: "+gender+" \n"+"Age: "+age+" \n"+"Charisma: "+charisma+" \n"+"Intelligence: "+intelligence
        #Text="Today is\nthe inauguration day and Trump is being sworn into office by Chief Justice John Roberts"
        self.keypressFunction(Text,30)
        
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
        # Call the parent's keypress handler
        self.keypressFunction(Text,44,240,44)
    
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
        print('Hello')
    
class StoryScreen(Menu):
    def __init__(self):
        print game_state.game.current_day
        self.menu_name = '...'
        
        self.keypressArray = [
            DayScreen #not implemented yet,
        ]
        self.titlesArray = [
            'Start Day',
        ]
        text = game_state.game.current_day.story_text
        self.keypressFunction(text) # Pass text
        
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
        # Call the parent's keypress handler
        self.keypressFunction()

class OpeningMenu(Menu):
    """
    ...
    """
    def __init__(self):
        # some things in self are in the parent class.
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
        # Call the parent's keypress handler
        self.keypressFunction()

    def box(self):
        print 'Box'

class Close(Menu):
    def __init__(self):
        pygame.display.quit()
        sys.exit()


if __name__ == "__main__":
    import sys
#    from Create_Character import *
    
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
