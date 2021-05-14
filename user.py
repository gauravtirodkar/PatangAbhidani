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
import requests, json

UPLOAD_FOLDER = "./upload_image/"
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
@app.route("/carou")
def carou():
    c = mysql.connection.cursor()
    c.execute("SELECT * FROM butterflydata ORDER BY RAND() LIMIT 5;")
    data = c.fetchall()
    c.close()

    return render_template("carou.html",data=data)
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

def create_plot(gallery_data):
    
    df = pd.DataFrame(gallery_data)
    if not (df.empty):
        fig = go.Figure(go.Bar(
        marker_color = '#32a852',
                x = df[7],
                y = df[14]))
        
        fig.update_layout(
        title={
            'text': "Species vs Count",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Species",
        yaxis_title="Count",
        xaxis_tickangle=45
        )
    else:
        fig = go.Figure()

        # Add trace
        fig.add_trace(
            go.Scatter(x=[0], y=[0])
        )

        # Add images
        fig.add_layout_image(
                dict(
                    source="static/img/2.jpg",
                    xref="x",
                    yref="y",
                    x=-1,
                    y=1,
                    sizex=2,
                    sizey=2,
                    sizing="stretch",
                    opacity=0.6,
                    layer="below")
        )

        # Set templates
        fig.update_layout(template="plotly_white")   

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def locn_plot(locinfo):
    
    df = pd.DataFrame(locinfo)
    if not (df.empty):
        data2 = go.Figure(go.Bar(
                marker_color = 'forestgreen',
                x = df[0],
                y = df[1]
            ))

        data2.update_layout(
        title={
            'text': "Location vs Count",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Location",
        yaxis_title="Count",
        xaxis_tickangle=45
        )
    else:
        data2 = go.Figure()

        # Add trace
        data2.add_trace(
            go.Scatter(x=[0], y=[0])
        )

        # Add images
        data2.add_layout_image(
                dict(
                    source="static/img/butterfly/3-1.jpg",
                    xref="x",
                    yref="y",
                    x=-1,
                    y=1,
                    sizex=2,
                    sizey=2,
                    sizing="stretch",
                    opacity=0.6,
                    layer="below")
        )

        # Set templates
        data2.update_layout(template="plotly_white") 
    graphJSON = json.dumps(data2, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def locnvsspecies(locn_data):
    
    df = pd.DataFrame(locn_data)
    if not (df.empty):
        data3 = go.Figure(go.Scatter  (
                marker_color = 'forestgreen',
                x = df[3],
                y = df[8],
                mode='markers'
            ))

        data3.update_layout(
        title={
            'text': "Location vs Species",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="Location",
        yaxis_title="Species",
        xaxis_tickangle=45
        )
    else:
        data3 = go.Figure()

        # Add trace
        data3.add_trace(
            go.Scatter(x=[0], y=[0])
        )

        # Add images
        data3.add_layout_image(
                dict(
                    source="static/img/1.jpg",
                    xref="x",
                    yref="y",
                    x=-1,
                    y=1,
                    sizex=2,
                    sizey=2,
                    sizing="stretch",
                    opacity=0.6,
                    layer="below")
        )

        # Set templates
        data3.update_layout(template="plotly_white") 

    graphJSON = json.dumps(data3, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

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
    cur.execute("SELECT city, COUNT(city) from butterflydata GROUP BY city")
    locinfo = cur.fetchall()
    cur.close()

    bar = create_plot(gallery_data)
    locndeets = locn_plot(locinfo)
    locnspecies = locnvsspecies(data)

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
        plot = bar,
        locndeets = locndeets,
        locnspecies = locnspecies,
        sess=session
    )

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
       
    # plcs = list(places)
    # spcs = list(sub_spec)
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * from butterflydata")
    # data = cur.fetchall()
    # df = pd.DataFrame(data)
    # for i in range(len(spcs)):
    #     spcs[i]=spcs[i].lower()
    # #print(spcs)
    # if (len(plcs)!=0):
    #     df1 = df.loc[df[3].isin(plcs)]
    # else:
    #     df1=df
    # #print(df1)
    # if (len(spcs)!=0):
    #     df2 = df.loc[df[8].isin(spcs)]
    # else:
    #     df2=df
    # #print(df2)
    # df = df1.merge(df2, how="inner", indicator=False)
    #print(df)


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
            cur.execute("SELECT *, COUNT(*) from butterflydata where city in {} and sub_species in {} GROUP BY sub_species".format(places, sub_spec))
            gallery_data = cur.fetchall()
        else:
            cur.execute("SELECT * from butterflydata")
            data = cur.fetchall()
            cur.execute("SELECT *, COUNT(*) from butterflydata GROUP BY sub_species")
            gallery_data = cur.fetchall() 
    df = pd.DataFrame(data)
    
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
    cur.execute("SELECT city, COUNT(city) from butterflydata GROUP BY city")
    locinfo = cur.fetchall()
    cur.close()

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
            <p> Scientific Name : <i> <b>{}</b> </i>""".format(
                sn
            )
            + """<br>Date : <b>{}</b>""".format(datee)
            # + """<br>Clicked by : <b>{}</b>""".format(cb)
            + """<br>Location : <b>{}</b>""".format(loc)
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
    if not (df.empty):
        sci_name = df[9] + " " + df[8]
        print("Show this : ", sci_name)
        for img1, lat, lon, loc, datee, sn, cb in zip(
            df[0], df[12], df[13], df[2], df[1], sci_name, df[6]
        ):

            popup = get_frame(img1, 150, 150, loc, datee, sn, cb)
            iframe = branca.element.IFrame(html=popup, width=200, height=200)
            popup = folium.Popup(iframe, max_width=200)
            
            if (lat!="" and lon!=""):
                lat=float(lat)
                lon=float(lon)
                marker = folium.Marker([lat, lon], popup=popup)

            marker.add_to(m)

    m.save("./templates/Heatmap_filter.html")
    url = "http://127.0.0.1:5000/map_filter"
    
    #Data for data analysis
    bar = create_plot(gallery_data)
    locndeets = locn_plot(locinfo)
    locnspecies = locnvsspecies(data)

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
        locnspecies = locnspecies,
        sess=session,
    )

@app.route("/speciesgallery/<string:species_name>/<string:sub_species>/")
def speciesgallery(species_name, sub_species):
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from butterflydata where sub_species = %s",( sub_species,))
    gallery_data = cur.fetchall()
    cur.execute("SELECT * from species where sub_species = %s",( sub_species,))
    breadcrumb = cur.fetchall()
    #print(gallery_data.length())
    cur.close()
    return render_template("species_details.html",gallery_data=gallery_data, breadcrumb=breadcrumb)

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

def altitude(lat,long):
  latlng = lat+" "+long
  apikey="AIzaSyB3zdxKTqiIaCpBc_1Yaqzc3X6kNsiRips"
  serviceURL = "https://maps.googleapis.com/maps/api/elevation/json?locations="+latlng+"&key="+apikey
  r = requests.get(serviceURL)
  y = json.loads(r.text)
  for result in y["results"]:
    elev=result["elevation"]
    return elev

@app.route("/img", methods=["GET", "POST"])
def img():
    if request.method == "POST":
        f = request.files["file"]
        f.filename=f.filename.replace(" ","_")
        f.save(os.path.join(app.config["UPLOAD_FOLDER"], f.filename))
        path = f'./upload_image/{f.filename}'
        img = image.load_img(path, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        model = load_model('./model.h5')
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
                result["search"],
                result["lat"],
                result["lng"]
            ]
            print(result["search"])
            print(result["lat"], result["lng"])

            elevation = altitude(result["text7"], result["text8"])

            print(result["text2"])
            date1 = result["text2"]
            day = date1[8:]
            month = date1[5:7]
            year = date1[0:4]

            fdate  = str(str(day) + "-" + str(month) + "-" + str(year))
            print(fdate)
            #print(result["text6"])
            res = result["text6"].split()
            res[1].lower()
            c = mysql.connection.cursor()
            c.execute("SELECT * FROM species WHERE sub_species = %s", (res[1],))
            d1 = c.fetchall()
            c.execute("INSERT INTO butterflydata (img,date,location,species,clicked_by,scientific_name,sub_species,species_name,sub_sub_family,sub_family,latitude,longitude,altitude) VALUES (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s)",(str1,fdate,result["text3"],result["text4"],result["text5"],result["text6"],d1[0][0],d1[0][1],d1[0][2],d1[0][3],result["text7"],result["text8"],elevation))
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
                    + """<br>datse : <b>{}</b>""".format(datee)
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