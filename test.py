#all important imports

from flask import Flask,request, json, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from sqlalchemy import desc, and_, or_, func
#func for aggregation in sql

from sqlalchemy.exc import IntegrityError
from settings import db,app
from datetime import date
import datetime
# app = Flask(__name__)
# db = SQLAlchemy(app)
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# POSTGRES = {
    # 'user': 'okdddtuimwkwre',
    # 'pw': ######,
    # 'db': 'd4g0u6alpfr93h',
    # 'host': 'ec2-107-22-160-199.compute-1.amazonaws.com',
    # 'port': '5432',
# }

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://okdddtuimwkwre:######@ec2-107-22-160-199.compute-1.amazonaws.com:5432/d4g0u6alpfr93h' % POSTGRES
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
	# if 'username' in session:
		# username = session['username']
		# return 'Logged in as ' + username +"<br /><b><a href='/logout'>click here to log out</a></b>"
	# return "You are not logged in <br><a href='/login'><b>click here to log in</b></a>"
	return render_template('login.html')

@app.route('/login',  methods=['POST'])
def login():
	
	username = request.form['username']
	password = request.form['password']
	
	if 'user' in session:
		session.pop('user', None)
	
	from database import Admin
	obj = Admin.query.filter(and_(Admin.username == username, Admin.password == password)).first()
	
	if obj != None:
		session['user'] = username
		return redirect(url_for('home'))
	else:
		claim = "Wrong Username or Password!!"
		return redirect(url_for('index'))
	

@app.route('/logout')
def logout():
	# remove the username from the session if it is there
	session.pop('user', None)
	return redirect(url_for('index'))			
			

@app.route('/home')
def home():
	# remove the username from the session if it is there
	#session.pop('username', None)
	if 'user' in session:
		username = session['user']
	return "Successfully Loged in as " + username

	
			
@app.route('/signUp')
def signUp():
    return render_template('ajax_test.html')

@app.route('/add_user', methods=['POST'])
def add_user():
	if 'user' in session:
		if session['user'] == 'Admin' :
			
			from database import Admin
			
			username = request.form['username']
			password = request.form['password']
			user = Admin(username, password)
			db.session.add(user)
			db.session.commit()
			return "New User named" + username + "and with password " + password + "successfully created!"
		else :
			return "You are not an Admin and so you can't Add a new User! Sorry!"
	else:
		return redirect(url_for('index'))
	
@app.route('/select')
def select_test():
    return render_template('select.html')	

	

	
@app.route('/signUpUser', methods=['POST'])
def signUpUser():
	#To register a user/admin 
	# Can be added only by the admin ad no other person has this privilege
	user =  request.form['username'];
	password = request.form['password'];
	
	all = Test.query.all()#returns  a list of objects
	
	
    #return json.dumps({'status':'OK','user':user,'pass':password});
	#list_of_data = ['abc','def','xyz']
	list_of_data = [[k.email, k.username] for k in all] 
	
	#return jsonify(list_of_data = list_of_data)
	return json.dumps(list_of_data)

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
	

@app.route('/get_list_of_products', methods=['GET'])
def list_of_products():
	#<form action = {{ url_for('list_of_products') }} method = 'POST' >
	#returns the list of products as a list of string! ex:occurence = ttani
	#occurrence = request.form['occurrence']
	occurrence = request.args.get('occurrence')
	#occurence = request.args.get('nn')
	from database import Product
	all_products = Product.query.all()
	#list_of_products = [[k.p_name, k.pid, k.p_price, k.p_category, k.p_sub_category] for k in all_products]
	#filtered_list = list(filter(lambda k: occurrence in k[0] ,list_of_products))
	
	filtered_list = {k.p_name: [k.pid, k.p_price, k.gst, k.p_category, k.p_sub_category] for k in all_products if occurrence in k.p_name}
	
	# //output -> ["krittania", "brittania"]
	#print(filtered_list)
	
	return json.dumps(filtered_list)	

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

@app.route('/filter_products')
def filter_products():
	return render_template('product_filter.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

@app.route('/all_products_filter', methods=['POST'])
def all_products_filter():
	stocks_gt = request.form['stock_gt']
	stocks_lt = request.form['stock_lt']
	category  = request.form['category']
	
	print(stocks_gt, stocks_lt, category)
	from database import Product, Stock
	#all_products = Product.query.filter_by().all()
	all_products = Product.query.all()
	#.with_entities()
	

	if(category == 'ANY'):
		q = Product.query
	else :
		q = Product.query.filter_by(p_category = category)
	if( stocks_gt != '-1'):
		q = q.join(Stock).filter(Stock.stocks_left >= stocks_gt)
	else:
		q = q.join(Stock)
	if( stocks_lt != '-1'):
		q = q.filter(Stock.stocks_left <= stocks_lt)
		
	q = q.with_entities(Product, Stock).all()
	
	products = {k[0].pid:[k[0].p_name, k[0].p_category, k[0].p_sub_category, k[0].p_price, k[0].gst, k[1].stocks_left] for k in q}
	
	#return render_template('filter_test.html', products = q)	
	return json.dumps(products)
	
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

@app.route('/fetch_suppliers')
def fetch_suppliers():
	from database import  Supplier
	lst = Supplier.query.all()
	supp = { k.s_name : k.sid for k in lst}
	return json.dumps(supp)
	
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

@app.route('/get_bills')#, methods=['GET'])	
def get_bills():
	# still have to pass the query result list to a html page to display bill details
	# to know the products involved in the bill ....use next funtion
	
 	# start_year = request.form['start_year']
	# start_month=request.form['start_month']
	# start_day = request.form['start_day']
	# end_year = request.form['end_year']
	# end_month = request.form['end_month']
	# end_day = request.form['end_day']
	
	#request.form['year']
	start = date(year=2017,month=11,day=18)
	end = date(year=2017,month=11,day=18)
	
	from database import Bills
	
	bills = Bills.query.filter(Bills.bill_date <= end).filter(Bills.bill_date >= start).all()
	
	print(bills)
	return "success"

@app.route('/get_details_of_bill')#, methods=['GET'])		
def get_details_of_bill():	
	
	#Gets details of the bill, i.e its products and cost of each product and quantity
	
	#bill_no = request.form['bill_id']
	bill_no = 2
	from database import Transactions, Product, Bills
	
	#q = Transactions.query.join(Product).filter(and_(Product.pid = Transactions.pid,Transactions.bill_no == bill_no)).all()
	q= Transactions.query.join(Product).filter(Transactions.bill_no == bill_no).with_entities(Product, Transactions).all()
	#[(<Product p3>,<Transaction 1>),(<Product p4>,<Transaction 2>)]
	#q[0][0].p_name ------------>'CrackDisk'
	b = Bills.query.filter_by(bill_no = bill_no).first()
	#return render_template()
	return render_template('bill_details_test.html', details = q, bill = b)

@app.route('/get_sales/<string:sales>')#, methods=['GET'])		
def get_sales(sales):
	
	from database import Transactions, Product, Bills
	
	
	if sales == 'monthly' :
		sales = 30
	elif sales == 'yearly' :
		sales = 365
	else:
		sales = 7
	start_date = datetime.date.today() + datetime.timedelta(-sales)
	end_date = datetime.date.today()
	
	
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	list_bill_no = [i.bill_no for i in q]
	
	
	
	# m = Transactions.query.filter(Transactions.bill_no.in_(list)).all()
	
	# m = Transactions.query.filter(Transactions.bill_no.in_(list)).with_entities(Transactions.bill_no, func.sum(Transactions.p_price), func.sum(Transactions.quantity)).group_by(Transactions.bill_no).all()
	
	# m = Transactions.query.filter(Transactions.bill_no.in_(list)).with_entities(Transactions.bill_no,Transactions.pid, func.sum(Transactions.quantity)).group_by(Transactions.bill_no,Transactions.pid).all()
	
	# m = Transactions.query.filter(Transactions.bill_no.in_(list_bill_no)).with_entities(Transactions.pid, func.sum(Transactions.quantity)).group_by(Transactions.pid).all()
	
	n = Transactions.query.join(Product).filter(Transactions.bill_no.in_(list_bill_no)).with_entities(Transactions.pid,Product.p_name, func.sum(Transactions.quantity)).group_by(Transactions.pid, Product.p_name).all()
	# products = [i[0] for i in n]
	products = {i[0]: [i[1], i[2] ] for i in n}
	#op: { 'p3' : ['Vim',15], 'p2' : ['CrackJack',5]}
	
	
	pids = list(products)
	
	m = Product.query.filter(Product.pid.in_(pids)).with_entities(Product.pid, Product.p_price).all()
	m = {i[0]: i[1] for i in m}
	#op: {'p3' : 30, 'p2': 10}
	
	mid = Transactions.query.join(Product).filter(Transactions.bill_no.in_(list_bill_no))
	
	#to get sub_categories of the products by grouping so that it's passable to page and can be used in Pie chart 
	
	
	sub_categories = mid.with_entities(Product.p_sub_category, func.sum(Transactions.quantity)).group_by(Product.p_sub_category).all()
	categories = mid.with_entities(Product.p_category, func.sum(Transactions.quantity)).group_by(Product.p_category).all()
	
	#mid.with_entities(Product.p_category, func.sum(Transactions.quantity)).group_by(Product.p_category).all()
	return render_template('monthly_sales.html',p = products, m = m, start_date = start_date,end_date = end_date, categories = categories, sub_categories = sub_categories)

@app.route('/get_tax_details_to_file')#, methods=['GET'])
def get_tax_details_to_file():
	from database import Bills, TaxesFiled
	
	last_filled = TaxesFiled.query.order_by(desc(TaxesFiled.id)).limit(1).first()
	last_filled_date = last_filled.end
	
	#Tax collected after the last filled date
	end_date = datetime.date.today() + datetime.timedelta(-1)
	bills = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= last_filled_date).all()
	
	
	last_filled_date = last_filled_date + datetime.timedelta(1)
	return render_template('details_of_tax.html',last_filled = last_filled, bills = bills, last_filled_date = last_filled_date)
	
	
@app.route('/file_taxes')#, methods=['GET'])
def file_taxes():
	from database import Bills, TaxesFiled
	
	start_date = datetime.date.today() + datetime.timedelta(-365)
	end_date = datetime.date.today() + datetime.timedelta(-1)
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	gst_list = [i.gst for i in q]
	
	total_gst = sum(gst_list)
	
	get_last_tax = TaxesFiled.query.order_by(desc(TaxesFiled.id)).limit(1).first()
	get_last_filed_date = get_last_tax.end
	
	if get_last_filed_date > start_date:
		return "you have Already filed the taxes for the year!"
	
	start_date = get_last_tax.start
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	gst_list = [i.gst for i in q]
	total_gst = sum(gst_list)
	
	tax = TaxesFiled(start_date, end_date, total_gst)
	
	db.session.add(tax)
	db.session.commit()
	
	return "Success"

@app.route('/add_user_page')
def add_user_page():
	if 'user' in session and session['user'] == 'Admin':
		return render_template('add_new_user_page.html')
	else: 
		return render_template('add_new_user_fail.html')

@app.route('/add_user_request', methods=['POST'])
def add_user_request():
	if 'user' in session and session['user'] == 'Admin':
		from database import Admin
		username = request.form['username']
		password = request.form['password']
		
		new_user = Admin(username, password)
		db.session.add(new_user)
		db.session.commit()
		
		return "new user "+ Username +"added Successfully"
		#to be completed
	else:
		return render_template('add_new_user_fail.html')

if __name__ == "__main__":
    app.run()
