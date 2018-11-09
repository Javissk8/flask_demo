from flask import Flask, render_template, request, redirect, url_for, flash
#from data import Notes
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField

app = Flask(__name__)
#notes = Notes()

#Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Element!'
app.config['MYSQL_DB'] = 'note_app'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#Init MySQL
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/notes')
def my_notes():
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM notes")

	notes = cur.fetchall()

	cur.close()
	
	if result > 0:
		return render_template('notes.html', notes = notes)
	else:
		return "No data"



@app.route('/note/<string:id>/')
def note(id):
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM notes WHERE id = %s",(id))

	note = cur.fetchone

	cur.close()

	return render_template('note.html', note = note)



#class UserForm(Form):
#	name = StringField("Nombre", [validators.Length(min=1, max=45)])
#	username = StringField("Nombre de usuario", [validators.Length(min=1, max=45)])
#	email = EmailField("Correo electronico", [validators .Email("Ingrese un email valido"), validators .Required("Ingrese un email por favor")])

class NoteForm(Form):
	title = StringField("Title", [validators.Length(min=1, max=45)])
	description = TextAreaField("Description", [validators.Length(min=5)])

@app.route('/edit-note/<string:id>', methods = ['GET','POST'])
def edit_note(id):
	cur = mysql.connection.cursor()

	#get note by id

	cur.execute("SELECT * FROM notes WHERE id = %s",(id))

	note = cur.fetchone()

	cur.close()

	form = NoteForm(request.form)

	form.title.data = note['title']
	form.description.data = note['description']

	if request.method == 'POST' and form.validate():

		title = request.form['title']
		description = request.form['description']

		#create cursor

		cur = mysql.connection.cursor()

		cur.execute("UPDATE notes SET title = %s, description = %s WHERE id = %s",(title, description, id))

		mysql.connection.commit()

		cur.close()

		return redirect(url_for('my_notes'))
	

	return render_template('edit_note.html', form = form)

@app.route('/delete-note/<string:id>', methods = ['POST'])
def delete_note(id):
	

	cur = mysql.connection.cursor()

	cur.execute("DELETE FROM notes WHERE id = %s", (id))

	mysql.connection.commit()

	cur.close()

	return redirect(url_for('my_notes'))

@app.route('/add-note', methods=['GET','POST'])
def add_note():
	form = NoteForm(request.form)

	if request.method =='POST' and form.validate():
		title = form.title.data
		description = form.description.data

		#create cursor

		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO notes(title, description) VALUES (%s,%s)",(title, description))

		mysql.connection.commit()

		cur.close()

		flash('agregaste la nota exitosamente','success')

		return redirect(url_for('add_note'))
	
	return render_template('add_note.html', form=form)



#@app.route('/add-user', methods=['GET','POST'])
#def add_user():
#	form

if __name__ == '__main__':
	app.secret_key = '12345'
	app.run(port = 4444, debug = True)