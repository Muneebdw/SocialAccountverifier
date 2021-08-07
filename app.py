from pickle import FALSE
import re
from flask import Flask, render_template, redirect, url_for, request
from multiprocessing import Pool, cpu_count
import threading
from instabot import Bot

import os 
import random
import string
import glob
bot = Bot()
app = Flask(__name__)
start = True
s_login = True
username = ""

otp = ""
def login():
    bot.login(username="SocialVerifierOTP", password="Verifier123")



def init():
   #global start
    global s_login
    global bot
    start = True
    print("Started")
    if(s_login==True):
        s_login = False
        try:
            cookie_del = glob.glob("config/*cookie.json")
            os.remove(cookie_del[0])
        except:
            print("Go")
        start =True
        Login = threading.Thread(target=login, args=(), daemon=True)
        Login.start()
        #Login.join()


def checkOTP(insertedotp):
    global otp
    if(insertedotp==otp):
        return True
    else:
        return False


def generateOTP():
    otp = "INST"
    otp += ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(5))
    return otp



def sendOTP(username):
    global otp
    global s_login
    user_id = bot.get_user_id_from_username(username)
    otp = generateOTP()
    bot.send_message(otp,user_id)
    print(username)
    #bot.logout()
    #s_login = True


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        #init()
        return render_template('home.html')

@app.route('/CheckVerified',methods=['GET','POST'])
def checkverific():
    if request.method =='GET':
        return render_template('CheckVerified.html')

@app.route('/ShowStatus',methods=['GET','POST'])
def showstat():
    if request.method == 'POST':
        username = request.form['Username']
        with open('Verified.txt','r') as f:
            if username in f.read():
                return render_template('RResult.html')
            else:
                return render_template('WResult.html')



# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def loginadmin():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('Verified')
    return render_template('login.html', error=error)

@app.route('/Verifyinsta',methods=['GET','POST'])
def verifyinsta():
    if request.method =='POST':
        global username
        username = request.form['Username']
        x = threading.Thread(target=sendOTP, args=(username,), daemon=True)
        x.start()
        #x.join()
        #print(username)
        return render_template('Instaverifier.html')


@app.route('/Result',methods=['GET','POST'])
def result():
    if request.method =='POST':
        global username
        InsertedOTP = request.form['OTP']
        if(checkOTP(InsertedOTP)):
            with open('Verified.txt','r') as f:
                if username in f.read():
                    f.close()
                else:
                    W = open('Verified.txt','a')
                    W.write(username+'\n')
                    W.close()
            return render_template('RResult.html')
        else:
            return render_template('WResult.html')

@app.route('/Verified',methods=['GET','POST'])
def showverified():
    if request.method=='GET':
        with open("Verified.txt", "r") as file:
            verified = file.readlines()
            return render_template('ShowVerified.html', text = verified)
    if request.method=='POST':
        username = request.form['Username']
        with open("Verified.txt", "r") as f:
            lines = f.readlines()
        with open("Verified.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != username:
                    f.write(line)
        with open("Verified.txt", "r") as file:
            verified = file.readlines()
            return render_template('ShowVerified.html', text = verified)



if __name__ == '__main__':
    app.run(debug=False, threaded=False)
