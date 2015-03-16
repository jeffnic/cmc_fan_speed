#!/usr/bin/env python

import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt
import shutil

dataPath = "/code/cmc_fan_speed/data/"
fileName = "10.35.0.0"


class PlotFanSpeed:

    def __init__(self):
        self.x = []
        self.y = []

    def plot(self):
        with open(os.path.join(dataPath,fileName)) as file:
            for line in file:
                lineSplit = line.split(",")
                # print lineSplit[1]
                if lineSplit[1] == "1":
                    self.x.append(lineSplit[0])
                    self.y.append(lineSplit[2].strip())
        print self.x
        print self.y


        plt.plot(self.x, self.y)
        plt.title("Fan speed for 10.35.0.0")
        plt.xlabel("server name")
        plt.ylabel("fan speeds")

        plt.savefig(os.path.join(dataPath,fileName + ".png"))
        fName = os.path.join(dataPath,fileName + ".png")
        self.fileCopy(fName)



    def fileCopy(self,fName):

        try:
            print "copying files"
            shutil.copy(fName, '/var/www/html/fan_speeds/file.png')
        except Exception as e:
            print e

if __name__ == "__main__":
    localRun = PlotFanSpeed()
    localRun.plot()


'''
    works with numeric data - for example
(my27)[root@donkeykong modules]# cat ../data/10.35.0.0
1.15,1,30
1.30,1,45
1.45,1,55
2,1,67
2.15,1,23
2.30,1,56
2.45,1,90
3,1,34
3.15,1,87



import matplotlib
matplotlib.use('Agg')
import os
import matplotlib.pyplot as plt

dataPath = "/code/cmc_fan_speed/data/"
fileName = "10.35.0.1"



class PlotFanSpeed:

    def __init__(self):
        self.x = []
        self.y = []

    def plot(self):
        with open(os.path.join(dataPath,fileName)) as file:
            for line in file:
                lineSplit = line.split(",")
                # print lineSplit[1]
                if lineSplit[1] == "1":
                    self.x.append(lineSplit[0])
                    self.y.append(lineSplit[2].strip())
        print self.x
        print self.y


        plt.plot(self.x, self.y)
        plt.title("Fan speed for 10.35.0.0")
        plt.xlabel("server name")
        plt.ylabel("fan speeds")

        plt.savefig(os.path.join(dataPath,fileName + ".png"))


if __name__ == "__main__":
    localRun = PlotFanSpeed()
    localRun.plot()
'''