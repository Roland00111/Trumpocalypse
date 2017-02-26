

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
down_in = None # A global variable for pygameui (menu custom fields)

###
# Class Signal, Control, Scene, Label, List from:
# https://github.com/fictorial/pygameui (sampler branch)
###
class Signal(object):
    def __init__(self):
        self.slots = []

    def add(self, slot):
        self.slots.append(slot)

    def __call__(self, *args, **kwargs):
        for slot in self.slots:
            slot(*args, **kwargs)
class Control(object):
    bgcolor = (255,120,71) #(255, 255, 255)
    border_color = (200, 200, 200)

    def __init__(self):
        self._frame = pygame.Rect(0, 0, 0, 0)
        self.bgcolor = Control.bgcolor
        self.border_color = Control.border_color
        self.border_width = 0
        self.padding = (0, 0)
        self.parent = None
        self.children = []
        self.interactive = True
        self.enabled = True
        self.hidden = False
        self.draggable = False
        self._selected = False
        self.on_mouse_down = Signal()
        self.on_mouse_up = Signal()
        self.on_drag = Signal()
        self.on_selected = Signal()
        self.on_focused = Signal()
        self.on_blurred = Signal()

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, new_frame):
        self._frame = new_frame
        self.layout()

    def layout(self):
        for child in self.children:
            child.layout()

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def remove_child(self, to_remove):
        for i, child in enumerate(self.children):
            if child == to_remove:
                del self.children[i]
                break

    def hit(self, pos):
        if not self._frame.collidepoint(pos):
            return None
        pos = (pos[0] - self.frame.left, pos[1] - self.frame.top)
        for child in reversed(self.children):
            if child.interactive and child.enabled:
                control = child.hit(pos)
                if control is not None:
                    return control
        return self

    def update(self, dt):
        for child in self.children:
            child.update(dt)

    def draw(self):
        surf = pygame.surface.Surface(self._frame.size)
        surf.fill(self.bgcolor)
        print 'children:',self.children
        for child in self.children:
            if child.hidden:
                continue
            child_surf = child.draw()
            surf.blit(child_surf, child._frame.topleft)
            if (child.border_width is not None and child.border_width > 0):
                pygame.draw.rect(surf, child.border_color, child._frame,
                                 child.border_width)
        return surf

    def became_focused(self):
        self._border_width_before_focus = self.border_width
        self.border_width = 2
        self.on_focused()

    def became_blurred(self):
        self.border_width = self._border_width_before_focus
        self.on_blurred()

    def became_selected(self, yesno):
        self.on_selected(self, yesno)

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, yesno):
        self._selected = yesno
        self.became_selected(yesno)

    def mouse_down(self, btn, pt):
        self.on_mouse_down(self, btn, pt)

    def mouse_up(self, btn, pt):
        self.on_mouse_up(self, btn, pt)

    def dragged(self, rel):
        self.on_drag(self, rel)

    def child_dragged(self, child, rel):
        pass

    def to_parent_point(self, point):
        return (point[0] + self.frame.topleft[0],
                point[1] + self.frame.topleft[1])

    def from_parent_point(self, point):
        return (point[0] - self.frame.topleft[0],
                point[1] - self.frame.topleft[1])

    def from_window_point(self, point):
        curr = self
        ancestors = [curr]
        while curr.parent:
            ancestors.append(curr.parent)
            curr = curr.parent
        for a in reversed(ancestors):
            point = a.from_parent_point(point)
        return point

    def to_window_point(self, point):
        curr = self
        while curr:
            point = curr.to_parent_point(point)
            curr = curr.parent
        return point

    def key_down(self, key, code):
        pass

    def key_up(self, key):
        pass

    @property
    def scene(self):
        curr = self
        while curr.parent is not None and not isinstance(curr.parent, Scene):
            curr = curr.parent
        return curr.parent
class Scene(Control):
    def __init__(self):
        Control.__init__(self)
        self._frame = pygame.Rect((0, 0), (854,480))
        self._focus = None

    def key_down(self, key, code):
        if self._focus is not None:
            self._focus.key_down(key, code)

    def key_up(self, key):
        if self._focus is not None:
            self._focus.key_up(key)

    @property
    def focus(self):
        return self._focus

    @focus.setter
    def focus(self, new_focus):
        if self._focus != new_focus:
            if self._focus is not None:
                self._focus.became_blurred()
            self._focus = new_focus
            self._focus.became_focused()

    def show_alert(self, message):
        alert = Alert(message)
        alert.frame = rect(0, 0, self.frame.w, max(120, self.frame.h // 3))
        self.add_child(alert)
class Label(Control):
    text_color = (90, 95, 90)
    padding = (8, 8)
    selected_bgcolor = (200, 224, 200)
    bgcolor = Control.bgcolor

    def __init__(self, text=None):
        Control.__init__(self)
        self.interactive = False
        self.font = pygame.font.SysFont('data/coders_crux/coders_crux.ttf', 16)
        self.text = text
        self.text_color = Label.text_color
        self.padding = Label.padding

    def size_of(self, text):
        return self.draw().get_size()

    def size_to_fit(self):
        self.frame.size = self.size_of(self.text)

    def draw(self):
        text_surf = self.font.render(self.text, True,
                                     self.text_color, self.bgcolor)
        size = text_surf.get_size()
        padded_size = (size[0] + self.padding[0] * 2,
                       size[1] + self.padding[1] * 2)
        surf = pygame.surface.Surface(padded_size)
        surf.fill(self.bgcolor)
        surf.blit(text_surf, self.padding)
        return surf

    def became_selected(self, yesno):
        Control.became_selected(self, yesno)
        if yesno:
            self.bgcolor = Label.selected_bgcolor
        else:
            self.bgcolor = Label.bgcolor
class List(Control):
    
    def __init__(self, labels):
        Control.__init__(self)
        self.border_width = 1
        self.labels = labels
        self._selected_index = None
        self.on_selection = Signal()
        self.container = Control()
        self.container.draggable = True
        self.container.on_mouse_down.add(self.container_down)
        self.container.on_mouse_up.add(self.container_up)
        y, w = 0, 0
        for text in labels:
            lbl = Label(text)
            lbl.frame.topleft = (0, y)
            size = lbl.size_of(text)
            y += size[1]
            w = max(w, size[0])
            lbl.size_to_fit()
            self.container.add_child(lbl)
        for child in self.container.children:
            child.frame.w = w
        self.container.frame.size = (w, y)
        self.add_child(self.container)
    
    def child_dragged(self, child, rel):
        self.container.frame.top += rel[1]
        self.container.frame.top = min(0, max(-self.container.frame.h,
                                              self.container.frame.top))
        self.container.frame.bottom = max(self.frame.h,
                                          self.container.frame.bottom)
        self.down_at = None  # any drag kills a click for selecting
    
    def container_down(self, control, mouse_button, mouse_pos):
        self.down_at = mouse_pos
    
    def container_up(self, control, mouse_button, mouse_pos):
        if self.down_at is None:
            return
        for i, child in enumerate(self.container.children):
            if child.frame.collidepoint(mouse_pos):
                self.selected_index = i
                return
        self.selected_index = None
    
    @property
    def selected_index(self):
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, index):
        child = self.container.children[index]
        child.selected = True
        if self._selected_index is not None:
            prev = self.container.children[self._selected_index]
            prev.selected = False
        self._selected_index = index
        self.on_selection(self, index)

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
    custom_fields = [] # To be filled in by menu classes that need buttons, selects, inputs, and number inputs
    
    
    
     
    
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
            field_type = string: 'select', 'button', 'input', 'number' (also input but limited to #s)
            field_content = array of strings: for select; string: button text, input default value, number default value
            field_label = string, a label to put beside the field
            field_event_hooks = array, an array of dict events, each dict event has a `type` and `callback_function`
            '''
            self.field_type         = field_type
            self.field_content      = field_content
            self.field_label        = field_label
            self.field_event_hooks  = field_event_hooks
            # Append this CustomField class instance to the parent class custom_fields array.
            Menu.custom_fields.append(self)
        def draw(self, offset):
            '''
            Draw this item onto the page.
            This happens when the keypressFunction is called.
            Return value: Return the height of this field. This way the next field may know where to draw itself.
            '''
            ###
            return 0
            pass
            
    def keypressFunction(self, text = False, size=22,top=40,boxHeight=300):
        scene = Scene()
        scene.lst = List(['Item %s' % str(i) for i in range(20)])
        scene.lst.frame = pygame.Rect(scene.frame.w // 2, 10, 150, 170)
        scene.lst.frame.w = scene.lst.container.frame.w
        scene.lst.selected_index = 1
        scene.add_child(scene.lst)
        #~ surface.fill((255,120,71))
        #~ field_offset = 0
        #~ for field in self.custom_fields:
            #~ # Draw the custom fields here.
            #~ # Pass the current height offset into the function.
            #~ field_offset = field_offset + field.draw(field_offset)
            #~ pass
        #~ pygame.display.update()
        #~ print self # Prints "<__main__.OpeningMenu instance at 0x7f5bb2a99d40>" or "<__main__.CreateCharacter instance at 0x7f5bb2a99ef0>"
        while 1:
            for event in pygame.event.get():
                ########
                # This would be where the iteration for CustomField events takes place
                # pseudo-code:
                # For field in self.custom_fields:
                #     For event_hook in field.field_event_hooks
                #         If event.type == event_hook['type']:
                #             event_hook['callback_function'](event)
                ########
                for field in self.custom_fields:
                    for event_hook, callback_function in field.field_event_hooks.iteritems():
                        if event.type == event_hook:
                            # Parentheses here execute the function. The event is passed as an argument to the function.
                            callback_function(event)
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
                    down_in = scene.hit(event.pos)
                    if down_in is not None and not isinstance(down_in, Scene):
                        down_in.mouse_down(event.button, down_in.from_window_point(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP:
                    up_in = scene.hit(event.pos)
                    if down_in == up_in:
                        down_in.mouse_up(event.button, down_in.from_window_point(event.pos))
                    down_in = None
                elif event.type == pygame.MOUSEMOTION:
                    if down_in is not None and down_in.draggable:
                        if down_in.parent is not None:
                            down_in.parent.child_dragged(down_in, event.rel)
                        down_in.dragged(event.rel)
                elif event.type == pygame.KEYDOWN:
                    scene.key_down(event.key, event.unicode)
                elif event.type == pygame.KEYUP:
                    scene.key_up(event.key)
                
                surface.blit(scene.draw(), (0, 0))
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
            Close,
            Close,
        ]
        self.titlesArray = [
            'Continue To Location',
            'Back To Previous Page'
        ]
        #~ self.CustomField( # Something along the lines of.........
            #~ 'select',
            #~ ['Choice 1', 'Choice 2', 'Choice 3'],
            #~ 'Make a "good" choice:',
            #~ { MOUSEBUTTONUP: self.select_on_mouseup }
        #~ )
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
