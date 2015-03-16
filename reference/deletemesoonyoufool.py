import paramiko
import re
import shlex

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="10.255.0.161", port=22, username="root", password="rootroot")
stdin, stdout, stderr = ssh.exec_command("getfanreqinfo")


for line in stdout.readlines():

    j = line.split("\t+")

    for item in j:
        m = re.search('^[1,2,3,4,5,6,7,8,9,"Switch"]',item)
        # print m
        if m:
            # print item.strip()
            shlexed = shlex.split(item)
            if len(shlexed) > 1:
                # print shlexed[0] + shlexed[1] + shlexed[-1]
                try:
                    print "%s, %s, Fan Speed %d" % (shlexed[0], shlexed[1], int(shlexed[-1]))
                except Exception as e:
                    continue
                    print e

print "--------------------"


# import spur
# shell = spur.SshShell(hostname="10.32.19.206", username="root", password="Dell123", port=22, missing_host_key=spur.ssh.MissingHostKey.accept)
# result = shell.run(["echo", "-n", "hello"])
# print result.output # prints hello
# print "--------------------------"