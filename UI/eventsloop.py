import config as cf
import pygame
import menu as MENU
from pygame.locals import *
import PygameUI
import sys # Used for sys.exit()

class EventsLoop:
    """This loop is running continuously to check for events.
    
    Any time a key on the keyboard is pressed or a mouse button is
    pressed it is filtered through this function.
      
    Drawing the next menu also takes place here, by creating a new
    Menu() class for the specified keypress index when a menu item is
    selected. When the game is first started an initial Menu instance is
    started using OpeningMenu(). OpeningMenu is just one of the many
    classes that inherit from the Menu class.
    
    To reduce CPU usage from 100% the loop utilizes a 
    call to pygame.time.wait(0). This is noted at this URL:
        https://www.gamedev.net/topic/
        518494-pygame-eating-up-my-cpu/#entry4368408
    The author states: "Giving up any remainder of the timeslice
    is the key to lowering CPU usage, which is done by sleeping - or,
    in the case of PyGame, calling time.wait()."
    """
    
    current_menu = None
    test_events = None
    Score = 0
    def __init__(self,test_events = None):
        '''The init function takes an optional test_events which if
        not None will run a set of events.
        
        :param list test_events:
			A list of keypress indexes to auto-"press".
        '''
        pygame.display.set_caption('Trumpocalypse!')
        # Start on opening menu. Then changes.
        self.cm = MENU.OpeningMenu() # Current menu reference
        self.test_events = test_events
        event_loop = True
        recurse_test = 0
        cf.gs.first_game_event=False
        while event_loop:
            self.process_pygame_events()
            # CPU wait.
            #http://git.net/ml/python.pygame/2003-07/msg00042.html
            #pygame.time.wait(0) makes the game wait until an action
            #is performed and since game is not animated having it
            #wait until an action is perfec so the wait(0) puts the
            #CPU to 0% usage when an action is not performed. Which
            #is most of the time
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
            self.cm = MENU.GameOverScreen()
    
    def set_first_game_event(self, event):
        '''
        This takes the first event as a param, and does starting
        duties such as making sure the music starts, but not twice.
        '''
        if cf.gs.first_game_event==False:
            print("setting first game event")
            cf.gs.first_game_event=event
            cf.start_music('spoopy.wav')
    
    def pui_has_alert(self, event):
        '''
        This takes a single event as the parameter and checks that
        there is no alerts that need to interupt game play and if
        there is no alerts then it returns false. If there is an
        alert than it returns true and shows the alert for the user.
        If there is an alert then stop everything except mouse down,
        mouse up, and quit.
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
            # Draw the scene.
            # This is important if changing between menus
            # with the Enter key and upon arriving an alert
            # pops up.
            # Without drawing the new menu before showing the alert,
            # the user is left on the previous menu viewing the alert.
            self.draw_scene()
            # Make sure to draw alert
            cf.surface.blit(self.cm.scene.draw_alert(), (0, 0))
            # and update, in the case of
            # self.cm.process_before_unload()=False and
            # chosen_position=True
            pygame.display.update()
            return True
        # If the code is down here then there is no alert.
        # Allow the event to be processed.
        return False
    
    def draw_scene(self):
        """Draw the scene: PygameUI, titlesArray, and main images."""
        #~ temp = pygame.Surface
        # Draw PygameUI.
        #~ temp.blit(self.cm.scene.draw(), (0, 0))
        cf.surface.blit(self.cm.scene.draw(), (0, 0))
        # Draw Menu
        if self.cm.body is False:
            self.cm.init(self.cm.titlesArray, cf.surface) 
            self.cm.draw()
        else:
            # Draw menu plus body
            self.cm.init(self.cm.titlesArray, cf.surface, 175) 
            self.cm.draw()
            self.cm.draw_menu_body()
        # Draw scene alert on top of menu and other elements.
        if self.cm.scene._has_alert is True:
            cf.surface.blit(self.cm.scene.draw_alert(), (0, 0))
        # Update
        if hasattr(self.cm,'om') == True:
            image = pygame.image.load('trump.png')
            cf.surface.blit(image, [-25, 235])
            image2 = pygame.image.load('trump2.png')
            cf.surface.blit(image2, [510, 235])
        pygame.display.update()
        # TODO:
        # Testing of screen stretch on resize.
        #~ pygame.transform.scale(cf.surface, cf.window_size)
        #~ s = pygame.display.set_mode(
                #~ cf.window_size, RESIZABLE)
        #~ cf.surface.set_mode(
                #~ cf.window_size, RESIZABLE)
        #~ s.blit(
        #~ cf.surface.set_mode(
                #~ cf.window_size, RESIZABLE)
        #~ s.blit(
        #~ cf.surface.blit(
            #~ pygame.transform.scale(cf.surface, cf.window_size),
            #~ (0,0))
        #~ pygame.display.flip()
        #~ pygame.display.update()
    
    def process_key_and_mouse(self, event):
        """Process mouse events and key events.
        
        If the Enter key is pressed then return the chosen
        menu position. Otherwise, return None.
        """
        #-----------------------------------
        # Key press events and mouse events.
        #-----------------------------------
        if event.type == KEYDOWN:
            print 'unicode key:',event.unicode
            print 'num key:',event.key
            # Toggle full screen
            # Apparently only works when running X11
            # Does HWSURFACE|DOUBLEBUF|RESIZABLE help with this?
            # This is per this suggestion:
            # https://groups.google.com/d/msg/
            #   pygame-mirror-on-google-groups/47n8sJMCEh0/
            #   laRN5-QPgFUJ
            # F11 key is 292.
            if event.key == 292:
                pygame.display.toggle_fullscreen()
            if event.key == K_UP:
                self.cm.draw(-1)
            elif event.key == K_DOWN:
                self.cm.draw(1)
            elif event.key == K_RETURN:
                return self.cm.get_position()
            elif event.key == K_ESCAPE:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                cf.down_in = self.cm.scene.hit(event.pos)
                if (cf.down_in is not None and
                    not isinstance(cf.down_in, PygameUI.Scene)):
                    cf.down_in.mouse_down(event.button,
                        cf.down_in.from_window_point(event.pos))
        elif event.type == pygame.MOUSEBUTTONUP:
            # http://stackoverflow.com/questions/10990137/
            # pygame-mouse-clicking-detection
            if event.button == 1:                 
                # PygameUI
                up_in = self.cm.scene.hit(event.pos)
                if cf.down_in == up_in:
                    cf.down_in.mouse_up(event.button,
                        cf.down_in.from_window_point(event.pos))
                cf.down_in = None
        elif event.type == pygame.MOUSEMOTION:
            if cf.down_in is not None and cf.down_in.draggable:
                if cf.down_in.parent is not None:
                    (cf.down_in.parent.
                    child_dragged(cf.down_in, event.rel))
                cf.down_in.dragged(event.rel)
        elif event.type == pygame.KEYDOWN:
            self.cm.scene.key_down(
                event.key, event.unicode)
            #https://pythonhosted.org/kitchen/unicode-frustrations.html
            #unicode type stores an abstract sequence of code points
            #https://pythonhosted.org/kitchen/glossary.html#term-code-points
            #code points make it so that we have a number pointing to a character without... 
            #worrying about implementation details of how those numbers are stored for the computer to read
            # .unicode allows you to encode the characters however you like ie. encode('latin1'))
            #by using unicode of KEYDOWN if can be used/converted for every encoding, making it universal of sorts
        elif event.type == pygame.KEYUP:
            self.cm.scene.key_up(event.key)
        elif event.type == pygame.VIDEORESIZE:
            cf.window_size = event.dict['size']
            #~ cf.surface = pygame.display.set_mode(
                #~ event.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
        return None
        
    def process_pygame_events(self):
        ''' This function contains our main while loop that is
        constantly checking for keyboard and mouse button presses.
        '''
        if cf.arcade_game != False:
            cf.arcade_game.run(pygame.event.get())
            return
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
                pygame.quit()
                sys.exit()
            # Check alert status
            if self.pui_has_alert(event):
                continue
            # Process key and mouse events
            chosen_position = self.process_key_and_mouse(event)
            #if chosen_key is not None:
            #    break
            #---------------------------
            # Drawing stuff starts here.
            #---------------------------
            self.draw_scene()
                
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
        
        # Clock tick
        # TESTING
        # TODO: This does not affect high CPU usage when doing pygame.init()
        # for the audio. Tick(20) or Tick(60), no difference.
        #pygame.time.Clock().tick(20)

    def test():
        '''Run tests.'''
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
