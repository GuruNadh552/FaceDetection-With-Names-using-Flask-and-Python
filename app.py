from flask import Flask, render_template, Response,request,redirect,url_for
from camera import Video

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verifyID')
def verifyID():
    return render_template('verifyID.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   if request.method == 'POST':
      if request.form['sid'] != 'admin' or request.form['pass_w'] != 'admin':
         error = 'Invalid username or password. Please try again!'
      else:
         return redirect(url_for('verifyID'))
   return render_template('index.html', error = error)

def gen(camera):
    while True:
        frame=camera.get_frame()
        yield(b'--frame\r\n'
       b'Content-Type:  image/jpeg\r\n\r\n' + frame +
         b'\r\n\r\n')

@app.route('/video')
def video():
    return Response(gen(Video()),
    mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(debug=True)
