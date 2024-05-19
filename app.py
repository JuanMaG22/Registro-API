from flask import Flask
from flask import render_template, request, redirect, Response, url_for, session,jsonify
from flask_mysqldb import MySQL,MySQLdb # pip install Flask-MySQLdb
import re

app = Flask(__name__,template_folder='template')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'login'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')   

@app.route('/admin')
def admin():
    return render_template('admin.html')   

# ACCESO---LOGIN
@app.route('/acceso-login', methods= ["POST"])
def login():
    data = request.get_json()
    correo = data.get('txtCorreo')
    password = data.get('txtPassword')

    if correo and password:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE correo = %s AND password = %s', (correo,password,))
        account = cur.fetchone()
        cur.close()
        
        if account:
            response = {
                'logueado': True,
                'id': account['id'],
                'id_rol': account['id_rol']
            }
            if 'id_rol'==1:
                return render_template("admin.html")           
            elif 'id_rol' ==2:
                return render_template("usuario.html")
            return jsonify(response), 200
                
        else:
            return jsonify({'mensaje': "Usuario o contraseña incorrectas"}), 401
    else:
        return jsonify({'mensaje': "Faltan datos obligatorios"}), 400

#registro---
@app.route('/registro')
def registro():
    return render_template('registro.html')  

@app.route('/crear-registro', methods= ["GET", "POST"])
def crear_registro(): 
    data = data.get_json()
    correo = data.get('txtCorreo')
    password = data.get('txtPassword')
    nombre = data.get('txtNombre')
    apellido = data.get('txtApellido')
    fecha_nacimiento = data.get('txtApellido')

    if correo and password and nombre and apellido and fecha_nacimiento:
        if re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            if len(password) <= 8:
                # Realizar la inserción en la base de datos
                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO usuarios (correo, password, nombre, apellido, fecha_nacimiento, id_rol) VALUES (%s, %s, %s, %s, %s, '2')",
                            (correo, password, nombre, apellido, fecha_nacimiento))
                mysql.connection.commit()
                cur.close()
                return jsonify({'mensaje': "Usuario registrado exitosamente"}), 201
            else:
                return jsonify({'mensaje': "La contraseña no debe exceder los 8 caracteres"}), 400
        else:
            return jsonify({'mensaje': "La contraseña debe contener un caracter especial"}), 400
    
    return render_template("index.html",mensaje2="Usuario Registrado Exitosamente")
#--------------------------------------------------

if __name__=='__main__':
    app.secret_key="juan_hds"

    #Nos crea de manera local al momento de correr
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)