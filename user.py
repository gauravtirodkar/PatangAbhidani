from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from bs4 import BeautifulSoup

app = Flask(__name__)
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'butterfly'
 
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html', user="LoggedIn")
@app.route('/map')
def map():
    return render_template('Heatmap.html')
@app.route('/specsdeets')
def specsdeets():
    #return render_template('species_details.html',user="LoggedIn")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from butterflydata")
    data = cur.fetchall()
    cur.execute("SELECT * FROM location")
    location = cur.fetchall()
    cur.execute("SELECT DISTINCT state FROM location")
    state = cur.fetchall()
    cur.close()
    return render_template('species_details.html', data=data, location=location, state=state, user="LoggedIn")

@app.route('/images')
def images_grid():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from butterflydata")
    data = cur.fetchall()
    cur.execute("SELECT * FROM location")
    location = cur.fetchall()
    cur.execute("SELECT DISTINCT state FROM location ")
    state = cur.fetchall()
    cur.close()
    return render_template('images_grid.html', data=data, location=location, state=state, user="LoggedIn")

@app.route('/updateTable',methods = ["POST"])
def updateTable ():
    name = tuple(request.form.getlist('list[]'))
    print(name)
    cur = mysql.connection.cursor()
    
    cur.execute("SELECT city FROM location where city IN {}".format(name))
    location = [item[0] for item in cur.fetchall()]
    location = tuple(location)

    cur.execute("SELECT * from butterflydata where location IN {}".format(location))
    data = cur.fetchall()

    cur.execute("SELECT DISTINCT state FROM location")
    state = cur.fetchall()
    cur.close()
    return render_template('images_grid.html', data=data, location=location, state=state, user="LoggedIn")
 

@app.route('/addData')
def addData():
    return render_template('addData.html', user="LoggedIn")

if __name__ == '__main__':
    app.run(debug=True)