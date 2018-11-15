from flask import Flask, render_template, request, redirect, url_for, flash, session
#from data import Notes
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from flask_wtf import CSRFProtect
import forms

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
csrf = CSRFProtect(app)

@app.route('/')
def index():
	if 'logged_in' in session:
		message = "{}'s notes" .format(session['username'])
		flash('has iniciado sesion exitosamente','success')
	else:
		message = "My notes"
	return render_template('home.html', message = message )

@app.route('/notes')
def my_notes():
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM notes WHERE id_user = %s",[session['id_user']])

	notes = cur.fetchall()

	message = "Las notas"

	cur.close()
	
	if result > 0:
		return render_template('notes.html', notes=notes, message = message)
	else:
		message = "No hay notas"
		return render_template('notes.html', message = message)



@app.route('/note/<string:id>/')
def note(id):
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM notes WHERE id = %s",(id))

	note = cur.fetchone

	cur.close()

	return render_template('note.html', note=note)

@app.route('/edit-note/<string:id>', methods=['GET','POST'])
def edit_note(id):
	cur = mysql.connection.cursor()

	#get note by id

	cur.execute("SELECT * FROM notes WHERE id = %s",(id))

	note = cur.fetchone()

	cur.close()

	form = forms.NoteForm(request.form)

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
	

	return render_template('edit_note.html', form=form)

@app.route('/delete-note/<string:id>', methods=['POST'])
def delete_note(id):
	

	cur = mysql.connection.cursor()

	cur.execute("DELETE FROM notes WHERE id = %s", (id))

	mysql.connection.commit()

	cur.close()

	return redirect(url_for('my_notes'))



@app.route('/add-note', methods=['GET','POST'])
def add_note():

	if 'logged_in' in session:
		form = forms.NoteForm(request.form)

		if request.method =='POST' and form.validate():
			title = form.title.data
			description = form.description.data

			#create cursor

			cur = mysql.connection.cursor()

			cur.execute("INSERT INTO notes(title, description, id_user) VALUES (%s,%s,%s)",(title, description, session['id_user']))

			mysql.connection.commit()

			cur.close()

			flash('agregaste la nota exitosamente','success')

			return redirect(url_for('add_note'))
		
		return render_template('add_note.html', form=form)

	else:
		return redirect(url_for('my_notes')), flash("necesitas estar logueado para agregar notas",'danger')
		
@app.route('/register', methods=['GET','POST'])
def add_user():
	form = forms.RegisterForm(request.form)
	if request.method == 'POST'and form.validate():
		name = form.name.data
		username = form.username.data
		email = form.email.data
		password = sha256_crypt.encrypt(str(form.password.data))

		#create cursor

		cur = mysql.connection.cursor()

		cur.execute("INSERT INTO users(name, username, email, password) VALUES (%s,%s,%s,%s)",(name, username, email, password))

		mysql.connection.commit()

		cur.close()

		flash('Datos agregados exitosamente','success')

		return redirect(url_for('add_user'))
	
	return render_template('register.html', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
	form = forms.LoginForm(request.form)
	try:
		if request.method == 'POST' and form.validate():
			username = form.username.data
			password_candidate = form.password.data
			print(username) 
			print(password_candidate)#este nomas lo hice para ver si si estaba jalando hasta esta parte

			cur = mysql.connection.cursor()
			cur.execute("SELECT * FROM users WHERE username = %s",[username])#este query no sirve :,(
			user = cur.fetchone()
			print(user["password"])
			cur.close()

			if sha256_crypt.verify(password_candidate, user["password"]):
				session['logged_in'] = True
				session['username'] = username
				session['id_user'] = user['id']
				
			else:
				flash("Contrasena incorrecta",'danger')
				

			return redirect(url_for('index'))

	except:
		flash("Ese usuario no existe",'danger')

	return render_template('login.html', form = form)


@app.route('/logout', methods=['GET','POST'])
def logout():
	session.clear()
	flash("You are now logged out",'success')
	
	
	return redirect(url_for('login'))
	



if __name__ == '__main__':
	app.secret_key = '12345'
	app.run(port = 4444, debug = True)