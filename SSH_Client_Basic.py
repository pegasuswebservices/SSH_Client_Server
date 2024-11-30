import paramiko #Import the module for SSH connections

def ssh_command(ip, port, user, passwd, cmd): #Function to connnect to an SSH server and execute a command

    client = paramiko.SSHClient() #Create SSH client instance

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #Set SSH Key policy to automatically ADD the SERVER'S KEY on first time connections

    client.connect(ip, port=port, username=user, password=passwd) #Connect to the server using the provided IP, Port and credentials

    _, stdout, stderr = client.exec_command(cmd) #returns a tuple of (stdin (data input)    ,     stdout(data output,    stderr(error messages)))
                                                    # _ ,   ensures that   stdin (data input)  is ignored


#----FORMAT THE OUTPUT OF THE COMMAND WE EXECUTE ON THE SERVER----------------------------------
    output = stdout.readlines() + stderr.readlines()  #Read the output from stdout  and stderr,  concatenate them together

    if output: #if there is an output
        print('---Output---')
        for line in output: 
            print(line.strip()) #strips the whitespace from each line in the output

#-------------------------------------------------


if __name__ == '__main__': #Runs only if script is executed directly 
    import getpass #import module to securely get password input without echoing

    user = input('Username: ') #prompt user for SSH username or hostname
    password = getpass.getpass()  #prompts user for password (without echoing it)    Like how when enter   SUDO password,  the password is not shown

    ip = input('Enter SSH Server IP Address: ')  #prompt for IP Address
    port = int(input('Enter port: ')) #prompt for PORT
    cmd = input('Enter command') #prompt for command

    ssh_command(ip, port, user, password, cmd)
