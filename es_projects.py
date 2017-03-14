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
        return [(valid_string(x['name'].upper()), x['level1code']) for x in concur.projects()['list-items']['list-item']]

def a_projects():
    auto = AutoTask()
    q = auto.query_projects(maxid=0)
    projects = []
    for x in [i for i in q[0] if is_svd(i)]:
        projects.append((valid_string(x['ProjectName'].upper()), x['ProjectNumber']))
    return projects

def valid_string(s):
    repl = {
        '"': '&quot;',
        '&': '&amp;',
        '\'': '&apos;',
        '<': '&lt;',
        '>': '&gt;',
    }
    for i in ['"', '&', '\'', '<', '>']:
        if i in s:
            s = s.replace(i, repl[i])
    return s

def is_svd(p):
    # Checks if AT project department is Prof. Service Delivery & Operations (id 29708067)
    try:
        return int(p['Department']) == 29708067
    except:
        return False

def sync_projects():
    cproj = c_projects()
    aproj = a_projects()
    unsynced = [p for p in aproj if p not in cproj]
    concur = Concur()
    with concur.token_manager():
        concur.post_projects(unsynced)
        


if __name__ == '__main__':
    if hasattr(ssl, '_create_unverified_context'):
        ssl._create_default_https_context = ssl._create_unverified_context
    print(sync_projects())