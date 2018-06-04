#!/usr/bin/env python3
#encoding: UTF-8

from socket import *
import time

HOST = gethostbyname(gethostname())
#HOST = "localhost"
PORT = 4300

if __name__ == "__main__":
    print("%s " % (HOST) + "Reading a file...")
    ## Build Country Dictionary
    countryDict = {}
    start = time.time()
    file = open('geo_world.txt')
    line = file.readline().split(' - ')
    while line != [""]:
        countryDict[line[0]] = line[1].strip('\n')
        line = file.readline().split(' - ')
    end = time.time()
    print("%s " % (HOST) + "Read in %f sec" % (end-start))

    server_sckt = socket(AF_INET, SOCK_DGRAM)
    server_sckt.bind((HOST, PORT))
    print("%s " % (HOST) + "Listening on localhost: %d" % (PORT))
    x = 0
    while True:
        (msg, client_addr) = server_sckt.recvfrom(2048)
        if x == 0:
            server_sckt.sendto("You are connnect to the GEO101 server".encode(), client_addr)
            print("%s " % (HOST) + "Connnected: %s" % str(client_addr[0].strip("'")))
            x = 1

        else:
            if msg.decode() == "BYE":
                print("%s " % (HOST) + "Disconnected: %s" % str(client_addr[0]).strip("'"))
                x = 0
                server_sckt.sendto(msg, client_addr)

            elif msg.decode() not in countryDict:
                print("%s " % (HOST) + "User Query: %s" % (msg.decode()))
                server_sckt.sendto("-There is no such country".encode(), client_addr)

            else:
                print("%s " % (HOST) + "User Query: %s" % (msg.decode()))

                msg_resp = "+" + countryDict[msg.decode()]
                server_sckt.sendto(msg_resp.encode(), client_addr)


    server_sckt.close()