import pygame
from pygame.locals import *

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2
 
    # get the height of the font
    fontHeight = font.size("Tg")[1]

    print(text)
    while text:
        #print(text)
        i = 1
 
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
 
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text) and text[i] != "\n":
            i += 1

        temp = text[:i].replace("\n","")
        #Becuase we are relpacing it with "" we are essentially repacling a
        #space with no space moving just that line off by one
        #but if I replace "" with " " it makes the beginning of a line
        #start with a space....

            
            #text = text[:i+1].replace("\n","")
        
        
 
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
 
        # remove the text we just blitted

        text = text[i:]
        
##        if text[i+1] == '\n':
##            text = text[i+1:]
##        else:
##            text = text[i:]
        print(text.replace("\n","|"))
