#!/usr/bin/python3.6
#-*- coding: utf-8 -*-

import os

FOTOS = ['*.jpg', '*.jpeg', '*.png']
VIDEOS = ['*.avi', '*.mov', '*.mts', '*.mp4']
WEBM = '.webm'
MINIATURA = '.miniatura'
#FOTOGRAMA = '.fotograma'
START_NUMBER = 10000
TIME_SORT_FILE = 'latestPicture.txt'
HTML_FILE = "index.html"

def isPhoto(fileName):
    for fotoExt in FOTOS:
        name, extension = os.path.splitext(fileName)
        if extension == fotoExt[1:]:
            return True

    return False

def isVideo(fileName):
    for video_ext in VIDEOS:
        name, extension = os.path.splitext(fileName)
        if extension == video_ext[1:]:
            return True

    return False
