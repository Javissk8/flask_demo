from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.fields.html5 import EmailField

class RegisterForm(Form):
	name = StringField("Nombre", [validators.Length(min=1, max=45)])
	username = StringField("Nombre de usuario", [validators.Length(min=1, max=45)])
	email = EmailField("Correo electronico", [validators.Email("Ingrese un email valido"), validators.DataRequired("Ingrese un email por favor")])
	password = PasswordField('Password',[validators.Length(min=4, max=45),validators.DataRequired(),validators.EqualTo("confirm",message='Password do not match') ])
	confirm = PasswordField('Confirm Password')

class NoteForm(Form):
	title = StringField("Title", [validators.Length(min=1, max=45)])
	description = TextAreaField("Description", [validators.Length(min=5)])

class LoginForm(Form):
	username = StringField("Nombre de usuario", [validators.Length(min=4, max=45)])
	password = PasswordField('Password',[validators.DataRequired()])
