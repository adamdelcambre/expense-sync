from __future__ import print_function
import requests
import re
import xmltodict
from WebDriver_config import CONCUR, AUTH
from contextlib import contextmanager


# example_parameters = {'modifiedafterdate':'2016-06-01T00:00:00'}


class Concur:
    def __init__(self, user):
        self.user = user
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
        headers = {'X-ConsumerKey': self.key}
        params = {
            'client_id': self.key,
            'client_secret': self.secret
        }
        r = requests.get(
            self.authurl,
            params=params,
            headers=headers,
            auth=(self.username, self.password)
        )
        regx = re.search("<Token>(.*)</Token>", r.text)
        reqtoken = regx.groups(0)[0]
        params['code'] = reqtoken
        r = requests.get(
            self.authurl,
            headers=headers,
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

    def getReports(self, params):
        if params is None:
            params = {}
        headers = {
            'X-ConsumerKey': self.key,
            'Authorization': 'OAuth ' + self.token
        }
        r = requests.get(
            self.url,
            headers=headers,
            params=params
        )
        return list(xmltodict.parse(r.content)['ReportsList']['ReportSummary'])

    def lists(self, offset=None, params=None):
        # Currently unused - needed for transferring projects from AT to concur, but not yet implemented
        headers = {
            'X-ConsumerKey': self.key,
            'Authorization': 'OAuth ' + self.token
        }
        if offset:
            r = requests.get(
                offset,
                headers=headers,
            )
        else:
            r = requests.get(
                CONCUR['LIST_URL'],
                headers=headers,
                params=params,
            )
        print(r.url)
        return xmltodict.parse(r.content)

    def report(self, e_id):
        headers = {
            'X-ConsumerKey': self.key,
            'Authorization': 'OAuth ' + self.token
        }
        r = requests.get(self.url2 + e_id, headers=headers)

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

