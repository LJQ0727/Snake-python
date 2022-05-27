# Design Doc  
#### Jiaqi Li &nbsp; 120090727  &nbsp;   School of Data Science  
  
## Overview
- This program is a Snake Game using Python GUI (turtle graphics). The game is composed of 3 main types of object: a snake, a monster and 9 food items. In the game, the player is going to use the 4 arrowkeys on the keyboard to move the snake, avoid hitting the monster and try to consume all food items on the canvas.  
- The snake's body grows by the size equal to the value of food item it consumes.   
- The player wins the game when his snake eats all the food without being captured by the monster, otherwise he loses. Further, the snake moves at a variable speed and its speed dramatically decreases when the body is extending. 

## Data Model
My program contains these global variables:  
- a `Screen` object to setup window size, coordinates and loop itself to react to mouse click and keystrokes
- 4 global `Turtle` objects for graphically displaying the game status, welcome message, the snake and the monster
- `integer` variables `g_contact` `g_extend_tail_value` and `g_time` to store the monster's contact time with snake body, how many tails the snake should expand, and the elapsed time
- `string` variable `g_motion` to store the current motion of the snake
- `bool` variables `g_initiate_game_module`, `g_snake_caught` and  `g_player_wins` to give signals to the program
- `list` variable `g_last_20_contact`, stores whether last 20 times refresh are considered as contact; is used to avoid continuous contacts, at default, it's [False] * 20
- `list` variable `g_food_list` stores all remaining food items in integer, e.g. [1,2,3,4]
- The tails of the snake are achieved using `stamp()`. `List` variable `g_stamp_location_list` stores all stamp (tail) locations, e.g. [(0,0), (200,200)]

## Program Structure  
Each function in this program is regarded as a component and serves one purpose.  
The functions' roles are concisely stated in their names.
- The `main()` function is the highest in status. 
  - It calls `draw_border()`, `set_turtles()`, `display_status()`, `display_startup_message()` to first set the screen components ready. 
  - Then when screen is on click, starts the `game_module()` function.
-  The `game_module()` inside `main()` basically contains all configurations of the snake game. 
   -  It first calls `generate_food()` to generate randomized food items on the canvas. 
   -  Then it uses `onkey()` to bind keystrokes `'Left'`, `'Right'`, `'Up'`, `'Down'`, `'space'` to event handler functions. 
   -  It then uses `ontimer()` to refresh the screen along with object movements on the screen. Including: `time_refresh()`, `snake_refresh()`, `monster_refresh()`, `check_win_lose_contact()`
   -  The `time_refresh()`, `snake_refresh()`, `monster_refresh()`, `check_win_lose_contact()` functions are the most important in this program. They use **recursion** to achieve loop. Every movement of the snake and monster, the change of time, the constant check of winning or losing, are achieved when refreshed.

## Processing Logic
> The logic to motion the snake and monster
- Use `snake_refresh()` function to motion the snake.
  - > The checking process
    - The check of whether the player has won or lost is left in the `check_win_lose_contact()` function, because that function has higher refresh rate (0.05s) and will be more accurate.
    - It makes predictions of the snake path to avoid head-to-head crash with the border. Achieved by making `g_snake_clone`, the clone of snake go one step further. If it exceeds the border, the snake won't move but `g_motion` will still be the player's last command.
    - It then checks whether the snake contacts food, by evaluating its distance to every food item.
  - > The moving snake and tail process
    - It sets the heading directions of `g_snake_turtle` according to `g_motion`
    - Let the tail move along with the snake by removing the earliest placed tail (stamp), and then stamp at the current location of `g_snake_turtle`.
    - Ultimately, the snake moves by calling `forward()` function, then update the screen
    - Recursion (calling itself at `ontimer(350)`)
- Use `monster_refresh()` to motion the monster.
  - > The moving process
    - In order to let the monster move in the closest way to the snake, check the angle between monster and snake using `towards()`
    - Set different heading directions according to the angle using `setheading()`, then `forward()`
    - Achieve variable speed by setting the recursion `ontimer()` in a random time
> The logic to extend the tail
  - If the tail needs to be extended (`g_extend_tail_value != 0`), then do not remove the earliest placed tail (stamp), and make `g_extend_tail_value -= 1`
  - In this way, the tail isn't "extending" at the end of the body, instead it's "extending" at the head.
> The logic to detect body contact between the snake and the monster
- Use `check_win_lose_contact()` function to check.
- > Checking contact
  - I used a `g_stamp_location_list` to save all locations of current stamps
  - Checks the monster's distance to every stamp using `distance()` method.
  - For any one of the distance, they're checked whether having contact with the monster.
    - In order to garantee precise check for 2 squares, I used the angle between them and sine and cosine functions to help the check.
    - In order to **make coninuous overlapping be regarded as only one contact**, I saves the recent 20 contact histories (1 second). Only when the contact occurs the first time in 1 second can it be regarded as a new contact.
- > Checking win or lose
  - The player wins if there's no remaining item in the `g_food_list`
  - The player loses when the 2 squares (monster and snake) are checked to be overlapping
  - In order to garantee precise check for 2 squares, I used the angle between them and **sine and cosine functions** to help the check. As depicted in picture.

## Function Specs
My program contians these functions handling different jobs:  
- Function1: `set_turtles()`:
  - Set properties of turtles
  - No parameter, returns `None`
- Function2: `draw_border()`:
  - Display motion area and status bar borders
  - Using the `border_turtle`
  - No parameter, returns `None`
- Function3: `display_status()`:
  - Displays status bar information
  - Including contact, time and motion
  - No parameter, returns `None`
- Function4: `generate_food()`:
  - Generate random locations of food
  - and make sure every food item aligns well with the snake head, by restricting their locations to specific pixels
  - Every food item is one turtle, named with their values `g_food_turtle_1`, `g_food_turtle_2` and so on
  - No parameter, returns `None`
- Functions: `move_snake_left()`, `move_snake_right()`, `move_snake_up()`, `move_snake_down()` and `pause_snake()`:
  - Act as event handlers
  - Bound to `onkey()` methods of `Screen()`
  - No parameter, returns `None`
- Function: `snake_refresh()`:
  - Refreshes the screen for every snake movement
  - Before making movement, checks whether the snake contacts food, avoids head-to-head crash with the border
  - Checks if the player has already won or lost by refering to `g_snake_caught()` and whether the length of `g_food_list` is 0. If so, ends the recursion.
  - It then makes predictions of the snake path to avoid head-to-head crash with the border. Achieved by making `g_snake_clone`, the clone of snake go one step further. If it exceeds the border, `g_motion` is set to `Paused`.
  - It then checks whether the snake contacts food, by evaluating its distance to every food item.
  - It sets the heading directions of `g_snake_turtle` according to `g_motion`
  - Let the tail move along with the snake by removing the earliest placed tail (stamp), and then stamp at the current location of `g_snake_turtle`.
  - Ultimately, the snake moves by calling `forward()` function, then updat the screen
  - Recursion (calling itself at `ontimer(350)`)
  - No parameter, returns `None`
- Function: `monster_refresh()`:
  - Refreshes the screen for every monster movement
  - Set different heading directions according to the angle using `setheading()`, then `forward()`
  - Achieve variable speed by setting the recursion `ontimer()` in a random time
  - No parameter, returns `None`
- Function: `check_win_lose_contact()`:
  - Checks whether the player has won or lost. The player wins if there's no remaining item in the `g_food_list`. The player loses when the 2 squares (monster and snake) are checked to be overlapping
  - In order to garantee precise check for 2 squares, I used the angle between them and **sine and cosine functions** to help the check.
  - For every stamp location, check whether the monster has contact with snake body. Stamp locations are already saved in `g_stamp_location_list`
  - Recursion using `ontimer(50)`
  - No parameter, returns `None`
- Remaining functions: `game_module()` and `main()`:
  - The game_module function contains all configurations of the game, calls functions to manipulate time, snake, monster, judges win or los; the main function calls it, plus some other setups

## Function Output
    