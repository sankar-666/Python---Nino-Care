from flask import *
from database import *

doctor=Blueprint('doctor',__name__)

@doctor.route('/doctorhome')
def doctorhome():
    return render_template('doctorhome.html')