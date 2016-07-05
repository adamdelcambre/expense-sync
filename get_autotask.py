from __future__ import print_function
from suds.client import Client
from suds.transport.http import HttpAuthenticated
import xmltodict
from WebDriver_config import AUTH, SOAP_URL, WSDL_URL, PROXIES


class AutoTask:

    def __init__(self, user):
        self.user = user

    def query(self, entity, field, op, value):
        t = HttpAuthenticated(
            username=AUTH['Autotask']['username'],
            password=AUTH['Autotask']['userpass'],
        )
        client = Client(
            url=WSDL_URL,
            location=SOAP_URL,
            proxy=PROXIES,
            transport=t
        )
        return client.service.query(
            xmltodict.unparse(
                {'queryxml': {
                    'entity': entity,
                    'query': {
                        'field': {
                            '#text': field,
                            'expression': {
                                '@op': op,
                                '#text': value}}}}}))

    def post(self, params):
        try:
            t = HttpAuthenticated(
                username=AUTH['Autotask']['username'],
                password=AUTH['Autotask']['userpass'],
            )

            client = Client(
                url=WSDL_URL,
                location=SOAP_URL,
                proxy=PROXIES,
                transport=t,
                faults=False
            )

            # Check if report exists first
            # check = self.query(
            # 'ExpenseReport', 'id', 'equals', params['atid'])
            # check = self.query(
            # 'ExpenseReport', 'Name', 'equals', params['name'])
            # if hasattr(check.EntityResults, 'Entity'):
            #   print 'on checking if exists'
            #   return (False, False)
            # else:
            #   pass

            # Getting user's autotask id, ending if none is found
            r = self.query('Resource', 'Email', 'equals', self.user)
            if hasattr(r.EntityResults, 'Entity'):
                userid = r.EntityResults.Entity[0].id
            else:
                return (False, False)

            # Building Array
            entityArray = client.factory.create('ArrayOfEntity')

            # Building Report
            report = client.factory.create('ExpenseReport')
            report.SubmitterID = userid
            report.Name = params['name']

            report.WeekEnding = params['weekending']
            report.id = '0'
            report.Submit = True
            report.Status = 1
            entityArray.Entity.append(report)
            # Posting
            x = client.service.create(entityArray)

            # Making sure it posted and getting the report id
            
            repid = x[1].EntityResults[0][0].id
        except KeyError:
            return (False, False)

        t = HttpAuthenticated(
            username=AUTH['Autotask']['username'],
            password=AUTH['Autotask']['userpass'],
        )

        client = Client(
            url=WSDL_URL,
            location=SOAP_URL,
            proxy=PROXIES,
            transport=t,
            faults=False
        )

        entryArray = client.factory.create('ArrayOfEntity')

        # Building Expenses
        # try:
        for x in params['entries']:
            print('Building Entry')
            entry = client.factory.create('ExpenseItem')
            entry.ExpenseReportID = repid
            entry.id = 0
            entry.ExpenseDate = x['date']
            entry.ExpenseAmount = x['amount']
            # hotel = 29685285 meals = 29685286  2 = mileage
            entry.ExpenseCategory = x['expense']
            entry.HaveReceipt = True
            # entry.GLCode = ?
            entry.AccountID = 29707842
            if x['expense'] == 2:
                entry.Miles = x['miles']
                entry.Destination = x['to']
                entry.Origin = x['from']
            entry.PaymentType = x['paytype']
            # 5 employee paid 9 company paid
            entry.BillableToAccount = True
            if x['description'] is None:
                entry.Description = 'None'
            else:
                entry.Description = x['description']
            entryArray.Entity.append(entry)
        # except:
        #   print 'on entry'
        #   return None

        # Posting
        xy = client.service.create(entryArray)
        return xy
