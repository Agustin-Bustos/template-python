import psycopg2, os
from flask import Flask, render_template,  redirect, request
from flask import send_from_directory


app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

conexion = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054"
    )
print("conexion realizada")
    
@app.route('/')
def home():
    # Crear un cursor    
    cursor = conexion.cursor()
    
    # Renderizar la plantilla con los resultados
    return render_template('sitio/index.html')

@app.route('/notas')
def notas1():
    #conexion=psycopg2.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM juegos")
    notas = cursor.fetchall()
    conexion.commit()
    return render_template('sitio/notas.html', lista_notas=notas)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/notas')
def notas():
    conexion=psycopg2.connect
    print(conexion)
    return render_template('sitio/notas.html')

@app.route('/login')
def login():
    return render_template('sitio/login.html')
 

@app.route('/admin/inicio')
def admin_inicio():
    return render_template('admin/index.html')

@app.route('/admin/notas')
def admin_notas():
    #conexion=psycopg2.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM juegos")
    notas = cursor.fetchall()
    conexion.commit()
    print(notas)
    return render_template('admin/notas.html', lista_notas= notas)


@app.route('/admin/notas/guardar', methods=['post'])
def admin_notas_guardar():
    _nombre=request.form['txtNombre']
    _archivo=request.files['txtImagen']
    _subtitulo=request.form['Subtitulo']
    print(_nombre)
    print(_archivo)
    print(_subtitulo)
    if _archivo!="":
        _archivo.save('templates/sitio/img/' + _archivo.filename)
    
    sql = "INSERT INTO juegos (ID, TITULO, SUBTITULO, IMAGEN) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre,_subtitulo, _archivo.filename)
    #conexion = psycopg2.connect()
    cursor = conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()
    return redirect('/admin/notas')

@app.route('/admin/notas/borrar', methods=['post'])
def admin_ropas_borrar():
    _Id=request.form['txtId']
    datos=_Id
    #conexion=psycopg2.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT Imagen FROM juegos WHERE id = %s;",(_Id))
    ropas=cursor.fetchall
    conexion.commit()
    print(ropas)
    #conexion=psycopg2.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM juegos WHERE juegos.id = %s;",(_Id))
    conexion.commit()
    return redirect('/admin/notas')

@app.route('/admin/logueado', methods=['post'])
def admin_login():
    return render_template('/admin/index.html')

if __name__ == "__main__":
    app.run(port=port)
