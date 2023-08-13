
from flask import Flask, render_template
import psycopg2, os

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


@app.route('/')
def home():
    # Crear un cursor
    print("conexion realizada")
    connection = psycopg2.connect(
        "postgres://fl0user:cbJHw60QaLkC@ep-green-mouse-73455054.us-east-2.aws.neon.tech:5432/mi-app?sslmode=require"
    )
    cursor = connection.cursor()
    
    # Consulta SQL
    query = "SELECT * FROM juegos;"

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados
    juegos = cursor.fetchall()

    # Cerrar el cursor
    cursor.close()

    # Renderizar la plantilla con los resultados
    return render_template('index.html', juegos=juegos)

if __name__ == "__main__":
    app.run(port=port)
