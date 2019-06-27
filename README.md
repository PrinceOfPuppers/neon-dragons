# snake-360
A 2 player game I made similar to slither.io, (only realized the similarity after I started making it)

Playing The Game
----------------
Click snakes to start

Controls:

    player 1 uses WASD, player 2 use arrow keys

    A/LeftArrow to move left
    D/RightArrow to move right

    W/UpArrow to dash forward


Goal:

    the goal of the game is currently to be the last person alive, you die by having your snake
    drop below 3 dots in length.

    In the future I plan to have the games time out after 5 or so minutes and state the winner 
    as the person with the longest snake


GamePlay:

    You can shorten you apponent by eating their segments (running your head into their body), 
    just be careful go for their first segment or you will mutually eat eachother.

    You can pick up orbs to increase or decrease your length; green increases, red decreases. 
    the more green/ red the orb, the greater the change.

----------------



Devlopment Goals
----------------

-clean and expand upon player constructor, allowing for more control over spawning characteristics 
(ie set locaiton and initial rotation and have the snake form properly in that direction)

-have config only created in main (proper main) function and passed to functions that need it 

-simplify and refactor main

-add particle effect on dead and on head change

-maybe have game pause on dead for a second when displaying particles

-have cut off segments drop an orb proportional to how many segments where cut off 

-add different head for player 2

-changing player tail based on length, similar to the heads

-change name of project to somthing more suitable

-improve preformance of dashing 

----------------


