from flask import *
from database import *

doctor=Blueprint('doctor',__name__)

@doctor.route('/doctorhome')
def doctorhome():
    return render_template('doctorhome.html')


@doctor.route('/doctor_view_appoinment')
def doctor_view_appoinment():
    data={}
    q="SELECT * FROM babies inner join appoinment using (babie_id) where doctor_id='%s'"%(session['did'])
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        aid=request.args['aid']
    else:
        action=None

    if action == "approve":
        q="update appoinment set status='Approved' where appoinment_id='%s'"%(aid)
        update(q)
        return redirect(url_for("doctor.doctor_view_appoinment"))
    
    if action == "reject":
        q="update appoinment set status='Rejected' where appoinment_id='%s'"%(aid)
        update(q)
        return redirect(url_for("doctor.doctor_view_appoinment"))
    return render_template('doctor_view_appoinment.html',data=data)
