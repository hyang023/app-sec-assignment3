import os
import random
from datetime import datetime
import subprocess
from subprocess import check_output
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

uname = ''
pword = ''
unamelist = [] 
pwordlist = [] 
twofalist = []
loginuserlist = []
logintimelist = []
logouttimelist = []
querylist = []
queryuserlist = []
queryresultlist = []

#def create_app(config=None):
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80))
    twofactr = db.Column(db.Integer())

class Query(db.Model):
    query_id = db.Column(db.Integer(), primary_key=True)
    querytxt = db.Column(db.Text())
    misspell = db.Column(db.Text())
    queryusr = db.Column(db.String(80), db.ForeignKey(User.username))
    username = db.relationship('User', foreign_keys='Query.username')
    
class Login(db.Model):
    login_id = db.Column(db.Integer(), primary_key=True)
    logitime = db.Column(db.String(30))
    logotime = db.Column(db.String(30))
    loginusr = db.Column(db.String(80), db.ForeignKey(User.username))
    username = db.relationship('User', foreign_keys='Query.username')

db.create_all()    
    
unamelist.append("admin")
pwordlist.append("Administrator@1")
twofalist.append("12345678901")

admin = User(username='admin', password='admin@example.com', twofactr='12345678901')
db.session.add(admin)
db.session.commit()
    
    #return app

@app.route('/')
def hello_world():
    missing = User.query.filter_by(username='missing').first()
    return (missing is None)

@app.route('/register', methods=['post', 'get'])
def register():
    value=random.randrange(1,100)
    message = ''
    if request.method == 'POST':
        uname = request.form.get('uname')
        pword = request.form.get('pword')
        twofa = request.form.get('2fa')
        adduser = User(username=uname, password=pword, twofactr=twofa)
        db.session.add(adduser)
        db.session.commit()
        if uname  and pword :
        	if uname in unamelist:
        	    message="Failure: username already exists"
        	else:
        	    unamelist.append(uname)
        	    pwordlist.append(pword)
        	    if twofa:
        	        if twofa.isdigit():
        	            twofalist.append(twofa)
        	    else:
        	        twofalist.append('no')
        	    message = "Success. Your username is "+uname
    return render_template('registration.html', message=message, value=value)

@app.route('/login',  methods=['post', 'get'])
def login():
    value=random.randrange(1,100)
    message = ''
    if request.method == 'POST':
        uname = request.form.get('uname')
        pword = request.form.get('pword')
        twofa = request.form.get('2fa')
        if uname  and pword :
        	message = "Incorrect password "+uname
        	if uname in unamelist:
        	    index = unamelist.index(uname)
        	    if pword in pwordlist:
        		    index2 = pwordlist.index(pword)
        		    if index == index2:
        		        message = "Success"
        		        loginuserlist.append(uname);
        		        now = datetime.now()
        		        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        		        logintimelist.append(current_time)
        	    if pwordlist[index] == pword:
        		    message = "Success "+loginuserlist[-1]+" is logged in at "+current_time
        	    if twofalist[index] != twofa and twofalist[index] != 'no':
        		    message = "Two-factor authentication failure"
    return render_template('login.html', message=message, value=value)

@app.route('/login_success', methods=['POST'])
def login_success():
    return render_template('login_success.html')

@app.route('/logout')
def logout():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    logouttimelist.append(current_time)
    return 'logged out'

@app.route('/spell_check', methods=['post', 'get'])
def spell_check():
    value=random.randrange(1,100)
    message = ''
    message2 = ''
    if request.method == 'POST':
        inputtext = request.form.get('inputtext')
        if inputtext:
            queryuserlist.append(loginuserlist[-1])
            querylist.append(inputtext)
            message = "Supplied Text: "+inputtext
            #stdout = check_output(['ls','-l']).decode('utf-8')
            f= open("test1.txt","w+")
            f.write(inputtext)
            f.close() 
            stdout = check_output(['chmod','755','a.out'])
            #stdout = check_output(['ls','-l']).decode('utf-8')
            stdout = check_output(['./a.out','test1.txt','wordlist.txt']).decode('utf-8')
            os.remove("test1.txt")
            message2 = "Misspelled words: "+stdout
            queryresultlist.append(stdout)
    return render_template('spellcheck.html', message=message, message2=message2, value=value)

@app.route('/history', methods=['post', 'get'])
def history():
    value=random.randrange(1,100)
    message1 = ''
    message2 = []
    user = ''
    if len(logintimelist)>len(logouttimelist):
        user = loginuserlist[-1]    
    if request.method == 'POST':
        inputtext = request.form.get('inputtext')
        if len(logintimelist)>len(logouttimelist) and loginuserlist[-1] == 'admin' and inputtext:
            message2 = [str(index) for index, value in enumerate(queryuserlist) if value == inputtext]
            message1 = inputtext+" has made "+str(len(message2))+" queries"
    elif len(logintimelist)>len(logouttimelist):
        message2 = [str(index) for index, value in enumerate(queryuserlist) if value == loginuserlist[-1]]
        message1 = "you have made "+str(len(message2))+" queries"
    return render_template('history.html', message1=message1, message2=message2, user=user, value=value)

@app.route('/history/query<int:query_id>')
def query_history(query_id):
    message1 = ''
    message2 = ''
    message3 = ''
    message4 = ''
    if query_id < len(queryuserlist):
        if loginuserlist[-1] == 'admin' or queryuserlist[query_id] == loginuserlist[-1]:
            message1 = str(query_id)
            message2 = queryuserlist[query_id]
            message3 = querylist[query_id]
            message4 = queryresultlist[query_id]
    return render_template('queryhistory.html', message1=message1, message2=message2, message3=message3, message4=message4)

@app.route('/login_history',  methods=['post', 'get'])
def login_history():
    value=random.randrange(1,100)
    user = ''
    message = "Admins can view login history page here"
    message1 = []
    message2 = []
    message3 = []
    inputuser = ''
    if len(logintimelist)>len(logouttimelist):
        user = loginuserlist[-1]   
    if request.method == 'POST':
        inputtext = request.form.get('inputtext')
        if len(logintimelist)>len(logouttimelist) and loginuserlist[-1] == 'admin' and inputtext:
            inputuser = inputtext
            temp = [index for index, value in enumerate(queryuserlist) if value == inputtext]
            message1 = [str(index) for index, value in enumerate(queryuserlist) if value == inputtext]
            for x in temp:
                message2.append(logintimelist[x])
                if len(logintimelist) == len(logouttimelist) or x < (len(logouttimelist)):
                    message3.append(logouttimelist[x])
                else:
                    message3.append("N/A")
    return render_template('loginhistory.html', message=message, message1=message1, message2=message2, message3=message3, value= value, user=user)
