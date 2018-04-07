#!/usr/bin/python3.6
#-*- coding: utf-8 -*-

import os
import glob
import exifread
import subprocess
import datetime
import locale

import namesAndPaths

locale.setlocale(locale.LC_TIME, "ca_ES.utf8")

# identificar tots els directoris amb fotos

for folder in sorted(os.walk('.')):

    print('Working on {}'.format(folder[0]))

    # find all media elements
    mediaList = []

    # search for pictures
    for fotoExt in namesAndPaths.FOTOS:
        # if there are uppercase names, transform them to lowercase
        tmp = glob.glob(os.path.join(folder[0], fotoExt.upper()))
        for nameUppercase in tmp:
            nameLowercase = os.path.basename(nameUppercase).lower()
            nameLowercase = os.path.join(os.path.dirname(nameUppercase), nameLowercase)
            if not os.path.isfile(nameLowercase):
                os.rename(nameUppercase, nameLowercase)
            else:
                print("strange error")
                print("stopping")
                quit()

        # add the files to the list
        tmp = glob.glob(os.path.join(folder[0], fotoExt))
        mediaList.extend(tmp)



    # search for videos
    for video_ext in namesAndPaths.VIDEOS:
        # if there are uppercase names, transform them to lowercase
        tmp = glob.glob(os.path.join(folder[0], video_ext.upper()))
        for nameUppercase in tmp:
            nameLowercase = os.path.basename(nameUppercase).lower()
            nameLowercase = os.path.join(
                    os.path.dirname(
                        nameUppercase),
                    nameLowercase)
            if not os.path.isfile(nameLowercase):
                os.rename(nameUppercase, nameLowercase)
            else:
                print("strange error")
                print("stopping")
                quit()

        # add the files to the list
        tmp = glob.glob(os.path.join(folder[0], video_ext))
        mediaList.extend(tmp)



    # the list with media elements has been created.
    # now create the thumbnails
    for i, mediaFileName in enumerate(mediaList):
        # images need a 'miniatura' file
        # only create the file if it does not exist
        if namesAndPaths.isPhoto(mediaFileName):
            miniaturaFileName = mediaFileName + namesAndPaths.MINIATURA
            if not os.path.isfile(miniaturaFileName):
                # file must be renamed
                with open(mediaFileName, 'rb') as f:
                    try:
                        # Return Exif tags
                        tags = exifread.process_file(f, details=False, stop_tag='Image DateTime')
                        imageDateTime = tags['Image DateTime']
                        imageDate, imageTime = str(imageDateTime).split(' ')
                        year, month, day = imageDate.split(':')
                        hour, minute, second = imageTime.split(':')

                    except:
                        hour = '00'
                        minute = '00'
                        second = '00'
                        year = '1900'
                        day = '01'
                        month = '01'

                number = namesAndPaths.START_NUMBER
#            print(mediaFileName)
                extension = os.path.splitext(mediaFileName)[1]
                while(True):
                    new_name = os.path.join(
                            folder[0],
                            '{}_{}_{}__{}_{}_{}__{}{}'.format(
                                year, month, day,
                                hour, minute, second,
                                number, extension)
                            )
                    if not os.path.isfile(new_name):
                        break
                    number = number + 1
#            print("renaming {} to {}".format(mediaFileName, new_name))
                os.rename(mediaFileName, new_name)
                mediaFileName = new_name
                mediaList[i] = new_name
                miniaturaFileName = mediaFileName + namesAndPaths.MINIATURA
                # create miniatura
                command = [
                        'convert', 
                        '-quality', '60', 
                        '-auto-orient',
                        '-geometry', '320',
                        mediaFileName,
                        miniaturaFileName
                        ]
#            print(" ".join(command))
                subprocess.call(command)

        # video files
        if namesAndPaths.isVideo(mediaFileName):
# ------------------- REMOVED --------------------------------
# FOTOGRAMA files are no longer created, because a small-size video (webm) is
# created
#            # create a thumnail image
#            fotogramaFileName = mediaFileName + namesAndPaths.FOTOGRAMA
#            if not os.path.isfile(fotogramaFileName):
#                # fotograma file must be created
#                command = [
#                        'ffmpeg', 
#                        '-i', mediaFileName,
#                        '-ss', '0',
#                        '-vframes', '1',
#                        '-vf', 'scale=320:-1',
#                        fotogramaFileName + '.jpg'
#                        ]
#                subprocess.call(command)
#                os.rename(fotogramaFileName + '.jpg', fotogramaFileName)
# ------------------- REMOVED --------------------------------

            # create a webm file for streaming
            webmFileName = mediaFileName + namesAndPaths.WEBM
            if not os.path.isfile(webmFileName):
                # fotograma file must be created
                command = [
                        'ffmpeg', 
                        '-i', mediaFileName,
                        '-c:v', 'libvpx-vp9',
                        '-minrate', '100k',
                        '-b:v', '800k',
                        '-maxrate', '2500k',
                        '-deadline', 'good',
                        webmFileName
                        ]
                subprocess.call(command)
