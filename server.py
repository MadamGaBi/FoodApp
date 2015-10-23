# encoding: utf-8

from flask import Flask, send_from_directory, request
app = Flask(__name__)

import pymysql

db_name = "gabi.db"
db = pymysql.connect(host='127.0.0.1', user='root', passwd='root', db='gabi', charset='utf8')
cur = db.cursor()

@app.route("/food/", methods=['POST','GET'])
def food_db():
	list_of_food = '<ul>\n'
	cur.execute('SELECT * FROM food')
	food_rows = cur.fetchall()
	cur.execute('SELECT * FROM price')
	price_rows = cur.fetchall()

	if request.method == 'POST':
		is_food_exists = False
		for food_row in food_rows:
			if food_row[1] == str(request.form.get("name_of_food")):
				is_food_exists = True
				for price_row in price_rows:
					cur.execute('UPDATE price SET price=%i WHERE id_food=%i' %(int((price_row[0] + int(request.form.get("price_of_food")))/2), food_row[0]))
					db.commit()
		if is_food_exists==False:
			cur.execute('INSERT INTO food (title) VALUES ("%s")' %(str(request.form.get("name_of_food"))))
			db.commit()
			cur.execute('SELECT id_food FROM food WHERE title = "%s"' %(str(request.form.get("name_of_food"))))
			id_food = cur.fetchone()
			cur.execute('INSERT INTO price VALUES (%i, "%s", 1, 1)' %(int(request.form.get("price_of_food")), id_food[0]))
			db.commit()

	for food_row in food_rows:
		for price_row in price_rows:
			if price_row[1] == food_row[0]:
				list_of_food += '<li>%s коштують %s грн.</li>\n' % (food_row[1], price_row[0])
	list_of_food += '</ul>\n' + add_food_form() + change_price_form()
	return list_of_food

def add_food_form():
	form = """<form action="/food/" method="post">\n
			<fieldset>\n
				<legend>Add food:</legend>\n<br>\n
					Name:<br>\n
						<input type="text" name="name_of_food" id="name_of_food" required>\n<br>\n
					Price:<br>\n
						<input type="text" name="price_of_food" id="price_of_food" defoult=None>\n<br>\n
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
			<br>\n
				<input type="submit" value="Submit">\n
			</fieldset>\n
		</form>\n"""
	return form

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('www', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

cur.close()
db.close()
