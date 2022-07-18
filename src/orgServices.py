import flask
import os
from csh_ldap import CSHLDAP, CSHMember
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata

from utils import csh_user_auth

app = flask.Flask(__name__)
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))

# instance_ro = CSHLDAP(app.config['LDAP_BIND_DN'], app.config['LDAP_BIND_PASS'], ro=True)

#https://github.com/jabbate19/Light/blob/6aa69d86b16a48e31da0911ade842e59149db9b7/website/light/__init__.py
# OIDC Authentication
CSH_AUTH = ProviderConfiguration(issuer=app.config["OIDC_ISSUER"],
                                 client_metadata=ClientMetadata(
                                     app.config["OIDC_CLIENT_ID"],
                                     app.config["OIDC_CLIENT_SECRET"]))
auth = OIDCAuthentication({'default': CSH_AUTH},
                          app)

auth.init_app(app)
app.secret_key = os.urandom(16)

@app.route('/csh-auth')
@app.route('/')
@auth.oidc_auth('default')
@csh_user_auth
def csh_auth(auth_dict=None):
    if auth_dict is None:
        return flask.redirect("/csh-auth")
    # q = User.query.get(auth_dict['uid'])
    # if q is not None:
    #     q.firstname = auth_dict['first']
    #     q.lastname = auth_dict['last']
    #     q.picture = auth_dict['picture']
    #     q.admin = auth_dict['admin']
    #     g.user = q # pylint: disable=assigning-non-slot
    # else:
    #     user = User(auth_dict['uid'], auth_dict['first'], auth_dict['last'], auth_dict['picture'], auth_dict['admin'])
    #     g.user = user # pylint: disable=assigning-non-slot
    #     db.session.add(user)
    # db.session.commit()
    # login_user(g.user)
    return flask.redirect('/home')