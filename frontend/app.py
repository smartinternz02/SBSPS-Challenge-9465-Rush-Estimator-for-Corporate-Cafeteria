from flask import Flask;
from flask import render_template,Response,request;
#import mysql.connector
import cv2
def camera_check():
    if camera.isOpened():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
       return "please connect to your camera"
global camera
camera = cv2.VideoCapture(0)
def gen_frames(): 
    import cv2
    
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

app = Flask(__name__)

@app.route("/")
def signin():
    return render_template('home.html')

@app.route("/signin")
def home():
    return render_template('index.html')

@app.route('/result',methods=['GET','POST'])
def result():
    mdb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="regester"
    )
    nocursor=mdb.cursor()
    if request.method=="POST":
        signup=request.form
        username=signup['user']
        password=signup['pass']
        nocursor.execute("select * from users where username='"+username+"' and password='"+password+"'")
        r=nocursor.fetchall()
        count=nocursor.rowcount
        if count==1:
            return render_template("result.html")
        elif count>1:
            return "More than one User"
        else:
            return render_template("signup.html")
    mdb.commit()
    nocursor.close()

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/video_feed")
def video():
    return camera_check()

@app.route("/analytics")
def analytics():
    return render_template('analytics.html')
        
        


if __name__=='__main__':
    app.run()