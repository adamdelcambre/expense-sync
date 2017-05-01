from __future__ import print_function
import pickle
from get_concur import Concur
from get_autotask import AutoTask
from datetime import datetime, timedelta, date
from WebDriver_config import CONCUR
from es_logging import LogCSV
import ssl



if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class ExpenseReports:

    def __init__(self):
        self.autotask = AutoTask()
        self.concur = Concur()
        self.values = CONCUR['VALUES']
        self.logfile = LogCSV()
        with open('ids.pkl', 'rb') as id_pickle:
            self.report_pickle = pickle.load(id_pickle)


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
            # If it's only one entry, the API doesn't return a list, just the entry
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


    def AT_post(self, expensereport, entries):
        d = datetime.strptime(expensereport['ReportDate'].split('.')[0], '%Y-%m-%dT%X')
        while d.weekday() != 5:
            d += timedelta(1)
        entry_output = {
            'name': expensereport['ReportName'],
            'weekending': str(d),
            'userid': expensereport['ExpenseUserLoginID'],
            'entries': [],
            }
        if entries is not None:
            for entry in entries:
                try:
                    project = entry['Custom4']['Code']
                except:
                    pass
                for y in self.values['alias'].keys():
                    if entry['ExpenseTypeName'] in self.values['alias'][y]:
                        expense = self.values['ExpenseCategory'][y]
                try:
                    entry_output['entries'].append({
                        'amount': entry['TransactionAmount'],
                        'expense': expense,
                        'paytype': 5,
                        'description': entry['VendorDescription'],
                        'date': entry['TransactionDate'],
                        'project': project
                    })
                except:
                    pass
        else:
            entry_output['entries'] == []
        if entry_output['entries'] == []:
            # Skip reports with no billable project-associated entries
            return None
        self.report_pickle.append(expensereport['ReportId'])
        self.logfile.content.append({
            'ReportName': entry_output['name'],
            'User': entry_output['userid'],
            })
        return self.autotask.post(entry_output)


    def is_billable(self, entry):
        return entry['ExpenseTypeName'] in ['Parking', 'Car Rental', 'Airfare', 'Transportation', 'Hotel']


    def save_pickle(self):
        with open('ids.pkl', 'wb') as pfile:
            pickle.dump(self.report_pickle, pfile)


    def reset_pickle(self):
        with open('ids.pkl', 'wb') as id_pickle:
            pickle.dump([], id_pickle)


    def main(self, testing=False, email_log=True, day_range=1):
        back_date = (datetime.today() - timedelta(days=day_range)).isoformat()
        with self.concur.token_manager():
            c_reports = [
                r for r in self.concur.getReports({'modifiedafterdate': back_date}) if
                r['ReportId'] not in self.report_pickle]
            if testing:
                c_reports = [i for i in c_reports if i['ExpenseUserLoginID'] == "devops@corus360.com"]
            for num, report in enumerate(c_reports):
                self.AT_post(report, self.C_entries(report['ReportId']))
                if testing:
                    print("Report #{} - {}".format(num, report['ReportName']))
        self.logfile.write_csv()
        self.save_pickle()
        if email_log:
            self.logfile.send_log()


if __name__ == '__main__':
    exp = ExpenseReports()
    exp.main(
        testing=False, # searches only reports from test accounts (devops/WebAdmin) and prints to console
        email_log=True, # Emails log of posted expenses
        day_range=1, # How many days back to check for reports
        )
