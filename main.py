from flask import Flask, render_template, request, redirect, url_for, session
from database import mysql
# from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
import bcrypt #pip install bcrypt https://pypi.org/project/bcrypt/
from admin.routes import admin
from branch.routes import branch
from courier.routes import courier
from courier_boy.routes import courier_boy
from customer.routes import customer


app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cms'
app.secret_key='itsMySecretKey'
mysql.init_app(app)


app.register_blueprint(admin)
app.register_blueprint(branch)
app.register_blueprint(courier)
app.register_blueprint(courier_boy)
app.register_blueprint(customer)



# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)

