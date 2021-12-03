from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os



app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)
app.debug= True
app.config['UPLOAD_FOLDER'] = 'upload'
app.config['MAX_CONTENT_LENGTH'] = (1024 * 1024)*10

# instrucciones que le damos a la app para conectarse a la base de datos
app.config['MYSQL_HOST']= 'localhost' #pero realmente no quiero que se conecte a esta direccion de enlace, sino una a la que todos puedan acceder
app.config['MYSQL_USER']= 'root' 
app.config['MYSQL_PASSWORD']= '' 
app.config['MYSQL_DB']= 'chat_bot2' 
mysql= MySQL(app)

lista=list()
# inicio de sesion
@app.route('/')
def index():
    return render_template('index2(inicio sesion).html')

# añadir un usuario
@app.route('/contacto', methods=['POST'])
def contacto():
    nombre= request.form.get('nombre')
    contraseña= request.form.get('contraseña')
    email= request.form.get('correo')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuarios (name, password, email) VALUES (%s, %s, %s)',
    (nombre, contraseña, email))
    mysql.connection.commit()
    session['id'] = cur.lastrowid
    return render_template('index3(menu principal).html', name= nombre)

# boton de panico principal
@app.route('/boton-de-panico')
def boton_panico():
    return render_template('index4(boton panico principal).html')

#boton de panico para agregar tu cosas; ya que no deberia preguntarte si es primera vez que entras al boton de panico al haber iniciado sesion.
@app.route('/primera_vez_boton')
def primera_vez_boton_panico():
    return render_template('index5(boton panico primera vez).html')

def transformar_foto_binario(foto):
    with open(foto, 'rb') as file:
        informacion_binaria1= file.read()
    return informacion_binaria1

# Esta ruta guarda la url que se han ingresado al boton de panico y transforma la foto en binario
@app.route('/guardando_datos', methods=['POST'])
def guardar_datos_boton():  
    foto_0= request.files['foto']
    filename = foto_0.filename
    foto_0.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    foto1 = transformar_foto_binario(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    url= request.form.get('cancion')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET photo= %s, enlaces= %s WHERE id= %s",
    (foto1, url, session['id']))
    mysql.connection.commit()
    return render_template('index3(menu principal).html')    




# boton de panico cuando ya se han agregado las cosas
@app.route('/guardado_boton')
def mostrar_guardado_boton_panico():
    return render_template("index6(guardado_boton).html")

# ruta para ingresar los datos, que luego se enviaran al /contacto
@app.route('/crear_cuenta')
def crear_cuenta():
    return render_template('index9(crear cuenta).html')

# dialogos del bot
@app.route('/chat')
def chat():
    return render_template('index10(chatbot).html')

# ajustes del bot
@app.route('/ajustes')
def ajustes():
    return render_template('index11(ajustes).html')

# lista de psicologos
@app.route('/psicologos')
def psicologos():
    return render_template('index12(lista psicologos).html')

#verificar si el usuario esta en la base de datos
@app.route('/verificacion', methods= ['POST'])
def verificar_usuario():
    if request.method == 'POST' and "correo.inicio.sesion" in request.form and "contrasena.inicio.sesion" in request.form:
        correo = request.form.get("correo.inicio.sesion")
        contrasena = request.form.get("contrasena.inicio.sesion")
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usuarios WHERE password = %s AND email = %s', 
        (contrasena, correo))
        cuenta = cur.fetchone()
        if cuenta:
            session['loggedin'] = True
            session['id'] = cuenta['id']
            session['fullname'] = cuenta['name']
            return render_template('index3(menu principal).html')
        else:
            return render_template('index14(error datos ingresados).html')

        
    #return render_template('index13(verificacion de usuario).html')

# lista de tareas
@app.route('/lista_tareas')
def lista_tareas():
    return render_template('index7(lista_tareas).html')



#@app.route('/agregar tarea', methods=['POST'])




if __name__=='__main__':
    app.run(debug=True, port=5000)
