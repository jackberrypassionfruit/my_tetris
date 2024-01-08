from my_tetris import MyTetris

falling_rocks = MyTetris()

# falling_rocks.release_the_blocks()
falling_rocks.play_game()


# block = [ 
#         '@',
#         '@',
#         '@',
#         '@'
#       ]

# block_90 = []
# for col_index in range(len(block[0])):
#   new_row = ''.join([row[col_index] for row in block[::-1]])
#   block_90.append(new_row)


# for row in block:
#   print(row)
# print()

# block = [ ''.join([ row[col_index] for row in block[::-1] ]) for col_index in range(len(block[0])) ]

# for row in block:
#   print(row)
# print()
  
# block = [ ''.join([ row[col_index] for row in block ]) for col_index in range(len(block[0]))[::-1] ]
# block = [ ''.join([ row[col_index] for row in block ]) for col_index in range(len(block[0]))[::-1] ]


# for row in block:
#   print(row)
# print()

# """
# TODO
# 1. implement rotation controls
# 2. solved curses problem in the console after running this script
#   - the /r (carriage return) symbol is not applied correctly after running "curses.initscr().getkey()"
# 3. add a win/lose condition
#   - clear lines when full
# """