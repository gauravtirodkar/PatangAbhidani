from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from bs4 import BeautifulSoup

""" from flask import Flask, url_for, render_template,request,session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) """
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



if __name__ == '__main__':
    app.run(debug=True)