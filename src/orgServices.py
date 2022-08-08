import flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from csh_ldap import CSHLDAP
from flask_pyoidc.flask_pyoidc import OIDCAuthentication
from flask_pyoidc.provider_configuration import ProviderConfiguration, ClientMetadata
from flask_login import login_user, logout_user, LoginManager
import pytz

from utils import csh_user_auth

app = flask.Flask(__name__)
app.config.from_pyfile(os.path.join(os.getcwd(), "config.py"))

# time setup for the server side time
eastern = pytz.timezone('America/New_York')

# LDAP instance init
ldap = CSHLDAP(app.config['LDAP_BIND_DN'],
               app.config['LDAP_BIND_PASS'], ro=True)

# https://github.com/jabbate19/Light/blob/6aa69d86b16a48e31da0911ade842e59149db9b7/website/light/__init__.py
# OIDC Authentication
CSH_AUTH = ProviderConfiguration(issuer=app.config["OIDC_ISSUER"],
                                 client_metadata=ClientMetadata(
                                     app.config["OIDC_CLIENT_ID"],
                                     app.config["OIDC_CLIENT_SECRET"]))
auth = OIDCAuthentication({'default': CSH_AUTH},
                          app)

auth.init_app(app)
app.secret_key = os.urandom(16)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'csh_auth'


@login_manager.user_loader
def load_user(user_id):
    q = User.query.get(user_id)
    if q:
        return q
    return None


@app.route("/logout")
@auth.oidc_logout
def _logout():
    logout_user()
    return flask.redirect("/", 302)


@app.route('/csh_auth')
@app.route('/')
@auth.oidc_auth('default')
@csh_user_auth
def csh_auth(auth_dict=None):
    if auth_dict is None:
        return flask.redirect("/csh_auth")
    user = User.query.get(auth_dict['uid'])
    if user is not None:
        user.firstname = auth_dict['first']
        user.lastname = auth_dict['last']
        user.picture = auth_dict['picture']
        user.admin = auth_dict['admin']
    else:
        user = User(auth_dict['uid'], auth_dict['first'],
                    auth_dict['last'], auth_dict['picture'], auth_dict['admin'])
        db.session.add(user)
    db.session.commit()
    login_user(user)
    return flask.redirect('/in')
