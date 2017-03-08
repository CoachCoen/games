raw_card_data = """
1:3 red:green
1:3 black:blue
1:3 blue:white
1:3 green:black
1:3 white:red

1:4 red:blue, 1
1:4 black:green, 1
1:4 blue:black, 1
1:4 green:green, 1
1:4 white:red, 1

1:1 green, 2 blue:red
1:1 red, 2 green:black
1:1 blue, 2 white:green
1:1 white, 2 black:blue
1:1 black, 2 red:white

1:2 blue, 2 black:white
1:2 white, 2 red:red
1:2 white, 2 green:black
1:2 blue, 2 red:green
1:2 green, 2 black:blue

1:1 blue, 2 red, 2 black:green
1:1 black, 2 white, 2 blue:black
1:1 green, 2 black, 2 white:red
1:1 white, 2 red, 2 green:blue
1:1 black, 2 blue, 2 green:white

1:1 blue, 1 red, 3 green:blue
1:1 white, 1 green, 3 blue:green
1:1 black, 1 green, 3 red:black
1:1 black, 1 blue, 3 white:white
1:1 white, 1 red, 3 black:red

1:1 red, 1 white, 1 blue, 1 black:green
1:1 green, 1 red, 1 white, 1 blue:black
1:1 black, 1 green, 1 red, 1 white:blue
1:1 blue, 1 black, 1 green, 1 red:white
1:1 white, 1 blue, 1 black, 1 green:red

1:1 red, 1 green, 1 white, 2 blue:black
1:1 red, 1 blue, 1 white, 2 black:green
1:1 red, 1 blue, 1 blue, 2 green:white
1:1 black, 1 blue, 1 green, 2 white:red
1:1 green, 1 white, 1 black, 2 red:blue

2:5 red:white, 2
2:5 black:red, 2
2:5 green:green, 2
2:5 white:black, 2
2:5 blue:blue, 2

2:6 red:red, 3
2:6 black:black, 3
2:6 green:green, 3
2:6 white:white, 3
2:6 blue:blue, 3

2:3 black, 5 red:white, 2
2:3 blue, 5 white:blue, 2
2:3 green, 5 blue:green, 2
2:3 white, 5 black:red, 2
2:3 red, 5 green:black, 2

2:1 green, 2 black, 4 red:white, 2
2:1 white, 2 green, 4 blue:red, 2
2:1 blue, 2 red, 4 green:black, 2
2:1 red, 2 white, 4 black:blue, 2
2:1 black, 2 blue, 4 white:green, 2

2:2 red, 3 blue, 3 black:red, 1
2:2 blue, 3 green, 3 black:blue, 1
2:2 white, 3 blue, 3 red:white, 1
2:2 black, 3 white, 3 green:black, 1
2:2 green, 3 white, 3 red:green, 1

2:2 red, 2 black, 3 green:white, 1
2:2 blue, 2 green, 3 red:blue, 1
2:2 white, 2 black, 3 blue:green, 1
2:2 white, 2 red, 3 black:red, 1
2:2 blue, 2 green, 3 white:black, 1

3:7 white:blue, 4
3:7 black:white, 4
3:7 blue:green, 4
3:7 green:red, 4
3:7 red:black, 4

3:3 white, 7 black:white, 5
3:3 blue, 7 white:blue, 5
3:3 black, 7 red:black, 5
3:3 red, 7 green:red, 5
3:3 green, 7 blue:green, 5

3:3 white, 3 red, 6 black:white, 5
3:3 green, 3 white, 6 blue:green, 5
3:3 black, 3 green, 6 red:black, 5
3:3 red, 3 blue, 6 green:red, 5
3:3 blue, 3 black, 6 white:blue, 5

3:5 black, 3 red, 3 black, 3 white:blue, 3
3:5 white, 3 red, 3 blue, 3 black:green, 3
3:5 red, 3 blue, 3 black, 3 green:white, 3
3:5 blue, 3 white, 3 black, 3 green:red, 3
3:5 green, 3 white, 3 red, 3 blue:black, 3
"""

raw_tile_data = """
4 blue, 4 green
4 white, 4 red
4 black, 4 red
4 green, 4 red
4 black, 4 green
4 white, 4 black
4 blue, 4 white
3 green, 3 blue, 3 red
3 blue, 3 green, 3 white
3 black, 3 red, 3 white
3 black, 3 red, 3 green
3 blue, 3 white, 3 red
3 black, 3 red, 3 blue
3 black, 3 white, 3 blue
"""
