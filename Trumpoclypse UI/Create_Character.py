'''
@author: avalanchy (at) google mail dot com
@version: 0.1; python 2.7; pygame 1.9.2pre; SDL 1.2.14; MS Windows XP SP3
@date: 2012-04-08
@license: This document is under GNU GPL v3

README on the bottom of document.

@font: from http://www.dafont.com/coders-crux.font
      more abuot license you can find in data/coders-crux/license.txt
'''
import pygame
import unittest

from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()


class Menu:
    lista = []
    by = []
    FontSize = 32
    font_path = 'data/coders_crux/coders_crux.ttf'
    font = pygame.font.Font
    dest_surface = pygame.Surface #how surface game is on is generated
    QuanityOfLista = 0 #initalizer
    #BackgroundColor = (51,51,51)
    BackgroundColor = (255,120,71)#color of background of menu itself (currently Trumps skin color :))
    BackgroundColorButton = (51,51,51)
    TextColor =  (255, 255, 153)
    SelectionColor = (153,102,255)
    PositionSelection = 0 #initalizer
    Position = (0,0) #set as initalizer
    menu_width = 0 
    menu_height = 0

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
    
    def init(self, lista, dest_surface):
        self.lista = lista
        self.dest_surface = dest_surface
        self.Quanity = len(self.lista)
        self.CreateStructure()
                
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

    def CreateStructure(self):
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
        x = self.dest_surface.get_rect().centerx - self.menu_width / 2 #Centering the menu to the middle of the screen 
        y = self.dest_surface.get_rect().centery - self.menu_height / 2
        mx, my = self.Position
        self.Position = (x+mx, y+my) 


if __name__ == "__main__":
    import sys
    #os.system("python yourfile.py")
    surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
    surface.fill((255,120,71)) #Color of the background of window
    
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
    menu = Menu()#necessary
    #menu.set_colors((255,255,255), (0,0,255), (0,0,0))#optional
    #menu.set_fontsize(48)#optional
    #menu.set_font('data/couree.fon')#optional
    #menu.move_menu(100, 99)#optional
    menu.init(['Manually Create Character.', 'Randomly Create Character.'], surface)#necessary
    #menu.move_menu(0, 25)#optional (the actual lettering ie. Start,Options...)
    menu.draw()#necessary
    
    pygame.key.set_repeat(199,69)#(delay,interval)
    pygame.display.update()
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    menu.draw(-1) #here is the Menu class function
                if event.key == K_DOWN:
                    menu.draw(1) #here is the Menu class function
                if event.key == K_RETURN:
                    if menu.get_position() == 0:#here is the Menu class function
                        print('Hello')
                        #Go to Menu where user can enter manual info about character
                    elif menu.get_position() == 1: #HERE is where you need to add the look to the next screen!!!!!!
                        print('Hello')
                        #Randomly Generate Character
                if event.key == K_ESCAPE:
                    pygame.display.toggle_fullscreen() # Toggle full screen #Apparently only works when running X11
                    #pygame.display.set_mode((800,600),pygame.FULLSCREEN) #Mess up the screen (at least with my laptop)
                pygame.display.update()
            elif event.type == QUIT:
                pygame.display.quit()
                sys.exit()
        #pygame.time.wait(8)
        