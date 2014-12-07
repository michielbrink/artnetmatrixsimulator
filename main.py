#!/usr/bin/python

#thanks to http://openbookproject.net/thinkcs/python/english3e/pygame.html

import argparse, socket, time, pygame

matrix_width = 10
matrix_height = 17
color_order = [2,0,1] #[r,g,b]
UDP_PORT = 6453
UDP_IP= "127.0.0.1"
bufferSize = 1024

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fullscreen", help="fullscreen mode",
                    action="store_true")
parser.add_argument("-b", "--blocksize", help="set blocksize")
args = parser.parse_args()



print("Active and listening for connections on port %s and ip %s" % (UDP_PORT, UDP_IP))
# create a datagram socket
sock = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# bind the socket to a port, to allow people to send info to it
sock.bind( (UDP_IP,UDP_PORT) )

pygame.init()
if args.blocksize:
    args.blocksize = int(args.blocksize)
      
else:
    infoObject = pygame.display.Info()
    args.blocksize = infoObject.current_w/matrix_height
    

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
    elif ev.type == pygame.KEYDOWN:
        if ev.key == pygame.K_ESCAPE:
            pygame.quit()

    for col in range(matrix_height):       # Run through cols drawing squares
        for row in range(matrix_width):           # Draw each row of the board.
            color = (data[data_number+color_order[0]],data[data_number+color_order[1]],data[data_number+color_order[2]])
            data_number += 3
            the_square = (args.blocksize*col, args.blocksize*row, args.blocksize*matrix_height, args.blocksize*matrix_width)
            surface.fill(color, the_square)

    pygame.display.flip()


pygame.quit()