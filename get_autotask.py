from __future__ import print_function
import xmltodict
from datetime import datetime, timedelta
import logging
from WebDriver_config import AUTH, SOAP_URL, WSDL_URL, PROXIES
from suds.client import Client
logging.getLogger('suds.client').setLevel(logging.CRITICAL)
from suds.transport.http import HttpAuthenticated


class AutoTask:

    def __init__(self):
        pass

    def query_projects(self, maxid=0):
        t = HttpAuthenticated(
            username=AUTH['Autotask']['username'],
            password=AUTH['Autotask']['userpass'],
        )

        client = Client(
            url=WSDL_URL,
            location=SOAP_URL,
            proxy=PROXIES,
            transport=t,
            faults=False,
        )
        query = """<queryxml>
                        <entity>Project</entity>
                        <query>
                            <condition>
                                <field>Status
                                    <expression op="lessthan">5</expression>
                                </field>
                            </condition>
                            <condition>
                                <field>id
                                    <expression op="greaterthan">{}</expression>
                                </field>
                            </condition>
                        </query>
                    </queryxml>""".format(str(maxid))
        result = client.service.query(query)
        try:
            result = result[1]['EntityResults']['Entity']
            max_id = int(max([x['id'] for x in result]))
        except:
            result = []
            max_id = 0
        return (result, max_id)

    def query(self, entity, field, op, value):
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

            r = self.query('Resource', 'Email', 'equals', params['userid'])
            if hasattr(r[1].EntityResults, 'Entity'):
                userid = r[1].EntityResults.Entity[0].id
            else:
                print('Error retrieving AT ID for report.')
                return (False, False)

            # Building Array
            entityArray = client.factory.create('ArrayOfEntity')

            # Building Report
            report = client.factory.create('ExpenseReport')
            report.SubmitterID = userid
            report.Name = params['name']
            report.WeekEnding = params['weekending']
            report.id = '0'
            report.Status = 1
            report.Submit = True
            entityArray.Entity.append(report)
            # Posting Report
            x = client.service.create(entityArray)

            # Making sure it posted and getting the report id
            try:
                repid = x[1].EntityResults[0][0].id
            except Exception as e:
                print('Posting report "{}" failed.'.format(params['name']))
                print('Error retrieving user ID: {}'.format(e))
                return None
        except KeyError:
            print('Error with report "{}": {}'.format(params['name'], e))
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
        print(params['project'])
        try:
            pid = self.query('Project', 'ProjectNumber', 'equals', params['project'])
            pid = pid[1]['EntityResults']['Entity'][0]['id']
        except Exception as e:
            print('Error retrieving project for report "{}": {}'.format(params['name'], params['project']))
            return None

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
        for x in params['entries']:
            entry = client.factory.create('ExpenseItem')
            entry.ExpenseReportID = repid
            entry.id = 0
            entry.ExpenseDate = x['date']
            entry.ExpenseAmount = x['amount']
            entry.ExpenseCategory = x['expense']
            entry.HaveReceipt = True
            if x['expense'] == 2:
                entry.Miles = x['miles']
                entry.Destination = x['to']
                entry.Origin = x['from']
            entry.PaymentType = x['paytype']
            entry.BillableToAccount = True
            entry.Description = str(x['description'])
            if pid:
                entry.ProjectID = pid
            entryArray.Entity.append(entry)

        # Posting Expenses to report
        entityArray.Entity[0].id = repid
        posted = client.service.create(entryArray)
        client.service.update(entityArray)
        return posted
