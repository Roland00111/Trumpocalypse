Index and Links
- [ ] #35 Inventory Page
- [ ] #34 Utilize Str/Int/Char
- [ ] #33 Level-up HP (and Str/Int/Char)
- [ ] #32 DayScreen Summary Lists
- [ ] #31 Karma, Influence, Butterfly Effect (KIB)
- [ ] #30 Score.
- [ ] #29 Make selected house and transit "scroll into view" when selected item is "hidden".
- [ ] #28 Alert user when house % or transit item % goes below zero and is removed.
- [ ] #26 Change mouse pointer.
- [ ] #25 Audio.
- [ ] #24 Overthrow Trump.
- [ ] #22.3 Show "map" of player's current city.
- [ ] #22.2 Show "map" of locations with associated events and player's current "Home".
- [ ] #22.1 Move locations.
- [ ] #22 Events only affect certain regions.
- [ ] #21.1 Add jobs.
- [ ] #21 Add lots more items.
- [ ] #20 Add lots more events.
- [ ] #19 Add width to self.body = { … } to dynamically change main text box width.
- [ ] #16 Manual character creation.
- [ ] #9 Counteracting the effects of events. (Too difficult for gameplay?)
- [ ] #8 Low or zero sanity.
- [ ] #7 eod_mods Summary Screen (enhanced StoryScreen)
- [ ] #6 eod_mods
~~~~~~~~~~~~~~~~~~~~~~~~~
########## Done ##########
~~~~~~~~~~~~~~~~~~~~~~~~~
- [x] #11 Add un-process events.--Done
- [x] #27 Change to dynamic sizing of the window.--Done (partial: F11 appears working)
- [x] #10 Add process events in eod_mods(). --Done
- [x] #23 Change HP font size.--Done
- [x] #X Make hours not go negative on work.--Done
- [x] #20.1 Refactor events into events.py.--Done
- [x] #18 Refactor jobs import to make uppercase.--Done
- [x] #17 Add story_text to events.--Done
- [x] #3 Take off hours for driving to work. Depends on (#2: Job and Jobs class).--Done
- [x] #4 Buff events rather than add duplicate events.--Done
- [x] #5 Make EventsScreen surface bigger to fit more events.--Done
- [x] #14 Killing the character again not fully working.--Done
- [x] #8 Font color for main box needs fixing.--Done
- [x] #13 Only allow Job.work() to work the number of hours remaining in the day.--Done
- [x] #12 Make game_state.game.mod_hours( ) function and refactor code. --Done
- [x] #15 Add character.job.income to bonuses_by_ratio.--Done
- [x] #1 Staying with Friends: Distance to stores change ...randomly.--Done
- [x] #2 Add a job class for character.--Done
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
########## Other Ideas ##########
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- [ ] #998 Genre
- [ ] #999 Different screens flow diagram (state machine? or...?)

## Features Under Consideration
* Idea: Use "W" and "S" for "Up" and "Down" on the main menu and "D" as "Enter".
  * Good for touchpad users.
* Add various "characters".
  * https://www.reddit.com/r/gaming/comments/68ij9r/ok_genius_idea_for_a_game/
  * Trump, Clinton, Bush, …, …, A. Lincoln, G. Washington, …, …, 
  * How to integrate?
  * Boss battles?
  * Buyable "Heroes"?
* TODO: After walking 25 miles +0.1 HP Upgrade?
* Event months remaining:
  * Idea: All inactive events go down one month remaining each month.
    * Eventually they go away.
  * Idea: Add (#) beside each event to show how many months they have remaining.
    * Ex: You got an STD (3). Meaning 3 months remain.
* Make an alert if there are still day hours remaining and the user presses "Next Month".
  * Just in case they do it on accident.
  * Go to next month? Yes, No.
* On CharacterHUD items list, only show important items.
  * No need to show transit and housing items as they are in the other lists.
  * Show: Food, Clothing, Cash, First Aid Kits
  * Create Inventory Page to show everything else, such as gardens, seeds, etc.
* Idea: HP living reward
  * Each day HP goes up +0.1 until maxxed.
* Age, Gender
  * How to utilize these?
  * Age: … 
  * Gender: … 
* Mini-games.
  * Snake Game.
* After event activated on EventScreen, it goes back to DayScreen.
  * Optional: Have it stay on EventScreen.
* Text to show when there are no events?
  * Idea: "There are no events to display."
* Bug: Food going negative on store inventories.
* Idea: Implement A.I. Q-Learning somewhere.

## Small Things Done
- [x] Done: Add +1 sanity each time you go to work.
- [x] Done: Do not allow both lists on EventScreen to be selected at the same time.
- [x] Fixed: Bug: On EventsScreen: After "Use first aid pack", if still alive, the activated event is still shown on left side. It is activated but lists are "stale". Fix: Redraw PygameUI elements if user is still alive (def click_use_first_aid). See draw_store_lists( ) for similar.
- [x] Done: Character HUD main lists: Change bgcolor of selected to bgcolor of game, so it is "not selectable".
- [x] Done: Document code for Friday's code review. Every class and many functions.
