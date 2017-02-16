from enum import Enum

# TODO Find a better home for this
class ChipType(Enum):
    green_emerald = 1
    blue_sapphire = 2
    red_ruby = 3
    white_diamond = 4
    black_onyx = 5
    yellow_gold = 6


row_1 = """
3 red: 1 green
3 black: 1 blue
3 blue: 1 white
3 green: 1 black
3 white: 1 red

4 red: 1 blue, 1 point
4 black: 1 green, 1 point
4 blue: 1 black, 1 point
4 green: 1 green, 1 point
4 white: 1 red, 1 point

1 green, 2 blue: 1 red
1 red, 2 green: 1 black
1 blue, 2 white: 1 green
1 white, 2 black: 1 blue
1 black, 2 red: 1 white

2 blue, 2 black: 1 white
2 white, 2 red: 1 red
2 white, 2 green: 1 black
2 blue, 2 red: 1 green
2 green, 2 black: 1 blue

1 blue, 2 red, 2 black: 1 green
1 black, 2 white, 2 blue: 1 black
1 green, 2 black, 2 white: 1 red
1 white, 2 red, 2 green: 1 blue
1 black, 2 blue, 2 green: 1 white

1 blue, 1 red, 3 green: 1 blue
1 white, 1 green, 3 blue: 1 green
1 black, 1 green, 3 red: 1 black
1 black, 1 blue, 3 white: 1 white
1 white, 1 red, 3 black: 1 red

1 red, 1 white, 1 blue, 1 black: 1 green
1 green, 1 red, 1 white, 1 blue: 1 black
1 black, 1 green, 1 red, 1 white: 1 blue
1 blue, 1 black, 1 green, 1 red: 1 white
1 white, 1 blue, 1 black, 1 green: 1 red

1 red, 1 green, 1 white, 2 blue: 1 black
1 red, 1 blue, 1 white, 2 black: 1 green
1 red, 1 blue, 1 blue, 2 green: 1 white
1 black, 1 blue, 1 green, 2 white: 1 red
1 green, 1 white, 1 black, 2 red: 1 blue
"""

row_2 = """
5 red: 1 white, 2 points
5 black: 1 red, 2 points
5 green: 1 green, 2 points
5 white: 1 black, 2 points
5 blue: 1 blue, 2 points

6 red: 1 red, 3 points
6 black: 1 black, 3 points
6 green: 1 green, 3 points
6 white: 1 white, 3 points
6 blue: 1 blue, 3 points

3 black, 5 red: 1 white, 2 points
3 blue, 5 white: 1 blue, 2 points
3 green, 5 blue: 1 green, 2 points
3 white, 5 black: 1 red, 2 points
3 red, 5 green: 1 black, 2 points

1 green, 2 black, 4 red: 1 white, 2 points
1 white, 2 green, 4 blue: 1 red, 2 points
1 blue, 2 red, 4 green: 1 black, 2 points
1 red, 2 white, 4 black: 1 blue, 2 points
1 black, 2 blue, 4 white: 1 green, 2 points

2 red, 3 blue, 3 black: 1 red, 1 point
2 blue, 3 green, 3 black: 1 blue, 1 point
2 white, 3 blue, 3 red: 1 white, 1 point
2 black, 3 white, 3 green: 1 black, 1 point
2 green, 3 white, 3 red: 1 green, 1 point

2 red, 2 black, 3 green: 1 white, 1 point
2 blue, 2 green, 3 red: 1 blue, 1 point
2 white, 2 black, 3 blue: 1 green, 1 point
2 white, 2 red, 3 black: 1 red, 1 point
2 blue, 2 green, 3 white: 1 black, 1 point
"""

row_3 = """
7 white: 1 blue, 4 points
7 black: 1 white, 4 points
7 blue: 1 green, 4 points
7 green: 1 red, 4 points
7 red: 1 black, 4 points

3 white, 7 black: 1 white, 5 points
3 blue, 7 white: 1 blue, 5 points
3 black, 7 red: 1 black, 5 points
3 red, 7 green: 1 red, 5 points
3 green, 7 blue: 1 green, 5 points

3 white, 3 red, 6 black: 1 white, 5 points
3 green, 3 white, 6 blue: 1 green, 5 points
3 black, 3 green, 6 red: 1 black, 5 points
3 red, 3 blue, 6 green: 1 red, 5 points
3 blue, 3 black, 6 white: 1 blue, 5 points

5 black, 3 red, 3 black, 3 white: 1 blue, 3 points
5 white, 3 red, 3 blue, 3 black: 1 green, 3 points
5 red, 3 blue, 3 black, 3 green: 1 white, 3 points
5 blue, 3 white, 3 black, 3 green: 1 red, 3 points
5 green, 3 white, 3 red, 3 blue: 1 black, 3 points
"""

raw_starter_decks = {
    0: row_1,
    1: row_2,
    2: row_3
}
