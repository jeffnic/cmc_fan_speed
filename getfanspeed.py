#!/usr/bin/env python2.7
'''

script to notify Noble owners of excessive noise caused by high fan speed
racadm -r 10.255.0.161 -u root -p rootroot getfanreqinfo

 append any argument to get debug output ('python getfanspeed debug')
'''


import paramiko
import re
import shlex
import time
import os.path
from modules.mail import Mail
from modules.get_tag import GetSvcTag
import sys
import datetime




class GetFanSpeed:

    def __init__(self):
        self.command = "racadm"
        self.username = "root"
        self.password = "rootroot"
        self.racCmd = "getfanreqinfo"
        # self.racCmd = "getsvctag"
        self.setPoint = 50
        self.dataPath = "data"
        self.outliers = []  # entire list of outliers, still messy
        self.topDir = "/code/cmc_fan_speed/"

    def getFanSpeed(self):
        # now = time.strftime("%c")
        now = datetime.datetime.now()
        now =datetime.datetime.now().strftime("%Y,%m,%d,%H,%M,%S")


        # Set debug switch
        debug = False
        try:
            if sys.argv[1]:
                debug = True
                print debug
            else:
                debug = False
        except:
            pass


        with open(os.path.join(self.topDir,"cmc_ip.txt")) as machines:
            for line in machines.readlines():
                outliers = []
                machinesSplit = line.split(",")
                cmcIP = machinesSplit[0]
                cmcPwd = machinesSplit[1].strip()
                cmcOwner = machinesSplit[2].strip()

                print "-------------------"
                print "Owner: %s" % cmcOwner
                print cmcIP

                # print cmcIP
                getTag = GetSvcTag()
                try:
                    tag = getTag.getServiceTag(cmcIP, cmcPwd)
                    print tag
                    self.outliers.append(tag)
                except:
                    self.outliers.append("NOTAG")
                #insert ssh stuff here
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=cmcIP, port=22, username=self.username, password=cmcPwd)
                stdin, stdout, stderr = ssh.exec_command(self.racCmd)


                for line in stdout.readlines():
                    j = line.split("\t+")

                    for item in j:
                        with open(os.path.join(self.topDir,self.dataPath,cmcIP), "a") as file:
                            m = re.search('^[1,2,3,4,5,6,7,8,9,"Switch"]',item)
                            if m:
                                shlexed = shlex.split(item)

                            # Print to the screen if debug is on
                            #     print "This is the value of debug --> %s: " % debug
                                if debug:
                                    if len(shlexed) > 1:
                                        try:
                                            print "%s, %s, Fan Speed %d" % (shlexed[0], shlexed[1], int(shlexed[-1]))

                                        except Exception as e:
                                            continue
                                            # print e


                                # Write offenders to a file
                                if len(shlexed) > 1:
                                    try:
                                        if int(shlexed[-1]) > self.setPoint:
                                            file.write(str(now) + "," + shlexed[0] + "," + shlexed[-1] + "\n")
                                            # print "Warning, fan speed for slot %s (%s) is requesting fan speed of %d%% " % (shlexed[0], shlexed[1], int(shlexed[-1]))
                                            # self.outliers.append("--------------------" + "\n")
                                            # self.outliers.append(tag + "\n")
                                            # self.outliers.append("Warning, fan speed for slot %s (%s) is requesting fan speed of %d%% " % (shlexed[0], shlexed[1], int(shlexed[-1])))
                                            outliers.append("Warning, fan speed for slot %s (%s) is requesting fan speed of %d%% " % (shlexed[0], shlexed[1], int(shlexed[-1])))
                                            # self.emailWarning(cmcIP, shlexed[0], shlexed[1], int(shlexed[-1]))
                                    except Exception as e:
                                        # print e
                                        continue

                        file.close()

                # newoutliers is the list of outliers in each chassis
                newOutliers = "\n\n".join(outliers)
                print newOutliers

                # send emails
                # self.emailWarning(cmcIP, newOutliers, cmcOwner)

        #self.outliers is a comprehensive list.. i think
        print "self.outliers follows this"
        print self.outliers


    # def emailWarning(self,ipaddr, slot, unitName, FanSpeed):
    def emailWarning(self, ipaddr, outliers, toWhom):
        mail = Mail()
        message = "Warning for chassis %s:\n\n %s \n\n\n If fan speeds are high because of testing etc, please ignore. If fan speeds are abnormally high for no reason, please have a look - thanks!" % (ipaddr, outliers)
        # message = "Warning, slot %s in chassis %s is requesting fan speed of %d%% " % (slot, ipaddr, FanSpeed)
        try:
            mail.newmail("Fan speed warning: " + ipaddr, message, toWhom)
        except Exception as e:
            print e



if __name__ == "__main__":
    localRun = GetFanSpeed()
    localRun.getFanSpeed()


'''

new to do list:
1) only send one email per chassis
2) graph historical data, attach it to the email (maybe)
3) create a sign up web page to populate CMC info



Old to do:
done 1) need ability to loop through multiple units, probably create a list from a static file and iterate through it
n/a  2) need ability to store historical data, possibly a database so it persists through a reboot
done 3) alternative to database, store historical data in a plain file for each chassis, three columns... date, slot number, fan speed
partially done 4) create logic to "catch" offenders, create a graph or historical chart and email it to admins, later directly to the offenders.
5)
'''







