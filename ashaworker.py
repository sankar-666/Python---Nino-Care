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

@ashaworker.route('/ashaworker_view_babies')
def ashaworker_view_babies():
    data={}
    q="select *,parent.fname as fparent,parent.lname as lparennt,babies.fname as fbaby,babies.lname as lbaby from parent inner join babies using (parent_id) inner join ashaworker using (place_id) where ashaworker.place_id=parent.place_id"
    data['res']=select(q)

    if 'action' in request.form:
        action=request.form['action']
        bid=request.form['bid']
    else:
        action=None

    if action == "send":
        data['showForm']=True

    if 'btn' in request.form:
        prec=request.form['prec']

        q="insert into precuation values (null,'%s','%s')"%(bid,prec)
        insert(q)
        return redirect(url_for("ashaworker.ashaworker_view_babies"))
        
    return render_template('ashaworker_view_babies.html',data=data)


@ashaworker.route('/ashaworker_add_vaccination')
def ashaworker_add_vaccination():
    data={}
    bid=request.args['bid']
    if 'btn'in request.form:
        vid=request.form['vid']

        q="insert into request values (null,'%s','%s',curdate(),curtime(),'pending')"%(vid,bid)
        insert(q)
        return redirect(url_for("ashaworker.ashaworker_add_vaccination",bid=bid))
    q='select * from request where baby_id="%s"'%(bid)
    data['res']=select(q)

    if 'action' in request.form:
        action=request.form['action']
        rid=request.form['rid']
    else:
        action=None

    if action == "complete":
        q="update request set status='Completed' where request_id='%s'"%(rid)
        update(q)
        return redirect(url_for("ashaworker.ashaworker_add_vaccination",bid=bid))
    return render_template('ashaworker_add_vaccination.html',data=data)

