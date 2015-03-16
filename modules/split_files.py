__author__ = 'root'


import os

class SeparateFile:
    def __init__(self):
        self.count = 0
        self.pathRoot = "/code/cmc_fan_speed/data"
        self.list1 = []


    def createUniqList(self,filename):
        tempList = []
        list = open(os.path.join(self.pathRoot,filename)).readlines()
        # print list
        for item in list:
            lineSplit = item.split(",")
            tempList.append(lineSplit[6])
        uniqList = sorted(set(tempList))

        self.matchLine(uniqList, filename, list)


    def matchLine(self, unique, filename, list):


        with open(os.path.join(self.pathRoot,filename),"r") as infile:

            index = 0
            while index < len(unique) - 1:
                print "generating unique lists, please be patient"
                for item in unique:
                    tempNamex = str(unique[index] + "x")
                    tempNamey = str(unique[index] + "y")

                    print "This is tempname: %s" % tempNamex
                    tempNamex = []
                    print tempNamex

                    print "This is tempNamey: %s" % tempNamey
                    tempNamey = []
                    print tempNamey

                    print item
                    print "..."
                    infile.seek(0,0)

                    for line in infile:
                        lineSplit = line.split(",")
                        if lineSplit[6] == unique[index]:
                            # print unique[index]
                            tempNamex.append(unique[index])
                            tempNamey.append(lineSplit[7].strip())


                    index += 1
                    print tempNamex
                    print tempNamey


'''
                    print "..."
                    infile.seek(0,0)
                    for line in infile:
                        lineSplit = line.split(",")

                        if lineSplit[6] == unique[index]:

                            try:
                                tempPath = os.makedirs(self.pathRoot + "/" + filename + "-tmp" + "/")
                                tempFile = tempPath + filename + unique[index]
                                # print tempPath
                                # print tempFile
                            except Exception as e:
                                print e

                                # continue

                            # print line
                            # print tempPath
                            # with open(tempPath, "w+") as output:
                            # with open(os.path.join(tempPath + filename + "-" + unique[index]),"a") as output:
                            #     output.write(line)
'''
                # index += 1



if __name__ == "__main__":
    localRun = SeparateFile()
    localRun.createUniqList("10.35.0.173")

