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
    places = request.form.getlist('locn')
    sub_spec = request.form.getlist('sub_spec')

    if len(places) == 1:
        places = tuple(tuple(places)+tuple(places))
    else:
        places = tuple(places)
    print(places)

    if len(sub_spec) == 1:
        sub_spec = tuple(tuple(sub_spec)+tuple(sub_spec))
    else:
        sub_spec = tuple(sub_spec)
    print(sub_spec)

    cur = mysql.connection.cursor()

    if len(places) > 1 and len(sub_spec) == 0:
        cur.execute("SELECT * from butterflydata where city in {}".format(places))
        data = cur.fetchall()
    elif len(sub_spec)>1 and len(places) == 0:
        cur.execute("SELECT * from butterflydata where sub_species in {}".format(sub_spec))
        data = cur.fetchall()
    elif len(places) > 1 and len(sub_spec) > 1:
        cur.execute("SELECT * from butterflydata where city in {} and sub_species in {}".format(places, sub_spec))
        data = cur.fetchall()
    else:
        cur.execute("SELECT * from butterflydata")
        data = cur.fetchall()
    '''cur.execute("SELECT * from butterflydata where city in {}".format(places))
    data = cur.fetchall()'''

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
    return render_template('images_grid.html', places=places, sub_spec = sub_spec, species=species, species_name=species_name, sub_sub_family=sub_sub_family, sub_family=sub_family, data=data, location=location, state=state, user="LoggedIn")



 

@app.route('/addData')
def addData():
    return render_template('addData.html', user="LoggedIn")

if __name__ == '__main__':
    app.run(debug=True)