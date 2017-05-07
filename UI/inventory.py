import random
import items as ITEMS # Items dictionary.
import config as cf
import math

class Inventory:
    '''
    This class deals with everything related to the inventory of
    the character.
    '''
    def __init__(self):
        '''
        Holds starting data and will get modified to hold the
        contents of the inventory.
        '''
        self.max_items = 999
        self.items = [] # Array of items.
        self.sorted_items = { # Sorted items
            'housing':[],
            'transit':[],
            'other':[],
            'cash':None, # Will be cash item.
            'food':None, # Will be food item.
        }
        self.is_store = False
    def house_degrade(self,ratio):
        '''
        Decraments house uses by aratio for cases where an event
        might cause you to loose 50% of your house for example.
        '''
        for house in self.sorted_items['housing']:
            house.remaining_uses *= ratio
            
    def item_count(self):
        '''
        Iterates throught self.items and returns a list of all
        items in array with number of uses left.
        '''
        storage = []
        for item in self.items:
            storage.append({'item':item, 'value': item.item_type +
                            ': ' + item.show_amount()})
        return storage
    
    def item_count_buy(self):
        '''
        Return a list of items available to buy and their buy price.
        Do not allow buying of cash.
        '''
        storage = []
        for item in self.items:
            if item.item_type == 'Cash':
                continue
            storage.append({'item':item, 'value': item.item_type +
                            ': ' + item.show_amount() + ' $' +
                            str(item.calculate_purchase_cost())})
        return storage
    
    def item_count_sell(self):
        '''
        Return a lits of items available to sell and their
        sell price.
        Do not allow selling of cash.
        '''
        storage = []
        for item in self.items:
            if item.item_type == 'Cash':
                continue
            storage.append({'item':item, 'value': item.item_type +
                            ': ' + item.show_amount() + ' $' +
                            str(item.calculate_resale_cost())})
        return storage
    
    def list_housing_types(self):
        '''
        Iterates through self.items and returns a list of all items
        that are considered housing types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in ITEMS.n['housing_types']:
                storage.append({'item':item, 'value': item.item_type +
                                ': ' + item.show_amount()})
        return storage
    
    def list_transit_types(self):
        '''
        Iterates through self.items and returns a list of all items
        that are considered transit types.
        '''
        storage = []
        for item in self.items:
            if item.item_type in ITEMS.n['transit_types']:
                storage.append({'item':item, 'value': item.item_type +
                                ': ' + item.show_amount()})
        return storage
    
    def num_items(self):
        ''' Returns the number of items in the inventory'''
        return len(self.items)
    
    def use_item(self, item, amount):
        '''
        Try to use an item in the inventory.
        Returns True if the item was used, False otherwise.
        :param item: An Item instance.
        :type item: Item.
        :param amount: The amount to use.
        :type amount: float or int.
        '''
        item = self.contains_item(item.item_type)
        if item is False: # Inventory does not contain item.
            return False
        if item.grouped_item is False:  # single item
            item.remaining_uses -= amount
            if item.remaining_uses <= 0:
                self.remove_item(item)
            return True
        else:                           # grouped item
            item.amount -= amount
            if item.amount <= 0:
                self.remove_item(item)
            return True
        
    def use_housing(self, amount):
        '''Use a specified amount of housing.'''
        c = cf.gs.game.character
        idx = c.selected_house_idx - 1
        item = self.sorted_items['housing'][idx]
        item.remaining_uses -= amount
        if item.remaining_uses <= 0:
            self.remove_item(item)
            # Reset housing and transit.
            c.reset_modes()
                
    def use_transit(self, distance):
        '''
        This is called whenever you travel some whwere like to
        work or to the store. The function then decrements the uses
        on the proper form of transportation.
        '''
        c = cf.gs.game.character
        mode = c.transit_mode
        if mode != 'Walking':
            idx = c.transit_mode_idx - 1
            # Minus one as walking is not in this list...
            t_item = self.sorted_items['transit'][idx]
            print 'remaining uses:',t_item.remaining_uses
            print 'distance:',distance
            t_item.remaining_uses -= distance
            if t_item.remaining_uses <= 0:
                self.remove_item(t_item)
                # Reset transit type.
                # (This also resets housing type.)
                c.reset_modes()
        
    def remove_item(self, item):
        '''
        Remove an item from this inventory.
        Item is removed from self.items and self.sorted_items.
        '''
        self.items.remove(item)
        # Remove from sorted items.
        if item.item_type in ITEMS.n['transit_types']:
            self.sorted_items['transit'].remove(item)
        elif item.item_type in ITEMS.n['housing_types']:
            self.sorted_items['housing'].remove(item)
        elif item.item_type == 'Cash':
            self.sorted_items['cash'].amount -= item.amount
        elif item.item_type == 'Food':
            self.sorted_items['food'].amount -= item.amount        
        else:
            self.sorted_items['other'].remove(item)
        
    def multiply_item(self, item_type = None, item_multiplier = None):
        '''
        Multiply an item by a multiplier.
        Typically this would be called multiply_item('Food', 0.5).
        Which, if the character has food, reduces Food by 50%.
        Round after mulitplying.
        
        :param str item_type: The type of item.
        :param float item_multiplier: The item amount multiplier.
        '''
        item = self.contains_item(item_type)
        if item:
            if item.grouped_item is False:  # single item
                item.remaining_uses *= item_multiplier
                item.remaining_uses = round(item.remaining_uses, 1)
            else:                           # grouped item
                item.amount *= item_multiplier
                item.amount = round(item.amount, 1)
                    
    def add_item(self, item_type = None, item_amount = None):
        '''
        Add an item to this inventory.
        If item_type is None then add a random item.
        If item_type is not None then add item of this type.
        Does the item already exist in the inventory?
        If so, then add the item's stats.
        '''
        #if new_item.grouped_item is False: # single item
        #        new_item.remaining_uses = item_amount 
        #    else:                               # grouped item
        #        new_item.amount = item_amount 
        if item_type != None:
            new_item = Item(item_type)
            if item_amount == 'random':
                if item_type == 'Cash':
                    a = random.randint(0,10000)
                    new_item.amount = a
                elif item_type == 'Food':
                    a = random.randint(0,100)
                    new_item.amount = a
            else:
                if new_item.grouped_item is False: # single item
                    new_item.remaining_uses = item_amount 
                else:                              # grouped item
                    new_item.amount = item_amount
            self.update_or_add_item(new_item)
        else:
            # A random item.
            n = random.randint(0, ITEMS.n['num_items']-1)
            rand_item = Item( ITEMS.n['all_choices'][n] )
            self.update_or_add_item(rand_item)
    
    def sorted_append(self, new_item):
        '''
        This function ensures that when an item is added to an
        inventory, the same item is also added to sorted_items.
        sorted_items is a dictionary which organizes the items
        in the inventory by type (transit, housing, cash, food, and
        other) for easy access.
        '''
        if new_item.item_type in ITEMS.n['transit_types']:
            self.sorted_items['transit'].append(new_item)
        elif new_item.item_type in ITEMS.n['housing_types']:
            self.sorted_items['housing'].append(new_item)
        elif new_item.item_type == 'Cash':
            self.sorted_items['cash'] = new_item
        elif new_item.item_type == 'Food':
            self.sorted_items['food'] = new_item
        else:
            self.sorted_items['other'].append(new_item)
            
    def update_or_add_item(self, new_item):
        ''' Updates or adds an item to the inventory.
        '''
        existing_item = self.contains_item(new_item.item_type)
        if existing_item != False:
            # Add to existing item.
            if existing_item.grouped_item is False:     # Single item.
                # Always add another single item.
                self.items.append( new_item )
                self.sorted_append( new_item )
            else:                        # Grouped item.
                # Store inventory (unbundle store inventory grouped
                # items).
                if self.is_store:   
                    self.items.append( new_item )
                    self.sorted_append( new_item )
                else:               # Character
                    existing_item.amount += new_item.amount
        else:
            self.items.append( new_item )
            self.sorted_append( new_item )
    
    def contains_item(self, item_type):
        '''
        Returns the item in the inventory if it exists.
        Otherwise returns False.
        This takes O(n) time as it searches entire list.
        '''
        for existing_item in self.items:
            if existing_item.item_type == item_type:
                return existing_item
        # Still here? Then the item is not in the inventory.
        return False
    
    def shabbitize(self, shabbiness):
        '''
        Make this inventory shabby.
        Always floor the shabbiness. So that 1 pie never become 0
        pies.
        So Food=110; Food-=ceil(110*.99)=[110-109]=1.
        :param shabbiness:
            The shabbiness ratio, expressed between 0 and 0.99.
        :type shabbiness: float.
        '''
        if shabbiness > 0:
            for item in self.items:
                # Make the shabbiness vary some,
                # between 20%-100% of current shabbiness.
                rand_shabby = random.randint(20, 100) / 100.0 
                if item.grouped_item is True:   # Grouped
                    item.amount -= math.floor(item.amount *
                                             shabbiness * rand_shabby)
                else:                           # Single
                    item.remaining_uses -= math.floor(item.
                    remaining_uses * shabbiness * rand_shabby)
        
class Item:
    '''
    For transit:
    Remaining Uses: The number of miles traveled before the item is
    deleted from character's inventory.
    '''
    def __init__(self, item_type = None):
        self.item_type = item_type
        self.purchase_cost = 0
        # A ratio of original cost, between zero to one.
        self.resale_cost = 0 
        self.amount = 0
        self.original_amount = 0
        self.remaining_uses = None
        self.max_remaining_uses = None  # To show how much is left.
        self.grouped_item = True        # Default is grouped.
        self.coordinates = {}           # For mapped items.
        self.set_item(item_type)
        
    def use_item(self, item_type):
        #TODO
        '''
        This will somehow use the item.
        Deincroment remaining_uses, along with in game effect.
        '''
        pass
    
    def sell_item(self):
        #TODO
        '''
        Sells the item based on either its remaining uses or amount
        remaining.
        '''
        pass
    
    def calculate_purchase_cost(self):
        '''
        Returns the purchase cost of the item or group of items.
        The cost is always rounded up.
        This is the same as self.calculate_resale_cost except
        the seller never pays the resale ratio.
        That is, the seller always sells as though the item were
        in new condition, minus whatever amount has been used.
        :return: The purchase cost of this item.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return math.ceil(self.purchase_cost * (self.amount /
                                                self.original_amount))
        else:                 # Single item (% remaining)
            return math.ceil(self.purchase_cost * (self.
                        remaining_uses / self.max_remaining_uses))
            
    def calculate_resale_cost(self):
        '''
        Returns the sell cost of the item or group of items.
        The cost is always rounded down. So if an item is only
        worth $0.80 then it is really worth $0.
        :return: The sell cost of this item.
        :rtype: str.
        '''

        #In the case of grouped items this is:
        #   floor: [ self.resale_cost * (self.amount /
        #    self.original_amount) ]
        #In the case of single items this is:
        #    floor: [ self.resale_cost * (self.remaining_uses /
        #    self.max_remaining_uses) ]
        
        if self.grouped_item: # Grouped item (num remaining)
            return math.floor(self.purchase_cost * self.resale_cost *
                              (self.amount / self.original_amount))
        else:                 # Single item (% remaining)
            return math.floor(self.purchase_cost * self.resale_cost *
                     (self.remaining_uses / self.max_remaining_uses))
    
    def show_amount(self):
        '''
        :return: The display value.
        :rtype: str.
        '''
        if self.grouped_item: # Grouped item (num remaining)
            return str(self.amount)
        else:                 # Single item (% remaining)
            return str(math.ceil(100*(1.0 * self.remaining_uses /
                                self.max_remaining_uses)))+'%'
        
    def set_item(self, item_type):
        '''
        Single use items have remaining_use that declines.
        Grouped use items have num_in_group that declines.
        :raises TypeError: If item_type is not in ITEMS.n['stats'].
        '''
        try:
            n = ITEMS.n['stats'][item_type]
            self.purchase_cost = n[0]
            self.resale_cost = n[1]
            self.amount = n[2]
            self.original_amount = n[2]
            self.remaining_uses = n[3]
            self.max_remaining_uses = n[3]
            if self.remaining_uses is None:
                self.grouped_item = True # Set self.grouped_item
            else:
                self.grouped_item = False
            # If transit item...
            # If housing item...
            if item_type in ITEMS.n['housing_types']:
                if item_type == 'Urban House':
                    self.coordinates['x'] = (random.uniform(0.0,2.0) *
                                             cf.plus_minus())
                    self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                             cf.plus_minus())
                elif item_type == 'Suburban House':
                    self.coordinates['x'] = (random.uniform(2.0,8.0) *
                                             cf.plus_minus())
                    self.coordinates['y'] = (random.uniform(2.0,8.0) *
                                             cf.plus_minus())
                elif item_type == 'Rural House':
                    self.coordinates['x'] = (random.uniform(8.0,20.0)*
                                             cf.plus_minus())
                    self.coordinates['y'] = (random.uniform(8.0,20.0)*
                                             cf.plus_minus())
        except:
            raise TypeError
