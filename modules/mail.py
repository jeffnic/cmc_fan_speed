


''' from http://www.tutorialspoint.com/python/python_sending_email.htm
'''
import smtplib
from smtplib import SMTPException

class Mail:

    def sendmail(self,message):

        sender = 'from_dk@smd.devops.dell.com'
        receivers = ['jeff_nichols@dell.com']
        message = message
        msg['Subject'] = subject

        try:
            smtpObj = smtplib.SMTP('pgh-smtp.us.dell.com')
            smtpObj.sendmail(sender, receivers, message)
            print "Sucess: Mail sent"
        except SMTPException:
            print "Error: Mail not sent"


# from http://stackoverflow.com/questions/7232088/python-subject-not-shown-when-sending-email-using-smtplib-module

# message = 'Subject: %s\n\n%s' % (SUBJECT, TEXT)
# and then:
# server = smtplib.SMTP(SERVER)
# server.sendmail(FROM, TO, message)
# server.quit()

    def newmail(self, subject,body,recipient):

        # subject = "This is a subject"
        # body = "This is text and stuff"
        SERVER = "pgh-smtp.us.dell.com"
        FROM = "dk@smd"
        TO = recipient

        message = 'Subject: %s\n\n\n%s' % (subject, body)
        server = smtplib.SMTP(SERVER)
        server.sendmail(FROM, TO, message)
        server.quit()


if __name__ == "__main__":
    localRun = Mail()
    localRun.newmail()
