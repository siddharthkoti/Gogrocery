INSERT INTO supplier(sid, s_name,s_contact_name, s_number, s_address)
VALUES
 ( 's1' , 'shashi', 'shashi',  657298, 'Bangalore'),
 ( 's1' , 'Siddharth Koti', 'siddharth',  826262, 'Bangalore'),
 ( 's1' , 'Damo', 'Damo',  132568, 'Bangalore'),

INSERT INTO Product( pid, p_category, p_sub_category, p_name, p_price, product_base_margin, product_sale_price, product_arrival_date, sid) 
VALUES
	('p1','Eatables','Biscuits', 'GoodDay', '10', '7', '12', '2016-12-25','s1'),
	('p2','Eatables','Biscuits', 'CrackJack', '10', '7', '12', '2016-12-25','s2'),
 
 INSERT INTO Stock(date, pid, stocks_left, sid, last_shipment_arrival)
 VALUES
	('2017-01-15', ('p1', 30, 's1', '2017-01-01'),
	('2017-02-05', ('p2', 45, 's2', '2017-01-20');

admin:
('admin','admin')
	
product:
INSERT INTO Product( pid, p_category, p_sub_category, p_name, p_price,gst, product_base_margin, product_sale_price,  sid) 
VALUES
('p5','Bath','Soap','Lifebuoy',32,12,25,35,'s2'),
('p1','Eatables','Biscuits','GoodDay',5,10,7,12,'s1'),
('p2','Eatables','Jam','CrackJack',10,18,7,12,'s2'),
('p3','Washing Cleaning','Washing Bar','Vim',30,5,6,36,'s1'),
('p4','Kitchen','Dish','CrackDisk',50,12,12,45,'s2');

Supplier:
INSERT INTO supplier(sid, s_name,s_contact_name, s_number, s_address)
VALUES
('s1','shashi','shashi','657298','Bangalore'),
('s2','Siddharth Koti','siddharth','826262','Bangalore'),
('s3','Damo','Damo','132568','Mangalore'),
('s4','Durgamba Agency','Mahesh','854555','Haridwar'),
('s5','Ramu Agency','Ramu','890778','Bangalore'),
('s6','Canam Agency','Shelly','88967','paris'),
('s7','Castrol Agency','Sheila','87096','California');

Customer:
INSERT INTO Customer( cid, c_name, c_number, c_email, c_address, city, Country)
VALUES
('c1','siddharth','112233','sid@gmail.com','Dwarka Nagar','Bangalore','India'),
('c2','shashi','657298','sha@gmail.com','Dwarka Nagar','Bangalore','India'),
('NONE','NONE','0','NONE','NONE','NONE','NONE');

stock:
INSERT INTO Stock( date, pid, stocks_left, sid, last_shipment_arrival)
VALUES
('2017-01-01','p5',115,'s2','2017-01-15'),
('2017-01-15','p1',30,'s1','2017-01-01'),
('2017-02-05','p2',45,'s2','2017-01-20'),
('2017-03-05','p3',55,'s2','2017-05-16'),
('2017-01-20','p4',98,'s1','2017-02-11');

supplier_product:
INSERT INTO Supplier_product( id, pid, sid)
VALUES
(1,'p3','s3');


