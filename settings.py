from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

POSTGRES = {
    'user': 'okdddtuimwkwre',
    'pw': '78ae3831414769bc68dc7b281f970db0d6e24b94edc2a40462a371800c2d6b2d',
    'db': 'd4g0u6alpfr93h',
    'host': 'ec2-107-22-160-199.compute-1.amazonaws.com',
    'port': '5432',
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://okdddtuimwkwre:78ae3831414769bc68dc7b281f970db0d6e24b94edc2a40462a371800c2d6b2d@ec2-107-22-160-199.compute-1.amazonaws.com:5432/d4g0u6alpfr93h' % POSTGRES
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_REGISTERABLE'] = True
