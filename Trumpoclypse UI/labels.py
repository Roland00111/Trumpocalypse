'''
Source: https://github.com/iminurnamez/pyroller/blob/master/data/components/labels.py
License: Pyroller is marked CC0.
'''
import os
import string
from itertools import cycle

import pygame as pg
#from .. 
#import prepare, tools



LOADED_FONTS = {}

BUTTON_DEFAULTS = {"call"               : None,
                   "args"               : None,
                   "call_on_up"         : True,
                   "font"               : None,
                   "font_size"          : 36,
                   "text"               : None,
                   "hover_text"         : None,
                   "disable_text"       : None,
                   "text_color"         : pg.Color("white"),
                   "hover_text_color"   : None,
                   "disable_text_color" : None,
                   "fill_color"         : None,
                   "hover_fill_color"   : None,
                   "disable_fill_color" : None,
                   "idle_image"         : None,
                   "hover_image"        : None,
                   "disable_image"      : None,
                   "hover_sound"        : None,
                   "click_sound"        : None,
                   "visible"            : True,
                   "active"             : True,
                   "bindings"           : ()}


#Helper function for MultiLineLabel class
def wrap_text(text, char_limit, separator=" "):
    """Splits a string into a list of strings no longer than char_limit."""
    words = text.split(separator)
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if len(word) + current_length <= char_limit:
            current_length += len(word) + len(separator)
            current_line.append(word)
        else:
            lines.append(separator.join(current_line))
            current_line = [word]
            current_length = len(word) + len(separator)
    if current_line:
        lines.append(separator.join(current_line))
    return lines


def _parse_color(color):
    if color is not None:
        try:
            return pg.Color(color)
        except ValueError:
            return pg.Color(*color)
    return color


class Label(object):
    """
    Parent class all labels inherit from. Color arguments can use color names
    or an RGB tuple. rect_attr should be a dict with keys of pygame.Rect
    attribute names (strings) and the relevant position(s) as values.
    Creates a surface with text blitted to it (self.image) and an associated
    rectangle (self.rect). Label will have a transparent bg if
    bg is not passed to __init__.
    """
    def __init__(self, path, size, text, color, rect_attr, bg=None):
        self.path, self.size = path, size
        #~ if (path, size) not in LOADED_FONTS:
            #~ LOADED_FONTS[(path, size)] = pg.font.Font(path, size)
        print path
        print size
        self.font = pg.font.Font(path, size)
        self.bg = _parse_color(bg)
        self.color = _parse_color(color)
        self.rect_attr = rect_attr
        self.set_text(text)

    def set_text(self, text):
        """Set the text to display."""
        self.text = text
        self.update_text()

    def update_text(self):
        """Update the surface using the current properties and text."""
        if self.bg:
            render_args = (self.text, True, self.color, self.bg)
        else:
            render_args = (self.text, True, self.color)
        self.image = self.font.render(*render_args)
        self.rect = self.image.get_rect(**self.rect_attr)

    def draw(self, surface):
        """Blit self.image to target surface."""
        surface.blit(self.image, self.rect)


# Should probably be depracated with Labels turned into sprites so that
# They can use standard sprite groups.
class GroupLabel(Label):
    """Creates a Label object which is then appended to group."""
    def __init__(self, group, path, size, text, color, rect_attr, bg=None):
        super(GroupLabel,self).__init__(path, size, text, color, rect_attr, bg)
        group.append(self)


class MultiLineLabel(object):
    """Creates a single surface with multiple labels blitted to it."""
    def __init__(self, path, size, text, color, rect_attr,
                 bg=None, char_limit=42, align="left", vert_space=0):
        attr = {"center": (0, 0)}
        lines = wrap_text(text, char_limit)
        labels = [Label(path, size, line, color, attr, bg) for line in lines]
        width = max([label.rect.width for label in labels])
        spacer = vert_space*(len(lines)-1)
        height = sum([label.rect.height for label in labels])+spacer
        self.image = pg.Surface((width, height)).convert()
        self.image.set_colorkey(pg.Color("black"))
        self.image.fill(pg.Color("black"))
        self.rect = self.image.get_rect(**rect_attr)
        aligns = {"left"  : {"left": 0},
                  "center": {"centerx": self.rect.width//2},
                  "right" : {"right": self.rect.width}}
        y = 0
        for label in labels:
            label.rect = label.image.get_rect(**aligns[align])
            label.rect.top = y
            label.draw(self.image)
            y += label.rect.height+vert_space

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Blinker(Label):
    """
    A blinking label. frequency is the number of milliseconds between blinks.
    """
    def __init__(self, path, size, text, color, rect_attr, frequency, bg=None):
        super(Blinker, self).__init__(path, size, text, color, rect_attr, bg)
        self.frequency = frequency
        self.elapsed = 0.0
        self.on = False
        self.blinking = True

    def update(self, dt):
        self.elapsed += dt
        while self.elapsed >= self.frequency:
            self.elapsed -= self.frequency
            if self.blinking:
                self.on = not self.on

    def draw(self, surface):
        if self.on:
            surface.blit(self.image, self.rect)


class MarqueeFrame(pg.sprite.Sprite):
    """A MarqueeFrame draws a ring of blinking lights around a label."""
    def __init__(self, rect_attr, image, bulb_radius, frequency, *groups):
        super(MarqueeFrame, self).__init__(*groups)
        self.frequency = frequency
        diam = bulb_radius*2
        image_rect = image.get_rect()
        width = ((image_rect.width//diam) + 3) * diam
        height = ((image_rect.height//diam) + 3) * diam
        self.rect = pg.Rect((0, 0), (width, height))
        self.bulbs = self.prepare_bulbs(bulb_radius)
        self.images = cycle(self.make_images(image))
        self.image = next(self.images)
        self.rect = self.image.get_rect(**rect_attr)
        self.elapsed = 0.0

    def make_images(self, center_image):
        images = []
        for frame in range(4):
            image = pg.Surface(self.rect.size).convert_alpha()
            image.fill((0,0,0,0))
            for i,bulb in enumerate(self.bulbs):
                if (frame+i)%2:
                    image.blit(prepare.GFX["bulb"], bulb)
            if frame >= 2:
                pos = center_image.get_rect(center=self.rect.center)
                image.blit(center_image, pos)
            images.append(image)
        return images

    def prepare_bulbs(self, bulb_radius):
        diam = bulb_radius*2
        bulbs = []
        bottom_bulbs = []
        left_bulbs = []
        for i in range(-diam, self.rect.width + diam, diam):
            x = self.rect.left + i
            y = self.rect.top
            y2 = self.rect.bottom-diam
            bulbs.append((x, y))
            bottom_bulbs.append((x, y2))
        for j in range(0, self.rect.height + diam, diam):
            x1 = self.rect.left
            x2 = self.rect.right-diam
            y = self.rect.top + j
            left_bulbs.append((x1, y))
            bulbs.append((x2, y))
        bulbs.extend(bottom_bulbs[1:-1][::-1])
        bulbs.extend(left_bulbs[::-1])
        return bulbs

    def update(self, dt):
        self.elapsed += dt
        while self.elapsed > self.frequency:
            self.elapsed -= self.frequency
            self.image = next(self.images)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class ButtonGroup(pg.sprite.Group):
    def get_event(self, event, *args, **kwargs):
        check = (s for s in self.sprites() if s.active and s.visible)
        for s in check:
            s.get_event(event, *args, **kwargs)


class Button(pg.sprite.Sprite):#, tools._KwargMixin):
    #~ _invisible = pg.Surface((1,1)).convert_alpha()
    #~ _invisible.fill((0,0,0,0))

    def __init__(self, rect_style, *groups, **kwargs):
        super(Button, self).__init__(*groups)
        self.process_kwargs("Button", BUTTON_DEFAULTS, kwargs)
        self.rect = pg.Rect(rect_style)
        rendered = self.render_text()
        self.idle_image = self.make_image(self.fill_color, self.idle_image,
                                          rendered["text"])
        self.hover_image = self.make_image(self.hover_fill_color,
                                           self.hover_image, rendered["hover"])
        self.disable_image = self.make_image(self.disable_fill_color,
                                             self.disable_image,
                                             rendered["disable"])
        self.image = self.idle_image
        self.clicked = False
        self.hover = False

    def render_text(self):
        font, size = self.font, self.font_size
        if (font, size) not in LOADED_FONTS:
            LOADED_FONTS[font, size] = pg.font.Font(font, size)
        self.font = LOADED_FONTS[font, size]
        text = self.text and self.font.render(self.text, 1, self.text_color)
        hover = self.hover_text and self.font.render(self.hover_text, 1,
                                                     self.hover_text_color)
        disable = self.disable_text and self.font.render(self.disable_text, 1,
                                                       self.disable_text_color)
        return {"text" : text, "hover" : hover, "disable": disable}

    def make_image(self, fill, image, text):
        if not any((fill, image, text)):
            return None
        final_image = pg.Surface(self.rect.size).convert_alpha()
        final_image.fill((0,0,0,0))
        rect = final_image.get_rect()
        fill and final_image.fill(fill, rect)
        image and final_image.blit(image, rect)
        text and final_image.blit(text, text.get_rect(center=rect.center))
        return final_image

    def get_event(self, event):
        if self.active and self.visible:
            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.on_up_event(event)
            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.on_down_event(event)
            elif event.type == pg.KEYDOWN and event.key in self.bindings:
                self.on_down_event(event, True)
            elif event.type == pg.KEYUP and event.key in self.bindings:
                self.on_up_event(event, True)

    def on_up_event(self, event, onkey=False):
        if self.clicked and self.call_on_up:
            self.click_sound and self.click_sound.play()
            self.call and self.call(self.args or self.text)
        self.clicked = False

    def on_down_event(self, event, onkey=False):
        if self.hover or onkey:
            self.clicked = True
            if not self.call_on_up:
                self.click_sound and self.click_sound.play()
                self.call and self.call(self.args or self.text)

    def update(self, prescaled_mouse_pos):
        hover = self.rect.collidepoint(prescaled_mouse_pos)
        pressed = pg.key.get_pressed()
        if any(pressed[key] for key in self.bindings):
            hover = True
        if not self.visible:
            self.image = Button._invisible
        elif self.active:
            self.image = (hover and self.hover_image) or self.idle_image
            if not self.hover and hover:
                self.hover_sound and self.hover_sound.play()
            self.hover = hover
        else:
            self.image = self.disable_image or self.idle_image

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class NeonButton(Button):
    """Neon sign style button that glows on mouseover."""
    width = 318
    height = 101

    def __init__(self, pos, text, call=None, args=None, *groups, **kwargs):
        try:
            on = "neon_button_on_{}".format(text.lower())
            off = "neon_button_off_{}".format(text.lower())
            on_image = prepare.GFX[on]
            off_image = prepare.GFX[off]
        except KeyError:
            text = text.replace("_", " ")
            blank = prepare.GFX["neon_button_blank"].copy()
            on_label = Label(prepare.FONTS["Saniretro"], 48, text,
                             (238,219,30), {"center":(159,50)})
            off_label = Label(prepare.FONTS["Saniretro"], 48, text,
                              (156,128,19), {"center":(159,50)})
            on_image = blank.subsurface((318,0,318,101))
            off_image = blank.subsurface((0,0,318,101))
            on_label.draw(on_image)
            off_label.draw(off_image)
        rect = on_image.get_rect(topleft=pos)
        settings = {"hover_image" : on_image,
                    "idle_image"  : off_image,
                    "call"        : call,
                    "args"        : args}
        settings.update(kwargs)
        super(NeonButton, self).__init__(rect, *groups, **settings)


class GameButton(Button):
    #~ ss_size = (320, 240)
    #~ width = ss_size[0]+20
    #~ height = ss_size[1]+20
    #~ font = prepare.FONTS["Saniretro"]

    def __init__(self, pos, game, call, *groups, **kwargs):
        path = os.path.join(".", "data", "states", game)
        try:
            image = pg.image.load(os.path.join(path, "image.png")).convert()
        except pg.error:
            image = prepare.GFX["default_image"]
        idle, highlight = self.make_images(game, image)
        rect = idle.get_rect(topleft=pos)
        settings = {"hover_image" : highlight,
                    "idle_image"  : idle,
                    "call"        : call,
                    "args"        : game}
        settings.update(kwargs)
        super(GameButton, self).__init__(rect, *groups, **settings)

    def make_images(self, game, icon):
        icon = pg.transform.scale(icon, self.ss_size).convert_alpha()
        icon_rect = icon.get_rect()
        label_text = game.replace("_", " ")
        label = Label(self.font, 48, label_text, "gold3", {"center": (0, 0)})
        rect = pg.Rect(0, 0, self.width, self.height+label.rect.h)
        icon_rect.midtop = (rect.centerx, 10)
        label.rect.midtop = icon_rect.midbottom
        frame = label.image.get_rect()
        frame.w = icon_rect.w
        frame.midtop=icon_rect.midbottom
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        image.blit(icon, icon_rect)
        image.fill(pg.Color("gray10"), frame)
        highlight = image.copy()
        pg.draw.rect(image, pg.Color("gold3"), icon_rect, 4)
        pg.draw.rect(image, pg.Color("gold3"), frame, 4)
        highlight.blit(prepare.GFX["game_highlight"], (0,0))
        for surface in (image, highlight):
            label.draw(surface)
        return (image, highlight)


class MoneyIcon(object):
    def __init__(self, topleft, size=(156, 70)):
        self.font = prepare.FONTS["Saniretro"]
        self.font_scale =  size[0] / 156.
        dollar = prepare.GFX["dollar_bill_yall"]
        self.dollar_image = pg.transform.smoothscale(dollar, size).convert_alpha()
        self.rect = self.dollar_image.get_rect(topleft=topleft)
        
    def update(self, amount):
        text = "${0:,.0f}".format(amount)
        font_size = int((64 - ((len(text) - 4) * 4)) * self.font_scale)
        self.surf = pg.Surface(self.rect.size).convert()
        dollar_rect = pg.Rect((0,0), self.rect.size)
        money_label = Label(self.font, font_size, text, "gray10",
                                       {"center": dollar_rect.center})
        self.surf.blit(self.dollar_image, (0,0))
        money_label.draw(self.surf)
        self.surf.set_alpha(140)
    
    def draw(self, surface):
        surface.blit(self.dollar_image, self.rect)
        surface.blit(self.surf, self.rect)

        
class TextBox(object):
    def __init__(self,rect,**kwargs):
        self.rect = pg.Rect(rect)
        self.buffer = []
        self.final = None
        self.rendered = None
        self.render_rect = None
        self.render_area = None
        self.blink = True
        self.blink_timer = 0.0
        self.accepted = string.ascii_letters+string.digits+string.punctuation+" "
        self.process_kwargs(kwargs)

    def process_kwargs(self,kwargs):
        defaults = {"id" : None,
                    "command" : None,
                    "active" : True,
                    "color" : pg.Color("white"),
                    "font_color" : pg.Color("black"),
                    "outline_color" : pg.Color("black"),
                    "outline_width" : 2,
                    "active_color" : pg.Color("blue"),
                    "font" : pg.font.Font(None, self.rect.height+4),
                    "clear_on_enter" : False,
                    "inactive_on_enter" : True}
        for kwarg in kwargs:
            if kwarg in defaults:
                defaults[kwarg] = kwargs[kwarg]
            else:
                raise KeyError("InputBox accepts no keyword {}.".format(kwarg))
        self.__dict__.update(defaults)

    def get_event(self,event, mouse_pos):
        if event.type == pg.KEYDOWN and self.active:
            if event.key in (pg.K_RETURN,pg.K_KP_ENTER):
                self.execute()
            elif event.key == pg.K_BACKSPACE:
                if self.buffer:
                    self.buffer.pop()
            elif event.unicode in self.accepted:
                self.buffer.append(event.unicode)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(mouse_pos)

    def execute(self):
        if self.command:
            self.command(self.id,self.final)
        self.active = not self.inactive_on_enter
        if self.clear_on_enter:
            self.buffer = []

    def update(self):
        new = "".join(self.buffer)
        if new != self.final:
            self.final = new
            self.rendered = self.font.render(self.final, True, self.font_color)
            self.render_rect = self.rendered.get_rect(x=self.rect.x+2,
                                                      centery=self.rect.centery)
            if self.render_rect.width > self.rect.width-6:
                offset = self.render_rect.width-(self.rect.width-6)
                self.render_area = pg.Rect(offset,0,self.rect.width-6,
                                           self.render_rect.height)
            else:
                self.render_area = self.rendered.get_rect(topleft=(0,0))
        if pg.time.get_ticks()-self.blink_timer > 200:
            self.blink = not self.blink
            self.blink_timer = pg.time.get_ticks()

    def draw(self,surface):
        outline_color = self.active_color if self.active else self.outline_color
        outline = self.rect.inflate(self.outline_width*2,self.outline_width*2)
        surface.fill(outline_color,outline)
        surface.fill(self.color,self.rect)
        if self.rendered:
            surface.blit(self.rendered,self.render_rect,self.render_area)
        if self.blink and self.active:
            curse = self.render_area.copy()
            curse.topleft = self.render_rect.topleft
            surface.fill(self.font_color,(curse.right+1,curse.y,2,curse.h))
