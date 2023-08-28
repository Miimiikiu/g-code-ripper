####USER VARIABLES####

# Assumes mm
stock_width = 77     # stock size along x
stock_length = 130
probe_points_x = 2   # number of points to probe along x
probe_points_y = 3   
z_safe = 15          # height of travel moves
z_probe_start = 5    # height immediately before probe
feed_rate_fast = 500 # feed rate during travel
feed_rate_slow = 20  # feed rate during probe


wcs_x = 0 # 0 = stock center, -stock_width/2 = stock left, stock-width/2 = stock right
wcs_y = -stock_length/2 # 0 = stock center, -stock_length/2 = stock bottom, stock-length/2 = stock top

path = 'G:\\My Drive\\NC Files\\Lathe Adapter\\Clamps\\stock_probe_W_{}_L_{}.nc'.format(stock_width, stock_length)

######################

buffer_x = (stock_width / 2) / probe_points_x # Buffer prevents G31 outside of stock from lead-in moves in g-code ripper or dangerously close to stock edge
buffer_y = (stock_length / 2) / probe_points_y

with open(path[:-3] + '_data.txt', 'w') as datafile: #create blank file for manual data entry
    
    with open(path, 'w') as outfile:
        outfile.write('(PATH: {})\n'.format(path))
        outfile.write('(Assumes Z0 is stock top)\n')
        outfile.write('(INSPECT G CODE CAREFULLY BEFORE USE)\n\n')
        outfile.write('G21 (Working in mm)\nG90\nF{}\nG54\n'.format(feed_rate_fast))
        first_x = int((-stock_width/2) - wcs_x + buffer_x) # round to integer for simplicity
        first_y = int((-stock_length/2) - wcs_y + buffer_y)
        outfile.write('G0 Z{}\nG0 X{} Y{}\n\n'.format(z_safe, first_x, first_y))
        for y in range(probe_points_y):
            for x in range(probe_points_x):
                x_coord = int((-stock_width/2 + (x * stock_width/probe_points_x)) - wcs_x + buffer_x)
                y_coord = int((-stock_length/2 + (y * stock_length/probe_points_y)) - wcs_y + buffer_y)
                print('({},{})'.format(x_coord, y_coord))
                outfile.write('G01 X{} Y{} Z{} F{}\n'.format(x_coord, y_coord, z_probe_start, feed_rate_fast))
                outfile.write('G31 Z-1 F{}\n'.format(feed_rate_slow))
                outfile.write('M0\n') # pause for user to record data
                outfile.write('G01 Z{} F{}\n'.format(z_probe_start, feed_rate_fast))
                datafile.write('{}.0000,{}.0000,\n'.format(x_coord, y_coord)) #fill in x & y values in manual data file, user fills in z values during probing
        outfile.write('G01 Z{} F{}\n'.format(z_safe, feed_rate_fast))
        outfile.write('M2')


print('INSPECT G CODE CAREFULLY BEFORE USE')