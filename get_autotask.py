from __future__ import print_function
from suds.client import Client
from suds.transport.http import HttpAuthenticated
import xmltodict
from datetime import datetime, timedelta
from WebDriver_config import AUTH, SOAP_URL, WSDL_URL, PROXIES


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
            faults=False
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
            # entry.ProjectID = ?? <------------------- Need to find proj id
            entryArray.Entity.append(entry)


        # Posting Expenses to report
        posted = client.service.create(entryArray)
        return posted
