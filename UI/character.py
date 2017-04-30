import inventory as INVENTORY
import random
import config as cf
import names
class Character:
    '''
    This class contains a default character and two hard coded
    characters for testing purposes. 
    '''
    def __init__ (self, create_type):
        ''' Default character '''
        self.name = 'Default'
        self.health = 3
        self.strength = 3
        self.gender = 'male'
        self.age = 40
        self.charisma = 3
        self.intelligence = 3
        self.sanity = 30
        self.inventory = INVENTORY.Inventory() # Give character an inventory.
        self.reset_modes() # Set transit and housing type.
        self.location = None # Will be set later.
        self.is_dead = False# Set to True when health=0 to end game
        self.game_over = False  # Set by EventsLoop
        if create_type == 'random':
            self.randomGenerate()
            pass

    def earn_money ( self, num_hours ):
        '''Earn money.
        Round amount to the nearest tenth.
        
        :param num_hours: The number of hours worked.
        :type num_hours: int or float.
        :return: Amount of money earned.
        :rtype: float.
        '''
        amount = round(self.job.income * (num_hours / 8), 1)
        self.inventory.add_item('Cash', amount)
        return amount

#updates health, the if statement should at some point add warning popup 
#or kill functionality of some sort to all screens. 
    def modifyHealth(self, number):
        self.health += number
#        if (self.health <= 0):

    def reset_modes(self):
        '''Reset transit and housing type to original values.
        '''
        # Transit index, default=0 (walking).
        self.transit_mode_idx = 0
        # Transit title, default='Walking'
        self.transit_mode = 'Walking'
        # House index, default=0
        self.selected_house_idx = 0
        # House title, default='Staying with Friends'
        self.selected_house = 'Staying with Friends'    
        
    def randomGenerate(self):
        ''' Eventually this will completly randomize what you get but
        for now this contains two characters that are chosen at
        randomly for the purpose of testing. This function also adds
        the characters starting items randomly.
        '''
        num = random.randint(0,1)
        if num == 0:
            r=random.randint(0,4994)
            self.name = names.NAMES_LIST[r]
            self.health = 3
            self.strength = 5
            self.gender = 'male'
            #Oldest verified human is ~122 years old female,116 Male
            self.age = random.randint(16,116)
            self.charisma = 3
            self.intelligence = 1
            #self.income = 10000
            self.sanity = 30
            # Add some random items.
            #To add item insert string of item (item_type) see Item
            #class, else it's random.
            self.inventory.add_item() 
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item('Food','random')
            self.inventory.add_item('Cash','random')
            # Location
            self.location = (cf.gs.game.locations.
                             random_location())
            self.job = self.location.random_job()
            
        elif num == 1:
            r=random.randint(0,4994)
            self.name = names.NAMES_LIST[r]
            self.health = 3
            self.strength = 1
            #why is gender important? as of now we dont have any
            #events that effect you because of your gender
            self.gender = 'female'
            #Oldest verified human is ~122.5 years old female,
            self.age = random.randint(16,122)
            self.charisma = 4
            self.intelligence = 5
            
            #self.income = 20000
            self.sanity = 30
            # Add some random items.
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item()
            self.inventory.add_item('Food','random')
            self.inventory.add_item('Cash','random')
            # Location
            self.location=cf.gs.game.locations.random_location()
            self.job = self.location.random_job()
    
    def born(self):
        print (self.name, ' is alive!')
    def died(self):
        print (self.name, ' is dead!')
