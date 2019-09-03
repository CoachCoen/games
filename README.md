# Games
Board and card games developed in Python 3

## Introduction
The current version implements the rules of the popular game "Splendor"

## Requirements
* Python 3
* Python libraries listed in requirements.txt

## Running the game
python3 app.py

## Current status
* All but one rule implemented
    * Can't take a face down card after taking a yellow chip
* Usually works well, although there is one bug (not replicated yet)
* Code is reasonably well structured (always room for improvement of course)
* Unit tests were started but need updating 
after a large refactoring exercise, and more are to be done
* An estimated 15% of functions, methods, etc, have docstrings, so need to 
catch up and then keep up
* Sphinx set up, documentation created

## The AI
The current AI is extremely simple, yet still plays a decent game 
(this may change when the final rules have been implemented)
* If it can buy a card, it will
* Otherwise it will take a random set of chips
* Failing that, it will take a yellow chip and reserve a card

## Future plans
* Complete the first game
    * Somewhat better graphics
    * Better test coverage, doc strings, etc
* Online version
    * Create a version which uses a Flask and 
some Javascript instead of pygame
    * Extract 'back-end' code, so can be shared between 
    pygame and online version, and used for other games
* Other game(s)
    * Possibly a card game such as Dominion, or the grid-based Acquire
* Improved AI
    * With the option for different AIs to compete, to compare their performance
