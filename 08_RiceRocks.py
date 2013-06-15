################################################################
# Vikas Gupta												   #
# vikas0633@gmail.com										   #
# 2013-06-14												   #
################################################################

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 1000
HEIGHT = 800
score = 0
lives = 3
time = 0.0
ANG_VEL = 0.08
THURST_ACC = 0.4
FRICTION = 0.05
rock_group = set([])
missile_group = set([])
ROCK_LIMIT = 12
TIME = 0.7
started = False
explosion_group = set([])


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45,45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
explosion_sound.set_volume(.3)

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(group,canvas):
    for obj in set(group):
        obj.draw(canvas)
        obj.update()
        if obj.update():
            group.remove(obj)

def group_collide(group,other_object):
    global lives, time
    for obj in set(group):
        if obj.collide(other_object):
            group.remove(obj)
            explosion_group.add(Sprite(obj.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound))
            return True
            
def group_group_collide(group1,group2):
    collisions = 0
    for obj in set(group1):
        
        if group_collide(group2, obj):
            group1.remove(obj)
            collisions += 1
    return collisions
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info, sound = None):
        
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrust_on = False
        self.sound = sound
       
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust_on == True:
            self.image_center = [135,45]
        else:
            self.image_center = [45,45]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def play_sound(self):
        if self.thrust_on == True:
            self.sound.play()
        else:
            self.sound.rewind()

        
    def update(self):
        self.vector = angle_to_vector(self.angle)
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.angle += self.angle_vel
        
                
        ### wrap the ship around the screen
        if self.pos[0] < 0:
            self.pos[0] += WIDTH
        if self.pos[1] < 0:
            self.pos[1] += HEIGHT
        if self.pos[0] > WIDTH:
            self.pos[0] -= WIDTH
        if self.pos[1] > HEIGHT:
            self.pos[1] -= HEIGHT
        
        ### update the velocity
        if self.thrust_on == True:
            self.vel[0] += THURST_ACC*(self.vector[0] +0.001)
            self.vel[1] += THURST_ACC*(self.vector[1] +0.001)
        
        
        self.vel[0] *= 1-FRICTION
        self.vel[1] *= 1-FRICTION
    
    def shoot(self):
        global missile_group
        self.pos_missile = [0,0]
        self.vel_missile = [0,0]
        self.pos_missile[0] = self.pos[0] + 35*self.vector[0]
        self.pos_missile[1] = self.pos[1] + 35*self.vector[1] 
        self.vel_missile[0] = self.vel[0]
        self.vel_missile[1] = self.vel[1]
        self.vel_missile[0] += 10*(self.vector[0])
        self.vel_missile[1] += 10*(self.vector[1])
        missile_group.add(Sprite(self.pos_missile, self.vel_missile, 0, 0, missile_image, missile_info, missile_sound))
        
    def keydown(self,key):
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel -= ANG_VEL
        if key == simplegui.KEY_MAP["right"]:
            self.angle_vel += ANG_VEL
        if key == simplegui.KEY_MAP["up"]:
            self.thrust_on = True
        if key == simplegui.KEY_MAP["space"]:
            self.shoot()
            
            
    def keyup(self,key):
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel += ANG_VEL 
        if key == simplegui.KEY_MAP["right"]:
            self.angle_vel -= ANG_VEL
        if key == simplegui.KEY_MAP["up"]:
            self.thrust_on = False
    
        
    def get_position(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
        
        
            
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
   
    def draw(self, canvas):
        global time
        if self.animated == True:
            global time
            ROCK_SIZE = self.image_size
            ROCK_CENTER = self.image_center
            ROCK_DIM = 24
            current_rock_index = (time % ROCK_DIM) // 1
            self.image_center = [ROCK_CENTER[0] +  current_rock_index * ROCK_SIZE[0], ROCK_CENTER[1]]
            time += 0.001
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel       
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        ### wrap the ship around the screen
        if self.pos[0] < 0:
            self.pos[0] += WIDTH
        if self.pos[1] < 0:
            self.pos[1] += HEIGHT
        if self.pos[0] > WIDTH:
            self.pos[0] -= WIDTH
        if self.pos[1] > HEIGHT:
            self.pos[1] -= HEIGHT
         
        # life span
        self.age += TIME
        if self.age < self.lifespan:
            return False
        else:
            return True
            
    def get_position(self):
        return self.pos
        
    def get_radius(self):
        return self.radius
    
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius()


## mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

    
           
def draw(canvas):
    global time, score, lives, rock_group, missile_group, started
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    
    ### check if lives are left are 0
    if lives == 0:
         started = False
            
    
    if not started:
        lives = 3
        score = 0
        rock_group = set([])
        missile_group = set([])

    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
    if started:
    
        # draw ship and sprites
        my_ship.draw(canvas)
        process_sprite_group(rock_group,canvas)
        if group_collide(rock_group,my_ship):
            lives -=1
        process_sprite_group(missile_group,canvas)
        process_sprite_group(explosion_group,canvas)
        # update ship and sprites
        my_ship.update()
        
        # play sound
        my_ship.play_sound()
        
        # missile hits
        score += group_group_collide(missile_group, rock_group)
    
    ### print score
    point = (WIDTH - 200 , 60 ) 
    text_size = 25
    color = "White"    
    canvas.draw_text("Score", point, text_size, color)
    point = (WIDTH - 180 , 90 )
    canvas.draw_text(str(score), point, text_size, color)
    
    ### print lives
    point = (100, 60 ) 
    text_size = 25
    color = "White"    
    canvas.draw_text("Lives", point, text_size, color)
    point = (120 , 90 ) 
    canvas.draw_text(str(lives), point, text_size, color) 
    
    

    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    ship_pos = my_ship.get_position()
    width = random.randint(0,WIDTH)
    height = random.randint(0,HEIGHT)
    ## makw sure rock is not too close
    while ( ship_pos[0] - 50 <= width <= ship_pos[0] + 50) or ( ship_pos[1] - 50 <= height <= ship_pos[1] + 50): 
        width = random.randint(0,WIDTH)
        height = random.randint(0,HEIGHT)
    ang_vel = random.random()/2
    if ang_vel > random.random()/4:
        ang_vel = random.random()/4 - ang_vel 
    if len(rock_group) < ROCK_LIMIT: 
        rock_group.add(Sprite([width, height], rock_vel, 0, ang_vel, asteroid_image, asteroid_info))

        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
rock_vel = random.random() - 0.5, random.random() - 0.5
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info, ship_thrust_sound)
rock_group.add(Sprite([WIDTH / 3, HEIGHT / 3], rock_vel, 0, 0, asteroid_image, asteroid_info))
missile_group.add(Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [0,0], 0, 0, missile_image, missile_info, missile_sound))

# register handlers
frame.set_keydown_handler(my_ship.keydown)
frame.set_keyup_handler(my_ship.keyup)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
