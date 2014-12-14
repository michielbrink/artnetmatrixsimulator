#!/usr/bin/python

#thanks to http://openbookproject.net/thinkcs/python/english3e/pygame.html

import argparse, socket, time, pygame

matrix_width = 10
matrix_height = 17
color_order = [2,0,1] #[r,g,b]
UDP_PORT = 6453
UDP_IP= "localhost"
bufferSize = 1024

data = [0]*531
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fullscreen", help="fullscreen mode",
                    action="store_true")
parser.add_argument("-b", "--blocksize", default=40,help="set blocksize")
parser.add_argument("--debug", help="enable debug", default=False)
args = parser.parse_args()



print("Active and listening for connections on port %s and ip %s" % (UDP_PORT, UDP_IP))
# create a datagram socket
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# bind the socket to a port, to allow people to send info to it
sock.bind( (UDP_IP,UDP_PORT) )

pygame.init()
args.blocksize = int(args.blocksize)

if args.fullscreen:
    surface = pygame.display.set_mode((args.blocksize*matrix_height, args.blocksize*matrix_width),pygame.FULLSCREEN)
else:
    surface = pygame.display.set_mode((args.blocksize*matrix_height, args.blocksize*matrix_width),pygame.RESIZABLE)


while True:

    byte_data = None
    data_number = 0
    try:
          
        # try to get a message on the socket
        byte_data, addr = sock.recvfrom( 531, socket.MSG_DONTWAIT ) # buffer size is 1024 bytes

        
    #  if no message was available, just wait a while
    except socket.error:
		pass
        # wait a bit to keep from clobbering the CPU
        #time.sleep(0.01)

    if byte_data:
         
        byte_data = byte_data[18:]
        data=[ord(i) for i in byte_data]
        print data

    # Look for an event from keyboard, mouse, etc.
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        break;
    elif ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_ESCAPE:
            pygame.quit()

    for col in range(matrix_height):       # Run through cols drawing squares
        for row in range(matrix_width):           # Draw each row of the board.
            r = data[data_number+color_order[0]]
            g = data[data_number+color_order[1]]
            b = data[data_number+color_order[2]]
            color = (r,g,b)
            the_square = (args.blocksize*col, (matrix_height)-(args.blocksize*row)-17, args.blocksize*matrix_height, args.blocksize*matrix_width)
            pygame.draw.rect(surface,color,the_square, 0)
            the_square = (args.blocksize*col, (matrix_height)-(args.blocksize*row)-17, args.blocksize*matrix_height, args.blocksize*matrix_width)
            pygame.draw.rect(surface,(0,0,0), the_square, 2)
            #surface.fill(color, the_square)
            data_number += 3

    pygame.display.flip()
    time.sleep(1./120)


pygame.quit()
