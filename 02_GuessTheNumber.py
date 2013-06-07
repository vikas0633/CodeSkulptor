# "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
# Author: Vikas Gupta [vgupta@birc.au.dk]

import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100

# define event handlers for control panel

# helper function to initial game
def init():
    
    global number, guesses_left
    number = random.randrange(0, num_range)
    guesses_left = math.ceil(math.log(num_range,2))
    print "\nNew game. Range is from 0 to", num_range
    
    print "Number of remaining guesses is", guesses_left
    
def range100():
    
    # button that changes range to range [0,100) and restarts
    global num_range
    num_range = 100
    init()
    
def range1000():
    
    # button that changes range to range [0,1000) and restarts
    global num_range
    num_range = 1000
    init()
    
def get_input(guess):
    
    global guesses_left
    guesses_left -= 1 # decrease guesses left by 1 for every guess a use makes
    
    guess = int(guess)
    print "\nGuess was", guess
    
    # check if the guess was higher
    if guess > number:
        print "Lower!"
        print "Number of remaining guesses is", guesses_left
     
    # check if the guess was lower
    if guess < number:
        print "Higher!"
        print "Number of remaining guesses is", guesses_left
     
    if guess == number:
        print "Correct!"
        init()
    
    if guesses_left == 0:
        print "\nCorrect number was", number
        print "Shall we try again!"
        init()

# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0, 100)", range100, 200)
f.add_button("Range is [0, 1000)", range1000, 200)
f.add_input("Enter a guess", get_input, 200)

init()
# start frame
f.start()

# always remember to check your completed program against the grading rubric
