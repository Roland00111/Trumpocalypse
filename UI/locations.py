import random
import store as STORE
import config as cf

class Location:
    '''Provide the player with a location. Each location has 1-4
    Store instance. Each location has a region name (passed in).
    Each location has 10-20 associated Job instances.
    Each location has an active_store_idx which specifies which
    store the player is current visiting (None if no store).
    '''
    def __init__(self,location_name):
        '''
        :param str location_name: A location name.
        '''
        self.location_name = location_name
        self.connected_regions = []
        self.stores = [
            STORE.Store() for i in range(random.randint(1,4))
        ]
        self.active_store_idx = None # Index of store being visited.
   
    def random_job(self):
        ''' Assigns a random job '''
        r = random.randint(0, 10)
        self.jobs = [ cf.gs.game.jobs.random_job()
                      for i in range(0, 10+r) ]
        
        r = random.randint(0, len(self.jobs)-1)
        return self.jobs[ r ]

    def menu_values(self):
        '''Takes no parameter but goes through the list of all???
        store names and gives each store a random distance from the
        users house and adds the string to an array called temp_array
        '''
        temp_array = []
        for store in self.stores:
            temp_array.append(store.name + ': ' +
                        str(store.distance_from_house()) + ' miles')
        return temp_array
    
class Locations:
    '''
    Handler for locations in the game. Each game has one instance
    of the Locations class. The Locations class instance has a list of
    Location class instances for each of the eight locations.
    The Locations class also has a friend_location attribute which
    specifies the X,Y coordinates of the friend's location.
    The friend_location attribute changes daily so that when 
    "staying with a friend" each day the player is starting from
    a new location (see StoryScreen).
    The list of regions is from:
    https://en.wikipedia.org/wiki/List_of_regions_of_the_United_States
    '''
    all_locations = [ #prototype
        'Middle Atlantic',
        'New England',
        'South Atlantic',
        'East South Central',
        'East North Central',
        'West North Central',
        'West South Central',
        'Mountain',
        'Pacific'
    ]
    def __init__(self):
        self.locations=[Location(name) for name in self.all_locations]
        self.friend_location = { 'coordinates': [ 0, 0 ] }
        pass
    
    def update_friend_location(self):
        '''This function sets the 0th and 1st element of
        self.friend_location to a random float, -20.0 to 20.0.
        '''
        self.friend_location['coordinates'][0] = (random.
                                    uniform(0.0, 20.0) * cf.plus_minus())
        self.friend_location['coordinates'][1] = (random.
                                    uniform(0.0, 20.0) * cf.plus_minus())
        
    def random_location(self):
        '''
        :return: A random location instance.
        :rtype: location.
        '''
        return self.locations[random.randint(0,len(self.locations)-1)]
