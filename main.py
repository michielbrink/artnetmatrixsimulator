#!/usr/bin/python

#thanks to http://openbookproject.net/thinkcs/python/english3e/pygame.html

import socket, time, pygame

matrix_width = 10
matrix_height = 17
blockratio = 100 #fill in a blocksize
color_order = [2,0,1] #[r,g,b]
UDP_PORT = 6453
UDP_IP= "0.0.0.0"
bufferSize = 1024

print("Active and listening for connections on port %s and ip %s" % (UDP_PORT, UDP_IP))
# create a datagram socket
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# bind the socket to a port, to allow people to send info to it
sock.bind( (UDP_IP,UDP_PORT) )


def draw_board():

    pygame.init()

    # Create the surface of (width, height), and its window.
    surface = pygame.display.set_mode((blockratio*matrix_height, blockratio*matrix_width))


    while True:

        byte_data = None
        data_number = 0

        try:
          
            # try to get a message on the socket
            byte_data, addr = sock.recvfrom( 531, socket.MSG_DONTWAIT ) # buffer size is 1024 bytes

        
        #  if no message was available, just wait a while
        except socket.error:

            # wait a bit to keep from clobbering the CPU
            time.sleep(0.01)

        if byte_data:
         
            byte_data = byte_data[18:]
            data=[ord(i) for i in byte_data]
            print data

        # Look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        for col in range(matrix_height):       # Run through cols drawing squares
            for row in range(matrix_width):           # Draw each row of the board.
                color = (data[data_number+color_order[0]],data[data_number+color_order[1]],data[data_number+color_order[2]])
                data_number += 3
                the_square = (blockratio*col, blockratio*row, blockratio*matrix_height, blockratio*matrix_width)
                surface.fill(color, the_square)

        # Now that squares are drawn, draw the queens.
  

        pygame.display.flip()


    pygame.quit()

if __name__ == "__main__":
    draw_board()    # 7 x 7 to test window matrix_size