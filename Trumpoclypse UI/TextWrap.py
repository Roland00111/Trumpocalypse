import pygame
from pygame.locals import *

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2
 
    # get the height of the font
    fontHeight = font.size("Tg")[1]
 
    while text:
        i = 1
 
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
 
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
 
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text):
            j = text.rfind(" ", 0, i) + 1
            temp = text[:j]
            if "\n" in temp:
                i = temp.rfind("\n",0,j) + 1
            else:
                i = j
        # render the line and blit it to the surface
        temp = text[:i].replace("\n","")
        if bkg:
            image = font.render(temp, 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(temp, aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
 
        # remove the text we just blitted
        
        text = text[i:]
 
    return text
