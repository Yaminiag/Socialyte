import sqlite3 as sql
import sys
import os
from flask import Flask,render_template,request,url_for,redirect,session
import random
from datetime import datetime,date

app=Flask(__name__)
app.secret_key='any string'
def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1


@app.route('/signup.html/')
def sign():
	return render_template('signup.html')

@app.route('/user.html/',methods=['POST','GET'])
def user():
    con=sql.connect('data.db')
    if 'fname' in session:
        cur=con.cursor()
        fn=session['fname']
        cur.execute("select user_id from Users where f_name=(?)",(fn,))
        uid=cur.fetchone()
        session['user_id']=uid[0]
        uid=session['user_id']

        cur.execute("select f_name from users where user_id in(select friend_id from friends where user_id=(?))",(uid,))
        rows = cur.fetchall()
        cur.execute("select email,location,dob from Users where f_name=(?)",(fn,))
        detail=cur.fetchone()
        cur.execute("select f_name from users where user_id in(select friend_id from friends where user_id='001' and friend_id<> (?) except select friend_id from friends where user_id=(?))",(uid,uid,))
        sugg=cur.fetchall()


        cur.execute("select distinct * from Posts where user_id=(?) order by post_date desc",(uid,))
        posts=cur.fetchall()
        #print(posts)

        i=0
        for post in posts:
            print(post[1])
            cur.execute("select count(*) from Post_likes where post_id=(?) group by post_id",(post[1],))
            likes=cur.fetchall()
            if not likes:
                likes=0
            else:
                likes=likes[0][0]
            print(likes)
            cur.execute("select comment_id,comment_content from Comments  where post_id=(?)",(post[1],))
            comm=cur.fetchall()
            # print(comm)
            cur.execute("select image_content from Photos where post_id=(?)",(post[1],))
            img=cur.fetchone()
            j=0
            for com in comm:

                    cur.execute("select count(*) from comment_likes where comment_id=(?) group by comment_id",(com[0],))
                    com_likes=cur.fetchall()
                    com_likes=com_likes
                    # print(com_likes)
                    if not com_likes:
                        com_likes=0
                    else:
                        com_likes=com_likes[0][0]
                    com=com+(com_likes,)
                    comm[j]=com
                    j=j+1
                    # print(com)
            print(comm)
            date=post[3]
            date=date.split('-')
            y=int(date[0])
            m=int(date[1])
            d=int(date[2])
            da=datetime(y,m,d)
            diff=datetime.now()-da
            diff=str(diff)
            diff=diff.split(',')
            difference=diff[0]
            if img == None:
                post+=(difference,likes,comm,())
            else:
                post+=(difference,likes,comm,img)
            posts[i]=post
            i=i+1
        session['posts']=posts
        session['detail']=detail
        session['rows']=rows
        return render_template('user.html',name=fn,rows=rows,detail=detail,posts=posts,sugg=sugg)





@app.route("/")
def main():
	return render_template('home.html')

@app.route('/reg',methods=['POST','GET'])
def reg():
	msg="none"
	if request.method == 'GET':
			f_name = request.args.get('f_name','')
			l_name = request.args.get('l_name','')
			email = request.args.get('email','')
			password = request.args.get('pwd','')
			cpassword=request.args.get('conf_pwd','')
			address=request.args.get('add','')
			dob=request.args.get('dob','')
			gender=request.args.get('gender','')
			phoneno=request.args.get('phno','')
			loc=request.args.get('loc','')
			with sql.connect("data.db") as con:
				cur = con.cursor()
				unique_sequence = uniqueid()
				u_id = next(unique_sequence)
				cur.execute("insert into Users values(?,?,?,?,?,?,?,?,?,?)",(u_id,f_name,l_name,address,email,phoneno,loc,dob,gender,password))
				con.commit()
				msg = "Record successfully added"
			return redirect("http://127.0.0.1:5000/login.html/")
			con.close()



@app.route('/login.html/',methods=['POST','GET'])
def login():
    con=sql.connect('data.db')
    error=None
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        completion=validate(username,password)
        if completion==False:
            error='Invalid Credentials.Please try again.'
        else:
            session['fname']=username
            if 'fname' in session:
                cur=con.cursor()
                fn=session['fname']
                cur.execute("select user_id from Users where f_name=(?)",(fn,))
                uid=cur.fetchone()
                uid=uid[0]
                session['user_id']=uid
                cur.execute("select email,location,dob from Users where f_name=(?)",(fn,))
                detail=cur.fetchone()
                session['detail']=detail
                return redirect("http://127.0.0.1:5000/wall.html/")
    return render_template('login.html',error=error)

def validate(username, password):
    con = sql.connect('data.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT f_name,password FROM Users")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[0]
                    dbPass = row[1]
                    if dbUser==username and dbPass==password:
                        completion=True
    return completion

@app.route('/post/',methods=['POST','GET'])
def post():
    if request.method == 'GET' and 'fname' in session:
        content= request.args.get('postcontent','')
        img = request.args.get('postimg','')
        fn=session['fname']
        print(img)
        rows=session['rows']
        detail=session['detail']
        posts=session['posts']
        with sql.connect("data.db") as con:
            cur = con.cursor()
            unique_sequence = uniqueid()
            p_id = next(unique_sequence)
            user_id=session['user_id']
            unique_sequence = uniqueid()
            ph_id = next(unique_sequence)

            date=datetime.now().date()
            time=datetime.now().time()
            h=str(time.hour)
            m=str(time.minute)
            s=str(time.second)
            t=h+":"+m+":"+s
            cur.execute("insert into Posts values(?,?,?,?,?)",(user_id,p_id,content,date,t))
            cur.execute("insert into Photos values(?,?,?,?,?,?)",(user_id,p_id,ph_id,img,date,t))

            con.commit()
    return redirect("http://127.0.0.1:5000/wall.html/")



@app.route('/wall.html/',methods=['POST','GET'])
def w():
    con=sql.connect('data.db')
    if 'fname' in session:
        cur=con.cursor()
        fn=session['fname']
        uid=session['user_id']


        cur.execute("select p2.post_id,p2.user_id,post_content from posts p1,post_likes p2 where p1.post_id=p2.post_id group by p2.post_id having count(*)>=2")
        a=cur.fetchall()
        k=0
        for b in a:
            cur.execute("select f_name from Users where user_id=(?)",(b[1],))
            c=cur.fetchone()
            c=c[0]
            b=b+(c,)
            a[k]=b
            k=k+1
            print(c)
        # print(a)




        print(a)
        cur.execute("select posts.user_id,post_id,post_content,post_date,post_time from posts inner join friends on friends.user_id=(?)where friends.friend_id=posts.user_id union select posts.user_id,post_id,post_content,post_date,post_time from posts inner join friends f1 on f1.user_id=(?)inner join friends as f2 on f2.user_id=f1.friend_id where f2.friend_id=posts.user_id and f2.friend_id<> (?) order by post_date desc",(uid,uid,uid,))
        detail=session['detail']
        posts=cur.fetchall()
        cur.execute("select posts.post_id from posts,post_likes where posts.post_id=post_likes.post_id group by posts.post_id having count(*)=(select max(count) from(select count(*) as count,posts.post_id from posts,post_likes where posts.post_id=post_likes.post_id group by posts.post_id)maximum )")
        populars=cur.fetchall()
        # print(populars)
        populars=populars[0]
        # print(populars)
        pop_post=[]
        for popular in populars:
            cur.execute("select user_id,post_content from Posts where post_id=(?)",(popular,))
            pop_details=cur.fetchall()
            pop_details=pop_details[0]
            # print(pop_details)
            pop_userid=pop_details[0]
            # print(pop_userid)
            pop_content=pop_details[1]
            # print(pop_content)
            cur.execute("select f_name from Users where user_id=(?)",(pop_userid,))
            pop_name=cur.fetchone()
            pop_name=pop_name[0]
            # print(pop_name)
            cur.execute("select image_content from Photos where post_id=(?)",(popular,))
            img=cur.fetchall()
            img=img[0][0]
            # print(img)
            # print(pop_details)
            pop_post.append((pop_name,pop_content,img))
            # print(pop_post)

        i=0
        for post in posts:
            cur.execute("select count(*) from Post_likes where post_id=(?) group by post_id",(post[1],))
            likes=cur.fetchall()
            if not likes:
                likes=0
            else:
                likes=likes[0][0]
            # print(likes)
            cur.execute("select comment_id,comment_content from Comments  where post_id=(?)",(post[1],))
            comm=cur.fetchall()
            # print(comm)
            j=0
            for com in comm:

                    cur.execute("select count(*) from comment_likes where comment_id=(?) group by comment_id",(com[0],))
                    com_likes=cur.fetchall()
                    com_likes=com_likes
                    # print(com_likes)
                    if not com_likes:
                        com_likes=0
                    else:
                        com_likes=com_likes[0][0]
                    com=com+(com_likes,)
                    comm[j]=com
                    j=j+1
                    # print(com)
            # print(comm)
            cur.execute("select image_content from Photos where post_id=(?)",(post[1],))
            img=cur.fetchone()
            print(img)
            cur.execute("select f_name from users where user_id =(?)",(post[0],))
            names=cur.fetchall()
            names=names[0][0]
            date=post[3]
            date=date.split('-')
            y=int(date[0])
            m=int(date[1])
            d=int(date[2])
            da=datetime(y,m,d)
            diff=datetime.now()-da
            diff=str(diff)
            diff=diff.split(',')
            difference=diff[0]
            if img == None:
                post+=(difference,names,likes,comm,())
            else:
                post+=(difference,names,likes,comm,img)
            posts[i]=post
            i=i+1
        print(posts)
        session['posts']=posts
        session['pop_post']=pop_post
        session['a']=a
        return render_template('wall.html',name=fn,detail=detail,posts=posts,pop_post=pop_post,a=a)

@app.route('/addfrnd/',methods=['POST','GET'])
def addfrnd():
    con=sql.connect('data.db')
    if request.method == 'POST' and 'fname' in session:
        cur=con.cursor()
        uid=session['user_id']
        fn=request.form.get('friend')
        cur.execute("select user_id from Users where f_name=(?)",(fn,))
        fid=cur.fetchone()
        fid=fid[0]
        date=datetime.now().date()
        time=datetime.now().time()
        h=str(time.hour)
        m=str(time.minute)
        s=str(time.second)
        t=h+":"+m+":"+s
        print(date)
        print(time)
        cur.execute("insert into Friends values(?,?,?,?)",(uid,fid,date,t))
        cur.execute("insert into Friends values(?,?,?,?)",(fid,uid,date,t))
        con.commit()

    return redirect("http://127.0.0.1:5000/user.html/")


@app.route('/like/',methods=['POST','GET'])
def like():
    try:
        con=sql.connect('data.db')
        if request.method == 'POST' and 'fname' in session:
            cur=con.cursor()
            uid=session['user_id']
            pid=request.form.get('like')
            print(pid)
            cur.execute("select user_id from Posts where post_id=(?)",(pid,))
            post_userid=cur.fetchone()
            post_userid=post_userid[0]
            print(post_userid)
            date=datetime.now().date()
            time=datetime.now().time()
            h=str(time.hour)
            m=str(time.minute)
            s=str(time.second)
            t=h+":"+m+":"+s
            print(date)
            print(time)
            cur.execute("insert into Post_likes values(?,?,?,?,?)",(post_userid,pid,uid,date,t,))

            con.commit()
        return redirect("http://127.0.0.1:5000/wall.html/")
    except:
        return redirect("http://127.0.0.1:5000/wall.html/")

@app.route('/comment/',methods=['POST','GET'])
def comment():
    con=sql.connect('data.db')
    if request.method == 'POST' and 'fname' in session:
        cur=con.cursor()
        uid=session['user_id']
        pid=request.form.get('comment')
        print(pid)
        cur.execute("select user_id from Posts where post_id=(?)",(pid,))
        post_userid=cur.fetchone()
        post_userid=post_userid[0]
        print(post_userid)
        content=request.form.get('comment_content')
        print(content)
        unique_sequence = uniqueid()
        c_id = next(unique_sequence)
        date=datetime.now().date()
        time=datetime.now().time()
        h=str(time.hour)
        m=str(time.minute)
        s=str(time.second)
        t=h+":"+m+":"+s
        print(date)
        print(time)
        cur.execute("insert into Comments values(?,?,?,?,?,?,?)",(post_userid,pid,c_id,uid,content,date,t,))

        con.commit()

    return redirect("http://127.0.0.1:5000/wall.html/")

@app.route('/search/',methods=['POST','GET'])
def search():
    con=sql.connect('data.db')
    if request.method == 'POST' and 'fname' in session:
        cur=con.cursor()
        s=request.form.get('search')
        s="%"+s+"%"
        print(s)
        cur.execute("select f_name,l_name from Users where (f_name like (?) or l_name like (?) or email like (?) or location like (?))",(s,s,s,s,))
        res=cur.fetchall()
        print(res)
        fn=session['fname']
        detail=session['detail']
        posts=session['posts']
        pop_post=session['pop_post']
        a=session['a']

    return render_template('wall.html',name=fn,detail=detail,posts=posts,pop_post=pop_post,res=res,a=a)


@app.route('/friends/',methods=['POST','GET'])
def friends():
    con=sql.connect('data.db')
    if 'fname' in session and request.method=='POST':
        cur=con.cursor()
        fr_name=request.form.get('friend')
        # print(fr_name)
        fn=session['fname']
        cur.execute("select user_id from Users where f_name=(?)",(fr_name,))
        fr_id=cur.fetchone()
        fr_id=fr_id[0]
        # print(fr_id)

        uid=session['user_id']

        cur.execute("select f_name from users where user_id in(select friend_id from friends where user_id=(?) intersect select friend_id from friends where user_id=(?))",(uid,fr_id,))
        rows = cur.fetchall()
        # print(rows)
        cur.execute("select email,location,dob from Users where f_name=(?)",(fr_name,))
        detail=cur.fetchone()
        cur.execute("select f_name from users where user_id in(select friend_id from friends where user_id=(?) and friend_id<> (?) except select friend_id from friends where user_id=(?))",(fr_id,uid,uid,))
        sugg=cur.fetchall()


        cur.execute("select distinct * from Posts where user_id=(?) order by post_date desc",(fr_id,))
        posts=cur.fetchall()
        # print(posts)
        i=0
        for post in posts:
            cur.execute("select count(*) from Post_likes where post_id=(?) group by post_id",(post[1],))
            likes=cur.fetchall()
            if likes==[]:
                likes=0
            else:
                likes=likes[0][0]
            # print(likes)
            # cur.execute("select f_name from users where user_id =(?)",(post[0],))
            # names=cur.fetchall()
            # names=names[0][0]
            cur.execute("select comment_id,comment_content from Comments  where post_id=(?)",(post[1],))
            comm=cur.fetchall()
            cur.execute("select image_content from Photos where post_id=(?)",(post[1],))
            img=cur.fetchone()
            j=0
            for com in comm:

                    cur.execute("select count(*) from comment_likes where comment_id=(?) group by comment_id",(com[0],))
                    com_likes=cur.fetchall()
                    com_likes=com_likes
                    # print(com_likes)
                    if not com_likes:
                        com_likes=0
                    else:
                        com_likes=com_likes[0][0]
                    com=com+(com_likes,)
                    comm[j]=com
                    j=j+1
                    # print(com)
            # print(comm)

            date=post[3]
            date=date.split('-')
            y=int(date[0])
            m=int(date[1])
            d=int(date[2])
            da=datetime(y,m,d)
            diff=datetime.now()-da
            diff=str(diff)
            diff=diff.split(',')
            difference=diff[0]
            if img == None:
                post+=(difference,likes,comm,())
            else:
                post+=(difference,likes,comm,img)
            # print(post)
            posts[i]=post
            i=i+1
    return render_template('friends.html',name=fr_name,detail=detail,rows=rows,posts=posts,sugg=sugg)

@app.route('/commentlike/',methods=['POST','GET'])
def commentlike():
    try:
        con=sql.connect('data.db')
        if request.method == 'POST' and 'fname' in session:
            cur=con.cursor()
            uid=session['user_id']
            cid=request.form.get('comlike')
            # print(cid)
            cur.execute("select user_id,post_id,commenter_id from Comments where comment_id=(?)",(cid,))
            com_userid=cur.fetchone()
            # print(com_userid)
            date=datetime.now().date()
            time=datetime.now().time()
            h=str(time.hour)
            m=str(time.minute)
            s=str(time.second)
            t=h+":"+m+":"+s
            # print(date)
            # print(time)
            print(com_userid[0],com_userid[1],cid,com_userid[2],uid,date,t)
            cur.execute("insert into comment_likes values(?,?,?,?,?,?,?)",(com_userid[0],com_userid[1],cid,com_userid[2],uid,date,t,))

            con.commit()
        return redirect("http://127.0.0.1:5000/wall.html/")
    except:
        return redirect("http://127.0.0.1:5000/wall.html/")


@app.route('/delete/',methods=['POST','GET'])
def delete():
    try:
        con=sql.connect('data.db')
        if request.method == 'POST' and 'fname' in session:
            cur=con.cursor()
            uid=session['user_id']
            pid=request.form.get('delete')
            cur.execute("delete from Posts where post_id=(?)",(pid,))
            con.commit()
            # print(pid)

        return redirect("http://127.0.0.1:5000/user.html/")
    except:
        return redirect("http://127.0.0.1:5000/user.html/")


@app.route('/share/',methods=['POST','GET'])
def share():
    try:
        con=sql.connect('data.db')
        if request.method == 'POST' and 'fname' in session:
            cur=con.cursor()
            uid=session['user_id']
            pid=request.form.get('share')
            cur.execute("select * from Posts where post_id=(?)",(pid,))
            p=cur.fetchone()
            print(p)
            date=datetime.now().date()
            time=datetime.now().time()
            h=str(time.hour)
            m=str(time.minute)
            s=str(time.second)
            t=h+":"+m+":"+s
            unique_sequence = uniqueid()
            p_id = next(unique_sequence)
            cur.execute("insert into Posts values(?,?,?,?,?)",(uid,p_id,p[2],date,t))
            cur.execute("insert into Shares values(?,?,?,?,?)",(p[0],pid,uid,date,t))
            con.commit()


        return redirect("http://127.0.0.1:5000/wall.html/")
    except:
        return redirect("http://127.0.0.1:5000/wall.html/")

@app.route('/signout/',methods=['POST','GET'])
def signout():
    if 'fname' in session:
        session.pop('fname')
        app.secret_key='any string'
    return redirect("http://127.0.0.1:5000/")

if __name__=="__main__":
	app.run(debug=True)
