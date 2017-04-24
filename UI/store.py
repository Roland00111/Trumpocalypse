import names as NAMES # People's names.
import random
import inventory as INVENTORY
import config as cf

class Store:
    '''
    Each store is located in a urban, suburban, or rural location.
    Then based on this, each store has a distance to park, to urban
    house, to suburban house, and to rural house.
    If urban,       distance=rand_float(0,2.0),
                    sub=dist+rand_float(0,4.0),
                    rur=dist+rand_float(0,8.0)
    If suburban,    distance=rand_float(0,4.0),
                    urb=dist+rand_float(0,4.0),
                    rur=dist+rand_float(0,8.0)
    If rural,       distance=rand_float(0,8.0),
                    urb=dist+rand_float(0,4.0),
                    sub=dist+rand_float(0,4.0)
    '''
    grocery_types = [   'Bodega',   'Mini-Market',  'Supermarket',
                        'Market',   'Delicatessen', 'Fishmonger',
                        'Butcher',  'Convenience Store',
                        'Mom-and-Pop',              'Corner Store']
    store_locations = [
        'urban', 'suburban', 'rural'
    ]
    
    def __init__(self):
        ''' Give store a shabbiness-gaudiness value:
        0 is low shabbiness, 0.99 is highly shabby.
        '''
        self.store_location = self.store_locations[ random.randint
                                                    (0, 2) ]
        self.coordinates = {} # 0=x, 1=y
        self.distances() # Set distances
        self.inventory = INVENTORY.Inventory()
        # Set so that inventory is unbundled.
        self.inventory.is_store = True 
        self.shabby = random.randint(0, 99) / 100.0
        for i in range(40):
            self.inventory.add_item()
        self.inventory.shabbitize(self.shabby)
        self.grocery_type = self.grocery_types[ random.randint(0,
                                        len(self.grocery_types)-1) ]
        self.name = NAMES.NAMES_LIST[ random.randint(0,
            len(NAMES.NAMES_LIST)-1) ] + "'s " + self.grocery_type
    
    def distances(self):
        '''Set store location based on location type.
        Note: Random choice provides random between + and - number:
        https://docs.python.org/2/library/random.html#random.choice
        '''
        if self.store_location == 'urban':
            self.coordinates['x'] = (random.uniform(0.0,2.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                     cf.plus_minus())
        elif self.store_location == 'suburban':
            self.coordinates['x'] = (random.uniform(2.0,8.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(2.0,8.0) *
                                     cf.plus_minus())
        else: # Assume rural
            self.coordinates['x'] = (random.uniform(8.0,20.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(8.0,20.0) *
                                     cf.plus_minus())
    
    def distance_from_house(self):
        '''Calculate the euclidean distance to the current house.
        Character's current housing is (string):
            cf.gs.game.character.selected_house
        :return: Distance in miles, rounded to the tenth.
        :rtype: int.
        '''
        # Friend's house
        if cf.gs.game.character.selected_house_idx == 0: 
            c1 = (cf.gs.game.locations.
                  friend_location['coordinates'])
        else:
            # Housing is always -1
            idx = cf.gs.game.character.selected_house_idx - 1 
            x = (cf.gs.game.character.inventory.
                 sorted_items['housing'][ idx ].coordinates)
            c1 = [x['x'], x['y']]
        c2 = self.coordinates
        return round(cf.euclidean(c1, [c2['x'], c2['y']]), 1)
