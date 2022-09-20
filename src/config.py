from os import environ as env
# automatically updates some dev envs.  need to remove for production.
try:
    __import__('envs.py')
except ImportError:
    pass

# Flask config
IP = env.get('IP', '0.0.0.0')
PORT = env.get('PORT', 8080)
SERVER_NAME = env.get('SERVER_NAME', 'slate.csh.rit.edu')
PREFERRED_URL_SCHEME = env.get('PREFERRED_URL_SCHEME', 'https')

POSTGRESQL_USER = env.get('POSTGRESQL_USER', '')
POSTGRESQL_PASSWORD = env.get('POSTGRESQL_PASSWORD')
POSTGRESQL_DATABASE = env.get('POSTGRESQL_DATABASE', 'usersDB')
POSTGRESQL_IP = env.get('POSTGRESQL_IP')
SQLALCHEMY_DATABASE_URI = env.get(
    'SQLALCHEMY_DATABASE_URI', "postgresql://" + str(POSTGRESQL_USER) + ":" + str(POSTGRESQL_PASSWORD) + "@" + str(POSTGRESQL_IP) + "/" + str(POSTGRESQL_DATABASE) + "")
SQLALCHEMY_TRACK_MODIFICATIONS = 'False'
# OpenID Connect SSO config CSH
OIDC_ISSUER = env.get('OIDC_ISSUER', 'https://sso.csh.rit.edu/auth/realms/csh')
OIDC_CLIENT_ID = env.get('OIDC_CLIENT_ID', 'slate')
OIDC_CLIENT_SECRET = env.get('OIDC_CLIENT_SECRET', 'NOT-A-SECRET')

LDAP_BIND_DN = env.get(
    "LDAP_BIND_DN", default="cn=rides,ou=Apps,dc=csh,dc=rit,dc=edu")
LDAP_BIND_PASS = env.get("LDAP_BIND_PASS", default=None)

G_CLIENT_ID = env.get('G_CLIENT_ID')
G_CLIENT_SECRET = env.get('G_CLIENT_SECRET')
G_PROJECT_ID = env.get('G_PROJECT_ID')