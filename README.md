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
-change config to yaml

-refactor code to have a cleaner main file, as well as adding a proper main function

-add insta-death to snakes that stray off screen

-fix logic for determining which head is used

-add in self intersection and eating

-adding menu and win/replay screen

-have cut off segments drop an orb proportional to how many segments where cut off 

-add monitor resolution option in menu

-greatly increase hitbox of orbs

-change appearence of orbs (have it be seperate from the hitbox size)

-add different head for player 2

-changing player tail based on length, similar to the heads

-change name of project to somthing more suitable
----------------


