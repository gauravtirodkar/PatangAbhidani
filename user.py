from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'butterfly'
 
mysql = MySQL(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from details")
    data = cur.fetchall()
    cur.close()
    return render_template('species_details.html', data=data,user="LoggedIn")

@app.route('/images')
def images_grid():
    return render_template('images_grid.html',user="LoggedIn")

if __name__ == '__main__':
    app.run(debug=True)