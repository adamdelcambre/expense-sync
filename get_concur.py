from __future__ import print_function
import requests
import re
import xmltodict
from WebDriver_config import CONCUR, AUTH
from contextlib import contextmanager



def list_xml(items):
    template = """\
    <list-item>
        <name>{}</name>
        <level1code>{}</level1code>
    </list-item>"""
    batch = '\n'.join([template.format(x[0], x[1]) for x in items])
    wrapper = """
    <list-item-batch xmlns="http://www.concursolutions.com/api/expense/list/2010/02">
    {}
    </list-item-batch>"""
    return wrapper.format(batch)


class Concur:
    def __init__(self):
        self.username = AUTH['Concur']['username']
        self.password = AUTH['Concur']['userpass']
        self.key = CONCUR['KEY']
        self.url = CONCUR['REPORTS_URL']
        self.url2 = CONCUR['REPORT_URL']
        self.authurl = CONCUR['AUTH_URL']
        self.secret = CONCUR['SECRET']
        self.revokeurl = CONCUR['REVOKE_URL']
        self.token = None

    @contextmanager
    def token_manager(self):
        self.getToken()
        try:
            yield
        finally:
            self.revokeToken()

    def getToken(self):
        params = {
            'client_id': self.key,
            'client_secret': self.secret
        }
        r = requests.get(
            self.authurl,
            params=params,
            headers=self.headers(),
            auth=(self.username, self.password)
        )
        regx = re.search("<Token>(.*)</Token>", r.text)
        reqtoken = regx.groups(0)[0]
        params['code'] = reqtoken
        r = requests.get(
            self.authurl,
            headers=self.headers(),
            params=params,
            auth=(self.username, self.password)
        )
        regx = re.search("<Token>(.*)</Token>", r.text)
        if regx is not None:
            self.token = regx.groups(0)[0]
            print('Got token.')
            return regx.groups(0)[0]
        else:
            return None

    def headers(self):
        payload = {'X-ConsumerKey': self.key}
        if self.token:
            payload['Authorization'] = 'OAuth ' + self.token
        return payload

    def getReports(self, params):
        if params is None:
            params = {}
        r = requests.get(
            self.url,
            headers=self.headers(),
            params=params
        )
        return list(xmltodict.parse(r.content)['ReportsList']['ReportSummary'])

    def projects(self):
        r = requests.get(
            CONCUR['LIST_URL'] + CONCUR['PROJECT_ID'] + '/items',
            headers=self.headers(),
        )
        return xmltodict.parse(r.content)

    def post_projects(self, plist, post_type='create'):
        headers = self.headers()
        headers['Content-type'] = "application/xml"
        posted = requests.post(
            CONCUR['LIST_URL'] + CONCUR['PROJECT_ID'] + '/batch?type={}'.format(post_type),
            data=list_xml(plist),
            headers=headers,
            )
        print(posted)
        return posted.content

    def report(self, e_id):
        r = requests.get(self.url2 + e_id, headers=self.headers())
        return xmltodict.parse(r.content)

    def revokeToken(self):
        if self.token is not None:
            headers = {'Authorization': 'OAuth ' + self.token}
            params = {
                'consumerKey': self.key,
                'user': self.username
            }
            response = requests.post(
                self.revokeurl,
                headers=headers,
                params=params,
            )
            print('Revoked tokens.')
            return response.status_code
        else:
            return None

