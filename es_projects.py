from __future__ import print_function
from get_autotask import AutoTask
from get_concur import Concur
from datetime import datetime, timedelta
from WebDriver_config import CONCUR
import ssl
import requests

# Both [x]_projects() functions return a list of tuples in this format: (PROJECT NAME, PROJECT NUMBER)

def c_projects():
    concur = Concur()
    with concur.token_manager():
        nextpage = 1
        projects = []
        while nextpage:
            if nextpage == 1:
                p = concur.projects()
            else:
                p = concur.projects(offset=nextpage)
            projects += [(i['Name'].upper(), i['Level1Code']) for i in p['ListItems']['Items']['ListItem']]
            nextpage = p['ListItems']['NextPage']
            if str(nextpage) != nextpage:
                nextpage = None
    return projects


def a_projects():
    auto = AutoTask()
    q = auto.query_projects(maxid=0)
    projects = []
    for x in [i for i in q[0] if is_svd(i)]:
        projects.append((x['ProjectName'].upper(), x['ProjectNumber']))
    return projects


def is_svd(p):
    # Checks if AT project department is Prof. Service Delivery & Operations (id 29708067)
    try:
        return int(p['Department']) == 29708067
    except:
        return False


def c_project(p):
    concur = Concur()
    with concur.token_manager():
        print(concur.headers())
        print(concur.post_project(p))


def copy_projects():
    c_project(("STEWART & STEVENSON (NB) REPLICATION", "P20160801.0002"))
    

if __name__ == '__main__':
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    copy_projects()