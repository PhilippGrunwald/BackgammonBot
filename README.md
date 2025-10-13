A simple PyGame application to play Backgammon against a Bot.

## The Bot
Thinks one turn of each player ahead using an ExpectiMax algorithm and a carefully created evaluation function. Surprinsingly, this simple Bot is already quite capable of playing a reasonable strong game.

*This Application was a toy project to avoid the bad wheather outside during vacation*

## Further Improvements
To obtain a much deeper search, one needs to improve the efficiency of the code a lot. Backgammon is a game, where equal states arise quite often in the Expectimax search, thus one obvious way to improve the bots performance is to introduce [*Zobrist hashing*](https://en.wikipedia.org/wiki/Zobrist_hashing).
The move generation can be improved further and all computationally heavy parts should be done by some compiled language like c++.
