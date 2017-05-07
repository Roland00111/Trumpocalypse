import random
import copy
import config as cf
import items as ITEMS

class Event:
    '''
    '''
    def __init__(self, event_text, bonuses={}, bonuses_by_ratio={},
                 story_text='', base_duration=0, duration_rand_min=0,
                 duration_rand_max=0):
        '''
        :param str event_text: Event title.
        :param dict bonuses: Event bonuses.
        :param dict bonuses_by_ratio:
            Event bonuses using a multiplier
            ('Cash':0.2 means the character is
            left with 20% of current cash).
        :param str story_text: A long-worded story for the event.
        :param int base_duration: Base number of months.
        :param int duration_rand_min:
            Random min. added number of months.
        :param int duration_rand_max:
            Random max. added number of months.
        '''
        self.event_text = event_text
        self.story_text = story_text
        self.bonuses = bonuses
        self.bonuses_by_ratio = bonuses_by_ratio
        self.base_duration = base_duration
        self.duration = None # Dynamic
        self.months_remaining = None # Dynamic
        self.duration_rand_min = duration_rand_min
        self.duration_rand_max = duration_rand_max
        # Will be changed to True at some point.
        self.activated = False
        #self.is_over = False
        
        
    def process(self):
        '''Process event. Each time the event happens
            months_remaining -= 1.
        
        Each bonus of the event does one of the following:
            1) update day hours remaining;
            2) update or add an inventory item;
            3) or, change one of the character's attributes,
            such as hp.
        '''
        c = cf.gs.game.character
        # Bonuses.
        for key, value in self.bonuses.iteritems():
            if key == 'hours':                     # Hours
                cf.gs.game.mod_hours(value)
            elif key in ITEMS.n['all_choices']:    # Inventory
                c.inventory.add_item(str(key),int(value))
                                     # Character attribute
            #Throwing in an if to catch the error from income no
            #longer being in character
            elif key == 'income':
                c.job.income += value
            else:
                print 'Modifying character attr:',key,'(',value,')'
                n = getattr(c,str(key))
                setattr(c,str(key),n+value)
        # Bonuses by ratio.
        # Round to one decimal when necessary.
        for key, value in self.bonuses_by_ratio.iteritems():
            if key == 'hours':
                cf.gs.game.mod_hours(value,True)
            elif key in ITEMS.n['all_choices']:
                c.inventory.multiply_item(str(key),float(value))
            elif key == 'income':
                c.job.income *= value
                c.job.income = round(c.job.income, 1)
            elif key == 'housing':
                c.inventory.house_degrade(value)
            elif key == 'health':
                c.modifyHealth(value)  
            else:
                n = getattr(c,str(key))
                setattr(c,str(key),n*value)
        # Decrement months.
        self.months_remaining -= 1
        # Make sure it is presently active.
        self.activated = True
        # If self.months_remaining <= 0 ...
        if self.months_remaining <= 0:
            self.activated = False
            #self.is_over = True
            # Delete this event.
            #del(self)
            

    def generate_duration(self):
        '''
        Generate the duration of this event. It is between
        [base_duration + duration_rand_min] and [base_duration +
        duration_rand_max].
        Then set months_remaining to be duration.
        '''
        self.duration = self.base_duration + random.randint(self.
                            duration_rand_min, self.duration_rand_max)
        self.months_remaining = self.duration
        
class Events:
    events_array = [
        #'life will never be the same after...'
        # Max event length ~24 characters bigger breaks the nl
        # character.
        Event(  'A Tsunami', {'health':-1,'sanity':-5}, {},
                'You were strolling along the beach, when you began'
                'to notice the waves drawing back from the coast. '
                'You began to run for higher ground and shouted that'
                ' you thought a Tsunami was coming. Many people did '
                'not believe you, and it was their last action  :-1 '
                'Health, -5 Sanity' ,
                2,0,1), #duration,duration_rand_min,
                        #duration_rand_max all in months
        
        Event(   'You Won the Lottery!', {'Cash':10000,'sanity':1},
                 {},
                'Yesterday, on a whim you bought your first and only '
                 'lottery ticket. You forgot about it, but after '
                 'watching the daily news, you found out that the '
                 'winning ticket, was bought from the store Which '
                 'you bought yours! After some searching you find '
                 'the ticket and bring it in, it was the winner!: '
                 'You Gain $10,000!',
                1,0,0),
        
        Event(  'Extreme Pollution', {'health':-1,'sanity':-1}, {},
                'Since the new President was elected there have been,'
                'developments which increased our industrial power and'
                'availability of work, but now it is coming back to '
                'haunt us. The country is in a state of panic, due to'
                'dangerous levels of CO2 in the atmosphere:  -1 Health,'
                '-1 Sanity',
                4,0,4),
        
        Event(  'Nuclear War', {'health':-2,'sanity':-5,'hours':-4}, {'housing':0.8},
                'It was deemed necessary to send an attack on Syria '
                'today. Russia did not take it kindly, and has '
                'decided to retaliate by attacking your home soil. A'
                ' nuke has been launched and your life will '
                'drastically change: -2 health -5 sanity -4 hours',
                6,0,6),
        
        Event(  'Martial Law', {'hours':-4,'sanity':-2,
                                 'income':-2500}, {},
                'A state of emergency has been declared, and Marshall'
                ' Law put into effect. Please remain calm and listen '
                'to all army officials. You will help the efforts of '
                'the country for free as it is your duty as a citizen!'
                ': -4 hours, -2 sanity, -2500 income',
                4,0,8),
        
        Event(  'Zombie Apocalypse', {'hours':-4,'sanity':-2,
                                      'income':-5000}, {},
                'Some people think it was voodoo, others think a government finally'
                'made it work. What I think, is I am going to keep my brains to myself.'
                'Zombies have made it to the United States and you must survive until'
                'the government can regain control: -4 hours -2 sanity -5000 income',
                4,0,8),
        
        Event(  'You Power Sleep', {'hours':2,'sanity':2}, {},
                'You had the nicest dream last night and although you cannot'
                'remember the specifics, you know there were puppies involved'
                '. You have not slept this well since you had no worries in the'
                'world and were living with your parents : +2 hours +2 sanity',
                1,0,0),
        
        Event(  'Find Supply Cache', {'Food':15,'Cash':1000,
                                      'sanity':1}, {},
                'You were playing with your metal detector for fun and'
                'it began to beep signifying a large metal object about'
                ' 4 feet under the ground, against your better instincts'
                'you decided to dig it up and found a hiddent supply cache!'
                'Thanks doomsday prepper! +15 food +$1000 +1 sanity' ,
                1,0,0),
        
        Event(  'Puppies!!',{'Cash':-1000, 'sanity':10}, {},
                'Today it was rainy and you saw a little girl walking her dog'
                '. For some reason, this made you think back of your first pet.'
                'As you began missing your first dog Spot you decide to give the'
                'Humane Society a visit. You play with some puppies '
                'and end up taking one home: +10 sanity -1000 Cash',
                1,0,0),
        
        Event(  'Tax Collector',{'Cash':-1000, 'sanity':-1},
                {'Cash':0.60}, # Removes $1000, then sets cash to 60%.
                'As you were cooking dinner, you heard a knock on your door.'
                'The government had sent a tax collector because you were'
                'overdue on your taxes. You wrote him a check for your overdue'
                ' taxes, and the late fees: -1000$ -1 sanity Cash 60%',
                1,0,1),
        
        Event(  'Curfew', {'hours':-4,'sanity':-2}, {},
                'Due to government request, everyone must be in their homes'
                'for their own safety 4 hours early every night. Some people'
                ' believe it was an effort to save electricity, others think '
                'it is because of dissidents. No one knows the real reason '
                'behind the curfew... : -4 hours -2 sanity',
                2,0,1),
        Event(  'Carnival', {'hours':-2,'sanity':10}, {},
                'Trump decided to send a carnival to your town in order to '
                'increase his support in the area. You decided to go to the '
                'carnival to relieve some of the stress from everything thats '
                'happening : -2 hours +10 sanity',
                2,0,1),
        Event(  'Death in the family', {'hours':-4,'sanity':-10,'Cash':-1000}, {},
                'Everything was starting to look up when you got a phone call '
                'from your Aunt Mable telling you your brother just died and '
                'you had to fly home to attend '
                'his funeral : -4 hours -10 sanity -1000 Cash',
                2,0,1),
        Event(  'Project Blue', {'hours':-6,'sanity':-2,'health':-1}, {},
                'You were eating your lunch watching the news when they '
                'announced that there is a pandemic happening called Project'
                ' Blue You must prepare for the pandemic and take the proper '
                'percautions : -6 hours -2 sanity -1 health',
                2,0,1),
        Event(  'EarthQuake', {'hours':-4,'sanity':-5,'Cash':-500}, {},
                'You were eating your lunch watching the news when the ground '
                'began to shake, you hid in the bathroom and luckily were not'
                'harmed. You cant say the same for your neighbors; you will '
                'never forget some of the things you saw this day. You decide'
                'to help out your community in the reparations: hours:-4, '
                'Sanity:-5, Cash:-500',
                2,0,1),
        Event(  'You got an STD',
                {'sanity':-5,'hours':-5,'health':-1,'Cash':-5000}, {},
                'You dont know exactly where it came from, but this morining'
                'you had some odd pus-filled bumps on your nether region.'
                'First you had to pay for the doctor, then the tests, and'
                'then even the medication to try to get rid of it all. The'
                'doctor said that if you are lucky it could never come back'
                ', but who knows for sure: hours:-5, Health:-1, '
                'Sanity:-5, Cash:-500',
                2,0,1),
        ]
    
    def __init__(self):
        self.inactive_events = []
        self.active_events = []
        #Last event will store, event name, and buffed in a boolean.
        self.last_random_event = ['placeholder',1]
    
    def regenerate_active_events(self):
        """Regenerate the active events list based on active events."""
        a = cf.gs.game.events.active_events
        temp_events = []
        for event in a:
            if event.activated == True:
                temp_events.append(event)
            #elif event.is_over == True:
                
        #cf.gs.game.events.
        self.active_events = temp_events

    def show_inactive_events(self):
        '''
        Return a list of inactive events.
        '''
        temp = [ ]
        for event in self.inactive_events:
            temp.append( {'item':event,'value':event.event_text} )
        return temp

    def show_active_events(self):
        '''
        Return a list of active events.
        '''
        temp = [ ]
        for event in self.active_events:
            temp.append( {'item':event,'value':event.event_text} )
        return temp

    
    def events_values(self):
        '''
        Returns a list of titles of current inactive events.
        :return: List of titles of current inactive events
        :rtype: list.
        '''
        events_temp = []
        for event in self.inactive_events:
            events_temp.append(event.event_text)
        return events_temp
        
    def random_event(self):
        '''
        Add a random event to inactive_events.
        '''
        num = random.randint(0,len(Events.events_array)-1)
        # copy v. deepcopy =same
        event = copy.deepcopy(Events.events_array[num]) 
        # Generate event duration.
        event.generate_duration()
        # Add to inactive events
        #Buffing the event if already in queue. Removing the original
        #event and adding a longer new event. Otherwise, would have
        #issues using the [-1] for last added later.
        count = 0
        for item in self.inactive_events:
            
            if (item.event_text == event.event_text):
                item.months_remaining += event.months_remaining
                self.last_random_event[1] = 1
                self.last_random_event[0] = item.event_text
                #this is to remove the event that we increased the new
                #events duration with.
                del self.inactive_events[count]
                break
            
            count +=1
        else:
            self.last_random_event[0] = event.event_text
            self.last_random_event[1] = 0
        
        self.inactive_events.append(event)
        
    def toggle_event(self, event):
        '''
        Move an event from self.inactive_event to self.active_event.
        Assumption: Once an event is activated it stays active until
        it runs out. Then it is removed altogether.
        
        Fire the event for the first time (event.process).
        
        :param event: The event to toggle.
        :type event: Event.
        '''
        for k,v in enumerate(self.inactive_events):
            if v == event:
                del self.inactive_events[k]
        # Run the event.
        event.process()
        # Add to active events if months remain > 0.
        if event.months_remaining > 0:
            self.active_events.append(event)

