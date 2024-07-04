import sys, time, curses, time, threading

class MyTetris():
  def __init__(self):
    self.board_width = 10
    self.board_height = 20
    self.game_over = False
    
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
    self.block_index = 0
    self.feeld = ['.' * self.board_width for i in range(self.board_height)]

    # Add walls and ground to carcasses. Those will be the bounds
    floor_carcasses = set([(x, -1) for x in range(self.board_width)])
    self.block_carcasses = floor_carcasses
    left_wall_carcasses =  set([(-1,               y) for y in range(100)]) # make it big just so we don't run out..
    self.block_carcasses = self.block_carcasses.union(left_wall_carcasses)
    right_wall_carcasses = set([(self.board_width, y) for y in range(100)]) # clear too many...congrats you won!
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
          found_row_to_remove = True
          break # out of for loop
      
  def stop_block(self):
    ''' 
    This method takes the current state of the block, and turns it into block carcasses
    '''
    block_coords = self.get_block_coords(block=self.current_block)
    for coord_x, coord_y in block_coords:
      self.feeld[coord_y] = self.feeld[coord_y][:coord_x] + '#' + self.feeld[coord_y][coord_x+1:]
    self.block_carcasses.update(block_coords)
    self.current_loc = [-1,-1]
    self.remove_full_rows()
        
  def rotate_block(self, block, clock_wise=True):
    clock_wise = -1 if clock_wise else 1
    # Holy Shit
    return [ ''.join([ row[col_index] for row in block[::-1*clock_wise] ]) for col_index in range(len(block[0]))[::clock_wise] ]

  def block_fall_down(self):
    dir = None
    while self.current_loc != [-1, -1]:
      if dir != '^':
        dir = None
        while not dir:
          key_press = curses.initscr().getkey()
          match key_press:
            case 'a':
              dir = '<'
            case 's':
              dir = 'V'
            case 'd':
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
      
      if self.check_if_will_collide('V'):
        self.stop_block()
      
      else:
        self.current_loc[1] -= 1
        
        
      
      # if self.check_if_will_collide('V'):
      #   self.stop_block()
      #   self.remove_full_rows()
      
      # if dir in ['<', '>', 'V'] and not self.check_if_will_collide(dir):
      #   if dir in ['<', '>']:
      #     match dir:
      #       case '<':
      #         self.current_loc[0] -= 1
      #       case '>':
      #         self.current_loc[0] += 1
      #   elif dir == 'V':
      #     self.current_loc[1] -= 1
      
      # else:
      #   self.current_loc[1] -= 1
              
              
      print(self)
      print(f'self.current_loc: {self.current_loc}\r')
      
  def release_block(self):
    current_block_height = len(self.current_block)
    self.current_loc = [self.board_width//2, self.board_height - current_block_height]
    self.block_fall_down()
    
  def game_timer(self):
    try:
      while self.game_over == False:
        time.sleep(1)
        if self.check_if_will_collide('V'):
          self.stop_block()
          
          self.block_index = self.block_index % len(self.blocks)
          self.current_block = self.blocks[self.block_index]
        else:
          self.current_loc[1] -= 1
        print(self)
        print(f'self.current_loc: {self.current_loc}\r')
    except Exception as e:
      print(e)
    
  def play_game(self):
    threading.Thread(target=self.game_timer).start()
    
    while self.block_index < 100:
      self.block_index = self.block_index % len(self.blocks)
      self.current_block = self.blocks[self.block_index]
      self.release_block()
      self.block_index += 1
      
    print('Woah, somebody actually won.\r')
    input('Click any button to quit')
    sys.exit()