import pygame
from pygame.locals import *

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

    def show_alert(self, message, btn1_text, btn2_text, btn_action):
        if self._has_alert is True: # Do not do two alerts at once (for now)
            return
        alert = Alert(message, btn1_text, btn2_text, btn_action)
        alert.frame = pygame.Rect(0, 0, self.frame.w, max(120, self.frame.h // 3))
        self._has_alert = True   # :)
        self._alert = alert      # :)
        self.add_child(alert)
        
    def draw_alert(self):
        '''Separate draw function for drawing alerts.
        '''
        return self._alert.draw()

class Label(Control):
    text_color = (90, 95, 90)
    padding = (8, 8)
    selected_bgcolor = (200, 224, 200)
    bgcolor = Control.bgcolor

    def __init__(self, text=None, label_bgcolor = (0,0,0)):
        Control.__init__(self)
        self.selected_bgcolor = label_bgcolor
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
            self.bgcolor = self.selected_bgcolor
        else:
            self.bgcolor = Label.bgcolor

class List(Control):
    
    def __init__(self, labels, selected_bgcolor, callback_function = False):
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
        for text in labels:
            lbl = Label(text,selected_bgcolor)
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
        '''
        If there is a callback function, then pass back the selected
        index and child text.
        '''
        if self.down_at is None:
            return
        for i, child in enumerate(self.container.children):
            if child.frame.collidepoint(mouse_pos):
                if self._selected_index == i:
                    return # No change in index.
                self.selected_index = i
                self.selected_value = child.text
                if self.callback_function:
                    self.callback_function(self.selected_index, child.text)
                return
        self.selected_index = None
    
    @property
    def selected_index(self):
        return self._selected_index
    
    @selected_index.setter
    def selected_index(self, index):
        child = self.container.children[index] # child=Label object
        if self._selected_index is not None:
            prev = self.container.children[self._selected_index]
            prev.selected = False
        child.selected = True
        self._selected_index = index
        self.on_selection(self, index)

class TextField(Control):
    prompt = '_'
    padding = (5, 2)

    def __init__(self):
        Control.__init__(self)
        self.label = Label('',(255,120,71))
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

    def __init__(self, message, btn1_text, btn2_text=None, callback_function=None):
        '''Create an alert box.
        
        If no value is passed to btn2_text then only one button is
        created.
        
        :param str message: The message on the alert.
        :param str btn1_text: The message on the first button.
        :param btn2_text: The message on the second button.
        :param callback_function: The function called for button clicks (with return arguments: True or False).
        :type btn2_text: str or None
        :type callback_function: def or None
        '''
        Control.__init__(self)

        self.bgcolor = Alert.bgcolor

        self.message = Label(message)
        large_font = pygame.font.SysFont('data/coders_crux/coders_crux.ttf', 16*2)
        self.message.font = large_font
        self.message.size_to_fit()
        self.message.bgcolor = self.bgcolor
        self.add_child(self.message)
        self.btn1_text = btn1_text
        self.btn2_text = btn2_text
        self.callback_function = callback_function

        if btn2_text == None:   # One button.
            self.btn = Button(btn1_text)
            self.btn.size_to_fit()
            self.btn.on_clicked.add(lambda btn: self.press(True)) # Send back True, even though there is no difference!
            self.add_child(self.btn)
        else:                   # Two buttons.
            self.btn = Button(btn1_text)
            self.btn.size_to_fit()
            self.btn.on_clicked.add(lambda btn: self.press(True))
            self.add_child(self.btn)
            
            self.btn2 = Button(btn2_text)
            self.btn2.size_to_fit()
            self.btn2.on_clicked.add(lambda btn: self.press(False))
            self.add_child(self.btn2)

    def layout(self):
        if self.btn2_text == None:  # One button.
            self.btn.frame.centerx = self.frame.w // 2
            self.btn.frame.bottom = self.frame.h - 10
        else:                       # Two buttons. Offset them 2+2=4px.
            self.btn.frame.left = self.frame.w // 2 - self.btn.frame.w - 2
            self.btn.frame.bottom = self.frame.h - 10
            self.btn2.frame.left = self.frame.w // 2 + 2
            self.btn2.frame.bottom = self.frame.h - 10
        self.message.frame.centerx = self.frame.w // 2
        self.message.frame.centery = (self.btn.frame.top // 2)

    def dismiss(self):
        self.scene._has_alert = False
        self.scene.remove_child(self)
        
    def press(self, yes_or_no):
        if self.callback_function != None:
            self.callback_function(yes_or_no) # Call action
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

    def __init__(self, text):
        Control.__init__(self)
        self.border_width = Button.border_width
        self.border_color = Button.border_color
        self.label = Label(text)
        bold_font = pygame.font.SysFont('data/coders_crux/coders_crux.ttf', 20)
        self.label.font = bold_font
        self.label.bgcolor = Button.bgcolor
        self.bgcolor = Button.bgcolor
        self.active_bgcolor = Button.active_bgcolor
        self.add_child(self.label)
        self.on_clicked = Signal()
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
        self.on_clicked(self)
