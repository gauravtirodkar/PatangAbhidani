from flask import Flask, render_template, request, redirect
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html',user="LoggedIn")

@app.route('/specsdeets')
def specsdeets():
    return render_template('species_details.html',user="LoggedIn")

@app.route('/images')
def images_grid():
    return render_template('images_grid.html',user="LoggedIn")

@app.route('/addData')
def addData():
    return render_template('addData.html',user="LoggedIn")

if __name__ == '__main__':
    app.run(debug=True)