import pickle
from getpass import getpass

AT_username = raw_input('Enter Autotask Username > ')
AT_password= getpass('Enter Autotask Password >')

C_username = raw_input('Enter Concur Username > ')
C_password= getpass('Enter Concur Password >')

AUTH = {
    'Autotask': {
        "username": AT_username,
        "userpass": AT_password,
    },
    'Concur': {
        "username": C_username,
        "userpass": C_password,
    },
}

with open('auth.pkl', 'w') as auth_file:
    pickle.dump(AUTH, auth_file)
