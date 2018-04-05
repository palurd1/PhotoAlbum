#!/usr/bin/python
# This Python file uses the following encoding: utf-8

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
    photoList = []
    tmp = os.path.join(folder[0], '*' + namesAndPaths.MINIATURA)
    photoList.extend(glob.glob(tmp))

    videoList = []
    tmp = os.path.join(folder[0], '*' + namesAndPaths.WEBM)
    videoList.extend(glob.glob(tmp))

    
    if not photoList == [] or not videoList == []:
        # there are media files in this folder
        # the HTML has to be created
        with open(os.path.join(folder[0], namesAndPaths.HTML_FILE), 'w') as f:
            f.write(
"""<!DOCTYPE HTML>
<html lang="ca"> 
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="content-type">
        <meta http-equiv="Refresh" content="86400">
        <link rel="stylesheet" href="/home/albert/public_html/fitxers/estils.css">
        <title>
            {title}
        </title>
    </head>

    <body alink="#fffa00" vlink="#ffb700" link="#ff0000" text="#f7f2ce" bgcolor="#000000" style="font-family:verdana">
        <center>

            <h1>
                {title}
            </h1>

            Feu click sobre una foto per ampliar-la i veure-la en alta
            resolució. Contingut autogenerat per un script de python.
""".format(title=os.path.basename(folder[0])))

            if not photoList == []:
                f.write("""
                <h2>
                    Fotos
                </h2>
""")

                # get the picture details from its name
                for item in sorted(photoList):
                    image_name = os.path.join('.', os.path.basename(item)[:-len(namesAndPaths.MINIATURA)])
                    year = int(os.path.basename(item)[0:4])
                    month = int(os.path.basename(item)[5:7])
                    day = int(os.path.basename(item)[8:10])
                    hour = int(os.path.basename(item)[12:14])  
                    minute = int(os.path.basename(item)[15:17])  
                    second = int(os.path.basename(item)[18:20]) 
                    image_timestamp = datetime.datetime.combine(datetime.date(year,month,day), datetime.time(hour, minute, second))
                    image_timestamp = image_timestamp.strftime('%A %d de %B de %Y, %X')
                    f.write("""
                <a href="{image}" rel="fotos" title = "{image_timestamp}">
                    <img src="{miniatura}" width="31%" border="\#000000" alt={image}>
                </a>""".format(
                    image=image_name,
                    image_timestamp = image_timestamp,
                    miniatura = image_name + namesAndPaths.MINIATURA
                    ))

            if not videoList == []:
                f.write("""
                <h2>
                    Videos
                </h2>
""")

                for item in sorted(videoList):
                    video_name = os.path.join('.', os.path.basename(item)[:-len(namesAndPaths.FOTOGRAMA)])

                    f.write("""
                <video width="30%" controls>
                    <source src="{video}" width="31%" type="video/webm">
                    alburru
                </video>
                """.format(video=video_name))

#                    f.write("""
#                <object width="30%" type="video/quicktime" data="{video}">
#                    <param name="controller" value="true" />
#                    <param name="autoplay" value="false" />
#                </object>
#                """.format(video=video_name))

#                    f.write("""
#                <a href="{video}" rel="videos" title = "{video}">
#                    <img src="{fotograma}" width="31%" border="\#000000" alt={video}>
#                </a>""".format(
#                        video = video_name,
#                        fotograma = video_name + namesAndPaths.FOTOGRAMA
#                        ))

            f.write("""

            <hr>
            <div style="text-align:right;color: \#ffffff;">
                <a href="http://palot.dyndns.org/~albert/tots_toros" style="color: \#fabada">
                    Tornar
                </a>
                <br>
                <i>
                    Darrera modificació: {day} a les {time}.
                </i>
            </div>
        </body>
    </html>""".format(
        day=datetime.datetime.now().strftime('%A %d de %B de %Y'),
        time=datetime.datetime.now().strftime('%X')))

