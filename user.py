from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from bs4 import BeautifulSoup
import json
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
    cur.execute("SELECT DISTINCT species_name,sub_family FROM species")
    species_name = cur.fetchall()
    print(species_name[0])
    cur.execute("SELECT DISTINCT sub_family FROM species")
    sub_family = cur.fetchall()
    cur.close()
    # print(data)
    # print(data[0][1])
    # aqi = [x[0][1] for x in data]
    # print(aqi)
    lst=[]
    for i in data:
        i= list(i)
        lst.append(i)
    print(lst)
    # pm10 = [x for x in data[7,8]]
    # pm100 = [x for x in data[1]]
    # pm101 = [x for x in data[4]]
    # pm102 = [x[6] for x in data]
    # pm103 = [x[5] for x in data]


    # fin = [aqi,pm10,pm100,pm101]
    # lst  =[]
    # print(fin)

    # for i in range(len(fin)):
    #     lst.append([fin[j][i] for j in  range(len(fin))])
    dict1={}
    dict1["data"]=lst 
    out_file = open("templates/data.txt", "w") 
    json.dump(dict1, out_file, indent = 6) 
    return render_template('images_grid.html', species=species, species_name=species_name, sub_family=sub_family, data=data, location=location, state=state, user="LoggedIn")

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