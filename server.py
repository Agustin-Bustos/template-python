import psycopg2, os
from flask import Flask, render_template, redirect, request, send_from_directory, session

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

app.secret_key="pepe1234"
print("conexion realizada")
    
@app.route('/')
def home():
    # Crear un cursor 
    conexion = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054"
    )   
    cursor = conexion.cursor()
    
    # Renderizar la plantilla con los resultados
    return render_template('sitio/index.html')

@app.route('/notas')
def notas1():
    conexion = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054"
    )
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
    conexion = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054"
    )
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
    conexion = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054"
    )
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM juegos")
    notas = cursor.fetchall()
    conexion.commit()
    print(notas)
    return render_template('admin/notas.html', lista_notas= notas)


#@app.route('/admin/notas/guardar', methods=['post'])
#def admin_notas_guardar():
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

@app.route('/admin/notas/guardar', methods=['POST'])
def admin_notas_guardar():

  try:
    # Obtener datos del formulario
    nombre = request.form['txtNombre']
    archivo = request.files['txtImagen'] 
    subtitulo = request.form['Subtitulo']

    # Conectar a la BD
    conexion = psycopg2.connect("postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054")

    # Preparar consulta con parámetros
    sql ='INSERT INTO "juegos" ("TITULO", "SUBTITULO", "IMAGEN") VALUES (%s, %s, %s);'
    
    # Manejar caso de archivo nulo
    if archivo:
      archivo.save('templates/sitio/img/' + archivo.filename) 
      imagen = archivo.filename
    else:
      imagen = None

    # Ejecutar query    
    datos =(nombre,subtitulo, archivo.filename)

    with conexion:
      with conexion.cursor() as cursor:
        cursor.execute(sql, datos)
        conexion.commit()

  except Exception as e:
    # Manejar error    
    conexion.rollback()
    print(f'Error al guardar nota: {e}')
  
  finally:
    # Cerrar conexión
    conexion.close()

  return redirect('/admin/notas')


@app.route('/admin/notas/borrar', methods=['post'])
def admin_ropas_borrar():
    _Id=request.form['txtId']
    datos=_Id
    conexion = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054"
    )
    cursor=conexion.cursor()
    cursor.execute(f'DELETE FROM "juegos" WHERE "juegos"."ID" = {_Id};')
    conexion.commit()
    return redirect('/admin/notas')

@app.route('/admin/logueado', methods=['post'])
def admin_login():
    user=request.form["txtuser"]
    clave=request.form["txtclave"]
    if user == "admin" and  clave == "admin":
        session["login"]=True
        session["user"]="administrador"
        return redirect ("/admin/inicio")
        
    else:
        print("Usuario o Clave incorrecta")
        session["login"]=False
        return redirect("/login")
        
# Agrega esta nueva ruta en tu código
@app.route('/admin/notas/actualizar/<int:nota_id>', methods=['GET', 'POST'])
def admin_actualizar_nota(nota_id):
    if request.method == 'POST':
        # Obtener datos del formulario de actualización
        nuevo_nombre = request.form['txtNombre']
        nuevo_archivo = request.files['txtImagen']
        nuevo_subtitulo = request.form['Subtitulo']

        try:
            # Conectar a la BD
            conexion = psycopg2.connect("postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054")  # Tu cadena de conexión

            # Consultar la nota existente
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM "juegos" WHERE "ID" = %s;', (nota_id,))
                nota_existente = cursor.fetchone()

                # Actualizar datos si el formulario incluyó un archivo
                if nuevo_archivo:
                    nuevo_archivo.save('templates/sitio/img/' + nuevo_archivo.filename)
                    nuevo_imagen = nuevo_archivo.filename
                else:
                    nuevo_imagen = nota_existente[3]

                # Ejecutar consulta de actualización
                sql = 'UPDATE "juegos" SET "TITULO" = %s, "SUBTITULO" = %s, "IMAGEN" = %s WHERE "ID" = %s;'
                nuevos_datos = (nuevo_nombre, nuevo_subtitulo, nuevo_imagen, nota_id)
                cursor.execute(sql, nuevos_datos)
                conexion.commit()

        except Exception as e:
            # Manejar error
            conexion.rollback()
            print(f'Error al actualizar nota: {e}')

        finally:
            # Cerrar conexión
            conexion.close()

        return redirect('/admin/notas')

    else:
        try:
            # Conectar a la BD
            conexion = psycopg2.connect("postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require&options=endpoint%3Dep-green-mouse-73455054")  # Tu cadena de conexión

            # Consultar la nota existente
            with conexion.cursor() as cursor:
                cursor.execute('SELECT * FROM "juegos" WHERE "ID" = %s;', (nota_id,))
                nota_existente = cursor.fetchone()

        except Exception as e:
            # Manejar error
            print(f'Error al obtener nota: {e}')

        finally:
            # Cerrar conexión
            conexion.close()

        return render_template('admin/actualizar_nota.html', nota=nota_existente)

    

if __name__ == "__main__":
    app.run(port=port, debug=True)
    
