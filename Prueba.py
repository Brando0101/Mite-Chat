from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='static')
# instrucciones que le damos a la app para conectarse a la base de datos
app.config['MYSQL_HOST']= 'localhost' #pero realmente no quiero que se conecte a esta direccion de enlace, sino una a la que todos puedan acceder
app.config['MYSQL_USER']= 'root' 
app.config['MYSQL_PASSWORD']= '' 
app.config['MYSQL_DB']= 'chat_bot' 
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
    cur.execute('INSERT INTO usuarios (fullname, password, email) VALUES (%s, %s, %s)',
    (nombre, contraseña, email))
    mysql.connection.commit()
    return render_template('index3(menu principal).html', name= nombre)

# boton de panico principal
@app.route('/boton-de-panico')
def boton_panico():
    return render_template('index4(boton panico principal).html')

#boton de panico para agregar tu cosas; ya que no deberia preguntarte si es primera vez que entras al boton de panico al haber iniciado sesion.
@app.route('/primera_vez_boton')
def primera_vez_boton_panico():
    return render_template('index5(boton panico primera vez).html')

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
@app.route('/verificacion')
def verificar_usuario():
    return render_template('index13(verificacion de usuario).html')

# lista de tareas
@app.route('/lista_tareas')
def lista_tareas():
    return render_template('index7(lista_tareas).html')



#@app.route('/agregar tarea', methods=['POST'])




if __name__=='__main__':
    app.run(debug=True, port=5000)
