import csv
import smtplib
from datetime import date
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



class LogCSV:

    def __init__(self):
        self.content = []
        self.msg = MIMEMultipart()
        self.logfile = 'ESLog_{}.csv'.format(date.today().isoformat())
        self.fields = ['ReportName', 'User']
        self.msg['Subject'] = 'Expense Sync Log'
        self.msg['From'] = 'ExpenseSync@corus360.com'
        self.msg['To'] = 'adelcambre@corus360.com'


    def write_csv(self):
        with open(self.logfile, 'wb') as logwrite:
            writer = csv.DictWriter(logwrite, fieldnames=self.fields)
            writer.writeheader()
            for line in self.content:
                writer.writerow(line)


    def send_log(self):
        with open(self.logfile, 'rb') as logread:
            part = MIMEApplication(logread.read(), Name=basename(self.logfile))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(self.logfile))
            self.msg.attach(part)
        s = smtplib.SMTP('mail.corus360.com')
        s.sendmail(
            self.msg['From'], 
            self.msg['To'], 
            self.msg.as_string()
            )
        s.quit()

