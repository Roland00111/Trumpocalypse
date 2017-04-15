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
import jobs as JOBS #Potential jobs

from pygame.locals import *

print 'surface:',surface

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

    class Field:
        ''' Saves some variables for the ????.'''
        
        test = ''
        Field = pygame.Surface
        Field_rect = pygame.Rect
        Selection_rect = pygame.Rect

    def move_menu(self, top, left):
        ''' Starting point for pygame window.'''
        
        self.Position = (top,left) 

    def set_colors(self, text, selection, background):
        ''' Sets the color for everything when called.'''
        
        self.BackgroundColor = background
        self.TextColor =  text
        self.SelectionColor = selection
        
    def set_fontsize(self,font_size):
        ''' Sets the font size.'''
        
        self.FontSize = font_size
        
    def set_font(self, path):
        '''Sets font type.'''
        
        self.font_path = path
        
    def get_position(self):
        '''Gets the position of the selecter????.'''
        
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
        menu = pygame.Surface((self.menu_width, self.menu_height))
        menu.fill(self.BackgroundColor)
        Selection_rect = self.by[self.PositionSelection].Selection_rect
        pygame.draw.rect(menu,self.SelectionColor,Selection_rect)

        for i in xrange(self.Quanity):
            menu.blit(self.by[i].Field,self.by[i].Field_rect)
        self.dest_surface.blit(menu,self.Position)
        return self.PositionSelection

    def CreateStructure(self, height_top):
        ''' Creates the structure for where all the items that can be
            selected are placed.
        '''
        shift = 0
        self.menu_height = 0
        self.font = pygame.font.Font(self.font_path, self.FontSize)
        for i in xrange(self.Quanity):
            self.by.append(self.Field())
            self.by[i].text = self.lista[i]
            self.by[i].Field = self.font.render(self.by[i].text, 1,
                                                self.TextColor)

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
        x = self.dest_surface.get_rect().centerx-self.menu_width/2
        y = self.dest_surface.get_rect().centery-self.menu_height/2
        y = y + height_top # Add top offset
        mx, my = self.Position
        self.Position = (x+mx, y+my) 
    
    def alert(self, message, buttons, callback_function=None,
              choice_list=None, choice_list_callback=None):
        '''Helper function to show alert using PygameUI scene.
        There is only one alert allowed at a time.
        
        See class Alert for parameter details.
        '''
        #~ if self.scene._has_alert:
            #~ self.scene._has_alert = False
        
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
         
        def button(self):
            pass
         
        def input_box(self):
            pass
        
        def number(self):
            # What if number is a list() instead of text field?
            pass
    
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
        # Calculate x offset
        w = self.scene.frame.w - 160 - 160
        xoff = self.dest_surface.get_rect().centerx - w/2 
        # Draw a box background.
        pygame.draw.rect(surface, (255,60,71),
            pygame.Rect(xoff, self.body['top'], w,
            self.body['height']), 10) 
        # There is a slight offset from the text
        # and the box. The box needs to contain the text.
        # So the text is going to be slightly smaller.
        # How about 8 pixels???? nescasary?
        rect = pygame.Rect((xoff+8,self.body['top']+8,
                w-8,300-8)) # left,top,width,height
        font = (pygame.font.Font
            ('data/coders_crux/coders_crux.ttf',
            self.body['font_size']))
        drawText(surface, self.body['text'], (0,0,0), rect,
                 font, aa=False, bkg=None)
