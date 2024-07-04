import sys, os, time, curses, time, threading, random

class MyTetris():
  def __init__(self):
    self.board_width = 10
    self.board_height = 20
    self.game_over = False
    self.cleared_rows = 0
    self.max_cleared_rows = 100
    self.game_step_interval = 1
    
    self.blocks = [
      [
        '.....',
        '.....',
        '@@@@@',
        '.....',
        '.....'
      ],
      [
        '...',
        '@@@',
        '@..',
      ],
      [
        '...',
        '@@@',
        '.@.',
      ],
      [
        '@@.',
        '.@@',
      ]
    ]
    self.next_block = random.choice(self.blocks)

    
    self.block_index = 0
    self.feeld = ['.' * self.board_width for i in range(self.board_height)]

    # Add walls and ground to carcasses. Those will be the bounds
    floor_carcasses = set([(x, -1) for x in range(self.board_width)])
    self.block_carcasses = floor_carcasses
    left_wall_carcasses =  set([(-1,               y) for y in range(self.max_cleared_rows)]) # make it big just so we don't run out..
    self.block_carcasses = self.block_carcasses.union(left_wall_carcasses)
    right_wall_carcasses = set([(self.board_width, y) for y in range(self.max_cleared_rows)]) # clear too many...congrats you won!
    self.block_carcasses = self.block_carcasses.union(right_wall_carcasses)
    
  def __repr__(self):
    print('\n\r'*(self.board_height+10))
    result = ''
    for line_index, line in enumerate(self.feeld):
      block_row = line_index - self.current_loc[1]
      # if self.current_loc == [-1,-1], then about to drop a new block
      if self.current_loc != [-1, -1] and 0 <= block_row < len(self.current_block):
        block_line = ''
        for col_index, col in enumerate(self.feeld[0]):
          block_col = col_index - self.current_loc[0]
          if self.current_loc[0] <= col_index < self.current_loc[0] + len(self.current_block[block_row]):
            block_row_col = self.current_block[block_row][block_col]
            if block_row_col == '@':
              block_line += block_row_col
            else:
              block_line += line[col_index]
          else:
            block_line += line[col_index]
        result += f'{block_line}\n\r'
      else:
        result += f'{line}\n\r'
        
    print(f'Cleared Rows: {self.cleared_rows}', end='\n\r\n\r')    
    
    print('Next Block:\r')
    for row in self.next_block[::-1]:
      print(f"{row}", end='\n\r')
      
          
    # return result # Image not flipped
    return '\n\r'.join(reversed(result.split('\n\r')))+'\n\r' # (Un)Flip the image upside down
  
  def get_block_coords(self, block=None):  
    block_coords = set()
    for block_row_index, block_row in enumerate(block):
      for block_col_index, block_col in enumerate(block_row):
        if block_col != '.':
          new_block_spot_x, new_block_spot_y = self.current_loc
          new_block_spot_x += block_col_index
          new_block_spot_y += block_row_index
          block_coords.update([(new_block_spot_x, new_block_spot_y)])
    return block_coords
    
  def check_if_will_collide(self, dir):
    potential_collisions = set()
    current_block_coords = self.get_block_coords(block=self.current_block)
    for block_spot in current_block_coords:
      collision_spot_x, collision_spot_y = block_spot
      match dir:
        case 'V':
          collision_spot_y -= 1
        case '<':
          collision_spot_x -= 1
        case '>':
          collision_spot_x += 1
      potential_collisions.update([(collision_spot_x, collision_spot_y)])
    return potential_collisions.intersection(self.block_carcasses)
  
  def remove_full_rows(self):
    found_row_to_remove = True
    while found_row_to_remove:
      found_row_to_remove = False
      for row_index, row in enumerate(self.feeld):
        if '.' not in row:
          self.feeld = self.feeld[:row_index] + self.feeld[row_index + 1:] + ['.'*self.board_width]
        
          carcasses_in_this_row = [coord for coord in self.block_carcasses if coord[1] == row_index and -1<coord[0]<self.board_width]
          for carcass in carcasses_in_this_row:
            self.block_carcasses.remove(carcass)
          
          carcasses_above_this_row = [coord for coord in self.block_carcasses if coord[1] > row_index and -1<coord[0]<self.board_width]
          for carcass in carcasses_above_this_row:
            self.block_carcasses.remove(carcass)
            self.block_carcasses.update([(carcass[0], carcass[1]-1)])
            
          self.cleared_rows += 1
          found_row_to_remove = True
          break # out of for loop
      
  def stop_block(self):
    ''' 
    This method takes the current state of the block, and turns it into block carcasses
    '''
    self.block_index += 1
    self.game_step_interval -= 0.01
    
    block_coords = self.get_block_coords(block=self.current_block)
    for coord_x, coord_y in block_coords:
      self.feeld[coord_y] = self.feeld[coord_y][:coord_x] + '#' + self.feeld[coord_y][coord_x+1:]
    self.block_carcasses.update(block_coords)
    self.current_loc = [-1,-1]
    self.remove_full_rows()

  def reset_block(self):    
    self.current_block = self.next_block
    current_block_height = len(self.current_block)
    self.current_loc = [self.board_width//2, self.board_height - current_block_height]
    
    block_choices = self.blocks[:]
    block_choices.remove(self.current_block)
    self.next_block = random.choice(block_choices)
        
  def rotate_block(self, block, clock_wise=True):
    clock_wise = 1 if clock_wise else -1
    return [ ''.join([ row[col_index] for row in block[::clock_wise] ]) for col_index in range(len(block[0]))[::-1*clock_wise] ]

  def release_new_block(self):
    self.reset_block()
    
    dir = None
    while self.current_loc != [-1, -1]:
      if dir != '^':
        dir = None
        while not dir:
          key_press = curses.initscr().getkey()
          match key_press:
            case 'a' | curses.KEY_LEFT:
              dir = '<'
            case 's':
              dir = 'V'
            case 'd' | curses.KEY_RIGHT:
              dir = '>'
            case 'w':
              dir = '^'
              
            case 'q' | 'e':
              rotated_block = self.rotate_block(self.current_block, clock_wise = key_press=='e')
              rotated_block_coords = self.get_block_coords(rotated_block)
              if not rotated_block_coords.intersection(self.block_carcasses):
                self.current_block = rotated_block
              print(self)
            case _:
              pass
      
      if dir in ['<', '>'] and not self.check_if_will_collide(dir):
        match dir:
          case '<':
            self.current_loc[0] -= 1
          case '>':
            self.current_loc[0] += 1
      
      elif self.check_if_will_collide('V'):
        self.stop_block()
      
      else:
        self.current_loc[1] -= 1
              
      print(self)
    
  def game_timer(self):
    while self.game_over == False:
      time.sleep(self.game_step_interval)
      if self.check_if_will_collide('V'):          
        self.stop_block()
        self.reset_block()
        
      else:
        self.current_loc[1] -= 1
      print(self)
    
  def play_game(self):
    
    print('''\
Controls:
          
Rotate:
  Counterclockwise:   Q
  Clockwise:          E

Left/Right:           A/D
Slam to Bottom:       W
Move Down by One(1):  S

To Quit:              Ctrl + C
''')
    input('Ready to start? Hit ENTER:\n')
    
    threading.Thread(target=self.game_timer, daemon=True).start() # daemon=True makes it so thread quits when program does
    
    try:
      while self.block_index < self.max_cleared_rows:
        self.release_new_block()
    except Exception as e:
      curses.endwin()
      print(e)
      sys.exit()
    except KeyboardInterrupt:
      curses.endwin()
      sys.exit()
      
    print('Woah, somebody actually won.', end='\n\r')
    input('Click any button to quit')
    sys.exit()
    
    
if __name__ == "__main__":
  falling_rocks = MyTetris()
  
  falling_rocks.play_game()