import psycopg2
import os
from flask import Flask, send_from_directory, render_template, redirect

try:
    connection=psycopg2.connect(
        host='ep-odd-resonance-87921203.us-east-2.aws.neon.tech',
        user='fl0user',
        password='z1iKnXGNSw9e',
        database='postgres'
        #port='5432'
    )
    
    print("conesion esitosa")
    
except Exception as ex:
    print(ex) 
    
    
    
    
app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)