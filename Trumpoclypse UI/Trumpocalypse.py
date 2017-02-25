

import pygame
import unittest
import random
from TextWrap import *

from pygame.locals import *


if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

game_state = None # A global variable to be accessible by all classes throughout the game.

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
    
    def keypressFunction(self, text = False, size=22,top=40,boxHeight=300):
        surface.fill((255,120,71))
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
        print self # Prints "<__main__.OpeningMenu instance at 0x7f5bb2a99d40>" or "<__main__.CreateCharacter instance at 0x7f5bb2a99ef0>"
        while 1:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
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
                pygame.display.update()

class Character:
    def __init__ (self, create_type):
        self.name = 'Default'
        self.health = 3
        self.strength = 3
        self.gender = 'male'
        self.age = 999
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
        if num == 0:
            self.name = 'Bill'
            self.strength = 2
            self.age = 86
        elif num == 1:
            pass
    
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
        #def randomCharacter():
        # self.ch
        #  passB

class Game:
    def __init__(self):
        self.terms_to_play = 1 # 1, 2, 999
        self.character = Character('random')
        #self.score = ...  # will be calculated on game over
        
class CreateCharacterManual(Menu):
    def __init__(self):
        '''Eg spend 20 points
        intelligence, charisma, sanity, cash
        '''
        self.menu_name = '...'
        self.keypressArray = [
            None,
            None,
            None,
            None,
            None, # Continue
        ]
        self.titlesArray = [
            'Continue To Location',
            'Back To Previous Page'
        ]
        # Call the parent's keypress handler
        self.keypressFunction()
    
class CreateCharacterAutomatic(Menu):
    def __init__(self):
        pass
        
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
        print game_state
        self.menu_name = '...'
        self.keypressArray = [
            CreateCharacterManual,
            CreateCharacterAutomatic,
        ]
        self.titlesArray = [
            'a',
            'b',
        ]
        text = 'This is some text that will be wrapped this way we can have a day beginning screen This is some text that will be wrapped this way we can have a day beginning screen This is some text that will be wrapped this way we can have a day beginning screen This is some text that will be wrapped this way we can have a day beginning screen This is some text that will be wrapped this way we can have a day beginning screen'
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
            DayScreen, # OptionsFunction #Using this for testing rn 
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
