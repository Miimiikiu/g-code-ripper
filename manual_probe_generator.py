"""

Copyright (c) 2023 Kieran Aponte
This software is licensed under the GPL V3 License.

"""

# The probe files generated from g-code-ripper often probe outside of the stock 
# due to lead-ins in the g code, so manual_probe_generator.py accepts the raw 
# stock dimensions and leaves a buffer for safety. While probing, record the 
# z values in stock_probe_W_xx_L_yy_data.txt. You can now use this instead of 
# steps 1-3 listed in README.MD.

# To ensure that your tool or collet does not collide with your clamps, please 
# use gcode_boundaries.py with your desired G-Code files: 
# https://github.com/Miimiikiu/gcode-boundaries

####USER VARIABLES####

# Assumes mm

stock_width = 76         # stock size along x
stock_length = 305       # stock size along y
num_probe_points_x = 2   # number of points to probe along x
num_probe_points_y = 2   # number of points to probe along y
z_safe = -18             # height of travel moves
z_probe_start = -28      # height immediately before probe
feed_rate_fast = 500     # feed rate during travel
feed_rate_slow = 20      # feed rate during probe

# Clamp buffers to prevent collision with clamps. The clamps on mine are at the top & bottom along the y axis
clamp_buffer_x = 0   # buffer should be >= 0
clamp_buffer_y = 20  # buffer should be >= 0

manual_points = True # Set True if for example you want to avoid the area of failed operation
if manual_points:
    probe_points_x = [-25, 25]
    probe_points_y = [30, 120]
    assert len(probe_points_x) == num_probe_points_x
    assert len(probe_points_y) == num_probe_points_y


wcs_x = 0 # 0 = stock center, -stock_width/2 = stock left, stock-width/2 = stock right
wcs_y = -stock_length/2 # 0 = stock center, -stock_length/2 = stock bottom, stock-length/2 = stock top
if manual_points:
    manual_ends = '_[{},{}]-[{},{}]'.format(probe_points_x[0], probe_points_y[0], probe_points_x[-1], probe_points_y[-1])
else:
    manual_ends = ''
path = 'G:\\My Drive\\NC Files\\Lathe Adapter V2\\6.34mm Stock Test\\stock_probe_W_{}_L_{}{}.nc'.format(stock_width, stock_length, manual_ends)

######################

buffer_x = (stock_width / 2) / num_probe_points_x # Buffer prevents G31 outside of stock from lead-in moves in g-code ripper or dangerously close to stock edge
buffer_y = (stock_length / 2) / num_probe_points_y

# raise generated buffers if collision with clamps may otherwise occur
if buffer_x < clamp_buffer_x:
    buffer_x = clamp_buffer_x 
if buffer_y < clamp_buffer_y:
    buffer_y = clamp_buffer_y

with open(path[:-3] + '_data.txt', 'w') as datafile: #create blank file for manual data entry
    
    with open(path, 'w') as outfile:
        outfile.write('(PATH: {})\n'.format(path))
        outfile.write('(Assumes Z0 is stock top)\n')
        outfile.write('(INSPECT G CODE CAREFULLY BEFORE USE)\n\n')
        outfile.write('G21 (Working in mm)\nG90\nF{}\nG54\n'.format(feed_rate_fast))
        first_x = int((-stock_width/2) - wcs_x + buffer_x) # round to integer for simplicity
        first_y = int((-stock_length/2) - wcs_y + buffer_y)
        outfile.write('G0 Z{}\nG0 X{} Y{}\n\n'.format(z_safe, first_x, first_y))
        
        for y in range(num_probe_points_y):
            for x in range(num_probe_points_x):
                if manual_points == False:
                    x_coord = int((-stock_width/2 + (x * stock_width/num_probe_points_x)) - wcs_x + buffer_x)
                    y_coord = int((-stock_length/2 + (y * stock_length/num_probe_points_y)) - wcs_y + buffer_y)
                else:
                    x_coord = probe_points_x[x]
                    y_coord = probe_points_y[y]
                print('({},{})'.format(x_coord, y_coord))
                outfile.write('G01 X{} Y{} Z{} F{}\n'.format(x_coord, y_coord, z_probe_start, feed_rate_fast))
                outfile.write('G31 Z{} F{}\n'.format(z_probe_start - 8, feed_rate_slow))
                outfile.write('M0\n') # pause for user to record data
                outfile.write('G01 Z{} F{}\n'.format(z_probe_start, feed_rate_fast))
                datafile.write('{}.0000,{}.0000,\n'.format(x_coord, y_coord)) #fill in x & y values in manual data file, user fills in z values during probing
        outfile.write('G01 Z{} F{}\n'.format(z_safe, feed_rate_fast))
        outfile.write('M2')


print('INSPECT G CODE CAREFULLY BEFORE USE')