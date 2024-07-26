# this is library used for socket functions
import socket

# used to implement command line and terminal commands into a python file
import sys

# function to create a socket
def create_socket():
    # enclose within try catch incase socket creation fails and will print the error message
    try:
        # first will define some global variables to hold ip of host and port number
        global host
        global port

        global s # the variable for our socket

        host = ""   # for now we are in the server file and it will be used so can leave this empty
        port = 9999 # uncommon port not used alot

        s = socket.socket() # initialize socket

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


#  function for Binding the socket and listening for connections
def bind_socket():
    # enclose within try catch incase socket binding fails and will print the error message
    # however we will continue to attempt to bind if fails (done through recursion)
    try:
        # to access global variables declared previously in another function, we have to use 'global' keyword again
        global host
        global port

        global s  # the variable for our socket

        print ("Binding the Port" + str(port))

        # this double bracket format is known as tuple in python
        s.bind((host, port))

        # now server will listen for connections and tolerate a maximum of 5 bad connections before throwing an error
        s.listen(5)

    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")

        # recursive function call (will try and bind again)
        bind_socket()