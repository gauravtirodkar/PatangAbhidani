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
    
    cur.execute("SELECT * FROM species")
    species = cur.fetchall()
    cur.execute("SELECT DISTINCT sub_sub_family, sub_family FROM species")
    sub_sub_family = cur.fetchall()
    cur.execute("SELECT DISTINCT species_name, sub_sub_family, sub_family FROM species")
    species_name = cur.fetchall()
    cur.execute("SELECT DISTINCT sub_family FROM species")
    sub_family = cur.fetchall()
    cur.close()
    return render_template('images_grid.html', species=species, species_name=species_name, sub_sub_family=sub_sub_family, sub_family=sub_family, data=data, location=location, state=state, user="LoggedIn")

@app.route('/updateTable',methods = ["POST"])
def updateTable ():
    places = request.get_json()
    places = tuple(places.get("locn"))

    print(places)

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM location ")
    location = cur.fetchall()

    cur.execute("SELECT * from butterflydata where city IN {}".format(places))
    data = cur.fetchall()

    print(data)

    cur.execute("SELECT DISTINCT state FROM location")
    state = cur.fetchall()

    cur.execute("SELECT * FROM species")
    species = cur.fetchall()
    cur.execute("SELECT DISTINCT sub_sub_family, sub_family FROM species")
    sub_sub_family = cur.fetchall()
    cur.execute("SELECT DISTINCT species_name, sub_sub_family, sub_family FROM species")
    species_name = cur.fetchall()
    cur.execute("SELECT DISTINCT sub_family FROM species")
    sub_family = cur.fetchall()
    cur.close()
    return render_template('images_grid.html', species=species, species_name=species_name, sub_sub_family=sub_sub_family, sub_family=sub_family, data=data, location=location, state=state, user="LoggedIn")


 

@app.route('/addData')
def addData():
    return render_template('addData.html', user="LoggedIn")

if __name__ == '__main__':
    app.run(debug=True)