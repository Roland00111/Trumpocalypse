import random
import math
import pygame
import pygame.midi

gs = None # Previously: game_state
surface = None
# A global variable for pygameui (menu custom fields)
down_in = None 
# Global variable for music is on or off.
music_on = True

arcade_game = False

window_size = (854,480)

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

def stop_music():
	pygame.mixer.music.stop()
	pygame.mixer.quit()
	
def start_music(musicName):
    # High CPU usage when calling pygame.init().
    # So instead just initialize pygame.mixer module separately.
    # It is still high CPU but then the user may choose
    # to turn the music off and CPU goes back to 0.
    # Do not call this:
    #	pygame.init()
    # Various settings to test:
    # pygame.mixer.pre_init(44100, -16, 2, 4096) # 4096 is ++cpu
    # pygame.mixer.pre_init(22050, -16, 2, 2048) 
    # pygame.mixer.pre_init(22050, -16, 1, 2048) 
    # pygame.mixer.pre_init(44100, -16, 1, 2048) 
    # pygame.mixer.pre_init(88200, -8, 1, 2048) 
    # pygame.mixer.pre_init(44100, -8, 2, 2048) 
    # pygame.mixer.pre_init(44100, -8, 2, 1024) 
    # pygame.mixer.pre_init(44100, -16, 1, 512) 
    # pygame.mixer.pre_init(22050, -16, 1, 512) 
    
    # Pre_init produces so-so cpu usage (25-50%).
    pygame.mixer.pre_init(11025, -8, 2, 256)
    pygame.mixer.init()
    pygame.mixer.music.load(musicName)
    pygame.mixer.music.play(-1)
    
    # A second test file.
    #pygame.mixer.music.load('Trumpocalypse-mixed2.ogg')
    #pygame.mixer.music.play(-1)
    
    # Does not work ("Memory error"):
    # pygame.mixer.Sound('Trumpocalypse-mixed2.ogg').play(loops=-1)
    
