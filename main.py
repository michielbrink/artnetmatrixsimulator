#!/usr/bin/python

# thanks to http://openbookproject.net/thinkcs/python/english3e/pygame.html
import argparse
import socket
import sys
import pygame

matrix_width = 10
matrix_height = 17
UDP_PORT = 6454
UDP_IP = "0.0.0.0"
bufferSize = 170 * 3

data = [0] * bufferSize
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fullscreen", help="fullscreen mode", action="store_true")
parser.add_argument("-s", "--snake", help="snake modes", action="store_true")
parser.add_argument("-b", "--blocksize", default=40, help="set blocksize")
parser.add_argument("--debug", help="enable debug", default=False)
args = parser.parse_args()

debug = args.debug

fmt = (UDP_PORT, UDP_IP)
fmtstr = "Active and listening for connections on port %s and ip %s" % fmt
print(fmtstr)
# create a datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# bind the socket to a port, to allow people to send info to it
sock.bind((UDP_IP, UDP_PORT))

pygame.init()
args.blocksize = int(args.blocksize)

if args.fullscreen:
    surface = pygame.display.set_mode((args.blocksize * matrix_height,
                                      args.blocksize * matrix_width),
                                      pygame.FULLSCREEN)
else:
    surface = pygame.display.set_mode((args.blocksize * matrix_height,
                                      args.blocksize * matrix_width),
                                      pygame.RESIZABLE)

while True:
    byte_data = None
    data_number = 0
    try:
        # try to get a message on the socket
        byte_data, addr = sock.recvfrom(bufferSize)

    #  if no message was available, just wait a while
    except socket.error:
        pass
    if byte_data:
        byte_data = byte_data[18:]
        data = [ord(i) for i in byte_data]
        if debug:
            print(data)

    # Look for an event from keyboard, mouse, etc.
    pygame.event.pump()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    #snake mode  (doesnt work yet)
    if args.snake:

        print "1"
        print data

        tempdata = []
        #transform data to tempdata
        for i in xrange(0, len(data), 3):
            tempdata.append((data[i],data[i+1],data[i+2]))

        print "2"
        print tempdata

        for x in range(0, matrix_width, 2):
            templist = []
            for y in range(matrix_height - 1, -1, -1):
                templist.append(tempdata[x * matrix_height + y])
            for y in range(0, matrix_height):
                tempdata[x * matrix_height + y] = templist[y]

        #transform tempdata back to data
        channels = len(data)/3
        data = []

        print "3"
        print tempdata

        for i in xrange(0, channels, 1):
            data.append(tempdata[i][0])
            data.append(tempdata[i][1])
            data.append(tempdata[i][2])

        print "4"
        print data

    # for every pixel get the color and place it on the right spot.
    # and then draw it.
    for col in range(matrix_height):
        for row in range(matrix_width):
            r = data[data_number + 0]
            g = data[data_number + 1]
            b = data[data_number + 2]
            color = (r, g, b)

            x = args.blocksize * col
            y = matrix_height - (args.blocksize * row) - matrix_height
            width = args.blocksize * matrix_height
            height = args.blocksize * matrix_width
            the_square = (x, y, width, height)
            pygame.draw.rect(surface, color, the_square, 0)

            x = args.blocksize * col
            y = matrix_height - (args.blocksize * row) - matrix_height
            width = args.blocksize * matrix_height
            height = args.blocksize * matrix_width
            the_square = (x, y, width, height)
            pygame.draw.rect(surface, (0, 0, 0), the_square, 2)

            # increment in steps of three since the packet is layed out as
            # values of r, g, b following eache other like that.
            data_number += 3
            if data_number >= len(data):
                break

    pygame.display.flip()


pygame.quit()
