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
        q="update appoinment set status='Approved' where appointment_id='%s'"%(aid)
        update(q)
        return redirect(url_for("doctor.doctor_view_appoinment"))
    
    if action == "reject":
        q="update appoinment set status='Rejected' where appointment_id='%s'"%(aid)
        update(q)
        return redirect(url_for("doctor.doctor_view_appoinment"))
    return render_template('doctor_view_appoinment.html',data=data)



@doctor.route('/doctorchat',methods=['post','get'])
def doctorchat():
    data={}
    uid=session['loginid']
    did=request.args['did']
    if 'btn' in request.form:
        name=request.form['txt']
    
        q="insert into chat values(NULL,'%s','%s','%s',now())"%(uid,did,name)
        insert(q)
        return redirect(url_for("doctor.doctorchat",did=did))
    q="SELECT * FROM chat WHERE (sender_id='%s' AND receiver_id='%s') OR (sender_id='%s' AND receiver_id=('%s')) order by chat_id"%(uid,did,did,uid)
    # q="select * from chats where senderid='%s' and receiverid=( select login_id from doctors where doctor_id='%s' )"%(uid,did)
    print(q)
    res=select(q)
    data['ress']=res
    
    return render_template("doctorchat.html",data=data,uid=uid)




@doctor.route('/doctorviewchats')
def doctorviewchats():
    data={}
    uid=session['loginid']
    q="SELECT * FROM `parent` WHERE login_id IN (SELECT IF(sender_id = '%s',receiver_id,sender_id) FROM chat WHERE sender_id='%s' OR receiver_id='%s')"%(uid,uid,uid)
    print(q)
    res=select(q)
    data['res']=res
    return render_template("doctorviewchats.html",data=data)