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

        print ("Binding the Port: " + str(port))

        # this double bracket format is known as tuple in python
        s.bind((host, port))

        # now server will listen for connections and tolerate a maximum of 5 bad connections before throwing an error
        s.listen(5)

    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\n" + "Retrying...")

        # recursive function call (will try and bind again)
        bind_socket()


#  Function to establish connection with a client (assuming the socket is listening already)
def accept_socket():

    # s.accpet() outputs an object of the connection or conversation
    # as well as a second output which is a list containing IP address and a port
    # so we initialized two new variables to hold each of these outputs
    conn, address = s.accept()

    # print out first element of the list (ip address) and the second element which is the port number of the client
    print("Connection has been established! |" + " IP " + address[0] + " | Port" + str(address[1]))

    # once connection has been established we can send commands over this connection to the client (other computer)
    # done through another custom function called send_commands (defined below)
    send_commands(conn)
    conn.close() # after socket has been established, we need to close the connection

# Function to send commands to client computer
def send_commands(conn):

    # conduct infinite while loop allowing us to send multiple commands before connection gets closed
    while True:
        # takes input from command prompt
        cmd = input()

        # if command is to quit
        if cmd == 'quit':
            conn.close()
            s.close()
            # remembering to close the command prompt as well
            sys.exit()

        # anything travelling over the connection between 2 computers is sent in bytes
        # to actually know if the user typed something into the command prompt we need to encode to bytes
        # and check if the length of that byte string is > 0. if it is, this means a command has been entered into cmd
        if len(str.encode(cmd)) > 0:
            # to send messages got to be converted from string to bytes
            conn.send(str.encode(cmd))
            # to receive messages got to be converted from bytes to string
            # in this case using the encoding format of utf-8 and in chunks of 1024 bits
            client_response = str(conn.recv(1024),"utf-8")

            # end="" basically allows the command prompt to go to the next line after generating output (as it would)
            print(client_response, end="")

def main():
    create_socket()
    bind_socket()
    accept_socket()

main()