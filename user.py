from flask import Flask, render_template, request, redirect
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


""" class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	username = db.Column(db.String(80), unique=True)
	password = db.Column(db.String(80))

	def __init__(self, name, username, password):
		self.name = name
		self.username = username
		self.password = password """

@app.route('/auth')
def auth():
	return render_template('layout/auth.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		name = request.form['username']
		passw = request.form['password']
		try:
			data = User.query.filter_by(username=name, password=passw).first()
		except:
			return "Incorrect Login"
	return render_template('layout/auth.html')

""" @app.route('/register', methods=['POST'])
def register():
	if request.method == 'POST':
		new_user = User(name=request.form['name'], username=request.form['username'], password=request.form['password'])
		db.session.add(new_user)
		db.session.commit()
	return render_template('auth.html') """

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
            marker = folium.Marker([lat,lon],
                                        popup=popup)

            marker.add_to(m)

        m.save("templates/Heatmap.html")

        return render_template("Heatmap.html", name = f.filename)  


if __name__ == '__main__':
    app.run(debug=True)