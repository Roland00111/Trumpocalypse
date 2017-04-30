import pygame
from pygame.locals import *

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    """
    Takes the parameters of surface, which is where the text is going
    to be displayed,cf.surface for example and the text, which is
    whatever text we want to be displayed, the color, which is
    well, the color (0,0,0) input format, and the font is the location
    of the font you would like to use alternatively. This function
    then calculates the maximum we can fit in the size of our textbox
    and draws it to our surface with whichever parameters we give.
    """
    rect = Rect(rect)
    y = rect.top
    lineSpacing = 0
    # get the height of the font
    fontHeight = font.size('Tg')[1]
    # Split by newline.
    sp_text = text.split('\n')
    # Loop through text.
    for text in sp_text:
        # Old code to print to screen.
        while text:
            i = 1
            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break
            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            temp = text[:i].strip()
            # if we've wrapped the text, then adjust the wrap to the
            # last word
            if i < len(text):
                i = text.rfind(' ', 0, i) + 1
            # render the line and blit it to the surface
            if bkg:
                image = font.render(temp[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(temp[:i], aa, color)
            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            # Remove leading and trailing newline and spaces.
            text = text[i:].strip()
