import random
import speech_recognition as sr
from flask import Flask, render_template,request
import cx_Oracle
from datetime import date
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\Subhadeep\Downloads\instantclient_19_9")
name1=""
app = Flask(__name__)

@app.route('/')
def home():
   return render_template("start.html")
def insert_score1(str1,c,today):
    con=cx_Oracle.connect('system/subhadeep005@localhost:1521/xe')  #Connect the database#
    c1=c
    str=str1
    date=today
    cursor=con.cursor()
    cursor.execute("insert into game_result(status,score,playing_date) values(:status,:score,:playing_date)",{'status':str,'Score':c1,'playing_date':date})    #insert value into database#
    con.commit()
    print("Record Inserted")
def insert_score2(str1,c,today):
    con=cx_Oracle.connect('system/subhadeep005@localhost:1521/xe')  #Connect the database#
    c1=c
    str=str1
    date=today
    cursor=con.cursor()
    cursor.execute("insert into game_result(status,score,playing_date) values(:status,:score,:playing_date)",{'status':str,'Score':c1,'playing_date':date})    #insert value into database#
    con.commit()
    print("Record Inserted")
@app.route("/play", methods=["GET","POST"])
def play(): 
    
    if request.method == 'POST':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak your guess!")
            audio = r.listen(source)
        try:
            guess = r.recognize_google(audio)
        except sr.UnknownValueError:
            guess = "Sorry, I didn't catch that. Please try again."
        except sr.RequestError as e:
            guess = "Could not request results from Google Speech Recognition service; {0}".format(e)
        
        WORDS = ["Apple", "Banana", "Grape", "Orange", "Mango", "Lemon","Watermelon","Stawberry","Guava"]
        word = random.choice(WORDS)
        guess_is_correct=guess.capitalize()
        
        if guess_is_correct== word:
            result = "WINNER!!You guessed it! The Fruit was {}.".format(word)
            print(guess)
            c1=0
            str1=""
            c1=c1+1
            str1="Win"
            today = date.today()
            insert_score1(str1,c1,today)
            request.method=""
        else:
            result = "LOOSE!!Sorry, you missed it. The Fruit was {}.".format(word)
            print(guess)
            c1=0
            str1=""
            str1="Loss"
            today = date.today()
            insert_score2(str1,c1,today)
            request.method=""


        return render_template('result.html', result=result)
    return render_template('play.html')

if __name__ == '__main__':
    app.run()