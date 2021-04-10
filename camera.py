#!/usr/bin/env python
import cv2
import mpy as mpy
from moviepy.editor import *
import pafy as pafy

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        faces = face_cascade.detectMultiScale(image, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def anonymize_face_simple(self, image, factor=3.0):
        # automatically determine the size of the blurring kernel based
        # on the spatial dimensions of the input image
        #to extract ROI
        (h, w) = image.shape[:2]
        kW = int(w / factor)
        kH = int(h / factor)
        # ensure the width of the kernel is odd
        if kW % 2 == 0:
            kW -= 1
        # ensure the height of the kernel is odd
        if kH % 2 == 0:
            kH -= 1
        # apply a Gaussian blur to the input image using our computed
        # kernel size
        return cv2.GaussianBlur(image, (kW, kH), 0, dst=image)

    def add_audio(self):
        video = pafy.new('https://www.youtube.com/watch?v=jr47YisIsz8&ab_channel=DuaLipa')
        stream = video.getbest(preftype='mp4')

        video = VideoFileClip(stream.url)
        audio = video.audio
        for t, video_frame in video.iter_frames(with_times=True):
            audio_frame = audio.get_frame(t)

