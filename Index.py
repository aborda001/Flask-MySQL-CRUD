from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

#Inicializacion Flask
app = Flask(__name__)

#Coneccion con MySql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'Userflask'
app.config['MYSQL_PASSWORD'] = 'password12'
app.config['MYSQL_DB'] = 'contacts'
mysql = MySQL(app)

app.secret_key='mysecretkey'

#Rutas y diferentes funciones para el CRUD 
@app.route('/')
def Index():
""" Conecta con la base de datos, obtiene todos los contactos y los almacena en una la variable 'data', 
al final retorna a la pagina principal (Index.html) """
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM contacts')
	data = cur.fetchall()
	return render_template('index.html', contacts = data)
 
@app.route('/add_contact',methods= ['POST'])
def add_contact():
""" Guarda los datos obtenidos del formulario con sus variables correspondientes, para ingresar los datos a la tabla 'contacts',
y al final retorna a la funcion principal (Index) """
	if request.method == 'POST':
		fullname = request.form['fullname']
		phone = request.form['phone']
		email = request.form['email']
		cur = mysql.connection.cursor()
		cur.execute('INSERT INTO  contacts (fullname, phone, email) VALUES (%s,%s,%s)',
			(fullname, phone, email))
		mysql.connection.commit()
		flash('Contact added successfully')
		return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
""" Selecciona el contacto, correspondiente al 'id' recolectado, almacena los datos en la variable 'data',
y terminar redireccionando al vista (edit.html)"""
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM contacts WHERE id = %s',(id))
	data = cur.fetchall()
	return render_template('edit.html', contact = data[0])

@app.route('/update/<string:id>',methods=['POST'])
def update(id):
""" Con el 'id' recolectado almacena los datos obtenidos del formulario con sus variables correspondientes,actualiza el contacto con el 'id' correspondiente,
y al final retorna a la funcion principal (Index) """
	if request.method == 'POST':
		fullname = request.form['fullname']
		phone = request.form['phone']
		email = request.form['email']
	cur = mysql.connection.cursor()
	cur.execute("""
		UPDATE contacts
		SET fullname = %s,
			email = %s,
			phone = %s
		WHERE id = %s
		""",(fullname,email,phone,id))
	mysql.connection.commit()
	flash('Contact updated successfully')
	return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
""" Con el 'id' recolectado ,elimina el contacto con el 'id' correspondiente,
y termina retornando a la funcion principal (Index) """
	cur = mysql.connection.cursor()
	cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
	mysql.connection.commit()
	flash('Contact deleted successfully')
	return redirect(url_for('Index'))

if __name__ == '__main__':
	app.run(port = 3000, debug = True)
