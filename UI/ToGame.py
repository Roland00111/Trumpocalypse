import jobs as JOBS #Potential jobs
import events as EVENTS
import menu as MENU
import store as STORE
import locations as LOCATIONS
import config as cf
import random
import time

class Game:
    '''Each game starts in January of 2017, in the first term
    of Donald Trump's presidency. Each game has a Jobs() instance,
    a Locations() instance, and an Events() instance.
    Each game starts without an instance of a Character().
    The user adds a Character() instance during Automatic or 
    Manual character creation.
    '''
    day_counter = 0
    current_year = 2017
    month_counter = 1
    month_day = 1
    term_count = 1
    def __init__(self):
        self.jobs = JOBS.Jobs()
        self.current_day = None
        # TODO: Necessary?
        #  self.opening_menu = MENU.OpeningMenu()
        #Character('random') creates charecter on start menu becasue
        #its an error.
        self.character = None 
        self.locations = LOCATIONS.Locations()
        self.events = EVENTS.Events()
        self.notices = Notices()
        
    def tally_score(self):
        score = 10000
        # score += item.calculate_resale_cost() or some new way?
        size = len(cf.gs.game.events.inactive_events)
        score -= (size*1000)
        # +500 for each day.
        score += self.day_counter * 500
        # +20000 for each term past the first one.
        score += (self.term_count-1) * 20000
        # +100 for each $10,000
        cash = cf.gs.game.character.inventory.sorted_items['cash']
        score += 100*(int(cash.amount/10000))
        return score

    def mod_hours(self,hours,operation=False):
        '''The parameters are the amount of hours if its adding time
        or -hours if its taking time away and the operation.By default
        the operation is False which equates to adding if you pass
        True then it multiplies. Finally it ensures that hours is
        greater than or equal to 0.
        '''
        if operation==False:
            cf.gs.game.current_day.day_hours += hours
        if operation==True:
            cf.gs.game.current_day.day_hours *= hours
        if cf.gs.game.current_day.day_hours < 0:
            cf.gs.game.current_day.day_hours=0
        
    class Day:
        day_hours = 16
        generated_date = 0
        #Only needed to be used once, every other time you can use
        #generated_date find it at the bottom of this class
        inauguration_day = 'January 20th' 

        def __init__(self):
            '''Set day hours to 16 and run end of day modifications.
            
            Run generate date to generate today's "date" and
            accompanying story text.
            
            Note: Do not do eod_mods and gen_date in the initializer.
            This is because, for example, with eod_mods it runs
            process events which in turn makes references to
            cf.gs.game.current_day.day_hours. As this is still
            being initialized this is still referencing the
            previous day!
            Instead do eod_mods and gen_date in StoryScreen.
            '''
            self.day_hours = 16

        def eod_mods(self):
            '''This function checks if you have enough food to go to
            the next day unharmed. Then checks if you are staying at
            your friends house to decrement sanity. Then checks if
            your sanity has gone below 0 and if it has then it
            decrements health and sets sanity to 5. 
            '''
            # Consume food.
            # If no food, health and sanity go down.
            food = (cf.gs.game.character.inventory.
                    sorted_items['food'])
            if (food.amount >= 3):
                food.amount -= 3
            elif (food.amount <3 ):
                food.amount = 0
                cf.gs.game.character.modifyHealth(-1)
                cf.gs.game.character.modifySanity(-1)
            # Housing.
            # Sanity -= 1 if staying with friends.
            # Use 2 housing each month.
            if cf.gs.game.day_counter != 1:
                if (cf.gs.game.character.selected_house == ('Staying with Friends')):
                    cf.gs.game.character.modifySanity(-1)
                else:
                    cf.gs.game.character.inventory.use_housing(2)
            
            # If cash < 0, sanity -= 1.
            cash = cf.gs.game.character.inventory.sorted_items['cash']
            if cash.amount < 0:
                cf.gs.game.character.modifySanity(-1)
                    
                #if sanity dips under zero at the end of the day it hurts
                #your health
            if (cf.gs.game.character.sanity <=0):
                cf.gs.game.character.modifySanity(5,True) # Absolute.
                cf.gs.game.character.modifyHealth(-1)
                # Add notice
                cf.gs.game.notices.add('Sanity bottomed out!')
            else:
                #Continue the events whose durations have not run out.
                pass
            
            # Process events.
            # Then regenerate active events.
            ae = cf.gs.game.events.active_events
            for event in ae:
                event.process()
            cf.gs.game.events.regenerate_active_events()
                
            # If events are > 5, toggle a random event.
            ie = cf.gs.game.events.inactive_events
            if len(ie) > 5:
                event = random.choice(ie)
                cf.gs.game.events.toggle_event(event)
                          
        def gen_date(self):
            g = cf.gs.game # A shortcut
            self.gen_story_text() # Generate today's story text
            if g.month_counter % 12 == 1 and g.day_counter != 1:
                g.current_year += 1
            if g.month_counter + 1 == 13:
                x=12
                month_day = 31
            else:
                x=g.month_counter + 1
                month_day = 1 #Needed because when Game.month_counter
                #== 12 it would go back a year, because it would be
                #12/?/2017 to 1/?/2017 and get confused 
            self.generated_date = self.randomDate(
                str(g.month_counter)+'/1/'+str(g.current_year),
                str(x)+'/'+str(month_day)+'/'+str(g.current_year),
                random.random()
            )
            
            # Reset game day counter incromentation 
            if g.month_counter == 12:
                g.month_counter = 0
        
        def gen_story_text(self):
            g = cf.gs.game # A shortcut
            if g.day_counter == 1:
                self.story_text = ('Today is ' +
                Game.Day.inauguration_day + '\ninauguration day, '+
                'Trump is being sworn into office by Chief Justice '+
                'John Roberts')
            elif g.day_counter % 48 == 0:
                g.term_count += 1
                self.story_text = ('Today is the Election day, '+
                                   'Trump is up for Relection')
            else:
                #If latest random event is a repeat, add again to the
                #text.
                event = cf.gs.game.events.last_random_event[0]
                if (cf.gs.game.events.last_random_event[1] == 1):
                    self.story_text = ('You are sitting on the couch'
                        ' watching the news while eating your '
                        'breakfast and drinking your arbitrary drink'
                        ', and the news comes on. The reporter is '
                        'raving about how life will never be the '
                        'same after...                 '
                        +event
                        + ' again!')
                else:
                    self.story_text = ('You are sitting on the couch'
                        ' watching the news while eating your '
                        'breakfast and drinking your arbitrary drink'
                        ', and the news comes on. The reporter is '
                        'raving about how life will never be the '
                        'same after...\n'
                        +event)
            
        def strTimeProp(self,start, end, format, prop):
            '''Get a time at a proportion of a range of two formatted
            times.
            The start and end should be strings specifying times formated
            in thegiven format (strftime-style), giving an interval
            [start, end].prop specifies how a proportion of the
            interval to be taken afterstart.  The returned time will
            be in the specified format.
            Taken From : http://stackoverflow.com/questions/553303/
                generate-a-random-date-between-two-other-dates
            By: Tom Alsberg
            '''
            stime = time.mktime(time.strptime(start, format))
            etime = time.mktime(time.strptime(end, format)) - 1
            ptime = stime + prop * (etime - stime)
            return time.strftime(format, time.localtime(ptime))

        def randomDate(self,start, end, prop):
            return self.strTimeProp(start, end, '%m/%d/%Y', prop)

class Notices:
    def __init__(self):
        """Create a list for notices."""
        self.n = []
        
    def add(self, notice=""):
        """Add a notice to be displayed."""
        self.n.append(notice)
        # Call CharacterHUD.__ update notices.
        
    def display(self):
        """Return up to twenty current notices for display."""
        lnotice = []
        #~ w = (244,234,244) # White
        #~ g = (144,238,144) # Green
        o = (255,215,194) # Orange
        count = 0
        for notice in reversed(self.n):
            # Iterate in reverse so that the newest notices
            # are displayed first.
            lnotice.append(
            {'item':None,'value':notice,
            'selected_bgcolor':o,'bgcolor':o,'font_size':18})
            if count >= 20: # 0-19
                break
            count += 1
        if len(lnotice) == 0:
            return [{'item':None,'value':'No notices.'}]
        else:
            return lnotice



