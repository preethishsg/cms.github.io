from flask import Blueprint,render_template,request,redirect,url_for,session
from flask.helpers import flash
from database import mysql
from flask_mysqldb import MySQLdb
import bcrypt

branch = Blueprint('branch', __name__, url_prefix='/branch', template_folder='templates',static_folder="static")

@branch.route('/')
def branch_index():

    return render_template('/branch/index.html')


@branch.route('/branch/branch_login',methods=["GET","POST"])
@branch.route('/branch_login',methods=["GET","POST"])
def branch_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
 
        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM branchlog WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()
 
        if (user):
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                # return('1')
                return render_template("branch/index.html")
            else:
                flash('email and password not match')
            return redirect(url_for('branch.branch_login'))
        else:
            flash('wrong email id')
            return redirect(url_for('branch.branch_login'))
    else:
        return render_template("branch/branch_login.html")

@branch.route('/courierBoys')
def courierBoys():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM courierboydb')
    data = cur.fetchall()
    cur.close()
    return render_template('branch/courierBoys.html',contacts = data)


@branch.route('/branch_application',methods=["GET","POST"])
@branch.route('branch/branch_application',methods=["GET","POST"])
def branch_application():
    if request.method == 'GET':
        return render_template("branch/branch_application.html")
    else:
        first_name = request.form['first_name'] 
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        zip = request.form['zip']


        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO branchDb (first_name,last_name,email,phone,address,address2,city,state,zip) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(first_name,last_name,email,phone,address,address2,city,state,zip))
        mysql.connection.commit()
        flash('register successful')
        return redirect(url_for('branch.branch_application'))


@branch.route('branch/decline/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('DELETE FROM courierboydb WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('branch.courierBoys'))