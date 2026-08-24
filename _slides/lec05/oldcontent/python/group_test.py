#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import random
import math
import sys

from fleet import *

testfleet = battleship_fleet()
testfleet.scatter()

all_algorithms = []
all_group_name = []

def sink_algorithm(board_state, _fleet, x1, y1):
  new_targets = []

  fleet_matrix = _fleet.fleet2matrix()

  # iterate through the adjacent squares
  for [dx,dy] in [[1,0],[0,1],[0,-1],[-1,0]]:
    if _fleet._ships[_fleet._index[fleet_matrix[x1,y1]]]._sunk:
      break
    x = x1+dx
    y = y1+dy
    # continue in direction until miss or no more board or ship sunk
    go_immediately_to_opposite = False
    for n in range(10):
      if _fleet._ships[_fleet._index[fleet_matrix[x1,y1]]]._sunk:
        break
      elif(x > 9 or x < 0 or y > 9 or y < 0):
        break
      elif(board_state[x,y] == '.'):
        if(fleet_matrix[x,y] == '.'):
          board_state[x,y] = 'M'
          break
        elif(fleet_matrix[x,y] != fleet_matrix[x1,y1]):
        # accidently hit an additional target!
          board_state[x,y] = 'H'
          go_immediately_to_opposite = True
          _fleet.update_status(board_state)
          if(not _fleet._ships[_fleet._index[fleet_matrix[x,y]]]._sunk):
            new_targets.append([x,y])
        else:
        # hit the same boat, woot!
          board_state[x,y] = 'H'
          go_immediately_to_opposite = True
          _fleet.update_status(board_state)
      else:
        break

      x += dx
      y += dy

    # try other direction if we have to hits in a straight line
    if(go_immediately_to_opposite):
      x = x1-dx
      y = y1-dy
      # continue in direction until miss or no more board or ship sunk
      for n in range(10):
        go_immediately_to_opposite = False
        if _fleet._ships[_fleet._index[fleet_matrix[x1,y1]]]._sunk:
          break
        elif(x > 9 or x < 0 or y > 9 or y < 0):
          break
        elif(board_state[x,y] == '.'):
          if(fleet_matrix[x,y] == '.'):
            board_state[x,y] = 'M'
            break
          elif(fleet_matrix[x,y] != fleet_matrix[x1,y1]):
          # accidently hit an additional target!
            board_state[x,y] = 'H'
            go_immediately_to_opposite = True
            _fleet.update_status(board_state)
            if(not _fleet._ships[_fleet._index[fleet_matrix[x,y]]]._sunk):
              new_targets.append([x,y])
          else:
          # hit the same boat, woot!
            board_state[x,y] = 'H'
            go_immediately_to_opposite = True
            _fleet.update_status(board_state)
        else:
          break

        x -= dx
        y -= dy

  # sink any new targets we accidentally found
  for target in new_targets:
    [x,y] = target
    board_state = sink_algorithm(board_state, _fleet, x, y)
    _fleet.update_status(board_state)
  return board_state

def grid2sequence(grid):
  sequence = [[-1,-1]]*100

  cnt = 0;
  for j in range(10):
    for k in range(10):
      if(grid[j][k] != '.'):
        sequence[grid[j][k]-1] = [j,k];
        cnt += 1;
      
  sequence = sequence[0:cnt]
  return sequence



# bubbles
def group1_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 49,'.', 39,'.', 21,'.', 38,'.', 48,'.'],\
             ['.', 40,'.', 22,'.', 20,'.', 37,'.', 47],\
             [ 41,'.', 23,'.',  7,'.', 19,'.', 36,'.'],\
             ['.', 24,'.',  8,'.',  6,'.', 18,'.', 35],\
             [ 25,'.',  9,'.',  1,'.',  5,'.', 17,'.'],\
             ['.', 10,'.',  2,'.',  4,'.', 16,'.', 34],\
             [ 26,'.', 11,'.',  3,'.', 15,'.', 33,'.'],\
             ['.', 27,'.', 12,'.', 14,'.', 32,'.', 46],\
             [ 42,'.', 28,'.', 13,'.', 31,'.', 45,'.'],\
             ['.', 43,'.', 29,'.', 30,'.', 44,'.', 50]];

  quad1   = [['.','.','.','.','.', 13,'.',  7,'.', 12],\
             ['.','.','.','.','.','.',  8,'.',  6,'.'],\
             ['.','.','.','.','.',  9,'.',  1,'.',  5],\
             ['.','.','.','.','.','.',  2,'.',  4,'.'],\
             ['.','.','.','.','.', 10,'.',  3,'.', 11],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  quad2   = [[ 13,'.',  7,'.', 12,'.','.','.','.','.'],\
             ['.',  8,'.',  6,'.','.','.','.','.','.'],\
             [  9,'.',  1,'.',  5,'.','.','.','.','.'],\
             ['.',  2,'.',  4,'.','.','.','.','.','.'],\
             [ 10,'.',  3,'.', 11,'.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  quad3   = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             [ 13,'.',  7,'.', 12,'.','.','.','.','.'],\
             ['.',  8,'.',  6,'.','.','.','.','.','.'],\
             [  9,'.',  1,'.',  5,'.','.','.','.','.'],\
             ['.',  2,'.',  4,'.','.','.','.','.','.'],\
             [ 10,'.',  3,'.', 11,'.','.','.','.','.']];

  quad4   = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.', 13,'.',  7,'.', 12],\
             ['.','.','.','.','.','.',  8,'.',  6,'.'],\
             ['.','.','.','.','.',  9,'.',  1,'.',  5],\
             ['.','.','.','.','.','.',  2,'.',  4,'.'],\
             ['.','.','.','.','.', 10,'.',  3,'.', 11]];

  clean   = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.',  4,'.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.',  3,'.','.','.','.','.'],\
             ['.',  8,'.',  7,'.','.','.','.','.','.'],\
             ['.','.','.','.','.','.',  5,'.',  6,'.'],\
             ['.','.','.','.','.',  2,'.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.',  1,'.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  static4 = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  cnt = 0
  quad = 0
  sequence0 = grid2sequence(static)
  sequences = []
  sequences.append(grid2sequence(quad1))
  sequences.append(grid2sequence(quad2))
  sequences.append(grid2sequence(quad3))
  sequences.append(grid2sequence(quad4))
  sequences.append(grid2sequence(clean))
  sequence = sequence0
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

        if(quad == 0):
          if(x < 5 and y >= 5):
            quad = 3
          elif(x < 5 and y < 5):
            quad = 4
          elif(x >= 5 and y < 5):
            quad = 1
          else:
            quad = 2
        else:
          quad = (quad+1)%4 + 1
        sequence=sequences[quad-1]
        cnt=0

    cnt += 1
    if(cnt >= len(sequence)):
      # randomly select next quadrant
      quad = random.randint(1,5)
      sequence=sequences[quad-1]
      cnt = 0
          

  return board_state

all_algorithms.append(group1_algorithm)
all_group_name.append("Bubbles")

def guess_fleet_pos(_fleet, board_state, nships=5):
  open_spots = []
  for j in range(10):
    for k in range(10):
      if board_state[j,k] == '.':
        open_spots.append([j,k])

  directions = [[1,0],[0,1],[-1,0],[0,-1]]
  unplaced = True
  x = 0
  y = 0
  dx = 0
  dy = 0
  n = 0
  while(unplaced):

    tries = 0
    nplaced = 0
    max_tries = 100000
    board = board_state.copy()

    for ship in _fleet._ships:
      if(not ship._sunk):
        #try to place the ship
        while(tries < max_tries):
          tries = tries+1
          n = ship._len
          idx = random.randint(0,len(open_spots)-1)
          x = open_spots[idx][0]
          y = open_spots[idx][1]
          z = random.randint(0,3)
          dx = directions[z][0]
          dy = directions[z][1]

          can_be_placed = True
          if(0 > x + (n-1)*dx or x + (n-1)*dx >= 10 or 0 > y + (n-1)*dy or y + (n-1)*dy >= 10):
            can_be_placed = False
          else:
            for k in range(n):
              if board[x+dx*k,y+dy*k] != '.':
                can_be_placed = False
          if(can_be_placed):
            for k in range(n):
              board[x+dx*k,y+dy*k] = 'x'
            nplaced = nplaced + 1
            break
      if(tries == max_tries):
        print("Max tries exceeded!")
        print(board)
        break
      if(nplaced == nships):
        unplaced = False
        break

    if tries != max_tries:
      unplaced = False
  if(nships == 1):
    return x,y,n,dx,dy
  return board

# empty set
def group2_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  while(not _fleet._sunk):
    
    ntrials = 1000
    counts = np.zeros([10,10],dtype=int)
    for tri in range(ntrials):
      board = guess_fleet_pos(_fleet, board_state)
      for j in range(10):
        for k in range(10):
          if board[j,k] == 'x':
            counts[j,k] += 1
#    print(board_state)

#    print(counts)
#    print(np.concatenate((board_state,counts)))

    idx = np.unravel_index(np.argmax(counts),counts.shape)
    x = idx[0]
    y = idx[1]

    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

  return board_state

all_algorithms.append(group2_algorithm)
all_group_name.append("Empty Set")

# kowtch
def group4_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 47,'.', 35,'.', 17,'.', 34,'.', 46,'.'],\
             ['.', 36,'.', 18,'.', 16,'.', 33,'.', 45],\
             [ 37,'.', 19,'.',  5,'.', 15,'.', 32,'.'],\
             ['.', 20,'.',  6,'.',  4,'.', 14,'.', 31],\
             [ 21,'.',  7,'.',  1,'.',  3,'.', 13,'.'],\
             ['.', 22,'.',  8,'.',  2,'.', 12,'.', 30],\
             [ 38,'.', 23,'.',  9,'.', 11,'.', 29,'.'],\
             ['.', 39,'.', 24,'.', 10,'.', 28,'.', 44],\
             [ 48,'.', 40,'.', 25,'.', 27,'.', 43,'.'],\
             ['.', 49,'.', 41,'.', 26,'.', 42,'.', 50]];

  cnt = 0
  sequence = grid2sequence(static)
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1

  return board_state

all_algorithms.append(group4_algorithm)
all_group_name.append("Kowtch")

# pdfj3
def group6_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [[ 49,'.', 44,'.', 33,'.', 34,'.', 45,'.'],\
             ['.', 32,'.', 24,'.', 23,'.', 28,'.', 46],\
             [ 41,'.', 18,'.', 14,'.', 15,'.', 29,'.'],\
             ['.', 26,'.',  4,'.',  3,'.', 13,'.', 38],\
             [ 40,'.', 16,'.',  1,'.',  8,'.', 22,'.'],\
             ['.', 25,'.',  5,'.',  2,'.', 12,'.', 37],\
             [ 39,'.',  9,'.',  6,'.',  7,'.', 21,'.'],\
             ['.', 27,'.', 10,'.', 11,'.', 17,'.', 43],\
             [ 47,'.', 30,'.', 19,'.', 20,'.', 31,'.'],\
             ['.', 48,'.', 35,'.', 36,'.', 42,'.', 50]];

  cnt = 0
  sequence = grid2sequence(static)
  while(not  _fleet._ships[-1]._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1


  while(not _fleet._sunk):
    foo= guess_fleet_pos(_fleet, board_state, 1)
    x0 = foo[0]
    y0 = foo[1]
    dx = foo[2]
    dy = foo[3]
    n  = foo[4]
    
    x = x0 + int(n/2)*dx
    y = y0 + int(n/2)*dy
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1

  return board_state

all_algorithms.append(group6_algorithm)
all_group_name.append("PDFJ^3")

# TNRR
def group7_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  inner_full = False
  while(not _fleet._sunk):
    if not inner_full:
      x = random.randint(2,7)
      y = random.randint(2,7)
    else:
      x = random.randint(0,9)
      y = random.randint(0,9)

    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
        if board_state[x,9-y] == '.':
          if fleet_matrix[x,9-y] == '.':
            board_state[x,9-y] = 'M'
          else:
            board_state[x,9-y] = 'H'
            board_state = sink_algorithm(board_state, _fleet, x, 9-y)
            _fleet.update_status(board_state)
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

      inner_full = True
      for j in range(2,8):
        if(not inner_full):
          break
        for k in range(2,8):
          if(board_state[j,k] == '.'):
            inner_full = False
            break

  return board_state

all_algorithms.append(group7_algorithm)
all_group_name.append("TNRR")

# Team Mo
def group8_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  start   = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.', 11,'.', 12,'.','.','.'],\
             ['.','.','.',  5,'.',  6,'.','.','.','.'],\
             ['.','.','.','.',  1,'.',  7,'.','.','.'],\
             ['.','.','.',  4,'.',  2,'.','.','.','.'],\
             ['.','.','.','.',  3,'.',  8,'.','.','.'],\
             ['.','.','.', 10,'.',  9,'.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];
 
  quad1   = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.',  3,'.','.','.','.','.','.','.','.'],\
             [  7,'.',  2,'.','.','.','.','.','.','.'],\
             ['.',  6,'.',  1,'.','.','.','.','.','.'],\
             [ 10,'.',  5,'.',  4,'.','.','.','.','.'],\
             ['.',  9,'.',  8,'.','.','.','.','.','.']];

  quad2   = [[ 11,'.', 10,'.',  7,'.','.','.','.','.'],\
             ['.',  8,'.',  5,'.','.','.','.','.','.'],\
             [  9,'.',  3,'.',  2,'.','.','.','.','.'],\
             ['.',  4,'.','.','.','.','.','.','.','.'],\
             [  6,'.',  1,'.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  quad3   = [['.','.','.','.','.','.',  8,'.',  9,'.'],\
             ['.','.','.','.','.',  4,'.',  5,'.', 10],\
             ['.','.','.','.','.','.',  1,'.',  6,'.'],\
             ['.','.','.','.','.','.','.',  2,'.',  7],\
             ['.','.','.','.','.','.','.','.',  3,'.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.']];

  quad4   = [['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.','.','.','.'],\
             ['.','.','.','.','.','.','.',  2,'.',  7],\
             ['.','.','.','.','.','.','.','.',  5,'.'],\
             ['.','.','.','.','.',  1,'.',  3,'.', 10],\
             ['.','.','.','.','.','.',  4,'.',  8,'.'],\
             ['.','.','.','.','.',  6,'.',  9,'.', 11]];

  cnt = 0
  quad = 0
  misscnt = 0
  sequences = []
  sequences.append(grid2sequence(start))
  sequences.append(grid2sequence(quad1))
  sequences.append(grid2sequence(quad2))
  sequences.append(grid2sequence(quad3))
  sequences.append(grid2sequence(quad4))
  sequence = sequences[0]
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
        misscnt = misscnt + 1
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

        if(quad == 0):
          if(x < 5 and y >= 5):
            quad = 3
          elif(x < 5 and y < 5):
            quad = 4
          elif(x >= 5 and y < 5):
            quad = 1
          else:
            quad = 2
        else:
          quad = (quad+1)%4 + 1
        sequence=sequences[quad-1]
        cnt=0

    cnt += 1
    if(cnt >= len(sequence) or misscnt == 6):
      # randomly select next quadrant
      quad = random.randint(0,4)
      sequence=sequences[quad]
      cnt = 0
      misscnt = 0
          

  return board_state

all_algorithms.append(group8_algorithm)
all_group_name.append("Team Mo")

# The Left
def group9_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [['.', 45,'.', 44,'.', 43,'.', 42,'.', 50],\
             [ 46,'.', 27,'.', 26,'.', 25,'.', 41,'.'],\
             ['.', 28,'.', 13,'.', 12,'.', 24,'.', 40],\
             [ 29,'.', 14,'.',  3,'.', 11,'.', 23,'.'],\
             ['.', 15,'.',  4,'.',  2,'.', 10,'.', 39],\
             [ 30,'.',  5,'.',  1,'.',  9,'.', 22,'.'],\
             ['.', 16,'.',  6,'.',  8,'.', 21,'.', 38],\
             [ 31,'.', 17,'.',  7,'.', 20,'.', 37,'.'],\
             ['.', 32,'.', 18,'.', 19,'.', 36,'.', 49],\
             [ 47,'.', 33,'.', 34,'.', 35,'.', 48,'.']];


  cnt = 0
  sequence = grid2sequence(static)
  x0 = 0
  x1 = 9
  y0 = 0
  y1 = 9
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    cnt += 1
    if(x0 <= x and x <= x1 and y0 <= y and y <= y1):
      if(board_state[x,y] == '.'):
        if fleet_matrix[x,y] == '.':
          board_state[x,y] = 'M'
        else:
          cnt = 0
          board_state[x,y] = 'H'
          board_state = sink_algorithm(board_state, _fleet, x, y)
          _fleet.update_status(board_state)
    if(cnt == 0 or cnt == len(sequence)):
      cnt = 0
      # get next largest rectangle:
      area = 0
      amax = 0
      xmax = 0
      ymax = 0
      dxmax = 0
      dymax = 0
      for j in range(10):
        for k in range(10):
          if(board_state[j,k] == '.'):
            for dx in range(1,11-j):
              for dy in range(1,11-k):
                empty = True
                for x in range(j,j+dx):
                  for y in range(k,k+dy):
                    if(board_state[x,y] != '.'):
                      empty = False
                      break
                  if(not empty):
                    break
                if(empty):
                  area = dx*dy
                  if((area > amax) or ( area==amax and abs(dx-dy)< abs(dxmax-dymax))):
                    amax = area
                    xmax = j
                    ymax = k
                    dxmax = dx
                    dymax = dy
      x0 = xmax
      x1 = xmax + dxmax-1
      y0 = ymax
      y1 = ymax + dymax-1
          
  return board_state

all_algorithms.append(group9_algorithm)
all_group_name.append("The Left")


# The Pink Panthers
def group10_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static1 = [[ 25,'.', 50,'.', 14,'.', 42,'.', 24,'.'],\
             ['.', 20,'.', 27,'.',  3,'.', 43,'.', 21],\
             [ 41,'.', 18,'.', 28,'.', 10,'.', 44,'.'],\
             ['.', 40,'.',  7,'.', 29,'.',  9,'.', 45],\
             [ 15,'.', 39,'.',  1,'.', 30,'.',  4,'.'],\
             ['.',  6,'.', 38,'.',  2,'.', 31,'.', 16],\
             [ 49,'.', 11,'.', 37,'.',  8,'.', 32,'.'],\
             ['.', 48,'.', 12,'.', 36,'.', 17,'.', 33],\
             [ 22,'.', 47,'.',  5,'.', 35,'.', 19,'.'],\
             ['.', 23,'.', 46,'.', 13,'.', 34,'.', 26]];

  static2 = [[ 33,'.','.', 22,'.','.', 27,'.','.', 32],\
             ['.', 29,'.','.', 13,'.','.', 20,'.','.'],\
             ['.','.', 15,'.','.',  3,'.','.', 19,'.'],\
             [ 21,'.','.', 10,'.','.',  7,'.','.', 28],\
             ['.', 12,'.','.',  1,'.','.',  4,'.','.'],\
             ['.','.',  6,'.','.',  2,'.','.', 14,'.'],\
             [ 26,'.','.',  8,'.','.',  9,'.','.', 23],\
             ['.', 17,'.','.',  5,'.','.', 16,'.','.'],\
             ['.','.', 18,'.','.', 11,'.','.', 30,'.'],\
             [ 31,'.','.', 25,'.','.', 24,'.','.', 34]];

  static3 = [[ 25,'.','.','.', 14,'.','.','.', 24,'.'],\
             ['.', 20,'.','.','.',  3,'.','.','.', 21],\
             ['.','.', 18,'.','.','.', 10,'.','.','.'],\
             ['.','.','.',  7,'.','.','.',  9,'.','.'],\
             [ 15,'.','.','.',  1,'.','.','.',  4,'.'],\
             ['.',  6,'.','.','.',  2,'.','.','.', 16],\
             ['.','.', 11,'.','.','.',  8,'.','.','.'],\
             ['.','.','.', 12,'.','.','.', 17,'.','.'],\
             [ 22,'.','.','.',  5,'.','.','.', 19,'.'],\
             ['.', 23,'.','.','.', 13,'.','.','.', 26]];

  static4 = [[ 20,'.','.','.','.',  3,'.','.','.','.'],\
             ['.', 18,'.','.','.','.', 10,'.','.','.'],\
             ['.','.', 16,'.','.','.','.', 13,'.','.'],\
             ['.','.','.',  7,'.','.','.','.',  9,'.'],\
             ['.','.','.','.',  1,'.','.','.','.',  4],\
             [  6,'.','.','.','.',  2,'.','.','.','.'],\
             ['.', 11,'.','.','.','.',  8,'.','.','.'],\
             ['.','.', 14,'.','.','.','.', 15,'.','.'],\
             ['.','.','.', 12,'.','.','.','.', 17,'.'],\
             ['.','.','.','.',  5,'.','.','.','.', 19]];

  cnt = 0
  sequences = []
  sequences.append(grid2sequence(static1))
  sequences.append(grid2sequence(static2))
  sequences.append(grid2sequence(static3))
  sequences.append(grid2sequence(static4))
  sequence = sequences[0]
  while(not _fleet._sunk):
    [x,y] = sequence[cnt]
    cnt += 1
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
        num = 0
        avg = 0
        if(not _fleet._sunk):
          for ship in _fleet._ships:
            if(not ship._sunk):
              avg = avg + ship._len
              num = num + 1
          avg = math.ceil(avg/num)
          sequence = sequences[avg-2]
          cnt = 0

  return board_state

all_algorithms.append(group10_algorithm)
all_group_name.append("The Pink Panthers")

# The Smash Bros
def group11_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [['.','.', 32,'.','.', 33,'.','.', 24,'.'],\
             [ 31,'.','.', 21,'.','.', 27,'.','.', 25],\
             ['.', 11,'.','.', 15,'.','.', 16,'.','.'],\
             ['.','.',  4,'.','.',  3,'.','.', 17,'.'],\
             [ 10,'.','.',  2,'.','.',  1,'.','.', 23],\
             ['.',  9,'.','.',  5,'.','.',  6,'.','.'],\
             ['.','.', 12,'.','.',  7,'.','.',  8,'.'],\
             [ 26,'.','.', 13,'.','.', 14,'.','.', 30],\
             ['.', 27,'.','.', 18,'.','.', 20,'.','.'],\
             ['.','.', 28,'.','.', 19,'.','.', 29,'.']];

  cnt = 0
  sequence = grid2sequence(static)
  while(not _fleet._sunk and cnt < len(sequence)):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1

  while(not _fleet._sunk):
    x = random.randint(0,9)
    y = random.randint(0,9)
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

  return board_state

all_algorithms.append(group11_algorithm)
all_group_name.append("The Smash Bros")

# The Three Musketeers
def group12_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  sequence = [[5,4],[4,3],[6,3],[6,5]]

  # shoot at middle first
  for cnt in range(len(sequence)):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

  # hereafter randomly move N,E,S,W by +2 for the next shot
  directions = [[2,0],[0,2],[-2,0],[0,-2],[1,1],[1,-1],[-1,1],[-1,-1]]
  while(not _fleet._sunk):
    z = random.randint(0,7)
    dx = directions[z][0]
    dy = directions[z][1]
    if(0 <= x + dx and x + dx < 10 and 0 <= y + dy and y+dy < 10):
      x = x + dx
      y = y + dy
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

  return board_state

all_algorithms.append(group12_algorithm)
all_group_name.append("The Three Musketeers")

# Tic-tac-Stub Your Toe
def group13_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)

  static  = [['.','.','.','.','.', 30,'.','.','.','.'],\
             ['.', 13,'.','.', 26,'.','.','.', 14,'.'],\
             ['.','.',  9,'.','.', 22,'.', 10,'.','.'],\
             ['.','.','.',  5, 18,'.',  6,'.','.','.'],\
             [ 31,'.', 23,'.',  1,  2, 17,'.', 25,'.'],\
             ['.', 27,'.', 19,  3,  4,'.', 21,'.', 29],\
             ['.','.','.',  8,'.', 20,  7,'.','.','.'],\
             ['.','.', 12,'.', 24,'.','.', 11,'.','.'],\
             ['.', 16,'.','.','.', 28,'.','.', 15,'.'],\
             ['.','.','.','.', 32,'.','.','.','.','.']];

  cnt = 0

  sequence = grid2sequence(static)
  while(not _fleet._sunk and cnt < len(sequence)):
    [x,y] = sequence[cnt]
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
    cnt += 1


  while(not _fleet._sunk):
    # Now find longest empty lines
    dxmax = 0
    dymax = 0
    xmax = 0
    ymax = 0
    lmax = 0
    for j in range(10):
      for k in range(10):
        if(board_state[j,k] == '.'):
          # try horizontal line
          for dx in range(1,10-j):
            if(board_state[j+dx,k] != '.'):
              break
          if(lmax < dx):
            lmax = dx
            xmax = j
            ymax = k
            dxmax = dx
            dymax = 0
          # try vertical line
          for dy in range(1,10-k):
            if(board_state[j,k+dy] != '.'):
              break
          if(lmax < dy):
            lmax = dy
            xmax = j
            ymax = k
            dxmax = 0
            dymax = dy

    x = xmax + int(dxmax/2)
    y = ymax + int(dymax/2)
  
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)

  return board_state

all_algorithms.append(group13_algorithm)
all_group_name.append("Tic-Tac-Stub Your Toe")

def random_algorithm(_fleet):
  fleet_matrix = _fleet.fleet2matrix()

  board_state = np.array([['.']*10]*10)
  while(not _fleet._sunk):
    x = random.randint(0,9)
    y = random.randint(0,9)
    if(board_state[x,y] == '.'):
      if fleet_matrix[x,y] == '.':
        board_state[x,y] = 'M'
      else:
        board_state[x,y] = 'H'
        board_state = sink_algorithm(board_state, _fleet, x, y)
        _fleet.update_status(board_state)
  return board_state

all_algorithms.append(random_algorithm)
all_group_name.append("Random Algorithm")

#algorithms = [random_algorithm, group1_algorithm, group2_algorithm, group5_algorithm, group6_algorithm]
#algorithms = [random_algorithm, extra_algorithm]
#algorithms = [random_algorithm]
#algorithm_names = ["Pure Random", "Counter-Clockwise Search", "Dark Knight", "Checkered Quadrants", "Spider Web", "Iterated Guess", "Pentagons", "X factor", "Swirl"]
for alg_idx in range(len(all_algorithms)):
  algorithm = all_algorithms[alg_idx]
  shot_avg = 0
  ntrials = 10000
  if alg_idx == 1:
    ntrials = 2
  elif alg_idx == 6:
    ntrials = 10000
#  algorithm_name = algorithm_names[alg_idx]
  for k in range(ntrials):
    testfleet.scatter()
    fleet_matrix = testfleet.fleet2matrix()

    board_state = algorithm(testfleet)
    nshots = 0
    for i in range(10):
      for j in range(10):
        if(board_state[i,j] != '.'):
          nshots += 1
    shot_avg += nshots
#    print("nshots=",nshots)

  shot_avg /= ntrials
#  print(algorithm_name, shot_avg)
  print(all_group_name[alg_idx], shot_avg)


