from __future__ import print_function
from collections import OrderedDict
from get_concur import Concur
from get_autotask import AutoTask
from datetime import datetime, timedelta, date
from WebDriver_config import CONCUR
import pickle
from os.path import basename
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import csv


class ExpenseReports:

    def __init__(self, user):
        self.user = user
        self.autotask = AutoTask(user)
        self.concur = Concur(user)
        self.values = CONCUR['VALUES']
        self.date_today = date.today().isoformat()
        self.log_contents = {'fields': [], 'contents': []}
        self.log_recipient = 'adelcambre@corus360.com'
        self.log_sender = 'ExpenseSync@corus360.com'


    def email_log_report(self, send_log=True):
        msg = MIMEMultipart()
        msg['Subject'] = 'Expense Sync Log - {}'.format(self.date_today)
        msg['From'] = self.log_sender
        msg['To'] = self.log_recipient

        logfile_name = 'ExpenseSync_Log_{}.csv'.format(self.date_today)

        with open(logfile_name, 'w') as logwrite:
            fieldnames = self.log_contents['fields']
            writer = csv.DictWriter(logwrite, fieldnames=fieldnames)
            writer.writeheader()
            for content in self.log_contents['contents']:
                writer.writerow(content)

        with open(logfile_name, 'rb') as logread:
            part = MIMEApplication(logread.read(), Name=basename(logfile_name))
            part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(logfile_name))
            msg.attach(part)
        if send_log:
            s = smtplib.SMTP('mail.corus360.com')
            s.sendmail(self.log_sender, self.log_recipient, msg.as_string())
            s.quit()


    def C_reports(self, params=None, getall=False):
        getresults = self.concur.getReports(params)['ReportsList']['ReportSummary']
        if getall:
            reports = [report for report in getresults]
        else:
            reports = [report for report in getresults if report['ExpenseUserLoginID'] == self.user]
        return reports


    def C_entries(self, report_ID):
        report_entries = []
        try:
            try:
                entries = self.concur.report(report_ID)['ReportDetails']['ExpenseEntriesList']['ExpenseEntry']
            except:
                entries = None
            if entries is not None and list(entries) == entries:
                report_entries.append([entry for entry in entries if self.is_billable(entry)])
                return report_entries[0]
            # If it's only one entry it the API doesn't return a list, just the entry
            else:
                try:
                    if self.is_billable(entries):
                        report_entries.append([entries])
                except IndexError:
                    return report_entries[0]
        except TypeError:
            return None
        try:
            return report_entries[0]
        except:
            return report_entries


    def AT_post(self, expensereport, entries, test=False):
        d = datetime.strptime(expensereport['ReportDate'], '%Y-%m-%dT%X')
        while d.weekday() != 5:
            d += timedelta(1)
        entry_output = {
            'name': expensereport['ReportName'],
            'weekending': str(d),
            'entries': [],
        }
        if entries is not None:
            for entry in entries:
                for y in self.values['alias'].keys():
                    if entry['ExpenseTypeName'] in self.values['alias'][y]:
                        expense = self.values['ExpenseCategory'][y]
                entry_output['entries'].append({
                    'amount': entry['TransactionAmount'],
                    'expense': expense,
                    'paytype': 5,
                    'description': entry['VendorDescription'],
                    'date': entry['TransactionDate'],
                })
        else:
            entry_output['entries'] == []
        if entry_output['entries'] == []:
            print("No billable entries.\n")
            return None
        if test:
            categories = {v: k for k, v in self.values['ExpenseCategory'].viewitems()}
            for e in entry_output['entries']:
                print("{} - ${}".format(categories[e['expense']], round(float(e['amount']), 2)))
            print('\n')
        else:
            return self.autotask.post(entry_output)


    def AT_billableProjects(self):
        projs = self.autotask.query('Project', 'Status', 'Equals', '2')
        billable_list = []
        for project in projs[1].Entity:
            expense_category = project.UserDefinedFields.UserDefinedField[2].Value
            if int(expense_category) == 2:
                print('yes')
                billable_list.append(project)
        return billable_list


    def save_report(self, report_id):
        with open('ids.pkl', 'r+') as id_pickle:
            data = pickle.load(id_pickle)
        with open('ids.pkl', 'w+') as id_pickle:
            data.append(report_id)
            pickle.dump(data, id_pickle)


    def report_is_saved(self, report_id):
        with open('ids.pkl', 'r') as id_pickle:
            data = pickle.load(id_pickle)
            return report_id in data


    def is_billable(self, entry):
        if entry['ExpenseTypeName'] in ['Parking', 'Car Rental', 'Airfare', 'Transportation', 'Hotel']:
            return True
        return False


    def reset_pickle(self):
        empty = []
        with open('ids.pkl', 'w') as id_pickle:
            pickle.dump(empty, id_pickle)


    def main(self, testing=False, get_all=False, email_log=True):
        back_date = (datetime.today() - timedelta(days=1)).isoformat()
        report_filter = {'modifiedafterdate': back_date}

        with self.concur.token_manager():

            if not get_all:
                report_filter = {}

            concur_reports = self.C_reports(
                                params=report_filter,
                                getall=get_all,)

            sync_ids = list(filter(
                            lambda x: not self.report_is_saved(x),
                            [rep['ReportId'] for rep in concur_reports]))    

            report_dict = {r['ReportId']: r 
                            for r in concur_reports 
                            if r['ReportId'] in sync_ids}

            for num, reportid in enumerate(sync_ids):
                print("Report #{} - {}".format(num, report_dict[reportid]['ReportName']))
                print(report_dict[reportid])
                self.log_contents['fields'] = list(report_dict[reportid])
                self.log_contents['contents'].append(report_dict[reportid])
                self.AT_post(
                    report_dict[reportid], 
                    self.C_entries(reportid),
                    test=testing)

        self.email_log_report(send_log=email_log)


if __name__ == '__main__':
    exp = ExpenseReports("devops@corus360.com")
    exp.reset_pickle()
    exp.main(
        testing=True, 
        get_all=True, 
        email_log=True
        )

