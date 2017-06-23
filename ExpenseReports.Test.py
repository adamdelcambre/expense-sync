from __future__ import print_function
import pickle
from get_concur import Concur
from get_autotask import AutoTask
from datetime import datetime, timedelta, date
from WebDriver_config import CONCUR
from es_logging import LogCSV
import ssl
import os
import sys



if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class ExpenseReports:

    def __init__(self):
        self.autotask = AutoTask()
        self.concur = Concur()
        self.logfile = LogCSV()
        self.idpkl = os.path.join(os.path.dirname(__file__), 'ids.pkl')
        with open(self.idpkl, 'rb') as id_pickle:
            self.report_pickle = pickle.load(id_pickle)


    def billable_entries(self, report):
        '''
        Takes a list of entries as retrieved from Concur as input 
        and outputs a list of the entries in that list are billable
        '''
        entries = report['ExpenseEntriesList']['ExpenseEntry']
        # If it's only one entry, the API doesn't return a list, just the entry
        if type(entries) is not list:
            entries = [entries] # Puts single entries into a list
        report_entries = []
        nonbillable_types = [
            'Personal Car Mileage', 
            'Business Meals', 
            'Entertainment - Client',
            'Entertainment - Staff',
            'Professional Subscriptions/Dues',
            'Tuition/Training Reimbursement',
            ]
        for entry in entries:
            if entry['ExpenseTypeName'] not in nonbillable_types:
                if entry['Custom4'] is not None:
                    report_entries.append(entry)
        return report_entries


    def AT_post(self, expensereport):
        d = datetime.strptime(expensereport['ReportDate'].split('.')[0], '%Y-%m-%dT%X')
        while d.weekday() != 5:
            d += timedelta(1)

        entry_output = {
            'name': expensereport['ReportName'],
            'weekending': str(d),
            'userid': expensereport['UserLoginID'],
            'entries': [],
            }

        entries = self.billable_entries(expensereport)
        if len(entries) > 0:
            for entry in entries:
                try:
                    category = CONCUR['VALUES']['alias'][entry['ExpenseTypeName']]
                except KeyError:
                    category = CONCUR['VALUES']['alias']['Other']
                entry_output['entries'].append({
                    'amount': entry['TransactionAmount'],
                    'expense': CONCUR['VALUES']['ExpenseCategory'][category],
                    'description': entry['VendorDescription'],
                    'date': entry['TransactionDate'],
                    'project': entry['Custom4'].get('Code', None),
                    'billable': entry['Custom6'].get('Value', False) == u'Customer Billable',
                })
        else:
            return None

        self.report_pickle.append(expensereport['ReportID'])
        self.logfile.content.append({
            'ReportName': entry_output['name'],
            'User': entry_output['userid'],
            })
        return self.autotask.post(entry_output)


    def save_pickle(self):
        with open(self.idpkl, 'wb') as pfile:
            pickle.dump(self.report_pickle, pfile)


    def reset_pickle(self):
        with open(self.idpkl, 'wb') as id_pickle:
            pickle.dump([], id_pickle)


    def main(self, testing=False, email_log=True, day_range=1):
        back_date = (datetime.today() - timedelta(days=day_range)).isoformat()
        with self.concur.token_manager():
            c_reports = [
                r for r in self.concur.getReports({'modifiedafterdate': back_date}) if
                r['ReportId'] not in self.report_pickle]
            for report in c_reports:
                self.AT_post(self.concur.report(report['ReportId'])['ReportDetails'])
        self.logfile.write_csv()
        self.save_pickle()
        if email_log:
            self.logfile.send_log()


if __name__ == '__main__':
    exp = ExpenseReports()
    exp.main(
        email_log=True, # Emails log of posted expenses 
        day_range=1, # How many days back to check for reports
        )
