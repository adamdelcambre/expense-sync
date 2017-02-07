import pickle
from getpass import getpass


def confirmPass(site):
	while True:
		password = getpass('Enter {} Password > '.format(site))
		conf = getpass('Re-enter {} Password > '.format(site))
		if password == conf:
			print('{} authentication saved.'.format(site))
			return password
		else:
			print('Error: Passwords do not match.')


AT_username = raw_input('Enter Autotask Username > ')
AT_password= confirmPass('Enter Autotask Password >')

C_username = raw_input('Enter Concur Username > ')
C_password= confirmPass('Enter Concur Password >')


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
