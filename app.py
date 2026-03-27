from flask import Flask,render_template,request
import sqlite3
app=Flask(__name__)

def init_db():
    conn=sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT,type TEXT,message TEXT)""")
    conn.commit()
    conn.close()

def auto_response(message):
    message=message.lower()
    responses={
        "appointment":"Yov can book appointment at +91-9876543210",
        "emergency":" Call emergency helpline: 108 immediately",
        "doctor":"Doctors are available from 9 AM to 5 PM",
        "covid":"Please follow safety guidelines and consult nearby hospitals"
    }
    for key in responses:
        if key in message:
            return responses[key]
    return "\u2705 Your request has been recorded. Out team will contact you soon."

@app.route("/",methods=["GET","POST"])
def index():
    response=""
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        user_type=request.form["type"]
        message=request.form["message"]
        conn=sqlite3.connect("database.db")
        cursor=conn.cursor()
        cursor.execute("INSERT INTO users (name,email,type,message) VALUES(?,?,?,?)",(name,email,user_type,message))
        conn.commit()
        conn.close()
        response=auto_response(message)
    return render_template("index.html",response=response)

if __name__=="__main__":
    init_db()
    app.run(debug=True)
