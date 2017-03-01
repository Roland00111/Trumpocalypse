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


class TextField(Control):
    prompt = '_'
    padding = (5, 2)

    def __init__(self):
        Control.__init__(self)
        self.label = Label('')
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
