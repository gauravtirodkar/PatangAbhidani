from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import os
import json
from csv import writer
import folium
import pandas as pd
import branca
import gzip
import time
import datetime
import random
from io import BufferedReader
UPLOAD_FOLDER = 'C:/applications/XAMPP/htdocs/butterfly'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
""" from flask import Flask, url_for, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) """
app = Flask(__name__)
 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'butterfly'
 
mysql = MySQL(app)

def insert_users(email,password,name):
    c = mysql.connection.cursor()
    c.execute("INSERT INTO user (email,password,name) VALUES (%s, %s, %s)",(email,password,name))
    mysql.connection.commit()
    c.close()

def check_valid_password(email,password):
    print("3 if")
    c = mysql.connection.cursor()
    print("4 if")
    email= str(email)
    c.execute("SELECT * FROM user where email = (%s)",(email,))
    print("5 if")
    data = c.fetchall()
    print("6 if")
    mysql.connection.commit()
    print("7 if")
    c.close()
    print("8 if")
    if len(data) == 1:
        print("9 if")
        print(password)
        print(data[0][2])
        return data[0][2] == password
    else:
        return False

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

@app.route('/upload')  
def upload():  
    return render_template("img.html")  
    
@app.route('/img', methods=['GET', 'POST'])
def img():
    if request.method == 'POST':  
        f = request.files['file']  
        result = request.form
        str1=str(f.filename)
        lst=[str1,result['text2'],result['text3'],result['text4'],result['text5'],result['text6'],result['text7'],result['text8']]
        print(lst)
        with open('static/combined.csv', 'a') as f_object:
        
            # Pass this file object to csv.writer()
            # and get a writer object
            writer_object = writer(f_object)
        
            # Pass the list as an argument into
            # the writerow()
            writer_object.writerow(lst)
        
            #Close the file object
            f_object.close()
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))  
        df = pd.read_csv("static/combined.csv")


        m = folium.Map(location=[20.593684, 78.96288],zoom_start=5,disable_3d=True)


        def get_frame(url,width,height,loc,datee,sn,cb):
            html = """ 
                    <!doctype html>
                <html>
            
                <img id="myIFrame" class="frame" width="{}px" height="{}px" src=http://localhost/butterfly/{}""".format(width,height,url) + """ frameborder="0" ></img>
                <p>scientific name :<b>{}</b>""".format(sn)+"""<br>date : <b>{}</b>""".format(datee)+"""<br>clicked by : <b>{}</b>""".format(cb)+"""<br>location : <b>{}</b>""".format(loc)+"""</p>
            
            
                <style>
            
                .frame {

                    border: 0;
                    
                    overflow:hidden;
                
                }
                </style>
                </html>"""
            return html
        for img1,lat,lon,loc,datee,sn,cb in zip(df['img'],df['latitude'],df['longitude'],df["location"],df['date'],df['scientific name'],df['click by']):

            popup = get_frame(img1,
                            150,
                            150,loc,datee,sn,cb)
            iframe = branca.element.IFrame(html=popup,width=200,height=200)
            popup = folium.Popup(iframe,max_width=200)
            marker = folium.Marker([lat,lon],popup=popup)

            marker.add_to(m)

        m.save("templates/Heatmap.html")

        return render_template("Heatmap.html", name = f.filename)  

@app.route("/new_login",methods = ["GET","POST"])
def new_login():
    if request.method == "POST":
        try:
            #REGISTER User
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            try:
                insert_users(email,password,name)
                return jsonify({"status":"Success"})
            except:
                return jsonify({"error":"User already exists"})
        except:
            email = request.form["email"]
            password = request.form["password"]
            if(check_valid_password(email,password)):
                print("1 if")
                return jsonify({"status":"Success"})
                print("2 if")
            else:
                return jsonify({"error":"Invalid Username or Password"})
    return render_template("new_login.html")



if __name__ == '__main__':
    app.run(debug=True)