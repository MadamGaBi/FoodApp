# encoding: utf-8

from flask import Flask, send_from_directory, request
app = Flask(__name__)

import pymysql

db_name = "gabi.db"
db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='gabi', charset='utf8')
cur = db.cursor()

@app.route("/food/", methods=['POST','GET'])
def food_db():
	cur.execute('SELECT * FROM food')
	food_rows = cur.fetchall()
	cur.execute('SELECT * FROM price')
	price_rows = cur.fetchall()
	
	if request.method == 'POST':
		is_food_exists = False
		for food_row in food_rows:
			if food_row[1] == str(request.form.get("name_of_food")):
				is_food_exists = True
				id_food_price = []
				for price_row in price_rows:
					id_food_price.append(price_row[1])
					if food_row[0] == price_row[1]:
						cur.execute('UPDATE price SET price=%i WHERE id_food=%i' %(int((price_row[0] + int(request.form.get("price_of_food")))/2), food_row[0]))
				if food_row[0] not in id_food_price:
					cur.execute('SELECT id_place FROM place WHERE (title, geo) = ("%s", "%s")' %(str(request.form.get("market_title")), str(request.form.get("area_title"))))
					id_place = cur.fetchone()
					cur.execute('INSERT INTO price (price, id_food, id_place, quantity) VALUES (%i, "%s", "%s", "%s")' %(int(request.form.get("price_of_food")), food_row[0], id_place[0], request.form.get("quantity_of_food")))
				db.commit()
		if is_food_exists==False:
			cur.execute('INSERT INTO food (title) VALUES ("%s")' %(str(request.form.get("name_of_food"))))
			db.commit()
			cur.execute('INSERT INTO place (title, geo) VALUES ("%s", "%s")' %(str(request.form.get("market_title")), str(request.form.get("area_title"))))
			db.commit()
			cur.execute('SELECT id_food FROM food WHERE title = "%s"' %(str(request.form.get("name_of_food"))))
			id_food = cur.fetchone()
			cur.execute('SELECT id_place FROM place WHERE (title, geo) = ("%s", "%s")' %(str(request.form.get("market_title")), str(request.form.get("area_title"))))
			id_place = cur.fetchone()
			cur.execute('INSERT INTO price (price, id_food, id_place, quantity) VALUES (%i, "%s", "%s", "%s")' %(int(request.form.get("price_of_food")), id_food[0], id_place[0], request.form.get("quantity_of_food")))
			db.commit()
	list_of_food = welcome_line()	
	list_of_food += """<table align="center" bgcolor=#ffffc0 border=1 cellpadding=4 width='90%'>\n 
				<thead>
					<tr> 
						<th width='50%'>Name of food</th> 
						<th width='50%'>Average price, hrn</th>
					</tr>
				</thead>
				<tbody>"""
	for food_row in food_rows:
		for price_row in price_rows:
			if price_row[1] == food_row[0]:
				list_of_food += """<tr> 
							<td>%s</td>
							<td>%s</td>
						</tr>""" % (food_row[1], price_row[0]/100)
	list_of_food += """</tbody>\n
			</table><br>\n
			<table align='center' cellpadding=4 width='90%'>
				<tr>
					<td>"""
	list_of_food += add_food_form() + """</td>\n<td>\n""" + change_price_form() + """</td>\n</tr>\n</table>\n""" + footer_line()
	return list_of_food

def welcome_line():
	line = """<div align='left'>
			<h1>Welcome to FoodApp!</h1>\n
			<h5><i>The most important and interesting WebSite of average prices of food in Kyiv.</i></h5>
			<br>
		</div>"""
	return line

def add_food_form():
	form = """<form action="/food/" method="post">\n
			<fieldset>\n
				<legend>Add food:</legend>\n<br>\n
					Name of food:<br>\n
						<input type="text" name="name_of_food" id="name_of_food" required>\n<br>\n
					Price:<br>\n
						<input type="text" name="price_of_food" id="price_of_food" defoult=None>\n<br>\n
					Residential area:<br>\n
						<input type="text" name="area_title" id="area_title" required>\n<br>\n
					Market:<br>\n
						<input type="text" name="market_title" id="market_title" required>\n<br>\n
					Quantity:<br>\n
						<input type="text" name="quantity_of_food" id="quantity_of_food" required>\n<br>\n
					<br>\n
						<input type="submit" value="Submit">\n
			</fieldset>\n
		</form>"""
	return form

def change_price_form():
	cur.execute('SELECT * FROM food')
	food_rows = cur.fetchall()
	form = """<form action="/food/" method="post">\n
			<fieldset>\n
				<legend>Change price:</legend>\n<br>\n
					Select name:<br>\n
						<select name="name_of_food"><br>\n"""
	for food_row in food_rows:
		form += '<option value=%s>%s</option>\n' % (food_row[1], food_row[1])
	form += """</select><br>\n
			Fill price:<br>\n
				<input type="text" name="price_of_food" required><br>\n
			Residential area:<br>\n
				<input type="text" name="area_title" id="area_title" required>\n<br>\n
			Market:<br>\n
				<input type="text" name="market_title" id="market_title" required>\n<br>\n
			Quantity:<br>\n
				<input type="text" name="quantity_of_food" id="quantity_of_food">\n<br>\n
			<br>\n
				<input type="submit" value="Submit">\n
			</fieldset>\n
		</form>\n"""
	return form

def footer_line():
	line = """<div align = 'right'>\n
			<footer>\n
				&copy; 2015 GaBi\n
			</footer>\n
		</div>"""
	return line

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('www', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

cur.close()
db.close()
