from flask import Flask, render_template, request, redirect, url_for
import pymysql
import pymysql.cursors
from dbconfig import getDBConnection


app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id, nombre, apellido FROM usuario")
        registro = cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        registro = []
    finally:
        cursor.close()
        connection.close()

    return render_template('form.html', contacts = registro,contact_to_edit=None)

@app.route('/', methods=['POST'])
def submit():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("INSERT INTO usuario (nombre, apellido) VALUES (%s,%s)", (nombre, apellido))
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))

@app.route('/edit/<int:contact_id>', methods =['GET'])
def edit(contact_id):
    connection = getDBConnection()
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    try:
        cursor.execute("SELECT id, nombre, apellido FROM usuario WHERE id=%s",(contact_id))
        contact = cursor.fetchone()
    except pymysql.MySQLError as e:
        app.logger.error(f"Error:{e}")
        contact = None
    finally:
        cursor.close()
        connection.close()
    return render_template('form.html',contacts=[], contact_to_edit=contact)

@app.route('/update/<int:contact_id>', methods =['POST'])
def update(contact_id):
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    
    connection = getDBConnection()
    cursor = connection.cursor()

    try:
        cursor.execute("UPDATE usuario SET nombre = %s, apellido = %s WHERE id=%s ", (nombre, apellido,contact_id))
        connection.commit()
    except pymysql.MySQLError as e:
        app.logger.error(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('index'))



if __name__ == "__main__":
    app.run(debug=True)