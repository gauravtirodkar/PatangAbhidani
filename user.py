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
import plotly
import plotly.graph_objs as go
import json


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
        return False\


@app.route("/")
def home():
    global session
    return render_template("index.html", sess=session)
@app.route("/car")
def car():
    c = mysql.connection.cursor()
    c.execute("SELECT * FROM butterflydata ORDER BY RAND() LIMIT 3;")
    data = c.fetchall()
    c.close()

    return render_template("carousel.html",data=data)

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
    cur.execute("SELECT *,COUNT(*) from butterflydata GROUP BY sub_species")
    gallery_data = cur.fetchall()
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
        gallery_data = gallery_data,
        location=location,
        state=state,
        user="LoggedIn",
        url=url,
        sess=session,
    )

def create_plot(gallery_data):
    
    df = pd.DataFrame(gallery_data)
    data1 = [
        go.Bar(
            marker_color = '#32a852',
            x = df[7],
            y = df[14]
        )
    ]
    graphJSON = json.dumps(data1, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def locn_plot(locinfo):
    
    df = pd.DataFrame(locinfo)
    data2 = [
        go.Bar(
            marker_color = '#32a852',
            x = df[0],
            y = df[1]
        )
    ]
    graphJSON = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@app.route("/updateTable", methods=["POST"])
def updateTable():
    places = request.form.getlist("locn")
    state_f = request.form.getlist("st")
    sub_spec = request.form.getlist("sub_spec")
    spec = request.form.getlist("spec")
    ssfam = request.form.getlist("ssfam")
    sfam = request.form.getlist("sfam")
    mnth = request.form.get("mnth")
  
    year = mnth[0:4]
    month = mnth[5:]

    fdate  = str(str(month) + "-" + str(year))

    print(fdate)

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
    for i in range(len(spcs)):
        spcs[i]=spcs[i].lower()
    #print(spcs)
    if (len(plcs)!=0):
        df1 = df.loc[df[3].isin(plcs)]
    else:
        df1=df
    #print(df1)
    if (len(spcs)!=0):
        df2 = df.loc[df[8].isin(spcs)]
    else:
        df2=df
    #print(df2)
    df = df1.merge(df2, how="inner", indicator=False)
    #print(df)
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
        '''if (lat!="" and lon!=""):
            lat=float(lat)
            lon=float(lon)
            marker = folium.Marker([lat, lon], popup=popup)

        marker.add_to(m)

    m.save("./templates/Heatmap_filter.html")'''
    url = "http://127.0.0.1:5000/map_filter"

    cur = mysql.connection.cursor()

    if fdate != "-":
        #data for filtered display of database
        if len(places) > 1 and len(sub_spec) == 0:
            cur.execute("SELECT * from butterflydata where city in {} AND SUBSTRING(date,-7) = (%s)".format(places),(fdate,))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata where city in {} AND SUBSTRING(date,-7) = (%s) GROUP BY sub_species".format(places),(fdate,))
            gallery_data = cur.fetchall()
        elif len(sub_spec) > 1 and len(places) == 0:
            cur.execute("SELECT * from butterflydata where sub_species in {} AND SUBSTRING(date,-7) = (%s)".format(sub_spec),(fdate,))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata where sub_species in {} AND SUBSTRING(date,-7) = (%s) GROUP BY sub_species".format(sub_spec),(fdate,))
            gallery_data = cur.fetchall()
        elif len(places) > 1 and len(sub_spec) > 1:
            cur.execute("SELECT * from butterflydata where city in {} and sub_species in {} AND SUBSTRING(date,-7) = (%s)".format(places, sub_spec),(fdate,))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata where city in {} and sub_species in {} AND SUBSTRING(date,-7) = (%s) GROUP BY sub_species".format(places, sub_spec),(fdate,))
            gallery_data = cur.fetchall()
        else:
            cur.execute("SELECT * FROM butterflydata WHERE SUBSTRING(date,-7) = %s",(fdate,))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) FROM butterflydata WHERE SUBSTRING(date,-7) = %s GROUP BY sub_species",(fdate,))
            gallery_data = cur.fetchall()
    else:
        #data for filtered display of database
        if len(places) > 1 and len(sub_spec) == 0:
            cur.execute("SELECT * from butterflydata where city in {}".format(places))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata where city in {} GROUP BY sub_species".format(places))
            gallery_data = cur.fetchall()
        elif len(sub_spec) > 1 and len(places) == 0:
            cur.execute("SELECT * from butterflydata where sub_species in {}".format(sub_spec))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata where sub_species in {} GROUP BY sub_species".format(sub_spec))
            gallery_data = cur.fetchall()
        elif len(places) > 1 and len(sub_spec) > 1:
            cur.execute("SELECT * from butterflydata where city in {} and sub_species in {}".format(places, sub_spec))
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT (*) from butterflydata where city in {} and sub_species in {} GROUP BY sub_species".format(places, sub_spec))
            gallery_data = cur.fetchall()
        else:
            cur.execute("SELECT * from butterflydata")
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata GROUP BY sub_species")
            gallery_data = cur.fetchall()

    

    #data for filter options
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
    cur.execute("SELECT location, COUNT(location) from butterflydata GROUP BY location")
    locinfo = cur.fetchall()
    cur.close()

    #Data for data analysis
    bar = create_plot(gallery_data)
    
    
    locndeets = locn_plot(locinfo)

    global session
    return render_template(
        "images_grid.html",
        places=places,
        state_f = state_f,
        sub_spec=sub_spec,
        spec = spec,
        ssfam = ssfam,
        sfam = sfam,
        mnth = mnth,
        species=species,
        species_name=species_name,
        sub_sub_family=sub_sub_family,
        sub_family=sub_family,
        data=data,
        gallery_data = gallery_data,
        location=location,
        state=state,
        user="LoggedIn",
        url=url,
        plot = bar,
        locndeets = locndeets,
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

            m.save("./templates/Heatmap.html")

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