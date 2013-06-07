# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [1, 1] # pixels per update (1/60 seconds)
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0
VEL = 5 ### paddle speed
ACC = 0.1 ### ball acceleration
score1 = 0
score2 = 0
hit = 0
highest = [0]

### write the score
def add_zero(BC):
    if BC < 10:
        return str(0)+str(BC)
    else:
        return str(BC)

def message():
    global score1, score2
    
    return str(add_zero(score1))+' '+str(add_zero(score2))

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel, hit # these are vectors stored as lists
 
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2

    paddle1_vel = 0
    paddle2_vel = 0
    
    hor_vel = random.randrange(230, 240)/60
    ver_vel = random.randrange(170, 180)/60
    
    
    
    if right == True:
        ball_vel = [hor_vel, ver_vel]
    else:
        ball_vel = [-1*hor_vel, ver_vel]
        
    hit = 0
    
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2, right, highest  # these are ints
    
    global score1, score2
    score1 = 0
    score2 = 0 
    highest = [0]
    right = True
    ball_init(right)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global vel, right, paddle1_vel, paddle2_vel, ACC, hit, highest
    
    
    
    ### print score
    point = (WIDTH / 2 - 83 , 60 ) # The point is the lower left-hand corner of the text
    text_size = 75
    color = "Lime"    
    c.draw_text(message(), point, text_size, color)
    
    point = (WIDTH/2 + 80 , HEIGHT - 10 ) # The point is the lower left-hand corner of the text
    text_size = 20
    color = "Green"
    c.draw_text("Continuous returns: "+str(hit), point, text_size, color)
    point = (80 , HEIGHT - 10 ) # The point is the lower left-hand corner of the text
    c.draw_text("Highest returns: "+str(max(highest)), point, text_size, color)
    
    # update paddle's vertical position, keep paddle on the screen
    
    paddle1_pos += paddle1_vel 
    paddle2_pos += paddle2_vel
    
    # make sure that paddle is not exceeding the top wall
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos -= paddle1_vel
    if paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos -= paddle2_vel
    
    # make sure that paddle is not exceeding the bottom wall
    if paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos -= paddle1_vel
    if paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos -= paddle2_vel
    
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    ### left paddle
    c.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]], 12, "White", "White")
    ### right paddle
    c.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], 12, "White", "White")
    
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    ### Hitting upper wall
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -1*ball_vel[1]
        
    ### Hitting bottom wall
    if ball_pos[1] >=  HEIGHT - BALL_RADIUS:
        ball_vel[1] = -1*ball_vel[1]

    ### test if the ball hitting the left paddle
    if paddle1_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT :
        if ball_pos[0] <=  BALL_RADIUS + PAD_WIDTH:
            ball_vel[0] = (-1-ACC)*ball_vel[0]
            hit += 1
            highest.append(hit)
    ### touching gutter on left
    elif ball_pos[0] <=  BALL_RADIUS:
        right = True
        score2 += 1
        print 'Continuos hits in the last game:   ' + str(hit)
        print 'Highest hits in the last game:  ' + str(max(highest))
        ball_init(right)

    ### test if the ball hitting the right paddle
    if paddle2_pos - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT :
        if ball_pos[0] >=  WIDTH - BALL_RADIUS - PAD_WIDTH:
            ball_vel[0] = (-1-ACC)*ball_vel[0]
            hit += 1
            highest.append(hit)
    ### touching gutter on right    
    elif ball_pos[0] >=  WIDTH - BALL_RADIUS:
        right = False
        score1 += 1
        
        print 'Continuos hits in the last game:   ' + str(hit)
        print 'Highest hits in the last game:  ' + str(max(highest))
        ball_init(right)    
    
    # draw ball and scores
    c.draw_circle( ball_pos, 15, 1, "White", "Red")
    #c.draw_circle( [WIDTH/2,HEIGHT/2], 50, 1, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= VEL
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel += VEL
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= VEL
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel += VEL
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_canvas_background("Gray")
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Restart", new_game, 150)

# start frame
frame.start()
