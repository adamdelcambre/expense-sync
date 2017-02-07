import csv
import smtplib
from datetime import date
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication



LOG_FILE = 'ESLog_{}.csv'.format(date.today().isoformat())
LOG_RECIP = 'adelcambre@corus360.com'
LOG_SENDER = 'ExpenseSync@corus360.com'
LOG_SUBJ = 'Expense Sync Log'
LOG_FIELDS = ['ReportName', 'ReportId', '', 'USER']


class LogCSV:

    def __init__(self):
        self.logfile = 'ESLog_{}.csv'.format(TODAY)
        self.fields = 'asd'
        self.content = []
        self.msg = MIMEMultipart()
        self.msg['Subject'] = LOG_SUBJECT
        self.msg['From'] = LOG_SENDER
        self.msg['To'] = LOG_RECIP


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
        s.sendmail(LOG_SENDER, LOG_RECIP, self.msg.as_string())
        s.quit()

def logCSV(content):
    with open(LOG_FILE, 'wb') as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writeheader()
        for line in content:
            writer.writerow(line)
