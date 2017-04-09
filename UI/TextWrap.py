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
        while font.size(text[:i])[0] < rect.width and i < len(text) and text[i] != "\n":
                            #~ print 'text[:i]:','"'+text[:i]+'"'
                            #~ print 'text[:i][0]:','"'+text[:i][0]+'"'
                            #~ print 'font.size(text[:i])[0]:',font.size(text[:i])[0]
                            #~ print 'rect.width:',rect.width
                            #~ print 'i:',i
                            #~ print 'len(text):',len(text)
                            #~ print 'text[i]:','"'+str(text[i])+'"'
            i += 1
        temp = text[:i].strip() #replace("\n","")
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
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
