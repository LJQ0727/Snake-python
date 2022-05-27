import turtle
from random import randint, shuffle
from time import time
from math import sin, cos, radians

# declare and configure screen
g_screen = turtle.Screen()
g_screen.setup(660,740)                             # set window size
g_screen.setworldcoordinates(-80,-80,580,660)       # set margin and coordinate
g_screen.title('Snake by Jiaqi Li')
g_screen.tracer(0)                                  # set update to manual

# declare global turtles
g_status_turtle = turtle.Turtle()                   # turtle for displaying status bar
g_message_turtle = turtle.Turtle()                  # turtle for displaying welcome message
g_snake_turtle = turtle.Turtle()                    # turtle as the snake
g_monster_turtle = turtle.Turtle()                  # turtle as the monster

# status bar information
g_contact = 0
g_time = 0
g_motion = 'Paused'

# whether to start the game
g_initiate_game_module = True                       # is used to avoid multiple mouse clicks
g_snake_caught = False                              # whether snake is caught
g_player_wins = False                               # whether player wins the game
g_last_20_contact = [False] * 20                    # denotes whether last 20 times refresh are considered as contact; is used to avoid continuous contacts
# because I check contact every 0.05 seconds, this store the recent 1 second contact trace

# denotes how many tails should expand
# at startup, extend tail by 5
g_extend_tail_value = 5

g_food_list = []                                    # stores all remaining food items in integers, e.g. [1,2,3,4]
g_stamp_location_list = []                          # stores all stamp locations, e.g. [(0,0), (200,200)]


def set_turtles():
    # set properties of turtles

    global g_snake_clone

    g_status_turtle.hideturtle()
    g_message_turtle.hideturtle()
    g_snake_turtle.up()
    g_snake_turtle.color('red')
    g_snake_turtle.shape('square')
    g_snake_turtle.goto(250,250)
    g_monster_turtle.up()
    g_monster_turtle.color('purple')
    g_monster_turtle.shape('square')
    while True:
        g_monster_turtle.goto(randint(50,450),randint(50,250))
        if g_monster_turtle.distance(g_snake_turtle) > 75:
            break                                                           # to make sure monster is not too close to snake at startup
    g_snake_clone = g_snake_turtle.clone()
    g_snake_clone.color('blue', 'black')
    g_snake_clone.hideturtle()

def draw_border():
    # display motion area and status bar borders

    # draw motion area
    border_turtle = turtle.Turtle()
    border_turtle.hideturtle()
    border_turtle.up()
    border_turtle.goto(0,500)
    border_turtle.down()
    border_turtle.pensize(2)        # accounting for the pensize to achieve 500*500 pixels
    border_turtle.setheading(180)
    for i in range(4):
        border_turtle.left(90)
        border_turtle.forward(500)

    # draw status bar
    border_turtle.right(90)
    border_turtle.forward(80)
    border_turtle.right(90)
    border_turtle.forward(500)
    border_turtle.right(90)
    border_turtle.forward(80)
    border_turtle.right(90)
    border_turtle.forward(500)
    border_turtle.right(90)

def display_status():
    # displays status bar information
    # including contact, time and motion
    g_status_turtle.clear()         # remove previous status bar information
    g_status_turtle.up()
    g_status_turtle.color('black', 'black')
    g_status_turtle.pensize(10)
    g_status_turtle.goto(80,530)
    g_status_turtle.write(f'Contact: {g_contact}', False, 'center', ('Arial', 15, 'bold'))
    g_status_turtle.goto(230,530)
    g_status_turtle.write(f'Time: {g_time}', False, 'center', ('Arial', 15, 'bold'))
    g_status_turtle.goto(390,530)
    g_status_turtle.write(f'Motion: {g_motion}', False, 'center', ('Arial', 15, 'bold'))
    g_screen.update()

def display_startup_message():
    # displays welcome message
    g_message_turtle.up()
    g_message_turtle.goto(48,280)
    g_message_turtle.write("Welcome to Jiaqi Li's snake game!\n\nIn this game, you're going to use the 4 arrowkeys on your keyboard \n to move the snake, avoid hitting the monster and try to consume all \nfood items on the canvas.\n\nYou win the game when your snake eats all the food without being \ncaptured by the monster. Good luck!\n\nMonster's speed slows down dramatically when snake's extending.\n\nClick anywhere to start...", False, 'left', ('Arial', 10, 'normal'))

def generate_food():
    # generate random locations of food

    global g_food_list

    x_list = [i for i in range(31,480,20)]      # available locations to put food
    y_list = [i for i in range(36,460,40)]      # to make sure every food item aligns well with the snake head

    for i in range(1, 10):                      # generate 9 food items as turtles, and name each by their values
    # change the range parameter changes the number of foods
        shuffle(x_list)
        shuffle(y_list)
        exec(f'''global g_food_turtle_{i}; \
            g_food_turtle_{i} = turtle.Turtle(); \
            g_food_turtle_{i}.hideturtle(); \
            g_food_turtle_{i}.up(); \
            g_food_turtle_{i}.goto(x_list.pop(0),y_list.pop(0)); \
            g_food_turtle_{i}.write(i, False, 'center', ('Arial', 15, 'normal')); \
            g_food_list.append(i);''')          # configure food items
        
def time_refresh():
    # refreshes time in status bar every 0.5 second
    
    global g_time
    global g_startup_time
    global g_snake_caught
    global g_player_wins

    g_time = int(time() - g_startup_time)
    display_status()
    
    if not g_snake_caught and not g_player_wins:
        g_screen.ontimer(time_refresh, 500)        # recursion

def move_snake_left():
    global g_motion
    g_motion = 'Left'
    display_status()

def move_snake_right():
    global g_motion
    g_motion = 'Right'
    display_status()

def move_snake_up():
    global g_motion
    g_motion = 'Up'
    display_status()

def move_snake_down():
    global g_motion
    g_motion = 'Down'
    display_status()

def pause_snake():
    global g_motion
    g_motion = 'Paused'
    display_status()

def snake_refresh():
    # refreshes the screen for every snake movement

    global g_motion
    global g_extend_tail_value
    global g_food_list
    global g_stamp_location_list
    global g_snake_caught
    global g_player_wins

    # if wins or loses stops refresh
    if g_snake_caught or g_player_wins:
        return 0

    # make the clone go to the same location as the snake
    g_snake_clone.goto(g_snake_turtle.position()[0], g_snake_turtle.position()[1])

    # set heading direction for snake and the clone
    if g_motion == 'Left':
        g_snake_turtle.setheading(180)
        g_snake_clone.setheading(180)
    elif g_motion == 'Right':
        g_snake_turtle.setheading(0)
        g_snake_clone.setheading(0)
    elif g_motion == 'Up':
        g_snake_turtle.setheading(90)
        g_snake_clone.setheading(90)
    elif g_motion == 'Down':
        g_snake_turtle.setheading(270)
        g_snake_clone.setheading(270)

    # use the clone to predict the next location of snake
    g_snake_clone.forward(20)       
    
    # avoids head-to-head crash with border; helped by the clone
    if g_snake_clone.position()[0] < 0 and g_motion == 'Left':
        pass
    elif g_snake_clone.position()[0] > 500 and g_motion == 'Right':
        pass
    elif g_snake_clone.position()[1] < 0 and g_motion == 'Down':
        pass
    elif g_snake_clone.position()[1] > 500 and g_motion == 'Up':
        pass
    elif g_motion == 'Paused':
        pass
    else:       # not head-to-head hitting border

        # use the clone to move tail and add stamp
        g_snake_clone.goto(g_snake_turtle.position()[0], g_snake_turtle.position()[1])      # clone go to the same location as the snake
        g_snake_clone.stamp()                                                               # add stamp to the last location of snake
        g_snake_turtle.forward(20)
        g_stamp_location_list.append(g_snake_turtle.position())
        
        # case snake contacts food
        for i in g_food_list:
            if eval(f'int(g_snake_turtle.distance(g_food_turtle_{i})) == 14'):              # the distance, when taking the integer part, is 14 when they overlap
                g_extend_tail_value += i
                g_food_list.remove(i)
                exec(f'g_food_turtle_{i}.clear()')

        # use the clone to extend tail
        if g_extend_tail_value == 0:
            g_snake_clone.clearstamps(1)
            g_stamp_location_list.pop(0)            # removes the earilest clone item
        else:
            g_extend_tail_value -= 1                # if the tail is to be extended, do not clear the stamp

    g_screen.update()
    g_screen.ontimer(snake_refresh, 350)            # change this to change snake's speed


def monster_refresh():
    # refreshes the screen for every monster movement

    global g_stamp_location_list
    global g_player_wins
    global g_snake_caught

    if g_player_wins or g_snake_caught:
        return 0

    angle = g_monster_turtle.towards(g_snake_turtle)        # angle between monster and snake
    if 0 <= angle <= 45 or 270 <= angle < 360:              # move right
        g_monster_turtle.setheading(0)
    elif 45 < angle < 135:                                  # move up
        g_monster_turtle.setheading(90)
    elif 135 <= angle <= 225:                               # move left
        g_monster_turtle.setheading(180)
    else:                                                   # move down
        g_monster_turtle.setheading(270)

    g_monster_turtle.forward(20)
    g_screen.update()

    if g_extend_tail_value > 0:
        g_screen.ontimer(monster_refresh, 850)              # when extending tail, slow down
    else:
        g_screen.ontimer(monster_refresh, randint(345, 600))    # move at variable speed
    # change the above to change monster's speed

def check_win_lose_contact():
    # check whether the player loses or monster is in contact with snake body
    # at a very high refresh rate, 0.05 seconds

    global g_snake_caught
    global g_contact
    global g_stamp_location_list
    global g_last_20_contact
    global g_player_wins

    # check whether the player wins
    if len(g_food_list) == 0:
        g_player_wins = True
        g_snake_turtle.write("\n\n   Winner!!\n  ", False, 'left', ('Arial', 15, 'bold'))

    # check whether snake is caught
    angle = radians(g_snake_turtle.towards(g_monster_turtle))
    degree_angle = g_snake_turtle.towards(g_monster_turtle)
    # make sure when the squares overlap, the snake is considered caught
    # using sine and cosine to help precisely check
    if 0 <= degree_angle <= 45 or 315 <= degree_angle < 360 or 135 <= degree_angle <= 225: 
        if abs(cos(angle) * g_snake_turtle.distance(g_monster_turtle)) <= 20:
            g_snake_caught = True
            g_monster_turtle.write('\n\n\n   Game Over!', False, 'left', ('Arial', 15, 'bold'))
            g_screen.update()
            return 0
    else:
        if abs(sin(angle) * g_snake_turtle.distance(g_monster_turtle)) <= 20:
            g_snake_caught = True
            g_monster_turtle.write('\n\n\n   Game Over!', False, 'left', ('Arial', 15, 'bold'))
            g_screen.update()
            return 0

    # examine contact with snake body
    contact_signal = False
    for i in range(len(g_stamp_location_list)):
        angle = radians(g_monster_turtle.towards(g_stamp_location_list[i]))     # angle between monster and each stamp
        degree_angle = g_monster_turtle.towards(g_stamp_location_list[i])       # the above angle in degrees
        # using sine and cosine to help precisely check
        if 0 <= degree_angle <= 45 or 315 <= degree_angle < 360 or 135 <= degree_angle <= 225: 
            if abs(cos(angle) * g_monster_turtle.distance(g_stamp_location_list[i])) <= 20:
                contact_signal = True
                g_last_20_contact.append(True)
                break
        else:
            if abs(sin(angle) * g_monster_turtle.distance(g_stamp_location_list[i])) <= 20:
                contact_signal = True
                g_last_20_contact.append(True)
                break

    if contact_signal:
        if g_last_20_contact.count(True) == 1:
            g_contact += 1
        g_last_20_contact.pop(0)
    else:
        g_last_20_contact.append(False)
        g_last_20_contact.pop(0)

    g_screen.ontimer(check_win_lose_contact, 50)        # 0.05s refresh rate


def game_module(x, y):      # the arguments here are just receives screen.onclick(), not used.
    global g_initiate_game_module
    global g_startup_time

    if g_initiate_game_module:
        g_startup_time = time()         # set startup time to current time
        g_message_turtle.clear()        # clear the startup message
        generate_food()

        # bind keystrokes to functions
        g_screen.onkey(move_snake_left, 'Left')
        g_screen.onkey(move_snake_right, 'Right')
        g_screen.onkey(move_snake_up, 'Up')
        g_screen.onkey(move_snake_down, 'Down')
        g_screen.onkey(pause_snake, 'space')

        # refresh time, snake, monster and check status
        g_screen.ontimer(time_refresh, 1000)
        g_screen.ontimer(snake_refresh, 400)
        g_screen.ontimer(monster_refresh, 550)
        g_screen.ontimer(check_win_lose_contact, 50)

        # avoid second-time screen click
        # this module is designed to only initiate once
        g_initiate_game_module = False
        

def main():
    # do preparations
    draw_border()
    set_turtles()
    display_status()
    display_startup_message()
    g_screen.update()

    # starts the game on click  
    g_screen.onclick(game_module)       
    g_screen.listen()
    g_screen.mainloop()


if __name__ == '__main__':
    main()