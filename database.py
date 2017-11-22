# DATABASE
# Define SCHEMA of the DATABASE
from settings import db
from datetime import datetime
import arrow


#foreign key relationship
#backref: creates a virtual column called 'student' in 'Student_feedback' class that references the 'Student' class.


class Customer(db.Model):
	cid = db.Column(db.String(10), primary_key = True)
	c_name = db.Column(db.String(25))
	c_number = db.Column(db.String(), unique = True)
	c_email = db.Column(db.String(30))
	c_address = db.Column(db.String(50))
	city = db.Column(db.String(20))
	country = db.Column(db.String(20))
	

	ref_from_bills_for_cid = db.relationship('Bills' , backref = 'customer', lazy = 'dynamic', passive_deletes=True)
	#ref_from_transactions_for_cid = db.relationship('Transactions' , backref = 'customer', lazy = 'dynamic')
	
	def __init__(self, cid, c_name, c_number, c_email, c_address, city, country):
		self.cid = cid
		self.c_name = c_name
		self.c_number = c_number
		self.c_email = c_email
		self.c_adddress = c_adddress
		self.city = city
		self.country = country

class Supplier(db.Model):
	sid = db.Column(db.String(10), primary_key = True)
	s_name = db.Column(db.String(25))
	s_contact_name = db.Column(db.String(25))
	s_number = db.Column(db.String(10), unique = True)
	s_address = db.Column(db.String(50))
	#product_id = db.Column(db.String(10),db.ForeignKey('product.pid'))
	#product_category = db.Column(db.String(25))
	#cost_price = db.Column(db.Integer)
	
	#ref_from_product_for_sid = db.relationship('Product', backref = 'supplier', lazy = 'dynamic')
	ref_from_stock_for_sid = db.relationship('Stock', backref = 'supplier', passive_deletes=True)
	ref_from_supplier_product_for_sid = db.relationship('Supplier_product' , backref = 'supplier', passive_deletes=True)
	
	def __init__(self, sid, s_name, s_contact_name, s_number, s_adddress):
		self.sid = sid
		self.s_name = s_name
		self.s_contact_name = s_contact_name
		self.s_number = s_number
		self.s_adddress = s_adddress
		#self.product = product #this is the product object which has to be passed so that foriegn key relationship is established
		#self.product_category = product_category
		#self.cost_price = cost_price
	

		
class Stock(db.Model):
	date = db.Column(db.Date)
	pid = db.Column(db.String(10), db.ForeignKey('product.pid', ondelete = 'CASCADE'), primary_key = True)
	#p_name = db.Column(db.String(25))
	#p_price = db.Column(db.Integer)
	stocks_left = db.Column(db.Integer)
	sid = db.Column(db.String(10),db.ForeignKey('supplier.sid', ondelete='CASCADE'))
	last_shipment_arrival = db.Column(db.Date, default = arrow.now().format('YYYY-MM-DD'))
	
	# p_name, p_price,
	def __init__(self, date, product,  stocks_left, supplier):
		self.date = date
		self.product = product
		#self.p_name = p_name
		#self.p_price = p_price
		self.stocks_left = stocks_left
		self.supplier = supplier
		

class Product(db.Model):
	
	pid = db.Column(db.String(10), primary_key = True)
	p_category = db.Column(db.String(25))
	p_sub_category = db.Column(db.String(25))
	p_name = db.Column(db.String(25))
	
	p_price = db.Column(db.Integer)
	gst = db.Column(db.Integer)
	product_base_margin = db.Column(db.Integer)
	
	product_sale_price = db.Column(db.Integer)
	#product_arrival_date = db.Column(db.DateTime())
	product_arrival_date = db.Column(db.Date, default = arrow.now().format('YYYY-MM-DD'))
	sid = db.Column(db.String(10),db.ForeignKey('supplier.sid', ondelete='CASCADE'))
	
	ref_from_stock_for_pid = db.relationship('Stock' , backref = 'product', passive_deletes=True)
	ref_from_transactions_for_pid = db.relationship('Transactions' , backref = 'product', passive_deletes=True)
	ref_from_supplier_for_pid = db.relationship('Supplier' , backref = 'product', passive_deletes=True)
	ref_from_supplier_product_for_pid = db.relationship('Supplier_product' , backref = 'product', passive_deletes=True)
	
	def __init__(self, pid, p_category, p_sub_category, p_name, p_price, gst, product_base_margin, product_sale_price, supplier):
		self.pid = pid
		self.p_category = p_category
		self.p_sub_category = p_sub_category
		self.p_name = p_name
		self.p_price = p_price
		self.gst = gst
		self.product_base_margin = product_base_margin
		self.product_sale_price = product_sale_price
		#self.product_arrival_date = product_arrival_date
		self.supplier = supplier

class Transactions(db.Model):
	tid = db.Column(db.Integer,  primary_key = True)
	bill_no = db.Column(db.Integer, db.ForeignKey('bills.bill_no', ondelete='CASCADE'))
	pid = db.Column(db.String(10), db.ForeignKey('product.pid', ondelete='CASCADE'))
	
	p_price = db.Column(db.Integer)
	sgst = db.Column(db.Float)
	cgst = db.Column(db.Float)
	quantity = db.Column(db.Integer)
	product_total = db.Column(db.Float)
	#bill_date= db.Column(db.Date)
	#cid = db.Column(db.String(10), db.ForeignKey('customer.cid'))
	
	def __init__(self, bills, product, p_price, sgst, cgst, quantity, product_total):
		self.bills = bills
		self.product = product
		self.p_price = p_price
		self.sgst = sgst
		self.cgst = cgst
		self.quantity = quantity
		self.product_total = product_total

		
class Bills(db.Model):
	bill_no = db.Column(db.Integer, primary_key = True)
	bill_date = db.Column(db.Date, default = arrow.now().format('YYYY-MM-DD'))
	bill_priority = db.Column(db.Integer)
	total_item = db.Column(db.Integer)
	bill_amt = db.Column(db.Integer)
	gst = db.Column(db.Float)
	ship_id = db.Column(db.Integer)
	ship_date = db.Column(db.Date, default = arrow.now().format('YYYY-MM-DD'))
	customer_name = db.Column(db.String(20))
	cid = db.Column(db.String(10), db.ForeignKey('customer.cid', ondelete='CASCADE'))
	city = db.Column(db.String(20))
	state = db.Column(db.String(20))
	country = db.Column(db.String(20))
	
	ref_from_transactions_for_bill_no = db.relationship('Transactions' , backref = 'bills', passive_deletes=True)
	
	def __init__(self, bill_priority, total_item, bill_amt, gst, ship_id, customer_name, customer, city, state, country):
		
		self.bill_priority = bill_priority
		self.total_item = total_item 
		self.bill_amt = bill_amt
		self.gst = gst
		self.ship_id = ship_id
		self.customer_name = customer_name
		self.customer = customer
		self.city = city
		self.state = state
		self.country = country

class Admin(db.Model):
	username = db.Column(db.String(25), primary_key = True)
	password = db.Column(db.String(25))
	
	def __init__(self,username, password):
		self.username = username
		self.password = password
		
class Supplier_product(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	pid = db.Column(db.String(10), db.ForeignKey('product.pid', ondelete='CASCADE'))
	sid = db.Column(db.String(10), db.ForeignKey('supplier.sid', ondelete='CASCADE'))
	
	def __init__(self, product, supplier):
		self.product = product
		self.supplier = supplier

db.create_all()