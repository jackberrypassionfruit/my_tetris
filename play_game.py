from my_tetris import MyTetris
import curses

falling_rocks = MyTetris()

try:
  falling_rocks.play_game()
except Exception as e:
  curses.endwin()
  print(e)
except:
  curses.endwin()


# """
# TODO
# 1. implement rotation controls
#   - does not occur about center, which is awkward
#   - can put blocks out of the right bounds, which is incorrect
# 2. add a win/lose condition
# """

# block_90 = []
# for col_index in range(len(block[0])):
#   new_row = ''.join([row[col_index] for row in block[::-1]])
#   block_90.append(new_row)
