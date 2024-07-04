from my_tetris import MyTetris
import curses, sys

falling_rocks = MyTetris()

# block = falling_rocks.blocks[0]
# for line in block:
#   print(line)

# print()
# rotated_block = falling_rocks.rotate_block(block)

# for line in rotated_block:
#   print(line)

# sys.exit()
try:
  falling_rocks.play_game()
except Exception as e:
  curses.endwin()
  print(e)
except:
  curses.endwin()
