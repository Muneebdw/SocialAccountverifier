from pickle import FALSE
from flask import Flask , request , render_template
from multiprocessing import Pool, cpu_count
import threading
from instabot import Bot
import os 
import glob
bot = Bot()
app = Flask(__name__)
start = True
def init():
    print("Started")


        

def sendOTP(username):
    global start
    if start==True:
        start=False
        try:
            cookie_del = glob.glob("config/*cookie.json")
            os.remove(cookie_del[0])
        except:
            print("Go")
        start =True
        bot.login(username="bhalli_r07", password="Lionzkillermuneeb123")
        user_id = bot.get_user_id_from_username("Arissein")
        bot.send_message('Test',user_id)
        print(username)


@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        init()
        return render_template('home.html')


@app.route('/Verifyinsta',methods=['GET','POST'])
def verifyinsta():
    if request.method =='POST':
        username = request.form['Username']
        sendOTP(username)
        #print(username)
        return render_template('Instaverifier.html')


@app.route('/Result',methods=['GET','POST'])
def result():
    if request.method =='POST':
        OTP = request.form['OTP']
        return render_template('Result.html')

if __name__ == '__main__':
    app.run(debug=False, threaded=False)
