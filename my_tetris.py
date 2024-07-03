import sys, time, curses

class MyTetris():
  def __init__(self):
    self.board_width = 10
    self.board_height = 20
    
    self.max_height = -1
    self.blocks = [
      ['@@@@'],
      [
        '.@.',
        '@@@',
        '.@.'
      ],
      # this next one is flipped because I'm storing the playfield upside down in memory
      [
        '@@@',
        '..@',
        '..@'
      ],
      [ 
        '@',
        '@',
        '@',
        '@'
      ],
      [
        '@@',
        '@@'
      ]
    ]
    
    self.hot_gas_index = 0
    self.feeld = ['.'*self.board_width for i in range(self.board_height)]
    self.block_carcasses = set()
    
  def __repr__(self):
    print('\n\r'*30)
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
          
          
          
    # return result
    return '\n\r'.join(reversed(result.split('\n\r')))+'\n\r' # (Un)Flip the image upside down
  
  def get_current_block_coords(self):  
    block_coords = set()
    for block_row_index, block_row in enumerate(self.current_block):
      for block_col_index, block_col in enumerate(block_row):
        if block_col != '.':
          new_block_spot_x, new_block_spot_y = self.current_loc
          new_block_spot_x += block_col_index
          new_block_spot_y += block_row_index
          block_coords.update([(new_block_spot_x, new_block_spot_y)])
    return block_coords
    
  def check_if_will_collide(self, dir):
    potential_collisions = set()
    current_block_coords = self.get_current_block_coords()
    # testing 
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
    rows_to_remove = []
    for row_index, row in enumerate(self.feeld):
      if '.' not in row:          
        rows_to_remove.append(row_index)
      
    for row_index in rows_to_remove:
      self.feeld = self.feeld[:row_index] + self.feeld[row_index + 1:] + ['.'*self.board_width]
      
      carcasses_in_this_row = [coord for coord in self.block_carcasses if coord[1] == row_index]
      for carcass in carcasses_in_this_row:
        self.block_carcasses.remove(carcass)
        
      carcasses_above_this_row = [coord for coord in self.block_carcasses if coord[1] > row_index]
      for carcass in carcasses_above_this_row:
        self.block_carcasses.remove(carcass)
        self.block_carcasses.update([(carcass[0], carcass[1]-1)])
  
  def stop_block(self):
    # This method takes the current state of the block, and turns it into block carcasses
    block_coords = self.get_current_block_coords()
    for coords in block_coords:
      coord_x, coord_y = coords
      self.feeld[coord_y] = self.feeld[coord_y][:coord_x] + '#' + self.feeld[coord_y][coord_x+1:]
    self.block_carcasses.update(block_coords)
    self.current_loc = [-1,-1]
    # TODO
    # create a function to find and remove all full rows
    self.remove_full_rows()
    # Return a value, max_height, which will be max(current_max_height, max_height_of_this_dead_block)
    return max(self.max_height, max([block_coord[1] for block_coord in block_coords]))
  
  def hot_gas(self, dir):
    match dir:
      case '<':
        if self.current_loc[0] > 0:
          self.current_loc[0] -= 1
      case '>':
        coord_right = self.current_loc[0] + len(self.current_block[0])
        if coord_right < len(self.feeld[0]):
          self.current_loc[0] += 1
        
  def rotate_block(self, block, clock_wise=True):
    clock_wise = 1 if clock_wise else -1
    return [ ''.join([ row[col_index] for row in block[::-1*clock_wise] ]) for col_index in range(len(block[0]))[::clock_wise] ]

  def block_fall_down(self, play_game):
    dir = None
    while self.current_loc != [-1, -1]:
      # move left or right, depending on wind instruction
      if dir != '^':
        dir = None
        while not dir:
          match curses.initscr().getkey():
            case 'a':
              dir = '<'
            case 's':
              dir = 'V'
            case 'd':
              dir = '>'
            case 'w':
              dir = '^'
            case 'q':
              self.current_block = self.rotate_block(self.current_block, clock_wise=False)
              print(self)
              print(f'self.current_loc: {self.current_loc}\r')
            case 'e':
              self.current_block = self.rotate_block(self.current_block, clock_wise=True)
              print(self)
              print(f'self.current_loc: {self.current_loc}\r')
            case _:
              pass
      if not self.check_if_will_collide(dir) and dir in ['<', '>']:
        self.hot_gas(dir)      
      if self.current_loc[1] == 0 or self.check_if_will_collide('V'):
        self.max_height = self.stop_block()
      else:
        self.current_loc[1] -= 1
      print(self)
      print(f'self.current_loc: {self.current_loc}\r')
      if not play_game:
        time.sleep(.25)
      
  def release_block(self, play_game = False):
    current_block_height = len(self.current_block)
    self.current_loc = [self.board_width//2, self.board_height - current_block_height]
    self.block_fall_down(play_game=play_game)    
    
  def release_the_blocks(self):
    for i in range(2022):
      self.block_index = i % len(self.blocks)
      
      self.release_block(play_game = False)
    print('max_height: ', self.max_height)
    
    
  def play_game(self):
    i = 0
    while True:
      self.block_index = i % len(self.blocks)
      self.current_block = self.blocks[self.block_index]
      self.release_block(play_game = True)
      i += 1