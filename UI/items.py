# items.py
""" A dictionary holding all of our items for the game. The key is
the item name in a string form and the value is a list containing the
attributes for the item.
"""

n = {
    'num_items': None, # Dynamically generated amount of item choices.
    'all_choices': [], # Dynamically generated list[ strings ] of item names.
    'stats': {
         # Cost, Resale, Amount, Remaining Use (None=Grouped)
        'Food':             [10,0.8,10, None], # 10 food cost $10; while life=9 food per day.
        'Pie':              [1,0,1, None],
        'Garden':           [200,0.5,10, None],
        'Lottery Ticket':   [10,0.4,1, None],
        'New Car':          [20000,0.5,1,1000],
        'Old Car':          [10000,0.4,1,600],
        'Speed Boat':       [20000,0.4,1,400],
        'Helicopter':       [500000,0.5,1,2500],
        'Bicycle':          [100,0.8,1,400],
        'Racing Bicycle':   [400,0.8,1,300],
        'Transit Pass':     [100,0.6,1,400],
        'Urban House':      [400000,0.7,1,100],
        'Suburban House':   [200000,0.5,1,90],
        'Rural House':      [100000,0.8,1,80],
        'Cash':             [0,0,1,None], #?
        'First Aid Kit':    [10,0.6,2,None],
        'Seeds':            [2,0.5,20,None],
        'Clothing':         [200,0.4,20,None], # 20 shirts for $10 per shirt = $200.
    },
    'transit_attributes':{  # Speed, Karma, Influence, Butterfly, Health Bonus
                            # KIB based on CO2 emissions, saving the planet,
                            # etc.
        'New Car':          [30,-1,0,0,0],
        'Old Car':          [25,0,-1,-1,0],
        'Speed Boat':       [30,-1,1,-1,0],
        'Bicycle':          [15,1,1,1,0.2],
        'Racing Bicycle':   [20,1,1,1,0.2],
        'Transit Pass':     [30,1,1,1,0.1],
        'Walking':          [5,1,1,1,0.2],
        'Helicopter':       [50,-1,2,-2,0],  
    },
    'transit_types': [ # List of transit modes
        'New Car',
        'Old Car',
        'Speed Boat',
        'Helicopter',
        'Bicycle',
        'Racing Bicycle',
        'Transit Pass',
    ],
    'housing_types': [ # List of housing modes
        'Staying with Friends',
        'Urban House',
        'Suburban House',
        'Rural House',
    ],
}

# Populate all_choices.
n['all_choices'] = [ k for k,v in n['stats'].iteritems() ]
n['num_items'] = len(n['all_choices'])
