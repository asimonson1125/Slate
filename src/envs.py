import os
os.environ["LDAP_BIND_DN"] = "cinnamon"
os.environ["LDAP_BIND_PASS"] = "2UB&aL5d$24m5f2"
os.environ["OIDC_CLIENT_ID"] = "slate"
os.environ["OIDC_CLIENT_SECRET"] = "OZ6a6DYv0zkuC3kHoCMNRxZ9o86sgm5g"
os.environ["OIDC_ISSUER"] = "https://sso.csh.rit.edu/auth/realms/csh"
os.environ["SERVER_NAME"] = "localhost:8080"
os.environ["PREFERRED_URL_SCHEME"] = 'http'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'