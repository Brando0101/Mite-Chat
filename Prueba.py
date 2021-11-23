from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='statics')
# instrucciones que le damos a la app para conectarse a la base de datos
app.config['MYSQL_HOST']= 'localhost' #pero realmente no quiero que se conecte a esta direccion de enlace, sino a la que todos puedan acceder
app.config['MYSQL_USER']= 'root' 
app.config['MYSQL_PASSWORD']= '' 
app.config['MYSQL_DB']= 'chat_bot' 
mysql= MySQL(app)

lista=list()

@app.route('/')
def index():
    return render_template('index2(menu principal).html')

@app.route('/contacto', methods=['POST'])
def contacto():
    nombre= request.form.get('nombre')
    contraseña= request.form.get('contraseña')
    email= request.form.get('correo')
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO usuarios (fullname, phone, email) VALUES (%s, %s, %s)',
    (nombre, contraseña, email))
    mysql.connection.commit()
    return render_template('index3(comienzo del programa).html', name= nombre)

@app.route('/boton-de-panico')
def boton_panico():
    return render_template('index4(boton panico principal).html')

@app.route('/primera_vez_boton')
def primera_vez_boton_panico():
    return render_template('index5(boton panico 1).html')

@app.route('/guardado_boton')
def mostrar_guardado_boton_panico():
    return render_template("index6(guardado_boton).html")

@app.route('/crear_cuenta')
def crear_cuenta():
    return render_template('index9(crear cuenta).html')

@app.route('/chat')
def chat():
    return render_template('index7(instrucciones1).html')









@app.route('/lista_tareas')
def lista_tareas():
    return render_template('index7(lista_tareas).html')



#@app.route('/agregar tarea', methods=['POST'])




if __name__=='__main__':
    app.run(debug=True, port=5000)
