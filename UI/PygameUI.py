import pygame
from pygame.locals import *
""" This file contains the Classes Signal, Control, Scene, Label, List
TextField, Alert, and Button. These classes all work together to
display the user interface.
https://github.com/fictorial/pygameui (sampler branch)
"""
class Signal(object):
    def __init__(self):
        self.slots = []

    def add(self, slot):
        self.slots.append(slot)

    def __call__(self, *args, **kwargs):
        for slot in self.slots:
            slot(*args, **kwargs)

class Control(object):
    #~ bgcolor = (255,120,71)
    bgcolor = (255,215,194) #(255, 255, 255)
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
        for child in self.children:
            if child.hidden:
                continue
            child_surf = child.draw()
            surf.blit(child_surf, child._frame.topleft)
            if (child.border_width is not None and child.border_width > 0):
                pygame.draw.rect(
                    surf,
                    child.border_color,
                    child._frame,
                    child.border_width
                )
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
        self._has_alert = False
        self._alert = None

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

    def show_alert(self, message, buttons, btn_action, choice_list,
                   choice_list_callback):
        if self._has_alert is True: # Do not do two alerts at once (for now)
            print 'show_alert:has alert'
            return
        alert = Alert(message, buttons, btn_action, choice_list,
                      choice_list_callback)
        alert.frame = pygame.Rect(0, 0, self.frame.w, max(120,
                                            self.frame.h // 3))
        self._has_alert = True   
        self._alert = alert      
        self.add_child(alert)
        
    def draw_alert(self):
        """Separate draw function for drawing alerts."""
        return self._alert.draw()

class Label(Control):
    """ This class is used for all of the scrolable lists such as the
    and the character stats.
    """
    padding = (8, 2)
    selected_bgcolor = (255,120,71) #(200, 224, 200)
    bgcolor = Control.bgcolor

    def __init__(self, text=None, label_bgcolor=(255,120,71),
                 item=None,text_color=(0,0,0),font_size=16):
        """ Takes as parameters text as a string type, label_bgcolor
        in the form of a list using the RGB color standard, item ???,
        text_color in the form of a list using the RGB color standard,
        and font_size in the form of an integer.
        """
        Control.__init__(self)
        self.selected_bgcolor = label_bgcolor
        self.interactive = False
        self.font = pygame.font.SysFont('data/coders_crux/coders_crux.ttf'
                                        , font_size)
        self.text = text
        self.text_color = text_color
        self.padding = Label.padding
        self.item = item

    def size_of(self, text):
        """ Parameters text form of a string and this function returns
        just the size.
        """
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
            self.bgcolor = self.selected_bgcolor
        else:
            self.bgcolor = Label.bgcolor

class List(Control):
    
    def __init__(self, labels, selected_bgcolor=(255,120,71),
                 callback_function = False):
        '''Initialize List().
        :param list labels:
            A list of labels, each label is a dictionary {'item':*item
            reference or None*, 'str':*a string*}.
        :param tuple selected_bgcolor: Color when selected.
        :param def callback_function: Callback function when clicked.
        '''
        Control.__init__(self)
        self.border_width = 1
        self.labels = labels
        self._selected_index = None
        self.selected_value = None # Value of selected item
        self.on_selection = Signal()
        self.container = Control()
        self.container.draggable = True
        self.container.on_mouse_down.add(self.container_down)
        self.container.on_mouse_up.add(self.container_up)
        self.callback_function = callback_function
        y, w = 0, 0
        for label in labels:
            if 'color' not in label:
                label['color']=(0,0,0)
            if 'font_size' not in label:
                label['font_size']=16
            
            lbl = Label(label['value'], selected_bgcolor, label['item'],
                        label['color'],label['font_size'])
            lbl.frame.topleft = (0, y)
            size = lbl.size_of(label['value'])
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
        """
        If there is a callback function, then pass back the selected
        index and child text.
        :return: In the case of the callback function, returns self.
            selected_index, self.selected_value, self.selected_item.
        """
        if self.down_at is None:
            return
        for i, child in enumerate(self.container.children):
            if child.frame.collidepoint(mouse_pos):
                if self._selected_index == i:
                    return # No change in index.
                self.selected_index = i
                self.selected_value = child.text
                self.selected_item = child.item
                if self.callback_function:
                    self.callback_function(
                        self.selected_index,
                        self.selected_value,
                        self.selected_item,
                        child)
                return
        self.selected_index = None
    
    def remove_selected(self, child):
        """Remove a list element onclick."""
        self.container.remove_child(child)
        # Set select index to none.
        self._selected_index = None
        
    @property
    def selected_index(self):
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, index):
        if index == None:
            # In the case that the child has been removed,
            # the selected index will be "None".
            # In this case, do nothing when this None thing is
            # clicked.
            return
        child = self.container.children[index] # child=Label object
        if self._selected_index is not None:
            try:
                # In the case that the user purchases or sells
                # an item, it will be removed via remove_child().
                # In which case, an error is raised if selected index
                # it outside the range of container.children.
                # That is, guard against if last item in list
                # is removed.
                prev = self.container.children[self._selected_index]
                prev.selected = False
            except:
                pass
        child.selected = True
        self._selected_index = index
        self.on_selection(self, index)

class TextField(Control):
    prompt = '_'
    padding = (5, 2)

    def __init__(self):
        Control.__init__(self)
        self.label = Label('',(255,215,194))
        #~ self.label = Label('',(255,120,71))
        self.label.padding = TextField.padding
        self.add_child(self.label)
        self.text = ''
        self.label.text = TextField.prompt
        self.max_len = None
        self.secure = False
        self.border_width = 1
        self.on_return = Signal()
        self.on_text_change = Signal()

    def layout(self):
        Control.layout(self)
        self.label.frame.size = self.frame.size

    def key_down(self, key, code):
        if key == pygame.K_BACKSPACE:
            self.text = self.text[0:-1]
        elif key == pygame.K_RETURN:
            self.on_return(self, self.text)
        else:
            try:
                self.text = '%s%s' % (self.text, str(code))
            except:
                pass
            self.on_text_change(self, self.text)

        if self.max_len is not None:
            self.text = self.text[0:self.max_len]

        if self.secure:
            self.label.text = '*' * len(self.text)

        self.label.text = self.text + TextField.prompt
        self.label.size_to_fit()

        if self.label.frame.right > self.frame.w - self.padding[0] * 2:
            self.label.frame.right = self.frame.w - self.padding[0] * 2
        else:
            self.label.frame.left = self.padding[0]

    def mouse_up(self, button, pt):
        self.scene.focus = self

class Alert(Control):
    bgcolor = (240, 240, 200)

    def __init__(self, message, buttons, callback_function=None,
                 choice_list=None, choice_list_callback=None):
        '''Create an alert box.
        Creates either one or two buttons plus buttons callback.
        Creates an additional list plus list callback.
        :param str message: The message on the alert.
        :param str buttons: List of strings for buttons.
        :param callback_function: The callback function for button
            clicks (with return arguments: True or False).
        :type callback_function: def.
        :param list choice_list: List of dictionaries for a PygameUI.
            List().
        :param choice_list_callback: The callback function for list
            clicks, in the format (selected_index, selected_value,
            selected_item).
        :type choice_list_callback: def.
        '''
        Control.__init__(self)
        self.bgcolor = Alert.bgcolor
        
        # Consider \n
        m = message.split('\n')
        self.messages = []
        for text in m:
            l = Label(text)
            large_font = (pygame.font.
                    SysFont('data/coders_crux/coders_crux.ttf', 16*2))
            l.font = large_font
            l.size_to_fit()
            l.bgcolor = self.bgcolor
            self.add_child(l)
            self.messages.append(l)
        
        self.callback_function = callback_function
        self.buttons = buttons

        if len(self.buttons) == 1:   # One button.
            self.btn = Button(buttons[0])
            self.btn.size_to_fit()
            # Send back True, even though there is no difference!
            self.btn.on_clicked.add(lambda btn: self.press(True)) 
            self.add_child(self.btn)
        else:                   # Two buttons.
            self.btn = Button(buttons[0])
            self.btn.size_to_fit()
            self.btn.on_clicked.add(lambda btn: self.press(True))
            self.add_child(self.btn)
            
            self.btn2 = Button(buttons[1])
            self.btn2.size_to_fit()
            self.btn2.on_clicked.add(lambda btn: self.press(False))
            self.add_child(self.btn2)
        
        self.clist = False
        if choice_list != None:
            if choice_list_callback is None: # This must be defined.
                raise ValueError
            self.clist_callback = choice_list_callback
            self.clist = List(choice_list, (200, 224, 200))
            self.clist.border_width = 1
            self.clist.container.draggable = True
            self.clist.callback_function = self.press_list
            self.add_child(self.clist)

    def layout(self):
        if len(self.buttons) == 1:  # One button.
            self.btn.frame.centerx = self.frame.w // 2
            self.btn.frame.bottom = self.frame.h - 10
        else:                       # Two buttons. Offset them 2+2=4px.
            self.btn.frame.left = self.frame.w // 2 - self.btn.frame.w - 2
            self.btn.frame.bottom = self.frame.h - 10
            self.btn2.frame.left = self.frame.w // 2 + 2
            self.btn2.frame.bottom = self.frame.h - 10
        
        if len(self.messages) == 1:     # Zero \n.
            self.messages[0].frame.centerx = self.frame.w // 2
            self.messages[0].frame.centery = (self.btn.frame.top // 2)
        elif len(self.messages) == 2:   # One \n.
            self.messages[0].frame.centerx = self.frame.w // 2
            self.messages[0].frame.centery = ((self.btn.frame.
                                top // 2) - self.messages[0].frame.h)
            self.messages[1].frame.centerx = self.frame.w // 2
            self.messages[1].frame.centery = (self.btn.frame.top // 2)
        else:                           # Assume no more than two \n.
            self.messages[0].frame.centerx = self.frame.w // 2
            self.messages[0].frame.centery = ((self.btn.frame.
            top // 2) - self.messages[0].frame.h - self.messages[1].
                                                              frame.h)
            self.messages[1].frame.centerx = self.frame.w // 2
            self.messages[1].frame.centery = ((self.btn.frame.
                                top // 2) - self.messages[0].frame.h)
            self.messages[2].frame.centerx = self.frame.w // 2
            self.messages[2].frame.centery = (self.btn.frame.top // 2)
        
        if self.clist != False:
            self.clist.frame = pygame.Rect(self.frame.w // 2, self.
                                           btn.frame.top, 150, 100)
            self.clist.frame.w = self.clist.container.frame.w
            # Actually center it.
            self.clist.frame.centerx = self.frame.w // 2 
            # Move buttons down.
            if len(self.buttons) == 1:
                self.btn.frame.bottom += 110
            else:
                self.btn.frame.bottom  += 110
                self.btn2.frame.bottom += 110
            # Make frame taller.
            self.frame.h += 110

    def dismiss(self):
        #~ self.scene._has_alert = False # Moved into press function.
        self.scene.remove_child(self)
        
    def press(self, yes_or_no):
        self.scene._has_alert = False # Reset alert state.
        if self.callback_function != None:
            self.callback_function(yes_or_no) # Call action
        self.dismiss()
    
    def press_list(self, selected_index, selected_value,
                   selected_item):
        self.clist_callback(selected_index, selected_value,
                            selected_item)
        self.dismiss()
    
    def draw(self):
        surf = Control.draw(self)
        pygame.draw.line(surf, (200, 200, 160),
                         (0, self.frame.bottom - 1),
                         (self.frame.w, self.frame.bottom - 1), 2)
        return surf

class Button(Control):
    bgcolor = (220, 220, 220)
    active_bgcolor = (200, 200, 200)
    border_width = 1
    border_color = (100, 100, 100)
    disabled_text_color = (128, 128, 128)

    def __init__(self, text, callback = False):
        Control.__init__(self)
        self.border_width = Button.border_width
        self.border_color = Button.border_color
        self.label = Label(text)
        bold_font = (pygame.font.
                    SysFont('data/coders_crux/coders_crux.ttf', 20))
        self.label.font = bold_font
        self.label.bgcolor = Button.bgcolor
        self.bgcolor = Button.bgcolor
        self.active_bgcolor = Button.active_bgcolor
        self.add_child(self.label)
        if callback is False:
            self.on_clicked = Signal()
        else:
            self.on_clicked = callback
        self.is_pressed = False

    def enable(self, yesno):
        self.enabled = yesno
        if self.enabled:
            self.label.text_color = Label.text_color
        else:
            self.label.text_color = Button.disabled_text_color

    def layout(self):
        Control.layout(self)
        self.label.frame.size = self.frame.size

    def size_to_fit(self):
        self.label.size_to_fit()
        self.frame.size = self.label.frame.size

    def mouse_down(self, btn, pt):
        Control.mouse_down(self, btn, pt)
        if self.enabled:
            self.label.bgcolor = self.active_bgcolor
            self.is_pressed = True

    def mouse_up(self, button, pt):
        Control.mouse_up(self, button, pt)
        self.label.bgcolor = self.bgcolor
        self.is_pressed = False
        if self.on_clicked is not False: 
            self.on_clicked(self)
