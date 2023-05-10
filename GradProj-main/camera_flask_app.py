from flask import Flask, redirect, url_for, render_template, request, flash, Response
import cv2
import datetime
import time
import os
import sys
import numpy as np
from threading import Thread
from sendmail import *
from convert_to_text import *

global capture, rec_frame, grey, switch, neg, face, rec, out, result, captured_img
capture = 0
grey = 0
switch = 1
# make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass


app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

result = None


def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame
    while True:
        success, frame = camera.read()
        if success:
            if (grey):
                # make frame green
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if (capture):  # capture frame
                capture = 0
                now = datetime.datetime.now()
                p = os.path.sep.join(
                    ['shots', "shot_{}.png".format(str(now).replace(":", ''))])
                cv2.imwrite(p, frame)
                global captured_img
                captured_img=p #save the img as a global variable
                
                ##frame에 사진 찍은거 띄우기 

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/en')
def index_en():
    return render_template('en.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/requests', methods=['POST', 'GET'])  # make responsable buttons
def tasks():
    global switch, camera, result
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture = 1
        elif request.form.get('grey') == 'Grey':
            global grey
            grey = not grey
        elif request.form.get('stop') == 'Stop/Start':  # stop or start the camera
            if (switch == 1):
                switch = 0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch = 1
        elif request.form.get('ok') == 'OK':
            global captured_img
            result = convert_to_text(captured_img)
            print(result)
            return render_template('index.html', email=result[0], title=result[1], text=result[2])
        elif request.form.get('upload') == 'Upload': ###여기 다시 보기!!!!!
            print("upload pushed")
            file = request.files['uploadFile']
            result = convert_to_text(file)
            print(result)
    elif request.method == 'GET':
        return render_template('index.html')
        # return redirect(url_for('tasks'))

    if result is not None:
        return render_template('index.html', email=result[0], title=result[1], text=result[2])
    else:
        return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    # Get the form data from the request object
    recipient = request.form['email']
    subject = request.form['title']
    message = request.form['text']

    # Create a MIME text object with the message
    msg = MIMEText(message)

    # Set the sender and recipient of the email
    msg['From'] = 'bik48154815@gmail.com'
    msg['To'] = recipient
    msg['Subject'] = subject

    # Connect to the SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('bik48154815@gmail.com', 'cknscchqmsgvalch')
        smtp.sendmail('bik48154815@gmail.com', recipient, msg.as_string())

    # Return a response to the client
    return 'Email sent successfully'


if __name__ == '__main__':
    app.run('127.0.0.1', port=4000, debug=True)

camera.release()
cv2.destroyAllWindows()


@app.route('/request', methods=['POST', 'GET'])  # make responsable buttons
def test():
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global yes
            yes = 1
    return render_template('en.html')
# def tasks():
#     global switch, camera, result
#     if request.method == 'POST':
#         if request.form.get('click') == 'Capture':
#             global capture
#             capture = 1
#         elif request.form.get('grey') == 'Grey':
#             global grey
#             grey = not grey
#         elif request.form.get('stop') == 'Stop/Start':  # stop or start the camera
#             if (switch == 1):
#                 switch = 0
#                 camera.release()
#                 cv2.destroyAllWindows()
#             else:
#                 camera = cv2.VideoCapture(0)
#                 switch = 1
#     elif request.method == 'GET':
#         return render_template('index.html')
#         # return redirect(url_for('tasks'))

#     if result is not None:
#         return render_template('index.html', email=result[0], title=result[1], text=result[2])
#     else:
#         return render_template('index.html')
