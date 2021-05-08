#!/usr/bin/env python
#
# Project: Video Streaming with face recognition
# Author: agametov [at] gmail [dot] com>
# Date: 2016/02/11
# Website: http://www.agametov.ru/
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, Response, make_response, render_template

from camera import VideoCamera, changeState

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/changeFirstButtonState')
def changeFirstButtonState():
    changeState(1488)
    return Response()


@app.route('/changeSecondButtonState')
def changeSecondButtonState():
    changeState(0)
    return Response()


@app.route('/changeCancelButtonState')
def changeCancelButtonState():
    changeState(1)
    return Response()


@app.route('/changeScreenshotButtonState')
def changeScreenshotButtonState():
    image_binary = VideoCamera().get_frame()
    response = make_response(image_binary)

    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % "screenshot")
    return response
    # return Response()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
