import sqlite3

conn = sqlite3.connect('data.db')
c=conn.cursor()
def create_table():
    c.execute('create table if not exists Users(user_id varchar(20),f_name varchar(20) not null,l_name varchar(20) not null,address varchar(50),email varchar(50) not null,phone_no varchar(10),location varchar(20),dob date,gender char(1) not null,password varchar(20) not null,primary key(user_id))')
    c.execute('create table if not exists Friends(user_id varchar(20),friend_id varchar(20),accept_date date not null,accept_time time not null,primary key(user_id,friend_id),foreign key(user_id)references Users(user_id) on delete cascade,foreign key(friend_id)references Users(user_id) on delete cascade)')
    c.execute('create table if not exists Posts(user_id varchar(20),post_id varchar(20),post_content varchar(100) not null,post_date date not null,post_time time not null,primary key(user_id,post_id),foreign key(user_id)references Users(user_id) on delete cascade)')

    c.execute('create table if not exists  Post_likes(user_id varchar(20),post_id varchar(20),liker_id varchar(20),like_date date not null,like_time time not null,primary key(user_id,post_id,liker_id),foreign key(liker_id)references Users(user_id) on delete cascade,foreign key(user_id,post_id)references Posts(user_id,post_id)on delete cascade)')

    c.execute('create table if not exists Photos(user_id varchar(20),post_id varchar(20),photo_id varchar(20) unique not null,image_content varchar(10) not null,photo_date date not null,photo_time time not null,primary key(user_id,post_id,photo_id),foreign key(user_id,post_id)references Posts(user_id,post_id) on delete cascade)')

    c.execute('create table if not exists Shares(user_id varchar(20),post_id varchar(20),sharer_id varchar(20),share_date date not null,share_time time not null,primary key(user_id,post_id,sharer_id),foreign key(sharer_id)references Users(user_id) on delete cascade,foreign key(user_id,post_id)references Posts(user_id,post_id) on delete cascade)')

    c.execute('create table if not exists Comments(user_id varchar(20),post_id varchar(20),comment_id varchar(20) unique,commenter_id varchar(20),comment_content varchar(100) not null,comment_date date not null,comment_time time not null,primary key(user_id,post_id,comment_id,commenter_id),foreign key(commenter_id)references Users(user_id) on delete cascade,foreign key(user_id,post_id)references Posts(user_id,post_id)on delete cascade)')

    c.execute('create table if not exists comment_likes(user_id varchar(20),post_id varchar(20),comment_id varchar(20),commenter_id varchar(20),comment_liker_id varchar(20),comment_like_date date not null,comment_like_time time not null,primary key(user_id,post_id,comment_id,commenter_id,comment_liker_id),foreign key(comment_liker_id)references Users(user_id) on delete cascade,foreign key(user_id,post_id,comment_id,commenter_id)references Comments(user_id,post_id,comment_id,commenter_id)on delete cascade)')

    c.execute('create table if not exists reply(user_id varchar(20),post_id varchar(20),comment_id varchar(20),commenter_id varchar(20),reply_id varchar(20)unique,replier_id varchar(20),reply_content varchar(100) not null,reply_date date not null,reply_time time not null,primary key(user_id,post_id,comment_id,commenter_id,reply_id,replier_id),foreign key(replier_id)references Users(user_id)on delete cascade,foreign key(user_id,post_id,comment_id,commenter_id)references Comments(user_id,post_id,comment_id,commenter_id)on delete cascade)')
def data_entry():
    c.execute("insert into Users values('001','Yash','Patil','xyz','yash.r.patil98@gmail.com','9962200288','Bangalore','1998-08-31','M','yash123'),('002','Vedant','Moktali','abc','vedantmoktali@gmail.com','9538342784','Bangalore','1998-02-13','M','vedant123'),('003','Yamini','Agarwal','def','yaminiagarwal09@gmail.com' ,'7677658872','Bangalore','1997-09-09','F','yamini123'),('004','Vibha','Puthran','shantinagar','vibhaputhran@gmail.com','9743055707','Bangalore','1998-03-05','F','vibha123'),('005','Vaani','Sundaresh','Bellandur','vaani@gmail.com','7760360288','Bangalore','1998-07-06','F','vaani123'),('006','Abc','DEF','Bellandur','abc@gmail.com','9876543210','Bangalore','1998-07-12','F','abc123')")

    c.execute("insert into Friends values('001','002','2018-03-03','12:50:02'),('001','003','2018-03-03','12:51:05'),('001','004','2018-03-03','12:52:05'),('001','005','2018-03-03','12:53:05'),('002','003','2018-03-04','12:54:05'),('002','004','2018-03-04','12:55:05'),('002','005','2018-03-04','12:56:05'),('003','004','2018-03-05','12:56:05'),('002','001','2018-03-03','12:50:02'),('003','001','2018-03-03','12:51:05'),('004','001','2018-03-03','12:52:05'),('005','001','2018-03-03','12:53:05'),('003','002','2018-03-04','12:54:05'),('004','002','2018-03-04','12:55:05'),('005','002','2018-03-04','12:56:05'),('004','003','2018-03-05','12:56:05')")

    c.execute("insert into Posts values('001','P001','Going crazy over donuts xD','2018-01-10','13:25:14'),('001','P002','Omg this is soo cute','2018-03-11','01:15:14'),('001','P009','When life gives you lemons, make lemonade','2018-03-15','11:25:14'),('002','P003','Omg this looks so freaking appetizing xD','2018-04-10','11:25:25'),('002','P004','Cats are the best thing in the world... after dogs obviously!','2018-03-11','09:34:14'),('003','P005','Dota 2 is hands down the best game ever XD XD','2018-03-10','16:25:14'),('004','P006','You are so freaking precious when you smile','2018-02-11','16:25:14'),('004','P007','ba dum tsss','2018-03-10','16:25:14'),('005','P008','Yamzee doodle went to town, riding on a pony','2018-03-11','16:25:14')")

    c.execute("insert into Post_likes values('001','P001','002','2018-03-12','16:25:14'),('001','P001','003','2018-03-12','17:25:14'),('001','P001','004','2018-03-12','18:25:14'),('001','P001','005','2018-03-12','19:25:14'),('002','P003','001','2018-03-12','16:52:41'),('003','P005','001','2018-03-12','16:25:14'),('003','P005','002','2018-02-12','17:22:29'),('004','P006','001','2018-03-12','16:52:41'),('005','P008','001','2018-03-12','16:52:41')")

    c.execute("insert into Photos values('001','P001','Ph001','/static/images/donut.jpg','2018-03-10','13:25:14'),('001','P002','Ph002','/static/images/dog.jpg','2018-03-11','01:15:14'),('002','P003','Ph003','/static/images/cake.jpg','2018-03-10','11:25:25')")

    c.execute("insert into Shares values('001','P001','002','2018-03-11','13:25:14'),('001','P002','003','2018-03-12','01:15:14'),('003','P005','004','2018-03-11','16:25:14'),('004','P006','005','2018-03-12','16:25:14'),('005','P008','001','2018-03-12','16:25:14')")

    c.execute("insert into Comments values('001','P001','C001','002','lol','2018-03-14','16:25:14'),('001','P001','C002','003','lel','2018-03-13','17:25:14'),('001','P001','C003','004','wew','2018-03-13','18:25:14'),('001','P001','C004','005','lma','2018-03-13','19:25:14'),('003','P005','C005','001','lol','2018-03-13','16:25:14'),('003','P005','C006','002','lel','2018-03-13','17:25:14'),('003','P005','C007','004','wew','2018-03-13','19:25:14'),('004','P006','C008','002','lol','2018-03-13','16:25:14')")

    c.execute("insert into comment_likes values('001','P001','C001','002','001','2018-03-13','20:25:14'),('001','P001','C001','002','003','2018-03-13','20:25:14'),('001','P001','C001','002','004','2018-03-13','20:25:14'),('001','P001','C001','002','005','2018-03-13','20:25:14'),('001','P001','C002','003','001','2018-03-13','20:25:14'),('001','P001','C003','004','001','2018-03-13','20:25:14')")

    c.execute("insert into reply values('001','P001','C001','002','R001','001','lol','2018-03-13','21:25:14'),('001','P001','C001','002','R002','003','lol','2018-03-13','21:25:14'),('001','P001','C001','002','R003','004','lol','2018-03-13','21:25:14'),('001','P001','C001','002','R004','005','lol','2018-03-13','21:25:14'),('001','P001','C002','003','R005','001','lol','2018-03-13','21:25:14'),('001','P001','C003','004','R006','001','lol','2018-03-13','21:25:14')")

    conn.commit()
    c.close()
    conn.close()
create_table()
data_entry()
