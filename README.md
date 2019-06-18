# snake-360
A 2 player game I made similar to slither.io, (only realized the similarity after I started making it)

Playing The Game
----------------
Controls:
    player 1 uses WASD, player 2 use arrow keys

    A/LeftArrow to move left
    D/RightArrow to move right

    W/UpArrow to dash forward


Goal:
    the goal of the game is currently to be the last person alive, you die by having your snake
    drop below 3 dots in length.

    In the future I plan to have the games time out after 5 or so minutes and state the winner as the person with the longest snake


GamePlay:
    You can shorten you apponent by eating their segments (running your head into their body), just be careful go for their
    first segment or you will mutually eat eachother.

    You can pick up orbs to increase or decrease your length; green increases, red decreases. the more green/ red the orb, the greater the change.
----------------



Devlopment Goals
----------------
-refactor code to have a cleaner main file, as well as adding a proper main function

-improve look of snakes by having the segments be circles rather than lines, current apperence is for easier debugging 

-add screen wrapping to snakes, current hurtle is with making this work with the collision detection

-adding menu and win/replay screen

-adding orb that changes the speed and potentially the turning speed of the snakes

-have cut off segments drop an orb proportional to how many segments where cut off 

-add monitor resolution option in menu 
----------------


