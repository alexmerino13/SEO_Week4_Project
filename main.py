from flask import Flask, render_template, url_for, flash, redirect
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

proxied = FlaskBehindProxy(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/menu")
def about():
    return render_template('menu.html', subtitle='Menu', text='This is a menu page')



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")