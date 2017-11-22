#all important imports

from flask import Flask,request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from sqlalchemy import desc, and_, or_, func
#func for aggregation in sql

from sqlalchemy.exc import IntegrityError
from settings import db,app
from datetime import date

# app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# POSTGRES = {
    # 'user': 'okdddtuimwkwre',
    # 'pw': '78ae3831414769bc68dc7b281f970db0d6e24b94edc2a40462a371800c2d6b2d',
    # 'db': 'd4g0u6alpfr93h',
    # 'host': 'ec2-107-22-160-199.compute-1.amazonaws.com',
    # 'port': '5432',
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://okdddtuimwkwre:78ae3831414769bc68dc7b281f970db0d6e24b94edc2a40462a371800c2d6b2d@ec2-107-22-160-199.compute-1.amazonaws.com:5432/d4g0u6alpfr93h' % POSTGRES
# app.config['SECRET_KEY'] = 'super-secret'
# app.config['SECURITY_REGISTERABLE'] = True



app.debug = True


class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=False)
	age = db.Column(db.Integer)
	email = db.Column(db.String(20),unique = True)
	
	
	def __init__(self,userrname,age,email):
		
		self.username = name
		self.age = age
		self.email = email
	
	def __repr_(self):
		return '<user %r>' % self.username

#db.create_all()

'''
INSERT INTO test (id,username,age,email) VALUES (10, 'Teddy', 23, 'Teddy@bear.com');
'''

@app.route('/')
def index():
	# This is just for testing
	all = Test.query.first()
	return render_template('testing.html',all = all)

@app.route('/signUp')
def signUp():
    return render_template('ajax_test.html')	
	
	
if __name__ == "__main__":
    app.run()