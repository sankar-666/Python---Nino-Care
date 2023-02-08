from flask import *
from database import *

api=Blueprint('api',__name__)


@api.route('/login')
def login():
    data={}
    un=request.args['username']
    pwd=request.args['password']
    z="select * from `login` where username='%s' and password='%s' "%(un,pwd)
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    return str(data)


@api.route("/reg",methods=['get','post'])
def reg():
    data={}

    fname=request.args['fname']
    lname=request.args['lname']
    place_id=request.args['place_id']
    phone=request.args['phone']
    email=request.args['email']
    username=request.args['uname']
    password=request.args['pass']
    hname=request.args['hname']
    rel=request.args['rel']
    dob=request.args['dob']

    q="select * from login where username='%s' and password='%s'"%(username,password)
    rep=select(q)

    if rep:
        data['status']='already'
    else:
        q="insert into `login` values(NULL,'%s','%s','parent') "%(username,password)
        ref=insert(q)
        v="insert into `parent` values(NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s') "%(ref,place_id,fname,lname,phone,email,rel,dob,hname)
        insert(v)
        data['status']='success'
    data['method']="reg"
    return str(data)

@api.route('/viewplace')
def viewplace():
    data={}

    z="select * from place"
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewplace'
    return str(data)


@api.route('/viewgroup')
def viewgroup():
    data={}

    z="select * from agegroup"
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewgroup'
    return str(data)



@api.route("/babyreg",methods=['get','post'])
def babyreg():
    data={}

    fname=request.args['fname']
    lname=request.args['lname']
    gender=request.args['gender']
    dob=request.args['dob']
    gid=request.args['gid']
    lid=request.args['lid']


    q="insert into `babies` values(NULL,(select parent_id from parent where login_id='%s'),'%s','%s','%s','%s','%s') "%(lid,fname,lname,gid,dob,gender)
    insert(q)
   
    data['status']='success'
    data['method']="babyreg"
    return str(data)

@api.route('/viewvideos')
def viewvideos():
    data={}

    z="select * from video"
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewvideos'
    return str(data)


@api.route('/viewnoti')
def viewnoti():
    data={}

    z="select * from notifications"
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewnoti'
    return str(data)



@api.route('/viewdoctors')
def viewdoctors():
    data={}

    z="select * from doctor"
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewdoctors'
    return str(data)


@api.route('/viewashaworkers')
def viewashaworkers():
    data={}

    z="select * from ashaworker"
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewashaworkers'
    return str(data)


@api.route('/viewbaby')
def viewbaby():
    data={}
    lid=request.args['lid']
    q="select * from parent where login_id='%s'"%(lid)
    pid=select(q)[0]['parent_id']
    z="select * from babies where parent_id='%s'"%(pid)
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewbaby'
    return str(data)


@api.route("/chatdetail")
def chatdetail():
	sid=request.args['sender_id']
	rid=request.args['receiver_id']
	
	data={}
	q="select * from chat where (sender_id='%s' and receiver_id='%s') or (sender_id='%s' and receiver_id='%s') group by chat_id "%(sid,rid,rid,sid)
	
	res=select(q)
	if res:
		data['status']="success"
		data['data']=res
	else:
		
		data['status']="failed"
	data['method']='chatdetail'
	
	return str(data)

@api.route("/chat")
def chat():
	data={}
	sid=request.args['sender_id']
	rid=request.args['receiver_id']
	det=request.args['details']
	
	
	q="insert into chat values(null,'%s','%s','%s',curdate())"%(sid,rid,det)
	insert(q)
	data['status']='success'
	data['method']='chat'
	return str(data)


@api.route('/sendappoitment')
def sendappoitment():
    data={}
    date=request.args['date']
    time=request.args['time']
    bid=request.args['bid']
    did=request.args['did']

    
    

    q="insert into appoinment values(null,'%s',%s,'%s','%s','pending')"%(did,bid,date,time)
    insert(q)
    data['status']='success'
    data['method']='sendappoitment'
    return str(data)



@api.route('/viewmyappoinments')
def viewmyappoinments():
    data={}
    lid=request.args['lid']
    z="SELECT *,CONCAT(doctor.fname,'',doctor.lname) AS doc,CONCAT(babies.fname,'',babies.lname) AS baby FROM appoinment INNER JOIN babies USING (babie_id) INNER JOIN doctor USING (doctor_id) WHERE parent_id=(SELECT parent_id FROM parent WHERE login_id='%s')"%(lid)
    print(z)
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewmyappoinments'
    return str(data)


@api.route('/viewprecuations')
def viewprecuations():
    data={}
    lid=request.args['lid']
    z="SELECT *,CONCAT(`babies`.`fname`,'',`babies`.`lname`) AS baby FROM `babies` INNER JOIN `parent` USING (parent_id) inner join precuation using (babie_id) WHERE parent_id=(SELECT parent_id FROM parent WHERE login_id='%s')"%(lid)
    print(z)
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewprecuations'
    return str(data)


@api.route('/viewvacciantion')
def viewvacciantion():
    data={}
    lid=request.args['lid']
    z="SELECT *,CONCAT(`babies`.`fname`,'',`babies`.`lname`) AS baby FROM `babies` INNER JOIN `parent` USING (parent_id) INNER JOIN `request` USING (babie_id) INNER JOIN `vaccinations` USING (vaccination_id) WHERE parent_id=(SELECT parent_id FROM parent WHERE login_id='%s')"%(lid)
    print(z)
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewvacciantion'
    return str(data)

@api.route('/viewfeedback')
def viewfeedback():
    data={}
    lid=request.args['lid']
    z="SELECT * from feedback WHERE parent_id=(SELECT parent_id FROM parent WHERE login_id='%s')"%(lid)
    print(z)
    res=select(z)

    if res:
        data['status']='success'
        data['data']=res
    else:
        data['status']='failed'
    data['method']='viewfeedback'
    return str(data)


@api.route('/addfeedback')
def addfeedback():
    data={}
    lid=request.args['lid']
    feed=request.args['feedback']
    z="insert into feedback values (null,(SELECT parent_id FROM parent WHERE login_id='%s'),'%s',curdate()) "%(lid,feed)
    insert(z)

    data['status']='success'

    data['method']='addfeedback'
    return str(data)