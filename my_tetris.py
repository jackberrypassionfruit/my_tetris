import sys, curses, time

class MyTetris():
  def __init__(self):
    with open(sys.argv[1], 'r', encoding='utf8') as infile:
      jet_push_text = infile.read()
    self.hot_gas_movement = list(''.join(jet_push_text.split('\n')))
    
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
      
    self.feeld = '''\
.......
.......
.......
.......\
'''.split('\n')

    self.block_carcasses = set()
    
  def __repr__(self):
    result = ''
    for line_index, line in enumerate(self.feeld):
      block_row = line_index - self.current_loc[1]
      # if self.current_loc == [-1,-1], then yet to drop a new block
      if self.current_loc != [-1, -1] and 0 <= block_row < len(self.blocks[self.block_index]):
        block_line = ''
        for col_index, col in enumerate(self.feeld[0]):
          block_col = col_index - self.current_loc[0]
          if self.current_loc[0] <= col_index < self.current_loc[0] + len(self.blocks[self.block_index][block_row]):
            block_row_col = self.blocks[self.block_index][block_row][block_col]
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
    return '\n\r'.join(reversed(result.split('\n\r'))) # (Un)Flip the image upside down
  
  def get_current_block_coords(self):  
    block_coords = set()
    for block_row_index, block_row in enumerate(self.blocks[self.block_index]):
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
  
  def stop_block(self):
    # This method takes the current state of the block, and turns it into block carcasses
    block_coords = self.get_current_block_coords()
    for coords in block_coords:
      coord_x, coord_y = coords
      self.feeld[coord_y] = self.feeld[coord_y][:coord_x] + '#' + self.feeld[coord_y][coord_x+1:]
    self.block_carcasses.update(block_coords)
    self.current_loc = [-1,-1]
    # Return a value, max_height, which will be max(current_max_height, max_height_of_this_dead_block)
    return max(self.max_height, max([block_coord[1] for block_coord in block_coords]))
  
  def hot_gas(self, dir):
    match dir:
      case '<':
        if self.current_loc[0] > 0:
          self.current_loc[0] -= 1
      case '>':
        coord_right = self.current_loc[0] + len(self.blocks[self.block_index][0])
        if coord_right < len(self.feeld[0]):
          self.current_loc[0] += 1
        
  
  def block_fall_down(self, play_game):
    dir = None
    while self.current_loc != [-1, -1]:
      # move left or right, depending on wind instruction
      if dir is not '^':
        if play_game:
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
              case _:
                pass
        else:
          dir = self.hot_gas_movement[self.hot_gas_index]
          self.hot_gas_index = (self.hot_gas_index + 1) % len(self.hot_gas_movement)
      if not self.check_if_will_collide(dir) and dir in ['<', '>']:
        self.hot_gas(dir)
      # print('\n'*30)
      # print(self)
      # print('self.current_loc: ', self.current_loc)
      # print('dir: ', dir)
      # print('self.hot_gas_index: ', self.hot_gas_index)
      # time.sleep(.25)
      
      if self.current_loc[1] == 0 or self.check_if_will_collide('V'):
        self.max_height = self.stop_block()
      else:
        self.current_loc[1] -= 1
      print('\n\r'*30)
      print(self)
      print('self.current_loc: ', self.current_loc)
      if not play_game:
        time.sleep(.25)
      
  def release_block(self, play_game = False):
    current_block_height = len(self.blocks[self.block_index])
    self.feeld += ['.......'] * (current_block_height)
    self.current_loc = [2, self.max_height + 4]
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
      self.release_block(play_game = True)
      i += 1