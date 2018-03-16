from flask import Flask
from flask import request
from flask import jsonify
import pyrebase
app = Flask(__name__)

@app.route("/performance")
def getParameters():
	args = request.args
	first = float(args['HR'])
	second = float(args['temp'])
	third = float(args['rpm'])
	valueForHr = normalizeHR ( 30 , 120 , first ) 
	valueForTemp = normalizeTemp ( 37 , second )
	valueForRPM = normalizeRPM ( 70 , third )
	feedback = performance ( valueForHr + valueForTemp + valueForRPM )
	return jsonify(diffHR=valueForHr,diffTemp=valueForTemp,diffRPM =valueForRPM,performance=feedback)

def normalizeHR ( age , desiredHR , actualHR):
    normAct =  actualHR / ( 220 - age )
    normDes = desiredHR / ( 220 - age )
    return modul( normAct - normDes ) 

def modul ( a ):
    if a < 0 :
       return -a
    return a

def normalizeTemp ( desiredTemp , actualTemp ):
    normAct = ( actualTemp -  28 ) / 14 
    normDes = ( desiredTemp - 28 ) / 14
    return modul(normDes-normAct)

def normalizeRPM ( desiredRPM , actualRPM ):
    normAct = ( actualRPM - 20 ) / 80
    normDes = ( desiredRPM - 20 ) / 80
    return modul(normDes-normAct)

def performance ( value ):
    if value < 0.1 :
         return "Very good"
    elif value < 0.2 :
         return "Good"
    else: 
    	return "Need for improvement"

@app.route("/listusers")
def getUsers():
     config = {
             "apiKey": "AIzaSyB9D_CH5n3K6Ip02Go32d3SCXqVdPAs15g",
             "authDomain": "utilizatori-46bfc.firebaseapp.com",
             "databaseURL": "https://utilizatori-46bfc.firebaseio.com",
             "projectId": "utilizatori-46bfc",
             "storageBucket": "utilizatori-46bfc.appspot.com",
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    users = db.child("users").get()
    date=""
    for user in users.each():
        date = date + user.val()
    jsonify(date)
    
if __name__ == "__main__":
    app.run()
