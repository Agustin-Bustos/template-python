connection_string = "postgres://fl0user:z1iKnXGNSw9e@ep-odd-resonance-87921203.us-east-2.aws.neon.tech:5432/postgres?sslmode=require"

# Intentar establecer la conexión
try:
    # Establecer la conexión
    connection = psycopg2.connect(connection_string)

    # Crear un cursor
    cursor = connection.cursor()

    # Realizar operaciones en la base de datos
    cursor.execute("SELECT * FROM PEPElol;")
    rows = cursor.fetchall()

    # Hacer algo con los datos recuperados
    for row in rows:
        print(row)

    # Cerrar el cursor y la conexión
    cursor.close()
    connection.close()

except psycopg2.Error as e:
    print("Error:", e)