# template for "Stopwatch: The Game"

import simplegui
# define global variables
time = 0
attempt = 0
score = 0
running = True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def add_zero(BC):
    if BC < 10:
        return str(0)+str(BC)
    else:
        return str(BC)

def format(time):
    
    ### return A:BC.D
    A = str(time // 600)
    
    BC = (time // 10 ) % 60
    BC = add_zero(BC)
    D = str(time % 10)
    
    return A + ":" + BC + "." + D
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global running
    timer.start()
    running = True
    
def stop():
    global time, attempt, score, running
    if running == True:
        if time % 10 == 0:
            score += 1
        attempt += 1
        timer.stop()
    running = False
    
def reset():
    global time, attempt, score, running
    time = 0
    attempt = 0
    score = 0
    running = True
    
def tick():
    global time
    time = time + 1

# define event handler for timer with 0.1 sec interval


# define draw handler
def draw(canvas):
    global time, attempt, score
    message = format(time)
    point = (60, 120) # The point is the lower left-hand corner of the text
    text_size = 75
    color = "Lime"
    canvas.draw_text(message, point, text_size, color)
    
    message = str(score)+'/'+str(attempt)
    point = (250, 30) # The point is the lower left-hand corner of the text
    text_size = 30
    color = "White"
    canvas.draw_text(message, point, text_size, color)
    
# create frame
frame = simplegui.create_frame("Testing", 300, 200)

# register event handlers
frame.add_button("Start", start, 150)
frame.add_button("Stop", stop, 150)
frame.add_button("Reset", reset, 150)

timer = simplegui.create_timer(100, tick)

frame.set_draw_handler(draw)

# start frame
frame.start()

# Please remember to review the grading rubric
