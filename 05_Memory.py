# implementation of card game - Memory
# Vikas Gupta

import simplegui
import random

lst = []
exposed = []
pre_index = ''
pre_pre_index = ''
moves = 0
# helper function to initialize globals
def init():
    global lst, exposed
    global state
    state = 0
    lst=range(8)
    lst.extend(range(8))
    random.shuffle(lst)
    exposed=[False for i in range(len(lst)) ]

def buttonclick():
    global state
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state = 1   
 
def move():
    global moves
    return 'Moves: '+str(moves)
        
# define event handlers
def mouseclick(click):
    global lst, exposed, state, moves
    # add game state logic here
    global mouse_pos, pre_index, pre_pre_index
    mouse_pos = click
    
    ### click the card and make true the number
    exposed[mouse_pos[0]//50] = True
    
    ### start of the game
    if state == 0:
        pre_pre_index = mouse_pos[0]//50
        state = 1
    elif state == 1:
        pre_index = mouse_pos[0]//50
        state = 2
    elif state == 2:
        if not lst[pre_pre_index] == lst[pre_index]:
            exposed[pre_pre_index] = False
            exposed[pre_index] = False

        pre_pre_index = mouse_pos[0]//50
        state = 1
    
    ### increment move by 1
    moves += 1
    label.set_text(move())
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = [5, 80]   
    for i in range(len(lst)):
        canvas.draw_text(str(lst[i]), pos, 80, "white")

        ### draw green ractangles
        if not exposed[i]: 
            canvas.draw_polygon([(50*i,0),(50*i,100),(50*(i+1),100),(50*(i+1),0)], 1, "white", "Green")
        pos[0] += 50
        

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)


# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)
label = frame.add_label("Moves: 0")

# get things rolling
frame.start()


# Always remember to review the grading rubric