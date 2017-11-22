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

@app.route('/bill_fill')
def bill_form():
	return render_template('bill_form.html')

@app.route('/bill_fill_backend', methods = ['POST'])
def bill_form_backend():
	from database import Bills, Product, Stock, Customer, Transactions
	
	products = request.form.getlist('product[]')	
	qty = request.form.getlist('qty[]')
	cost = request.form.getlist('cost[]')
	cgst = request.form.getlist('cgst[]')
	sgst = request.form.getlist('sgst[]')
	total = request.form.getlist('total[]')
	gst = request.form['gst']
	
	length = len(products)
	bill_amt = sum(map(float, total))
	
	c = Customer.query.filter_by(cid = 'NONE').first()
	c_name = c.c_name
	
	
	
	bill = Bills(3, length, bill_amt, gst,-1, c_name ,c , 'NONE', 'NONE', 'NONE')
	for i in range(length):
		prod = Product.query.filter_by(p_name = products[i]).first()
		t = Transactions(bill, prod, cost[i],sgst[i],cgst[i], qty[i], total[i]);
		s = Stock.query.filter_by(pid = prod.pid).first()
		s.stocks_left = s.stocks_left - int(qty[i])
		db.session.add(t)
		db.session.commit()
		
	db.session.add(bill)
	db.session.commit()
	
	print(products, qty, cgst, sgst, total)
	return "success!"

@app.route('/all_products')
def all_products():
	
	from database import Product
	all_products = Product.query.all()
	return render_template('products_test.html', products = all_products)

#@app.route('/all_suppliers', methods=['POST'])	
@app.route('/all_suppliers')
def all_suppliers():
	from database import Supplier
	
	all_suppliers = Supplier.query.all()
	return render_template('supplier_test.html', suppliers = all_suppliers)


@app.route('/all_products_filter', methods=['POST'])
def all_products_filter():
	stocks_gt = request.form['stock_gt']
	stocks_lt = request.form['stock_lt']
	category  = request.form['category']
	
	from database import Product, Stock
	#all_products = Product.query.filter_by().all()
	all_products = Product.query.all()
	#.with_entities()
	if(category == any):
		q = Product.query
	else :
		q = Product.query.filter_by(p_category = category)
	if( stocks_lt != -1):
		q = Product.query.join(Stock).filter(Stock.stocks_left <= stocks_lt)
	if( stocks_gt != -1):
		q = Product.query.join(Stock).filter(Stock.stocks_left >= stocks_gt)
	q = q.all()
	
	
	return render_template('filter_test.html', products = q)

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
	from database import Supplier, Supplier_product
	#try:
	
		
	s_name = request.form['name']
	s_contact_name = request.form['contact']
	s_number = request.form['mobile_no']
	s_address = request.form['address']
	
	sid = Supplier.query.order_by(desc(Supplier.sid)).limit(1).all()
	sid = sid[0]
	sid = sid.sid 
	prefix = sid[:1]
	postfix = int(sid[1:])
	postfix = postfix + 1
	sid = prefix + str(postfix)
		
	#Create a Supplier object to insert into the Supplier table
	supplier = Supplier(sid, s_name, s_contact_name, s_number, s_address)
	
	db.session.add(supplier)
	db.session.commit()
		
	return 'Supplier record added successfully'
	
	'''
	except IntegrityError:
		db.session.rollback()
		return "Account already exists.."
	except:
		db.session.rollback()
		return "Cannot register user..."
	'''

@app.route('/add_product', methods=['POST'])
def add_product():
	from database import Product, Supplier, Supplier_product
	#try:
	
	p_category = request.form['category']
	p_sub_category = request.form['sub_category']
	p_name = request.form['name']
	p_price = request.form['price']
	gst = request.form['gst']
	product_base_margin = request.form['base_margin']
	p_sale_price = request.form['sale_price']
	sid = request.form['suppplier']
	
	pid = Product.query.order_by(desc(Product.pid)).limit(1).all()
	pid = pid[0]
	pid = pid.pid 
	prefix = pid[:1]
	postfix = int(pid[1:])
	postfix = postfix + 1
	pid = prefix + str(postfix)
		
	#Create a product object to insert into the Product table
	product = Product(pid, p_category, p_sub_category, p_name, p_price,product_base_margin, p_sale_price, sid)
	
	#get supplier obj from database 
	supp = Supplier.query.filter_by(sid = sid).first()
	supplier_product = Supplier_product( product, supp)
	
	db.session.add(product)
	db.session.add(supplier_product)
	
	db.session.commit()
		
	return 'product record added successfully'
@app.route('/fetch_categories')
def fetch_categories():
	from database import Product, Stock
	lst = Product.query.distinct(Product.p_category).all()
	category_lst = [k.p_category for k in lst]
	return json.dumps(category_lst)

@app.route('/fetch_sub_categories', methods=['GET'])
def fetch_sub_categories():
	category = request.args.get('val')
	
	from database import Product, Stock
	lst = Product.query.filter_by(p_category = category).distinct(Product.p_sub_category).all()
	category_lst = [k.p_sub_category for k in lst]
	return json.dumps(category_lst)

@app.route('/fetch_products', methods=['GET'])
def fetch_products():
	category = request.args.get('val1')
	sub_category = request.args.get('val2')
	
	from database import Product, Stock
	lst = Product.query.filter_by(p_category = category).filter_by(p_sub_category = sub_category).all()
	category_lst = [[k.p_name,k.pid] for k in lst]
	return json.dumps(category_lst)	
if __name__ == "__main__":
    app.run()