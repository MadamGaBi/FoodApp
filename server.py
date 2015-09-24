# encoding: utf-8

from flask import Flask, send_from_directory, request
app = Flask(__name__)

database = [('Помідори', 5), ('Огірки', 7), ('Апельсини', 12)]


@app.route("/food/", methods=['POST','GET'])
def food():
	if request.method == "POST":
		is_food_exists = True
		for i in database:
			if i[0] == str(request.form["name_of_food"]):
				is_food_exists = False
				database[database.index(i)] = (str(request.form["name_of_food"]), ((i[1] + int(request.form["price_of_food"]))/2.0))
		if is_food_exists:
			database.append((str(request.form["name_of_food"]), int(request.form["price_of_food"])))
			
	s = '<ul>\n'
	for i in database:
		s += '<li>%s коштують %i грн.</li>\n' % (i[0],i[1])
	s += '</ul>\n' + add_food_form() + change_price_form()
	return s


def add_food_form():
	form = '<form action="/food/" method="post">\n<fieldset>\n<legend>Add food:</legend>\n<br>\nName:<br>\n<input type="text" name="name_of_food" id="name_of_food" required>\n<br>\nPrice:<br>\n<input type="text" name="price_of_food" id="price_of_food" defoult=None>\n<br>\n<br>\n<input type="submit" value="Submit">\n</fieldset>\n</form>'
	return form


def change_price_form():
	form = '<form action="/food/" method="post">\n<fieldset>\n<legend>Change price:</legend>\n<br>\nSelect name:<br>\n<select name="name_of_food"><br>\n'
	for i in database:
		form += '<option value=%s>%s</option>\n' % (i[0],i[0])
	form += '</select><br>\nFill price:<br>\n<input type="text" name="price_of_food" required><br>\n<br>\n<input type="submit" value="Submit">\n</fieldset>\n</form>\n'
	return form

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('www', path)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

