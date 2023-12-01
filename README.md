# Trumpocalypse
Text based game for Software Development project

Project name: Trumpocalypse

Goal for the project: The goal for this project is to make a game similar to the Oregon trail. However this game will focus on following the life of a person attempting to survive the effects of the Donald Trump presidency. Players will begin in the United States and attempt to survive through either one term of presidency, two terms of presidency, or dictator Trump(endless till you lose). We will begin with using Pygame and plan to add at least one main story,a system to save your inventory,shop for more items, and random events.

Customer: Muhtasim Mahir

Project Manager: Roland Carignan

Other people on project: Nick DeAguiar, Jesse Thew, David Shumway

February Goals: Main story line for the game should be functioning and playable. state diagram complete and in progress of being implemented. Barebones unittest module.

March Goals:  Entire main story line implemented and functional. Add additional storylines and side games/options

End of Semester Goals: To add images to illustrate the story line and locations/menus.

Read-the-docs automated documentation: http://trumpocalypse.readthedocs.io/en/latest/.

Lines of python code: 260965 (`git ls-files | grep ".py" | xargs cat | wc -l`).

## To play Trumpocalypse on Linux and Mac

1. Download the project.
2. Open the ```dist``` folder.
3. Open the executable file ```Trumpocalypse```.

Notes:
* This runs without any other installed software.
* This is built using pyinstaller.
* Only the folder ```dist``` and its contents are required to play.
* This runs on Linux (tested) and Mac (not tested).

## To play Trumpocalypse on Windows (not working)

1. Download and run the file /dist-win/Trumpocalypse.exe.

Notes:
* This is built using https://hub.docker.com/r/cdrx/pyinstaller-windows/. To be specific, the command: ```~/Trumpocalypse/UI$ docker run -v "$(pwd):/src/" cdrx/pyinstaller-windows:python2 "pyinstaller --onefile Trumpocalypse.py"```.

## To play Trumpocalypse using python and pygame

Requirements: python 2.7 and pygame 1.9.2.

```
$ git clone https://github.com/Roland00111/Trumpocalypse
```

Install python2 and pygame (RHEL):
```
$ sudo dnf install virtualenv python2
$ virtualenv --python=python2 venv
$ . venv/bin/activate
$ pip install pygame==1.9.2
```

Start Trumpocalypse:
```
$ cd ./Trumpocalypse/UI
$ python Trumpocalypse.py
```

## Gameplay notes

Press F11 to play in full-screen mode.

## To build executables

1. Change all instances of SysFont('...' to SysFont('arial' and reduce size on these by 50%.
2. Run ```pyinstaller --onedir Trumpocaylpse.py```.
3. Copy into the folder ```./dist/Trumpocalyse/``` the images and audio, the folder ```./data/```, and ```high_score.txt```. 

## Presentation feedback:
"
The only real data structures feedback is related to the ability to save and restore game state. There was also some feedback on the user interface and overall design.

Save feature: You should plan how you are going to save game progress rather than waiting until that is awkward because there is so much to save. You suggested saving the user input and replaying it, but that will not work given random events unless you also save the random seed. A lazy approach would be to put all of your game state into an object and pickle it. A more satisfying approach would be to write the game state in JSON format, which can be easily extended if you have new state to save.

UI: The text color is unreadable. Suggest making a lighter colored box for the text, and choose a text color that is distinguishable when you squint.

Fun factor: want the choices that a user makes to make a bigger impact on how the game progresses."

Presentation for code review: 04/14/17
