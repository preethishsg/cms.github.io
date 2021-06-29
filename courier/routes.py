from flask import Blueprint,render_template

courier = Blueprint('courier', __name__, url_prefix='/courier', template_folder='templates')

@courier.route('/')
def courier_index():

    return render_template('courier/index.html')