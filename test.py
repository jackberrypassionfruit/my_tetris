# from my_tetris import MyTetris

# falling_rocks = MyTetris()

# falling_rocks.release_the_blocks()
# falling_rocks.play_game()


# block_90 = []
# for col_index in range(len(block[0])):
#   new_row = ''.join([row[col_index] for row in block[::-1]])
#   block_90.append(new_row)

def rotate_block(block, clock_wise=True):
  clock_wise = 1 if clock_wise else -1
  return [ ''.join([ row[col_index] for row in block[::-1*clock_wise] ]) for col_index in range(len(block[0]))[::clock_wise] ]

block = [
        '@@@',
        '..@',
        '..@'
      ]

for row in block:
  print(row)
print()

block = rotate_block(block, clock_wise=True)

for row in block:
  print(row)
print()
  
block = rotate_block(block, clock_wise=False)
block = rotate_block(block, clock_wise=False)

for row in block:
  print(row)
print()

# """
# TODO
# 1. implement rotation controls
# 2. solved curses problem in the console after running this script
#   - the /r (carriage return) symbol is not applied correctly after running "curses.initscr().getkey()"
# 3. add a win/lose condition
#   - clear lines when full
# """