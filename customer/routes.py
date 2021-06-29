from flask import Blueprint,render_template, request, redirect, url_for, session,flash
import bcrypt #pip install bcrypt https://pypi.org/project/bcrypt/
from database import mysql
from flask_mysqldb import MySQLdb

customer = Blueprint('customer', __name__, url_prefix='/', template_folder='templates',static_folder="static")


@customer.route('/')
@customer.route('/index')
def customer_index():
    return render_template('customer/index.html')

@customer.route('/feedback')
def feedback():
    return render_template('customer/feedback.html')

@customer.route('/compliant')
def compliant():
    return render_template('customer/compliant.html')

@customer.route('/about')
def about():
    return render_template('customer/about.html')

@customer.route('/contact')
def contact():
    return render_template('customer/contact.html')

@customer.route('/register', methods=["GET", "POST"]) 
def register():
    if request.method == 'GET':
        return render_template("customer/register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
 
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('customer.customer_index'))


@customer.route('/login',methods=["GET","POST"])
def cu_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
 
        if (user):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                # return('1')
                return render_template("customer/index.html")
            else:
                flash('Error password and email not match')
                return redirect(url_for('customer.cu_login'))
                # return render_template("customer/error.html")
                # return "Error password and email not match"
        else:
            flash('user not found! please register.')
            return redirect(url_for('customer.cu_login'))
            # return render_template("customer/notfound.html")
            # return("Error user not found")
    else:
        return render_template("customer/index.html")
# def cu_login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password'].encode('utf-8')
 
#         curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
#         curl.execute("SELECT * FROM users WHERE email=%s",(email,))
#         user = curl.fetchone()
#         curl.close()
 
#         if len(user) > 0:
#             if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
#                 session['name'] = user['name']
#                 session['email'] = user['email']
#                 return render_template("customer/index.html")
#             else:
#                 return render_template("customer/error.html")
#         else:
#             return "Error user not found"
#     else:
#         return render_template("customer/login.html")
 
@customer.route('/logout')
def logout():
    session.clear()
    return render_template("customer/index.html")
