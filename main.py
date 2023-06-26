import turtle
import random
import time
import os
import pip   # for attempt to autoinstall boombox, ok in linux, partial sucess in nt

def import_boom_box(boombox):  # compability interface to linux / MS /Mac eq to winsound module
    try:
        __import__(boombox)
    except ImportError:
        print ("for sound boombox module is needed")
        print (" pip install boombox")
        pip.main (['install' , boombox])

from boombox import BoomBox     # please install package boombox by     pip install boombox
sound = BoomBox("1.wav", wait=False)
sound_lenght=1850  # im micro seconds
blip = BoomBox("blip.wav", wait=False)
 
intro_screen =turtle.Screen()
intro_screen.setup(600, 800)
intro_screen.bgpic("1.png")
intro_screen.update()

introBoard = turtle.Turtle()              # all these need to be scarped and should be made into tight object
introBoard.speed(0)
introBoard.shape("square")
introBoard.color("white")
introBoard.penup()
introBoard.hideturtle()

for i in range(5):
    time.sleep(1)
    introBoard.clear()
    introBoard.goto(175,-50)
    introBoard.write("{}".format(i+1), align="center", font=("ds-digital", 50, "bold"))
introBoard.clear()
del introBoard
# print (start_time , elapsed_time)   #debug lines
# exit(0)

score =0
windows = turtle.Screen()                  #initiliaze  Screen
windows.title("SpaceAstroJam")
windows.setup(600, 800)
windows.bgpic("space.png")
windows.tracer(0)
windows.listen()
low_speed=3
high_speed=5

Rocks_list = ("01.gif","02.gif","03.gif","04.gif","05.gif","06.gif","07.gif","08.gif","09.gif","10.gif","12.gif","13.gif","14.gif","15.gif","16.gif","17.gif","18.gif","19.gif","20.gif","21.gif","22.gif","23.gif","24.gif","25.gif","26.gif")
FarObj_list=("1.gif","2.gif", "3.gif", "4.gif","s1.gif")
spaceFarObj_list=[]
#scoreBoards
for i in range(3):                       # all these need to be scarped and should be made into tight object
    var=random.choice(FarObj_list)
    windows.register_shape(var)
    farObj = turtle.Turtle()
    windows.register_shape(var)
    farObj.shape(var)
    farObj.up()
    farObj.goto(random.randint(-280, 280), random.randint(-280, 280))
    spaceFarObj_list.append(farObj)
    
scoreBoard = turtle.Turtle()              # all these need to be scarped and should be made into tight object
scoreBoard.speed(0)
scoreBoard.shape("square")
scoreBoard.color("white")
scoreBoard.penup()
scoreBoard.hideturtle()
scoreBoard.goto(0,280)
    
windows.register_shape("rocket.gif")      # all these need to be scarped and should be made into tight object
Rocket = turtle.Turtle()
Rocket.shape("rocket.gif")
Rocket.shapesize(2, 2)
Rocket.up()
Rocket.goto(0, -300)

for i in range(len(Rocks_list)):            # solved this way to elimainate the shortcomings in turtle 
    windows.register_shape(Rocks_list[i])    

rockFall_list=[]
for i in range(4):                          
    Rock=random.choice(Rocks_list)          # generate set of 8 rocks and reuse it in loop
    spaceRocks = turtle.Turtle()            # all these need to be scarped and should be made into tight object
    spaceRocks.shape(Rock)
    spaceRocks.shapesize(2, 2)
    spaceRocks.up()
    spaceRocks.speed(random.randint(low_speed, high_speed))
    spaceRocks.goto(random.randint(-250, 250), 560)
    rockFall_list.append(spaceRocks)

def spawn_new_rock():
    var1=random.choice(Rocks_list)
    rck_new = turtle.Turtle()
    rck_new.shape(var1)
    rck_new.shapesize(2, 2)
    rck_new.up()
    rck_new.speed(random.randint(low_speed, high_speed))
    rck_new.goto(random.randint(-250, 250), 450)  
    rockFall_list.append(rck_new)          

def mv_spaceRocks():                             # hacked the limitation of the turtle
    for rck in rockFall_list:               
        if (rck.speed()>0):                      # to avoid the uncessarry expensive goto 
            rck.goto(rck.xcor(), rck.ycor() - rck.speed())
        if rck.ycor() < -400:                    # spawn new random object after it falls
            rockFall_list.remove(rck)
            rck.clear()
            rck.hideturtle()
            del rck
            spawn_new_rock()

blip = BoomBox("blip.wav", wait=False)

def move_left():                            
    if Rocket.xcor() >= -200:
        blip.play()
        Rocket.goto(Rocket.xcor() - 25, Rocket.ycor())

def move_right():
    if Rocket.xcor() <= 200:
        blip.play()
        Rocket.goto(Rocket.xcor() + 25, Rocket.ycor())

def move_up():
    blip.play()
    if Rocket.ycor() <= 0:
        Rocket.goto(Rocket.xcor(), Rocket.ycor() + 25)

def gameover():
    scoreBoard.goto(0,0)
    scoreBoard.write("Game Over".format(score,level), align="center", font=("ds-digital", 25, "bold"))
    time.sleep(5)

def move_down():
    blip.play()
    if Rocket.ycor() >= -250:
        Rocket.goto(Rocket.xcor(), Rocket.ycor() - 25)
    
windows.onkey(move_left, "Left")
windows.onkey(move_right, "Right")
windows.onkey(move_up, "Up")
windows.onkey(move_down, "Down")

game_over = False

bcksound=BoomBox("1.wav", wait=False)  # randomly play this sound inside loop with pribability 1/100
bcksound_len=1850                      # for making a unified code for linux and nt. altenative approach appropriate if for either system only
bcksound.play()
bcksound_start=int(time.time()*1000)

s=0                   #score
level = 0             #level
increment_Score=1000
    
while not game_over:
    t=int(time.time()*1000)            # for the sound file calc
    time.sleep(0.005)    #This is system dependent  nedds to be tweaked for controlling speed
    y=t - bcksound_start
    if y > bcksound_len:               # play sound again if time longer than lenght of sound 
        bcksound.play()
        bcksound_start=int(time.time()*1000)
        #print(y)   #debug line
    mv_spaceRocks()    
    scoreBoard.clear()
    high_score = score                 # score need to be saved in the file 
    scoreBoard.write("score: {}  level: {}".format(score,level), align="center", font=("ds-digital", 18, "bold"))

    if (score > increment_Score ):     #level tweaker
        level+=1
        increment_Score+=1000 +250*level   # tweaked to make the each level last approx same time
        if level % 2==0:                   # level tweaked by changing speed of rocks as well as no or spaceRcks
            if low_speed < 5:
                low_speed +=1
            elif high_speed < 9:
                high_speed +=1
        else :
            spawn_new_rock()
                
    for i in rockFall_list:           # check collision .can be made the radius of the object if tuple is used insted of the list
        if (i.ycor()<=-300):          # preety bug giving effect as intended :) hence is no bug at all
            score= score + 5
        if i.distance(Rocket) <= 45:  # value here can be tweaked here to match ( pixel  size )/2 of turtle img for perfect collosion but lot of work with slight visual improvement  
            gameover()
            game_over = True;
                 
    #debug line
    #print ('level {} rocks {}   lower {}  upper {} '.format(level ,len(rockFall_list), low_speed, high_speed ) )
    windows.update()
bcksound.stop()

# catch here for intro and a perfect place for goto to restart game . but dumb python demands the while(1) : instead
