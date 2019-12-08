import os
import random
from datetime import datetime
import subprocess
from subprocess import check_output
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
unamelist = [] 
pwordlist = [] 
twofalist = []
loggedin = ''
loginuserlist = []
logintimelist = []
logouttimelist = []
querylist = []
queryuserlist = []
queryresultlist = []

#def create_app(config=None):
app = Flask(__name__)
#db.init_app(app)

unamelist.append("admin")
pwordlist.append("Administrator@1")
twofalist.append("12345678901")
    
    #return app

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/register', methods=['post', 'get'])
def register():
    value=random.randrange(1,100)
    message = ''
    if request.method == 'POST':
        uname = request.form.get('uname')
        pword = request.form.get('pword')
        twofa = request.form.get('2fa')

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
        		        loggedin = uname;
        		        loginuserlist.append(uname);
        		        now = datetime.now()
        		        current_time = now.strftime("%H:%M:%S")
        		        logintimelist.append(current_time)
        	    if pwordlist[index] == pword:
        		    message = "Success "+loggedin+" is logged in"
        	    if twofalist[index] != twofa and twofalist[index] != 'no':
        		    message = "Two-factor authentication failure"

    return render_template('login.html', message=message, value=value)

@app.route('/login_success', methods=['POST'])
def login_success():
    return render_template('login_success.html')

@app.route('/logout')
def logout():
    loggedin = []
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    logouttimelist.append(current_time)
    return render_template('logged out')

@app.route('/spell_check', methods=['post', 'get'])
def spell_check():
    value=random.randrange(1,100)
    message = ''
    message2 = ''
    if request.method == 'POST':
        inputtext = request.form.get('inputtext')
        if inputtext:
            queryuserlist.append(loggedin)
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

@app.route('/history')
def history():
    message1 = "you have made [number] queries"
    message2 = "All of your queries are listed here"
    return render_template('history.html', message1=message1, message2=message2)

@app.route('/history/query<int:query_id>')
def query_history(query_id):
    if loggedin == 'admin' or queryuserlist[query_id] == loggedin:
        message1 = str(query_id)
        message2 = queryuserlist[query_id]
        message3 = querylist[query_id]
        message4 = queryresultlist[query_id]
    return render_template('queryhistory.html', message1=message1, message2=message2, message3=message3, message4=message4)

@app.route('/login_history')
def login_history():
    message = "Admins can view login history page here"
    return render_template('loginhistory.html', message=message)
