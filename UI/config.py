import random

gs = None # Previously: game_state
surface = None

def plus_minus():
    '''Return a random +1 or -1.
    
    :rtype: int.
    '''
    return random.random()*2 - 1
