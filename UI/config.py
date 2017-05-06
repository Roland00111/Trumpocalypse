import random
import math
import pygame

gs = None # Previously: game_state
surface = None
# A global variable for pygameui (menu custom fields)
down_in = None 
# Global variable for music is on or off.
music_on = True

arcade_game = False

def plus_minus():
    '''
    Return a random +1 or -1.
    :rtype: int.
    '''
    return random.random()*2 - 1

def euclidean(p1, p2):
    '''
    Determine euclidean distance between two points.
    Pretty straightforward: http://stackoverflow.com/a/4169284/2178774.
    :param list p1: A list with first element=x, second=y.
    :param list p2: A list with first element=x, second=y.
    :return: Euclidean distance between points.
    :rtype: int.
    '''
    return math.sqrt((p2[0] - p1[0]) ** 2 +
                     (p2[1] - p1[1]) ** 2)

def start_music(musicName):
    pygame.init()
    pygame.mixer.music.load(musicName)
    pygame.mixer.music.play(-1)
