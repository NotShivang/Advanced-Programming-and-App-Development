# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_cloudsql_mysql]
import os

from flask import Flask, render_template, request, jsonify, flash, session, redirect, url_for
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)


if os.environ.get('GAE_ENV') == 'standard':
        unix_socket = '/cloudsql/{}'.format(db_connection_name)
        cnx = pymysql.connect(user=db_user, password=db_password,
                              unix_socket=unix_socket, db=db_name)
else:
        host = '127.0.0.1'
        cnx = pymysql.connect(user=db_user, password=db_password,
                              host=host, db=db_name)

finalemail = ""
admin = ""

@app.route('/')
def main():

    with cnx.cursor() as cursor:
        cursor.execute('SELECT * from Event;')
        data = cursor.fetchall()

    return render_template('home.html', data=data)


@app.route('/Venues')
def vven():
    with cnx.cursor() as cursor:

        cursor.execute('SELECT * from Venue;')
        data = cursor.fetchall()
        
    return render_template('venue.html', data=data)


@app.route('/Venues2')
def vven2():
    with cnx.cursor() as cursor:

        cursor.execute('SELECT * from Venue;')
        data = cursor.fetchall()
        
    return jsonify(data)

@app.route('/ShowEvent')
def showevent2():
    with cnx.cursor() as cursor:

        cursor.execute('SELECT * from Event;')
        data = cursor.fetchall()
        
    return jsonify(data)

@app.route('/Login')
def tlogin():
    return render_template('Login.html')

@app.route('/Login', methods=['POST'])
def login():
    global finalemail
    global admin
    email = request.form['email']
    _email = str(email)
    pwd = request.form['pwd']
    _pwd = int(pwd)
    with cnx.cursor() as cursor:
        cursor.execute('SELECT count(*) from Users where email = %s and password = %s ;',(_email,_pwd))
        d = cursor.fetchone()
        cursor.execute('SELECT count(*) from Admin where email = %s;',[_email])
        admin2 = cursor.fetchone()
        if(d!=(0,)):
            finalemail = _email
            if(admin2!=(0,)):
                admin = "true"
                return render_template('tadminhome.html')
            else:
                return render_template('thome.html')
        else:
            return str("Wrong UserName or Wrong PIN")

@app.route('/Login2', methods=['POST'])
def login2():
    global finalemail
    global admin
    email = request.form['email']
    _email = str(email)
    pwd = request.form['pwd']
    _pwd = int(pwd)
    with cnx.cursor() as cursor:
        cursor.execute('SELECT count(*) from Users where email = %s and password = %s ;',(_email,_pwd))
        d = cursor.fetchone()
        cursor.execute('SELECT count(*) from Admin where email = %s;',[_email])
        admin2 = cursor.fetchone()
        if(d!=(0,)):
            finalemail = _email
            if(admin2!=(0,)):
                admin = "true"
                return jsonify({'message':'Admin Confirmed'})
            else:
                return jsonify({'message':'User Confirmed'})
        else:
            return jsonify({'message':'Wrong UserName or Wrong PIN'})

@app.route('/userhome')
def tt():
    global finalemail
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * from Event;')
        data = cursor.fetchall()
        cursor.execute('SELECT eventid from Registered2 where userid = %s',[finalemail])
        registeredfor = cursor.fetchall()
    return render_template('userhome.html', data=data, femail = finalemail, registeredfor = registeredfor)


@app.route('/userhome2')
def tt2():
    global finalemail
    with cnx.cursor() as cursor:
        cursor.execute('SELECT eventid from Registered2 where userid = %s',[finalemail])
        registeredfor = cursor.fetchall()
    return jsonify(registeredfor)

@app.route('/adminhome')
def t():
    global finalemail
    with cnx.cursor() as cursor:
        cursor.execute('SELECT * from Event;')
        data = cursor.fetchall()
        cursor.execute('SELECT eventid from Registered2 where userid = %s',[finalemail])
        registeredfor = cursor.fetchall()
    return render_template('adminhome.html', data=data, femail = finalemail, registeredfor = registeredfor)


@app.route('/admintemp', methods=['POST'])
def admintemp():
    email = str(request.form['email'])
    name = str(request.form['fname'])
    with cnx.cursor() as cursor:
        
        cursor.execute('''Insert into Admin (name,email) values (%s,%s)''',(name,email))
        cursor.execute('''commit;''')

    return jsonify({"mess":"Admin Added"})


@app.route('/Signup')
def tsignup():
    return render_template('Signup.html')

@app.route('/Signup', methods=['POST'])
def signup():
    email = str(request.form['email'])
    name = str(request.form['fname'])
    sname =str(request.form['sname'])
    password = int(request.form['pwd'])
    zipcode = int(request.form['zipcode'])
    phone =int(request.form['phone'])
    etype1 =str(request.form['etype1'])
    etype2 =str(request.form['etype2'])
    etype3 =str(request.form['etype3'])
    with cnx.cursor() as cursor:
        
        cursor.execute('''Insert into Users (email,name,sname,password,zipcode,phone,etype1,etype2,etype3) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(email,name,sname,password,zipcode,phone,etype1,etype2,etype3))
        cursor.execute('''commit;''')   
    
    return render_template('tlogin.html')

@app.route('/create')
def tcreate():
    with cnx.cursor() as cursor:
        cursor.execute('''SELECT venuename FROM Venue;''')
        vname1 = cursor.fetchall()
        return render_template('create.html',vennames = vname1)

@app.route('/create', methods=['POST'])
def create():
    global finalemail
    global admin
    venue = str(request.form['vennames'])
    v=venue.split("'")
    venue=v[1]
    capacity = int(request.form['capacity'])
    remaining = int(request.form['remspots'])
    fee =int(request.form['fees'])
    begin =str(request.form['bt'])
    end =str(request.form['et'])
    typ = str(request.form['type'])

    with cnx.cursor() as cursor:
        cursor.execute('''SELECT venueid FROM Venue where venuename = %s ''',[venue])
        venueid = int(cursor.fetchone()[0])
        cursor.execute(''' select availability from VenueSlots2 where datetime2 >= %s and datetime2 <%s AND venueid=%s''', (begin,end,venueid))
        flag=0
        for m in cursor.fetchall():
            if (m==(0,)): 
                flag=1
        if(flag==0):
            cursor.execute('''SELECT EventID FROM Event ORDER BY EventID DESC LIMIT 1 ''')
            eventid = cursor.fetchone()[0]
            eventi = eventid+1
            cursor.execute('''Insert into Event (EventID, EventCreator,Venue,Capacity,RemainingSpots, Fee_USD,Begintime,endtime,Type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(eventi,finalemail,venue,capacity,remaining,fee,begin,end,typ))
            cursor.execute('''commit;''')
            cursor.execute('''Update VenueSlots2 set availability = 0, EventID = %s where venueid = %s and datetime2 between %s and %s''',(eventi,venueid,begin,end))
            cursor.execute('''commit;''')
            if(admin=="true"):
                return render_template('tadminhome.html')
            else:
                return render_template('thome.html')
        else:
            return("Not Available")

@app.route('/create2', methods=['POST'])
def create2():
    global finalemail
    global admin
    venue = str(request.form['vennames'])
    capacity = int(request.form['capacity'])
    remaining = int(request.form['remspots'])
    fee =int(request.form['fees'])
    begin =str(request.form['bt'])
    end =str(request.form['et'])
    typ = str(request.form['type'])

    with cnx.cursor() as cursor:
        cursor.execute('''SELECT venueid FROM Venue where venuename = %s ''',[venue])
        venueid = int(cursor.fetchone()[0])
        cursor.execute(''' select availability from VenueSlots2 where datetime2 >= %s and datetime2 <%s AND venueid=%s''', (begin,end,venueid))
        flag=0
        for m in cursor.fetchall():
            if (m==(0,)): 
                flag=1
        if(flag==0):
            cursor.execute('''SELECT EventID FROM Event ORDER BY EventID DESC LIMIT 1 ''')
            eventid = cursor.fetchone()[0]
            eventi = eventid+1
            cursor.execute('''Insert into Event (EventID, EventCreator,Venue,Capacity,RemainingSpots, Fee_USD,Begintime,endtime,Type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(eventi,finalemail,venue,capacity,remaining,fee,begin,end,typ))
            cursor.execute('''commit;''')
            cursor.execute('''Update VenueSlots2 set availability = 0, EventID = %s where venueid = %s and datetime2 between %s and %s''',(eventi,venueid,begin,end))
            cursor.execute('''commit;''')
            if(admin=="true"):
                return jsonify({'message':'Admin Created Event Successfully, Press Back'})
            else:
                return jsonify({'message':'User Created Event Successfully, Press Back'})
        else:
            return jsonify({'message':'Not Available'})

@app.route('/addvenue')
def tvenueadd():
    return render_template('addvenue.html')

@app.route('/addvenue', methods=['POST'])
def venueadd():
    vname = str(request.form['vname'])
    vlocation =str(request.form['vlocation'])
    vzipcode = int(request.form['vzip'])
    vfees = int(request.form['vfees'])
    with cnx.cursor() as cursor:
        cursor.execute('''SELECT venueid FROM Venue ORDER BY venueid DESC LIMIT 1 ''')
        venueid = cursor.fetchone()[0]
        venuei = venueid+1
        cursor.execute('''Insert into Venue (venueid, venuename,location,zipcode,fees) values (%s,%s,%s,%s,%s)''',(venuei,vname,vlocation,vzipcode,vfees))
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (1,'2019-08-01 08:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (2,'2019-08-01 09:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (3,'2019-08-01 10:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (4,'2019-08-01 11:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (5,'2019-08-01 12:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (6,'2019-08-01 13:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (1,'2019-08-02 08:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (2,'2019-08-02 09:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (3,'2019-08-02 10:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (4,'2019-08-02 11:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (5,'2019-08-02 12:00:00',%s,1,NULL);''',[venuei])
        cursor.execute(''' Insert into VenueSlots2 (slot,datetime2,venueid,availability,eventid) VALUES (6,'2019-08-02 13:00:00',%s,1,NULL);''',[venuei])
        cursor.execute('''commit;''')
        return render_template('tadminhome.html')

@app.route('/deleteevent')
def tdelete():
    return render_template('deleteevent.html')

@app.route('/deleteevent',methods=['POST'])
def deleteevent(eid=0):
    if(eid==0):
        eid=int(request.form['eventid'])
    else:
        teid = eid
    with cnx.cursor() as cursor:
        cursor.execute(''' delete from Registered2 where eventid=%s ''',[eid])
        cursor.execute(''' update VenueSlots2 set availability=1,eventid =null where eventid = %s ''',[eid])
        cursor.execute(''' delete from Event where EventID = %s ''',[eid])
        cursor.execute('''commit;''')
    return render_template('tadminhome.html')

@app.route('/deletevenue')
def tdelvenue():
    with cnx.cursor() as cursor:
        cursor.execute('''SELECT venuename FROM Venue;''')
        vname1 = cursor.fetchall()
        return render_template('deletevenue.html',vennames = vname1)

@app.route('/deletevenue',methods=['POST'])
def delvenue():
    venue = str(request.form['vennames'])
    v=venue.split("'")
    venue=v[1]
    with cnx.cursor() as cursor:
        cursor.execute('''SELECT venueid FROM Venue where venuename = %s ''',[venue])
        venueid = int(cursor.fetchone()[0])
        cursor.execute(''' delete from VenueSlots2 where venueid=%s ''',[venueid])
        cursor.execute('''commit;''')
        cursor.execute('''SELECT EventID FROM Event where Venue = %s ''',[venue])
        eventids = cursor.fetchall()
        for x in eventids:
               deleteevent(x)
        cursor.execute(''' delete from Venue where venueid=%s ''',[venueid])
        cursor.execute('''commit;''')
        return render_template('tadminhome.html')

@app.route('/deleteuser')
def tdeluser():
    with cnx.cursor() as cursor:
        cursor.execute('''SELECT email FROM Users;''')
        vname1 = cursor.fetchall()
        return render_template('deleteuser.html',vennames = vname1)

@app.route('/deleteuser',methods=['POST'])
def deluser():
    uemail = str(request.form['vennames'])
    u=uemail.split("'")
    uemail=u[1]
    with cnx.cursor() as cursor:
        cursor.execute('''SELECT eventid FROM Registered2 where userid=%s  ''',[uemail])
        eventids1 = cursor.fetchall()
        cursor.execute(''' delete from Registered2 where userid=%s ''',[uemail])
        cursor.execute('''commit;''')
        for x in eventids1:
            cursor.execute('''update Event set RemainingSpots = RemainingSpots + 1 where EventID = %s''',[x])
            cursor.execute('''commit;''')
        cursor.execute('''SELECT EventID FROM Event where EventCreator = %s ''',[uemail])
        eventids = cursor.fetchall()
        for y in eventids:
            deleteevent(y)
        cursor.execute(''' delete from Users where email=%s ''',[uemail])
        cursor.execute('''commit;''')
        return render_template('tadminhome.html')


@app.route('/join')
def tjoin():
    return render_template('join.html')

@app.route('/join', methods=['POST'])
def join():
    with cnx.cursor() as cursor:
        global finalemail
        eventid = int(request.form['eventid'])

        cursor.execute('''select RemainingSpots from Event where EventID = %s''',[eventid])
        countone = cursor.fetchone()[0]
        cc = int(countone)
        if(cc>0):
            cursor.execute('''insert into Registered2 (eventid,userid) values (%s,%s)''',(eventid,finalemail))
            cursor.execute('''update Event set RemainingSpots = RemainingSpots -1 where EventID = %s''',[eventid])
            cursor.execute('''commit;''')
            if(admin=="true"):
                return render_template('tadminhome.html')
            else:
                return render_template('thome.html')
        else:
            return("Sorry Event is full")

@app.route('/join2', methods=['POST'])
def join2():
    with cnx.cursor() as cursor:
        global finalemail
        eventid = int(request.form['eventid'])

        cursor.execute('''select RemainingSpots from Event where EventID = %s''',[eventid])
        countone = cursor.fetchone()[0]
        cc = int(countone)
        if(cc>0):
            cursor.execute('''insert into Registered2 (eventid,userid) values (%s,%s)''',(eventid,finalemail))
            cursor.execute('''update Event set RemainingSpots = RemainingSpots -1 where EventID = %s''',[eventid])
            cursor.execute('''commit;''')
            if(admin=="true"):
                return 
            else:
                return jsonify({'message':'Successfully joined the Event, Press Back'})
        else:
            return jsonify({'message':'No Space in the Event'})

@app.route('/unregister')
def tunregister():
    with cnx.cursor() as cursor:
        global finalemail
        cursor.execute('SELECT eventid from Registered2 where userid = %s',[finalemail])
        registeredfor = cursor.fetchall()
        if(registeredfor!=(0,)):
            return render_template('unregister.html',regis = registeredfor)
        else:
            return("You haven't registered for any Events")

@app.route('/unregister', methods=['POST'])
def unregister():
    with cnx.cursor() as cursor:
        global finalemail
        eventid = int(request.form['eventidunregis'])
        cursor.execute(''' delete from Registered2 where userid=%s and eventid =%s''',(finalemail,eventid))
        cursor.execute('''update Event set RemainingSpots = RemainingSpots +1 where EventID = %s''',[eventid])
        cursor.execute('''commit;''')
        if(admin=="true"):
            return render_template('tadminhome.html')
        else:
            return render_template('thome.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	