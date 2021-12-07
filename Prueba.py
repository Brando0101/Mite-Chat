from flask import Flask, render_template, request, session, url_for, redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import smtplib
from random import randint



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


# inicio de sesion
@app.route('/')
def index():
    return render_template('index2(inicio sesion).html')

# añadir un usuario
@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST' and 'nombre' in request.form and 'contrasena' in request.form and 'correo' in request.form: # los and son para verificar que se ingresan datos en los espacios
        nombre= request.form.get('nombre')
        contraseña= request.form.get('contrasena')
        email= request.form.get('correo')
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usuarios WHERE email = %s', 
        (email,))
        cuenta = cur.fetchall()
        #print(cuenta)
        if cuenta:
            return render_template('index15(correo ya existe).html')
        else:
            cur.execute('INSERT INTO usuarios (name, password, email) VALUES (%s, %s, %s)',
            (nombre, contraseña, email,))
            mysql.connection.commit()
        session['id'] = cur.lastrowid #last row id =  id de la ultima fila
        return render_template('index3(menu principal).html', name= nombre)

# boton de panico principal
@app.route('/boton-de-panico')
def boton_panico():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT photo, enlaces FROM usuarios WHERE id = %s',
    (session['id'],))
    #print(session['id'])
    cuenta = cur.fetchall()
    #print(cuenta)
    for datos in cuenta:
        if datos['photo'] == None and datos['enlaces'] == None:
            return render_template('index5(boton panico primera vez).html')
        elif datos['photo'] != None and datos['enlaces'] != None:
            return redirect(url_for('mostrar_guardado_boton_panico'))

#boton de panico para agregar tu cosas; ya que no deberia preguntarte si es primera vez que entras al boton de panico al haber iniciado sesion.
# ya no se utiliza esta ruta
@app.route('/primera_vez_boton')
def primera_vez_boton_panico():
    return render_template('index5(boton panico primera vez).html')

# funcion que transforma la foto a binario
def transformar_foto_binario(foto):
    with open(foto, 'rb') as file:
        informacion_binaria1= file.read()
    return informacion_binaria1

# Esta ruta guarda la url y la imagen que se han ingresado al boton de panico 
@app.route('/guardando_datos', methods=['POST'])
def guardar_datos_boton():  
    foto_0= request.files['foto']
    filename = foto_0.filename
    #print(filename)
    foto_0.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    foto1 = transformar_foto_binario(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    url= request.form.get('cancion')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE usuarios SET photo= %s, enlaces= %s WHERE id= %s",
    (foto1, url, session['id']))
    mysql.connection.commit()
    return render_template('index3(menu principal).html')    

    
# Muestra lo que se ha guardado en el boton de panico
@app.route('/guardado_boton')
def mostrar_guardado_boton_panico():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT photo, enlaces FROM usuarios WHERE id = %s',
    (session['id'],))
    cuenta = cur.fetchall()
    for datos in cuenta:
        foto_bd = datos['photo']
        with open('static/salir.jpg', 'wb') as file:
            foto_final = file.write(foto_bd)
        url_final = datos['enlaces']
    url_final_cambiada=url_final.replace("watch?v=","embed/")
    url_final_cambiada+= "?autoplay=1"
    print(url_final_cambiada)
    return render_template("index6(guardado_boton).html", foto_mostrar = foto_final, url_salida = url_final_cambiada)

# ruta para ingresar los datos, que luego se enviaran al /contacto
@app.route('/crear_cuenta')
def crear_cuenta():
    return render_template('index9(crear cuenta).html')

# chat bot como tal (Mite)
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


@app.route('/redirigir_arica')
def ir_arica():
    return render_template('index24(ir arica).html')
@app.route('/redirigir_tarapaca')
def ir_tarapaca():
    return render_template('index25(ir tarapaca).html')
@app.route('/redirigir_antofagasta')
def ir_antofagasta():
    return render_template('index26(ir antofagasta).html')
@app.route('/redirigir_atacama')
def ir_atacama():
    return render_template('index27(ir atacama).html')
@app.route('/redirigir_coquimbo')
def ir_coquimbo():
    return render_template('index28(ir coquimbo).html')
@app.route('/redirigir_metropolitana')
def ir_metropolitana():
    return render_template('index29(ir metropolitana).html')
@app.route('/redirigir_ohiggins')
def ir_ohiggins():
    return render_template('index30(ir ohiggins).html')
@app.route('/redirigir_maule')
def ir_maule():
    return render_template('index31(ir maule).html')
@app.route('/redirigir_nuble')
def ir_nuble():
    return render_template('index32(ir nuble).html')
@app.route('/redirigir_biobio')
def ir_biobio():
    return render_template('index33(ir biobio).html')
@app.route('/redirigir_araucania')
def ir_araucania():
    return render_template('index34(ir araucania).html')
@app.route('/redirigir_losrios')
def ir_losrios():
    return render_template('index35(ir losrios).html')
@app.route('/redirigir_loslagos')
def ir_loslagos():
    return render_template('index36(ir loslagos).html')
@app.route('/redirigir_aysen')
def ir_aysen():
    return render_template('index37(ir aysen).html')
@app.route('/redirigir_magallanes')
def ir_magallanes():
    return render_template('index38(ir magallanes).html')






















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



# solo redirige a un html luego de presionar que se le ha olvidado la contraseña
@app.route('/redirigir_rest_contrasena')
def redirigir():
    return render_template('index16(pide correo para restablecer contra).html')


# Funcion que crea un numero al azar, que posteriormente sera enviado al correo para restablecer la contraseña
def numero():
    numero_verificador= str(randint(1000,9999))
    return numero_verificador
verificador=numero()


# le envia el codigo de verificacion al correo
@app.route('/enviar_correo_para_restablecer', methods=['POST'])
def envia_correo_pw():
    numero_verificador=verificador
    print(numero_verificador)
    mensaje = 'tu numero verificador es ' + numero_verificador
    correo_1= request.form.get('correo_restablecer')
    print(correo_1)
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT id FROM usuarios WHERE email = %s', 
    [correo_1])
    cuenta = cur.fetchone()
    print(cuenta)
    session['id'] = cuenta['id']
    print(session['id'])
    server = smtplib.SMTP('smtp.gmail.com', 587) #aqui me conecto al 'servidor' de gmail
    server.starttls()
    server.login('mite.tu.acompanante@gmail.com', 'Miteproyecto')
    server.sendmail('mite.tu.acompanante@gmail.com', correo_1, mensaje)
    server.quit()
    return render_template('index17(verificar codigo).html')


# verifica si el codigo ingresado es el correcto
@app.route('/verificar')
def verificar_codigo():
    codigo = request.args.get('codigo_ingresado')
    numero_verificador = verificador
    print(codigo)
    if codigo == numero_verificador:
        return render_template('index18(restablecer contrasena).html')
    else:
        return render_template ('index19(codigo incorrecto).html')


# aqui el usuario ingresa su nueva contraseña, y esta se cambia por la antigua en la base de datos
@app.route('/cambiar_contrasena', methods=['POST'])
def cambiar_pw():  
    nueva_pw = request.form.get('nueva_contrasena')
    nueva_pw_1= request.form.get('nueva_contrasena_2')
    if nueva_pw == nueva_pw_1:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE usuarios SET password= %s WHERE id= %s",
        ([nueva_pw], session['id']))
        mysql.connection.commit()
        return render_template('index2(inicio sesion).html')
    else:
        return render_template('index20(las pw no coinciden).html')


# cambio de contraseña cuando se esta dentro del sistema (ya se esta logeado)
@app.route('/cambiar_contrasena_dentro', methods=['POST'])
def cambiar_pw_dentrosistema():  
    nueva_pw = request.form.get('nueva_contrasena')
    nueva_pw_1= request.form.get('nueva_contrasena_2')
    if nueva_pw == nueva_pw_1:
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("UPDATE usuarios SET password= %s WHERE id= %s",
        ([nueva_pw], session['id']))
        mysql.connection.commit()
        return render_template('index3(menu principal).html')
    else:
        return render_template('index23(las pw no coinciden, dentro sistema).html')



# redirige al menu principal cuando se clickea el boton de retroceder
@app.route('/redirigir_menuprincipal')
def redirigir_menuprincipal():
    return render_template ('index3(menu principal).html')

# redirige para cambiar contraseña (desde ajustes)
@app.route('/redirigir_cambiopw')
def redirigir_cambiopw():
    return render_template('index22(cambio pw dentro).html')

# redirige para cambiar lo que se tiene en el boton de panico
@app.route('/redirigir_cambioboton')
def redirigir_cambioboton():
    return render_template('index5(boton panico primera vez).html')

# lista de tareas
lista=list()

@app.route('/lista_tareas')
def lista_tareas():
    return render_template('index7(lista_tareas).html', lista_1= lista)

@app.route('/anadir_tarea', methods= ['GET', 'POST'])
def anadir_tarea():
    if request.method == 'GET':
        return render_template('index21(anadir tarea).html')
    else:
        tarea = request.form.get('nueva_tarea')
        lista.append(tarea)
        return redirect(url_for('lista_tareas'))

# cerrar sesion
@app.route('/deslogearse')
def deslogearse():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index2(inicio sesion).html')









if __name__=='__main__':
    app.run(debug=True, port=5000)
