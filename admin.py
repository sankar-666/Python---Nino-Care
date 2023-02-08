from flask import *
from database import *

admin=Blueprint('admin',__name__)

@admin.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')


@admin.route('/admin_view_parents')
def admin_view_parents():
    data={}
    q="select * from parent"
    data['res']=select(q)
    return render_template('admin_view_parents.html',data=data)


@admin.route('/admin_view_babies')
def admin_view_babies():
    data={}
    q="select *,parent.fname as fparent,parent.lname as lparennt,babies.fname as fbaby,babies.lname as lbaby from parent inner join babies using (parent_id)"
    data['res']=select(q)
    return render_template('admin_view_babies.html',data=data)


@admin.route('/admin_view_vaccination')
def admin_view_vaccination():
    data={}
    bid=request.args['bid']
    q="SELECT * FROM `vaccinations` INNER JOIN `request` USING (vaccination_id) where baby_id='%s'"%(bid)
    data['res']=select(q)
    return render_template('admin_view_vaccination.html',data=data)



@admin.route('/admin_manage_place',methods=['get','post'])
def admin_manage_place():
    data={}
    if 'btn' in request.form:
        place=request.form['place']
        
    
        q="insert into place values (null,'%s')"%(place)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.admin_manage_place"))

    data={}
    q="select * from place"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        pid=request.args['pid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from place where place_id='%s'"%(pid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            place=request.form['place']

            q="update place set place='%s' where place_id='%s' "%(place,pid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.admin_manage_place"))
    if action == "delete":
        q="delete from place where place_id='%s' "%(pid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_place"))
    return render_template('admin_manage_place.html',data=data) 




@admin.route('/admin_manage_ashaworker',methods=['get','post'])
def admin_manage_ashaworker():
    data={}
    q="select * from place"
    data['place']=select(q)

    if 'btn' in request.form:
        fname=request.form['fname']
        lname=request.form['lname']
        place_id=request.form['place']
        phone=request.form['phone']
        email=request.form['email']
        pwd=request.form['pwd']
        uname=request.form['uname']
        
    
        q="select * from login where username='%s'"%(uname)
        res=select(q)
        if res:
            flash("This Username already exist!, try register with new one.")
        else:
            q="insert into login values(null,'%s','%s','ashaworker')"%(uname,pwd)
            lid=insert(q)
            q="insert into ashaworker values (NULL,'%s','%s','%s','%s','%s','%s')"%(lid,place_id,fname,lname,phone,email)
            insert(q)
            flash("Registration successfull")
            return redirect(url_for("admin.admin_manage_ashaworker"))


    q="select * from ashaworker"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        aid=request.args['aid'] 
        lid=request.args['lid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from ashaworker where ashaworker_id='%s'"%(aid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            fname=request.form['fname']
            lname=request.form['lname']
            
            phone=request.form['phone']
            email=request.form['email']

            q="update ashaworker set fname='%s', lname='%s', phone='%s', email='%s' where place_id='%s' "%(fname,lname,phone,email,aid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.admin_manage_ashaworker"))
    if action == "delete":
        q="delete from ashaworker where ashaworker_id='%s' "%(aid)
        delete(q)
        q="delete from login where login_id='%s' "%(lid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_ashaworker"))
    return render_template('admin_manage_ashaworker.html',data=data) 




@admin.route('/admin_manage_vaccination',methods=['get','post'])
def admin_manage_vaccination():
    data={}
    if 'btn' in request.form:
        name=request.form['name']
        age=request.form['age']
        total=request.form['total']
        
    
        q="insert into vaccinations values (null,'%s','%s','%s')"%(name,age,total)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.admin_manage_vaccination"))

    data={}
    q="select * from vaccinations"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        vid=request.args['vid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from vaccinations where vaccination_id='%s'"%(vid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            name=request.form['name']
            age=request.form['age']
            total=request.form['total']

            q="update vaccinations set name='%s', age_group='%s', total_number='%s' where vaccination_id='%s' "%(name,age,total,vid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.admin_manage_vaccination"))
    if action == "delete":
        q="delete from vaccinations where vaccination_id='%s' "%(vid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_vaccination"))
    return render_template('admin_manage_vaccination.html',data=data) 




@admin.route('/admin_manage_notifications',methods=['get','post'])
def admin_manage_notifications():
    data={}
    if 'btn' in request.form:
        title=request.form['title']
        des=request.form['des']
       
        q="insert into notifications values (null,'%s','%s',curdate())"%(title,des)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.admin_manage_notifications"))

    data={}
    q="select * from notifications"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        nid=request.args['nid'] 
    else:
        action=None

    
    if action == "update":
        q="select * from notifications where notification_id='%s'"%(nid)
        val=select(q)
        data['raw']=val

        if 'update' in request.form:
            title=request.form['title']
            des=request.form['des']

            q="update notifications set title='%s', des='%s'where notification_id='%s' "%(title,des,nid)
            update(q)
            flash("Updated Successfully")
            return redirect(url_for("admin.admin_manage_notifications"))
    if action == "delete":
        q="delete from notifications where notification_id='%s' "%(nid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_notifications"))
    return render_template('admin_manage_notifications.html',data=data) 



import uuid
@admin.route('/admin_manage_babyvideos',methods=['get','post'])
def admin_manage_babyvideos():
    data={}
    if 'btn' in request.form:
        title=request.form['title']
        video=request.files['video']
        path="static/uploads"+str(uuid.uuid4())+video.filename
        video.save(path)        
    
        q="insert into video values (null,'%s','%s')"%(title,path)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.admin_manage_babyvideos"))

    data={}
    q="select * from video"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        vid=request.args['vid'] 
    else:
        action=None

    
    
    if action == "delete":
        q="delete from video where video_id='%s' "%(vid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_babyvideos"))
    return render_template('admin_manage_babyvideos.html',data=data) 



@admin.route('/admin_manage_agegroup',methods=['get','post'])
def admin_manage_agegroup():
    data={}
    if 'btn' in request.form:
        gname=request.form['gname']
        mage=request.form['mage']
        maxage=request.form['maxage']
        
    
        q="insert into agegroup values (null,'%s','%s','%s')"%(gname,mage,maxage)
        insert(q)
        flash("Successfully Added")
        return redirect(url_for("admin.admin_manage_agegroup"))

    data={}
    q="select * from agegroup"
    data['res']=select(q)
    data['count']=len(select(q))

    if 'action' in request.args:
        action=request.args['action']
        gid=request.args['gid'] 
    else:
        action=None

    
    
    if action == "delete":
        q="delete from agegroup where group_id='%s' "%(gid)
        delete(q)
        flash("Deleted Successfully")
        return redirect(url_for("admin.admin_manage_agegroup"))
    return render_template('admin_manage_agegroup.html',data=data) 

