from flask import *
from database import *

ashaworker=Blueprint('ashaworker',__name__)

@ashaworker.route('/ashaworkerhome') 
def ashaworkerhome():
    return render_template('ashaworkerhome.html')


@ashaworker.route('/ashaworker_view_assignedplace')
def ashaworker_view_assignedplace():
    data={}
    q="SELECT * FROM `ashaworker` INNER JOIN `place` USING (place_id) where ashaworker_id='%s'"%(session['aid'])
    data['res']=select(q)
    return render_template('ashaworker_view_assignedplace.html',data=data)

@ashaworker.route('/ashaworker_view_babies',methods=['get','post'])
def ashaworker_view_babies():
    data={}
    q="select *,parent.fname as fparent,parent.lname as lparennt,babies.fname as fbaby,babies.lname as lbaby from parent inner join babies using (parent_id) inner join ashaworker using (place_id) where ashaworker.place_id=parent.place_id"
    data['res']=select(q)

    if 'action' in request.args:
        action=request.args['action']
        bid=request.args['bid']
    else:
        action=None

    if action == "sendz":
        print("hello")
        data['showForm']=True

    if 'btn' in request.form:
        prec=request.form['prec']

        q="insert into precuation values (null,'%s','%s')"%(bid,prec)
        insert(q)
        flash("Precuation Added Successfully")
        return redirect(url_for("ashaworker.ashaworker_view_babies"))
        
    return render_template('ashaworker_view_babies.html',data=data)


@ashaworker.route('/ashaworker_add_vaccination',methods=['get','post'])
def ashaworker_add_vaccination():
    data={}
    q="select * from vaccinations "
    data['vaccine']=select(q)
    bid=request.args['bid']
    if 'btn'in request.form:
        vid=request.form['vid']

        q="insert into request values (null,'%s','%s',curdate(),curtime(),'pending')"%(vid,bid)
        insert(q)
        flash("Request Added")
        return redirect(url_for("ashaworker.ashaworker_add_vaccination",bid=bid))
    

    q='select * from request where babie_id="%s"'%(bid)
    data['res']=select(q)


    if 'action' in request.args:
        action=request.args['action'] 
        rid=request.args['rid']
    else:
        action=None

    if action == "finish":
        q="update request set status='Completed' where request_id='%s'"%(rid)
        update(q)
        flash("Vaccination Completed")
        return redirect(url_for("ashaworker.ashaworkerhome"))
    return render_template('ashaworker_add_vaccination.html',data=data,bid=bid)




@ashaworker.route('/ashaworkerchat',methods=['post','get'])
def ashaworkerchat():
    data={}
    uid=session['loginid']
    did=request.args['did']
    if 'btn' in request.form:
        name=request.form['txt']
    
        q="insert into chat values(NULL,'%s','%s','%s',now())"%(uid,did,name)
        insert(q)
        return redirect(url_for("ashaworker.ashaworkerchat",did=did))
    q="SELECT * FROM chat WHERE (sender_id='%s' AND receiver_id='%s') OR (sender_id='%s' AND receiver_id=('%s')) order by chat_id"%(uid,did,did,uid)
    # q="select * from chats where senderid='%s' and receiverid=( select login_id from doctors where doctor_id='%s' )"%(uid,did)
    print(q)
    res=select(q)
    data['ress']=res
    
    return render_template("ashaworkerchat.html",data=data,uid=uid)




@ashaworker.route('/ashaworkerviewchat')
def ashaworkerviewchat():
    data={}
    uid=session['loginid']
    q="SELECT * FROM `parent` WHERE login_id IN (SELECT IF(sender_id = '%s',receiver_id,sender_id) FROM chat WHERE sender_id='%s' OR receiver_id='%s')"%(uid,uid,uid)
    res=select(q)
    data['res']=res
    return render_template("ashaworkerviewchat.html",data=data)