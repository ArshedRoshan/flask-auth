from flask import Flask,redirect,url_for,request,render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()


def apps():
   app = Flask(__name__,template_folder='Templates')
   CORS(app,supports_credentials=True)
   app.config['SECRET_KEY'] = 'your secret key'
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/flask-managment1'
   db.init_app(app)
   migrate = Migrate(app, db)
   
   app.debug = True
   return app