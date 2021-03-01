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
    return render_template('index.html',user="LoggedIn")

@app.route('/specsdeets')
def specsdeets():
    #return render_template('species_details.html',user="LoggedIn")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from butterflydata")
    data = cur.fetchall()
    cur.close()
    return render_template('species_details.html', data=data,user="LoggedIn")

@app.route('/images')
def images_grid():
    return render_template('images_grid.html',user="LoggedIn")

@app.route('/addData')
def addData():
    return render_template('addData.html',user="LoggedIn")

if __name__ == '__main__':
    app.run(debug=True)