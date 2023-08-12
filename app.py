from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

try:
    connection = psycopg2.connect(
        host='ep-green-mouse-73455054.us-east-2.aws.neon.tech',
        user='fl0user',
        password='cbJHw60QaLkC',
        database='mi-app'
    )
    print("Conexión exitosa")
except Exception as ex:
    print(ex)

@app.route('/')
def home():
    # Crear un cursor
    cursor = connection.cursor()

    # Consulta SQL
    query = "SELECT * FROM juegos;"

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados
    juegos = cursor.fetchall()

    # Cerrar el curso
    cursor.close()

    # Renderizar la plantilla con los resultados
    return render_template('index.html', juegos=juegos)

if __name__ == "__main__":
    app.run()
