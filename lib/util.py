import getpass
import ldap3
import ssl


BASE = 'dc=chaotikum,dc=org'
SERVER = 'ldaps://ldap.chaotikum.net'
ADMIN = 'cn=admin,' + BASE


def connect():
	server = ldap3.Server(SERVER)
	server.tls.validate = ssl.CERT_REQUIRED

	password = getpass.getpass('Login as %s: ' % ADMIN)
	if password == '':
		return None

	connection = ldap3.Connection(server, user=ADMIN, password=password)

	if not connection.bind():
		return None

	return connection

def user_exists(c, username):
    return c.search(search_base=BASE, search_filter='(&(objectClass=posixAccount)(uid=%s))' % username)

def change_password(c, userdn, password):
	try:
		c.extend.standard.modify_password(userdn, new_password=password)
		return True
	except:
		return False

def add_group(c, username, groupname):
	if not user_exists(c, username):
		print('User \'%s\' not found.', group)
		return False

	if not c.search(search_base=BASE, search_filter='(&(objectClass=posixGroup)(cn=%s))' % groupname):
		print('Group \'%s\' not found.', group)
		return False

	groupdn = c.response[0]['dn']

	return c.modify(groupdn, {'memberUid': [(ldap3.MODIFY_ADD, [username])]})
