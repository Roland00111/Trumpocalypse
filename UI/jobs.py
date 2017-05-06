import config as cf
import random

# Area is one of 'urban', 'suburban', or 'rural'
j = {
	'CEO': {
		'title': 'CEO',
		'income': 20000,
		'company': 'United Chocolate Refiners, Inc.',
		'area': 'suburban',
		'events': {
			"Personal Emergency": 4.0,
			"Easy Day":8.0,
			"Got Call as Leaving":9.0,
			"Done Early":7.0,
		}
              },
        'Therapist': {
		'title': 'Therapist',
		'income': 15000,
		'company': "Psyche Saver", 
		'area': 'suburban',
		'events': {
			"Only had one very troubled patient": 4.0,
			"Dealt with a bunch of wack jobs":8.0,
			"Patient Emergency had to stay late":9.0,
			"Accidently laughed at patient, felt bad stopped sesh early":6.0,
		}
	},
        'Pro Cuddler': {
		'title': 'Pro Cuddler',
		'income': 10000,
		'company': "Karen's Cuddlers'", 
		'area': 'suburban',
		'events': {
			"Only one Cuddlee today": 4.0,
			"Full Cuddling Day":8.0,
			"Cuddle Overload! Today":9.0,
			"Had to leave Cuddle sesh early":6.0,
		}
	},
        'Acting Person': {
		'title': 'Acting Person',
		'income': 30000,
		'company': "Bollywood", 
		'area': 'urban',
		'events': {
			"No scene today": 4.0,
			"Normal Day":8.0,
			"OT shooting movie":9.0,
			"Easy Day":6.0,
		}
	},
        'Fire Bender': {
		'title': 'Fire Bender',
		'income': 12000,
		'company': "Ohhhhla-O-O-O Tribe", 
		'area': 'rural',
		'events': {
			"Moist... Very Moist Day": 4.0,
			"Just Another Bending Day":8.0,
			"Bending ALLLL them flames":9.0,
			"Accidently burned down a forest, got sad and stopped for day":6.0,
		}
	},
        'Water Bender': {
		'title': 'Water Bender',
		'income': 12000,
		'company': "Ohhhhla-A-A-A Tribe", 
		'area': 'rural',
		'events': {
			"Low water levels": 4.0,
			"Just Another Bending Day":8.0,
			"Bending ALLLL that water":9.0,
			"Accidently killed fish when bending, got sad and stopped for day":6.0,
		}
	},
        'Plant Breeder': {
		'title': 'Plant Breeder',
		'income': 8000,
		'company': "Flora's Floral Falacio", #Too much?? hahaha
		'area': 'rural',
		'events': {
			"Plant's not feeling it today": 4.0,
			"Normal Plant Breeding Day":8.0,
			"Plants got busy today":9.0,
			"Done early as job is pointless":6.0,
		}
	},
        'Nutritionist': {
		'title': 'Nutritionist',
		'income': 10000,
		'company': "Nelson's Health Nuts",
		'area': 'suburban',
		'events': {
			"Accidently ate GMO!!": 4.0,
			"Normal Organic Day":8.0,
			"Vegan meeting after work":9.0,
			"Done Early due to Pesticides":6.0,
		}
	},
        'Pro Athlete': {
		'title': 'Pro Athlete',
		'income': 30000,
		'company': "WNBA/NBA",
		'area': 'urban',
		'events': {
			"Easy Practice": 4.0,
			"Game Day":8.0,
			"OT!":9.0,
			"Injured in Game":6.0,
		}
	},
        'Escort': {
		'title': 'Escort',
		'income': 16000,
		'company': "Linda's Lovers",
		'area': 'urban',
		'events': {
			"Only one customer": 4.0,
			"Normal day":8.0,
			"Busy night ;)":9.0,
			"Kidnapped but made it home":6.0,
		}
	},
        'Logger': {
		'title': 'Logger',
		'income': 14000,
		'company': 'Lumberjacks LLC',
		'area': 'rural',
		'events': {
			"Out of trees": 4.0,
			"Normal day":8.0,
			"Someone got hurt, had to do extra":9.0,
			"Fast pace t":7.0,
		}
	},
        'Politican': {
            'title': 'Politican', 
            'income':16500,
            'company': "USA BABY", 
            'area': 'suburban',
            'events':{
                "Half-Day (Nothing new)":4.0,
                "Average Day":8.0,
                "Filibuster":9.0,
                "Left early, dispite bills needing to be passed":7.0,
                }
        },
        'Student': {
            'title': 'Student', 
            'income':3000,
            'company': "Generic College", 
            'area': 'urban',
            'events':{
                "Catch-up on school work":4.0,
                "Average Day":8.0,
                "Had to work overtime":9.0,
                "Got someone to cover end of shift":7.0,
                }
        },
        'Entrepreneur': {
            'title': 'Entrepreneur', 
            'income':17000,
            'company': "Hometown Rescue", 
            'area': 'urban',
            'events':{
                "Not Busy":4.0,
                "Average Day":8.0,
                "Too much to do":9.0,
                "Need small break from work":7.0,
                }
        },
        'Contractor': {
            'title': 'Contractor', #Roofer??
            'income':12000,
            'company': "Ray's Roofers", 
            'area': 'suburban',
            'events':{
                "Nailed Hand on Accident":4.0,
                "Average Day":8.0,
                "Productive Day":9.0,
                "Need break from heat":7.0,
                }
        },
        'Uber Driver': {
            'title': 'Uber Driver',
            'income':4000,
            'company': "Uber", 
            'area': 'urban',
            'events':{
                "Car broke down":4.0,
                "Average Day":8.0,
                "Long Trip":9.0,
                "Taking it easy":7.0,
                }
        },
        'Fishermen': {
            'title': 'Fishermen',
            'income':7000,
            'company': "Ocean Abusers", 
            'area': 'rural',
            'events':{
                "Capsized":4.0,
                "Average Catch":8.0,
                "Stuck on the seas":9.0,
                "Caught quota":7.0,
                }
        },
        'Programmer': {
            'title': 'Programmer',
            'income':15000,
            'company': "Freelance", #I have no idea for name
            'area': 'urban',
            'events':{
                "Honest about time actually worked":4.0,
                "Easy Day":8.0,
                "Have to meet deadline":9.0,
                "Done Early":7.0,
                }
        },
	'Plumber': {
            'title': 'Plumber',
            'income':10000,
            'company': "Bob's flushers",
            'area': 'rural',
            'events':{
                "Flesh Wound":4.0,
                "Easy Day":8.0,
                "Sewage Everywhere":9.0,
                "Done Early":7.0,
                }
        },
	'Farmer': {
            'title': 'Farmer',
            'income':5000, #plus food?
            'company': "Joe's Organics",
            'area': 'rural',
            'events': {
                "Easy Day":8.0,
                "Heat Stroke":4.0,
                "Summer Equinox":9.0,
                "Fatigued":7.0,
                }
        },
        'Janitor': {
            'title': 'Janitor',
            'income': 5000,
            'company': 'SUNY Plattsburgh',
            'area':'urban',
            'events': {
                "Easy Day":8.0,
                "Kid Shit on Floor":9.0,
                "Inhaled Too Much Cleaner":4.0,
                "Early Release":7.0,
                }
        },
        'Family Wealth': {
            'title':'Family Wealth',
            'income':20000,
            'company': "Mommy and Daddy",
            'area':"suburban",
            'events': {
                'Did nothing':8.0,
                'Parents Feeling Generous':9.0,
                'Parents want me to get a job':4.0,
                'Parents gave up on me getting a job':7.0,
                }
        },
        'Twitch Streamer': {
            'title':'Twitch Streamer',
            'income':8000,
            'company': "Twitch",
            'area':"urban",
            'events': {
                'Played all day':14.0,
                'Played 9-5':8.0,
                'You got banned from Twitch':2.0,
                'Carpal Tunnel':6.0,
                }
        },
            
}
    
class Jobs:
    '''Handler for jobs in the game. Each game has one instance
    of the Jobs class. The Jobs class currently has one function,
    which is to provide a random Job class instance when appropriate.
    The jobs list is stored in jobs.py.
    '''
    def __init__(self):
        pass
    def random_job(self):
        ''' This generates a random job for the user '''
	global j
        r = random.randint(0,len(j.keys())-1)
        x = j.values()[r]
        return Job(x['title'], x['income'], x['company'], x['area'],
                   x['events'])
		   
class Job:
    ''' Deals with anythinng that deals with the characters job'''
    def __init__(self,title=None,income=None,company=None,area=None,
                 work_events=None):
        ''' The parameters are title, income, company, area, and
        work_events and asigns them to the charecter.
        '''
        self.title = title
        self.income = income
        self.company = company
        self.area = area
        self.work_events = work_events
        self.coordinates = {}
        #self.distances_call = 
        self.distances()

    def work(self):
        ''' This is called when the character goes to work so it
        decrements time and increases there cash.
        '''
        self.random_dictPos = random.randint(0,
                                            len(self.work_events)-1)
        
        self.hours_worked = (self.work_events.values()
                              [self.random_dictPos])
        if self.hours_worked > cf.gs.game.current_day.day_hours:
            self.hours_worked = cf.gs.game.current_day.day_hours
        cf.gs.game.mod_hours(-self.hours_worked)
        print self.hours_worked
        self.money_made = (cf.gs.game.character.
                           earn_money( self.hours_worked))
        print self.money_made

        return (self.work_events.keys()[self.random_dictPos] + ' \n'
                + ' \nWorked: ' + str(self.hours_worked)
                + ' \nYou made: '+ str(self.money_made))

    def distances(self):
        '''Set store location based on location type.
        Note: Random choice provides random between + and - number:
        https://docs.python.org/2/library/random.html#random.choice
        '''
        if self.area == 'urban':
            self.coordinates['x'] = (random.uniform(0.0,2.0) *
                                     cf.plus_minus())
            self.coordinates['y'] = (random.uniform(0.0,2.0) *
                                     cf.plus_minus())
        elif self.area == 'suburban':
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
