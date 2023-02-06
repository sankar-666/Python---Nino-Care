from flask import *
from database import *

ashaworker=Blueprint('ashaworker',__name__)

@ashaworker.route('/ashaworkerhome') 
def ashaworkerhome():
    return render_template('ashaworkerhome.html')