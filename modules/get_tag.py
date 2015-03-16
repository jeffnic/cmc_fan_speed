__author__ = 'jeff_nichols'


import paramiko
import re
import os
import shlex

class GetSvcTag:
    def __init__(self):

        self.blah = "blah"
        self.username = "root"
        self.racCmd = "getsvctag"


    def getServiceTag(self, ip, pwd):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip, port=22, username=self.username, password=pwd)
        stdin, stdout, stderr = ssh.exec_command(self.racCmd)

        for line in stdout.readlines():
            # print line
            j = line.split("\t+")
            for item in j:
                m = re.search('^["Chassis"]',item)
                if m:
                    pass
                    # print item
                    shlexed = shlex.split(item)
                    return shlexed[1]
                    # print "IP Address: %s; Service Tag: %s" % (ip, shlexed[1])





if __name__ == "__main__":
    localRun = GetSvcTag()
    localRun.getServiceTag("10.255.0.161", "rootroot")
