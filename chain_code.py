import sys
import numpy as np

def next_index_in_neighbourhood(x, y, direction):

  dx, dy = dir_to_coord(direction)
  next_x = x + dx
  next_y = y + dy
  return next_x, next_y

def dir_to_coord(direction):
  if direction == 0:
    dx = 0
    dy = 1
  if direction == 1:
    dx = -1
    dy = 1
  if direction == 2:
    dx = -1
    dy = 0
  if direction == 3:
    dx = -1
    dy = -1
  if direction == 4:
    dx = 0
    dy = -1
  if direction == 5:
    dx = 1
    dy = -1
  if direction == 6:
    dx = 1
    dy = 0
  if direction == 7:
    dx = 1
    dy = 1

  return dx, dy

def trace_boundary(image, background=0):

  M, N = image.shape
  previous_directions = [] # A list of previous directions (forms the chain code)
  start_search_directions = [] # A list of starting directions for local search
  boundary_positions = [] # A list of (x,y) boundary pixels
  tortuosidad = 0 # Valor acumulado de la suma absoluta de las pendientes

  found_object = False # A variable that indicate if (while we are searching
                       # the local neighbourhood of a pixel) we have found an
                       # object pixel (a pixel with a value different than the
                       # background).

  # We look for the upper left object pixel, and set that as the starting point.
  for x in range(M):
    for y in range(N):
      if not (image[x, y] == background):
        p0 = [x, y]
        found_object = True
        break
    if found_object:
      break

  # We initialize the different lists
  boundary_positions.append(p0)
  previous_directions.append(7)
  start_search_directions.append(np.mod((previous_directions[0] - 6), 8))

  n = 0 # Counter for boundary pixels
  while True:
    # Check convergence criteria. We terminate the algorithm when we are back
    # at the starting point.
    if n > 2:
      if ((boundary_positions[n-1] == boundary_positions[0]) and
              (boundary_positions[n] == boundary_positions[1])):
        break

    search_neighbourhood = True # This variable indicates whether to continue
                                # to search the local neighbourhood for an
                                # object pixel
    loc_counter = 0 # This variable keeps track of how many local neighbourhood
                    # pixels we have searched.
    x, y = boundary_positions[n] # We get the (x,y)-coordinates of our current
                                 # position on the boundary.

    # Then, we search the neighbourhood of (x,y) for an object pixel.
    while search_neighbourhood:

      # Find the next pixel in the neighbourhood of (x,y) to check (we search
      # in a clockwise direction in the local neighbourhood also)
      direction = np.mod(start_search_directions[n] - loc_counter,8)
      next_x, next_y = next_index_in_neighbourhood(x, y, direction)

      # If we go beyond the image frame, we skip it, and continue the search
      # from the next pixel in the neighbourhood.
      if next_x < 0 or next_x >= M or next_y < 0 or next_y >= N:
        search_neighbourhood = True
        loc_counter += 1
        continue

      # Check if we encountered an object pixel
      if not (image[next_x, next_y] == background):
        # Found one: terminate the search in this neighbourhood
        search_neighbourhood = False
      else:
        # Did not find one: continue the search in this neighbourhood
        loc_counter += 1
        #search_neighbourhood = True

    # We append the direction we used to find the object pixel to the chain
    # code, and also update the list of boundary positions
    #actualizamos el valor de la tortuosidad
    previous_directions.append(direction)
    boundary_positions.append([next_x, next_y])
    if direction == 1 or 7:
        tortuosidad+=0.25
#        print(n,tortuosidad,direction)
    elif direction == 2 or 6:
        tortuosidad+=0.5
#        print(n,tortuosidad,direction)
    elif direction == 3 or 5:
        tortuosidad+=0.75
#        print(n,tortuosidad,direction)
    elif direction == 1:
        tortuosidad+=1.0
#        print(n,tortuosidad,direction)
    

    # From this direction, we can decide where to start the search in the next
    # iteration.
    if np.mod(direction, 2):
        # direction is odd
      start_search_directions.append(np.mod(direction - 6, 8))
    else:
        # direction is even
      start_search_directions.append(np.mod(direction - 7, 8))

    n += 1

  chain_code = previous_directions[1:-1]

  return chain_code, boundary_positions, tortuosidad
