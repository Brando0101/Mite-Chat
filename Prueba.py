from flask import Flask, render_template, request
from random import randint

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index2(menu principal).html')


@app.route('/contacto', methods=['POST'])
def contacto():
    nombre= request.form.get('nombre')
    numero= request.form.get('numero')
    email= request.form.get('correo')
    return render_template('index3(añadir datos).html', name= nombre, number= numero, correo= email)

@app.route('/boton-de-panico')
def boton_panico():
    return render_template('index4(boton panico principal).html')

@app.route('/primera_vez_boton')
def primera_vez_boton_panico():
    return render_template('index5(boton panico 1).html')

@app.route('/guardado_boton')
def mostrar_guardado_boton_panico():
    return render_template("index6(guardado_boton).html")



if __name__=='__main__':
    app.run(debug=True, port=5000)
