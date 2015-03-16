#!/usr/bin/python
# Author
# Date:
# Purpose: send command to remote system using ssh, parse output and report 

#remote_command.py -i 10.255.0.45 -u root -p password -c getfanreqinfo 

import argparse
import pexpect
import time
import shlex
from mail import Mail


def parseFanSpeed(filename):
    logFile = open(filename, 'r')
    for line in logFile:
        args = line.split()
        if len(args) > 4:
            speed = args[len(args)-1].strip()
            try:
                speed = int(speed)
            except:
                continue

#            print 'fan speed', speed        
            print args[1], 'fan speed is', speed
        
    logFile.close()
    return

commandList ={"getfanreqinfo":parseFanSpeed}

class RemoteCmd:
    
#    def __init__(self):
#        pass
    
    def argread(self, source=None):
        
        if source:
            argParseInput = shlex.split(source)
            print argParseInput,"this is argParseInput"             #debug
        else:
            argParseInput = None
        
        parser = argparse.ArgumentParser(description='remote login via ssh and run commands')
        group = parser.add_mutually_exclusive_group()
    
        group.add_argument('--ipaddress','-i', help = "remote login via ssh", required=False, type=str)
        group.add_argument('--cmc-file', '-C', help = "list of ip add", required=False, default = "cmc_ip", type=argparse.FileType('rt',0))
    
        parser.add_argument('--user', '-u', help = "username", required=False, default = "root", type=str)
        parser.add_argument('--password', '-p', help = "password", required=False, default = "calvin", type=str)
        parser.add_argument('--command', '-c', help = "command", required=False, default = "getfanreqinfo", type=str)
    #    parser.add_argument('--command', -'c', help = "command", required=False, default = "getfanreqinfo", type=str)
        args = vars(parser.parse_args(argParseInput))
#        print args, "this is args inside the argread module"
        return args
    
    def login(self, cmd=None):
        myargs = self.argread(cmd)
        print myargs, "this is myargs inside the login module"
        runflag = True
        while(runflag):
            
            # if user didn't give an ip address at cmd line, we try a file
            if  myargs["ipaddress"]:
                auth = [myargs["ipaddress"], myargs["user"], myargs["password"]]
                runflag = False
                
            else:
                line = myargs["cmc_file"].readline().strip()
                if not line:
                    break            
                auth = line.split(" ", 2)
            
            login = "ssh" + " " + auth[1] + "@" + auth[0] + " " + myargs["command"]
            print login
            ssh_newkey = 'Are you sure you want to continue connecting'
            child = pexpect.spawn(login)
            while (True):
                # add key prompt, password prompt, shell prompt, timeout, disconnect
                #      0                1               2           3         4
                #
                i = child.expect([ssh_newkey, 'password', ' \$ ', pexpect.TIMEOUT, pexpect.EOF])
                # did the host hang up on us?
                if i == 4:
                    print 'host hung-up on us'
                    print "Here is the buffer"
                    log = auth[0]+'.log'
                    print child.before, child.after
                    logFile = open(log, 'w+')
                    logFile.write(child.before)
                    logFile.close()
                    child.close()
 #                   commandList[myargs["command"]](log)
                    break
                    #return False
                # did we timeput waiting for the prompt?
                elif i == 3:
                    print 'ssh timeout'
                    print "ssh could not login, here is the buffer"
                    print child.before, child.after
                    return False
                # did we get a shell prompt - success!
                elif i == 2:
                    child.sendline(myargs["command"])
                    print child.before, child.after
                    time.sleep(5)
                    child.interact()
                    return True
                # Are we being prompted for password?
                elif i == 1:
                    child.sendline(auth[2])
                    time.sleep(2) 
                # Are we being prompted to accept the ssh key?
                elif i == 0:
                    child.sendline('yes')
                             
        return None

if __name__ == '__main__':
    
    receivers = ['jeff_nichols@dell.com']

    message = '''From: From Person <from@fromdomain.com>
    To: To Person <to@todomain.com>    
Subject: SMTP e-mail test

This is a test e-mail message.'''
    remCmd = RemoteCmd()
    remCmd.login()
    mail = Mail('from@fromdomain.com')
    mail.send(receivers, message)


#END
