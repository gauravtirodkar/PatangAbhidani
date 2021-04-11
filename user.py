from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import matplotlib.pyplot as plt
import numpy as np
import os
import folium
import pandas as pd
import branca
import datetime
from keras.preprocessing import image
from numpy import loadtxt
from keras.models import load_model
import tensorflow as tf


UPLOAD_FOLDER = "C:/xampp/htdocs/butterfly"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])
""" from flask import Flask, url_for, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) """
app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "butterfly"

mysql = MySQL(app)
global session
session = False


def insert_users(email, password, name):
    c = mysql.connection.cursor()
    c.execute(
        "INSERT INTO user (email,password,name) VALUES (%s, %s, %s)",
        (email, password, name),
    )
    mysql.connection.commit()
    c.close()


def check_valid_password(email, password):
    c = mysql.connection.cursor()
    email = str(email)
    c.execute("SELECT * FROM user where email = (%s)", (email,))
    data = c.fetchall()
    mysql.connection.commit()
    c.close()
    if len(data) == 1:
        return data[0][2] == password
    else:
        return False


@app.route("/")
def home():
    global session
    return render_template("index.html", sess=session)


@app.route("/map")
def map():
    return render_template("Heatmap.html")


@app.route("/map_filter")
def map_filter():
    return render_template("Heatmap_filter.html")


@app.route("/specsdeets")
def specsdeets():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from butterflydata")
    data = cur.fetchall()
    cur.execute("SELECT * FROM location")
    location = cur.fetchall()
    cur.execute("SELECT DISTINCT state FROM location")
    state = cur.fetchall()
    cur.close()
    return render_template(
        "species_details.html",
        data=data,
        location=location,
        state=state,
        user="LoggedIn",
    )


@app.route("/images")
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
    url = "http://127.0.0.1:5000/map"
    global session
    return render_template(
        "images_grid.html",
        species=species,
        species_name=species_name,
        sub_sub_family=sub_sub_family,
        sub_family=sub_family,
        data=data,
        location=location,
        state=state,
        user="LoggedIn",
        url=url,
        sess=session,
    )


@app.route("/updateTable", methods=["POST"])
def updateTable():
    places = request.form.getlist("locn")
    sub_spec = request.form.getlist("sub_spec")

    if len(places) == 1:
        places = tuple(tuple(places) + tuple(places))
    else:
        places = tuple(places)
    

    if len(sub_spec) == 1:
        sub_spec = tuple(tuple(sub_spec) + tuple(sub_spec))
    else:
        sub_spec = tuple(sub_spec)
   
    plcs = list(places)
    spcs = list(sub_spec)
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from butterflydata")
    data = cur.fetchall()
    df = pd.DataFrame(data)

    df1 = df.loc[df[3].isin(plcs)]
    df2 = df.loc[df[8].isin(spcs)]
    df = df1.merge(df2, how="inner", indicator=False)

    m = folium.Map(location=[20.593684, 78.96288], zoom_start=5, disable_3d=True)

    def get_frame(url, width, height, loc, datee, sn, cb):
        html = (
            """ 
                <!doctype html>
            <html>
        
            <img id="myIFrame" class="frame" width="{}px" height="{}px" src=http://localhost:3000/butterfly/{}""".format(
                width, height, url
            )
            + """ frameborder="0" ></img>
            <p>scientific name :<b>{}</b>""".format(
                sn
            )
            + """<br>date : <b>{}</b>""".format(datee)
            + """<br>clicked by : <b>{}</b>""".format(cb)
            + """<br>location : <b>{}</b>""".format(loc)
            + """</p>
        
        
            <style>
        
            .frame {

                border: 0;
                
                overflow:hidden;
            
            }
            </style>
            </html>"""
        )
        return html

    for img1, lat, lon, loc, datee, sn, cb in zip(
        df[0], df[12], df[13], df[2], df[1], df[7], df[6]
    ):

        popup = get_frame(img1, 150, 150, loc, datee, sn, cb)
        iframe = branca.element.IFrame(html=popup, width=200, height=200)
        popup = folium.Popup(iframe, max_width=200)
        marker = folium.Marker([lat, lon], popup=popup)

        marker.add_to(m)

    m.save("E:/Project_TE/testing/PatangAbhidani/templates/Heatmap_filter.html")
    url = "http://127.0.0.1:5000/map_filter"

    cur = mysql.connection.cursor()

    if len(places) > 1 and len(sub_spec) == 0:
        cur.execute("SELECT * from butterflydata where city in {}".format(places))
        data = cur.fetchall()
    elif len(sub_spec) > 1 and len(places) == 0:
        cur.execute(
            "SELECT * from butterflydata where sub_species in {}".format(sub_spec)
        )
        data = cur.fetchall()
    elif len(places) > 1 and len(sub_spec) > 1:
        cur.execute(
            "SELECT * from butterflydata where city in {} and sub_species in {}".format(
                places, sub_spec
            )
        )
        data = cur.fetchall()
    else:
        cur.execute("SELECT * from butterflydata")
        data = cur.fetchall()
    """cur.execute("SELECT * from butterflydata where city in {}".format(places))
    data = cur.fetchall()"""

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
    global session
    return render_template(
        "images_grid.html",
        places=places,
        sub_spec=sub_spec,
        species=species,
        species_name=species_name,
        sub_sub_family=sub_sub_family,
        sub_family=sub_family,
        data=data,
        location=location,
        state=state,
        user="LoggedIn",
        url=url,
        sess=session,
    )


@app.route("/addData")
def addData():
    return render_template("addData.html", user="LoggedIn")


@app.route("/upload")
def upload():
    global session
    if session == True:
        xyz=False
        return render_template("img.html", sess=session,xyz=xyz)
    else:
        return new_login()


@app.route("/img", methods=["GET", "POST"])
def img():
    if request.method == "POST":
        f = request.files["file"]
        f.filename=f.filename.replace(" ","_")
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
        path = f'C:/xampp/htdocs/butterfly/{f.filename}'
        img = image.load_img(path, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        model = load_model('E:/Project_TE/testing/PatangAbhidani/model.h5')
        classes = model.predict(x)
        if classes[0]<0.5:
            result = request.form
            str1 = str(f.filename)
            str1 = str1.replace(" ", "_")
            lst = [
                str1,
                result["text2"],
                result["text3"],
                result["text4"],
                result["text5"],
                result["text6"],
                result["text7"],
                result["text8"],
            ]
            c = mysql.connection.cursor()
            c.execute("INSERT INTO butterflydata (img,date,location,sub_species,clicked_by,scientific_name,latitude,longitude) VALUES (%s, %s, %s,%s, %s, %s,%s,%s)",(str1,result["text2"],result["text3"],result["text4"],result["text5"],result["text6"],result["text7"],result["text8"]))
            mysql.connection.commit()
            c.close()
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from butterflydata")
            data = cur.fetchall()
            df = pd.DataFrame(data)
            m = folium.Map(location=[20.593684, 78.96288], zoom_start=5, disable_3d=True)
            def get_frame(url, width, height, loc, datee, sn, cb):
                html = (
                    """ 
                        <!doctype html>
                    <html>
                
                    <img id="myIFrame" class="frame" width="{}px" height="{}px" src=http://localhost:3000/butterfly/{}""".format(
                        width, height, url
                    )
                    + """ frameborder="0" ></img>
                    <p>scientific name :<b>{}</b>""".format(
                        sn
                    )
                    + """<br>date : <b>{}</b>""".format(datee)
                    + """<br>clicked by : <b>{}</b>""".format(cb)
                    + """<br>location : <b>{}</b>""".format(loc)
                    + """</p>
                
                
                    <style>
                
                    .frame {

                        border: 0;
                        
                        overflow:hidden;
                    
                    }
                    </style>
                    </html>"""
                )
                return html

            for img1, lat, lon, loc, datee, sn, cb in zip(df[0], df[12], df[13], df[2], df[1], df[7], df[6]):
                popup = get_frame(img1, 150, 150, loc, datee, sn, cb)
                iframe = branca.element.IFrame(html=popup, width=200, height=200)
                popup = folium.Popup(iframe, max_width=200)
                if (lat!="" and lon!=""):
                    lat=float(lat)
                    lon=float(lon)
                    marker = folium.Marker([lat,lon], popup=popup)

                marker.add_to(m)

            m.save("E:/Project_TE/testing/PatangAbhidani/templates/Heatmap.html")

            return render_template("Heatmap.html", name=f.filename)
        else:
            xyz=True
            global session
            return render_template("img.html",sess=session,xyz=xyz)

@app.route("/logout") 
def logout():
    global session
    session = False
    return home()

@app.route("/new_login", methods=["GET", "POST"])
def new_login():
    global session
    if request.method == "POST":
        try:
            # REGISTER User
            email = request.form["email"]
            name = request.form["name"]
            password = request.form["password"]
            try:
                insert_users(email, password, name)
                session = True
                return jsonify({"status": "Success"})
            except:
                return jsonify({"error": "User already exists"})
        except:
            email = request.form["email"]
            password = request.form["password"]
            if check_valid_password(email, password):
                session = True
                return jsonify({"status": "Success"})
            else:
                return jsonify({"error": "Invalid Username or Password"})
    return render_template("new_login.html", sess=session)


if __name__ == "__main__":
    app.run(debug=True)