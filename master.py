#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys
import nltk
import time
from shutil import copyfile
from imagerobot import ImageRobot
from searchrobot import SearchRobot
from videorobot import VideoRobot
from uploadrobot import UploadRobot
from urllib.error import HTTPError
import cv2
import numpy as np

def make_project_directory(search_term):
    try:
        search_term = search_term.replace(" ", "_")
        print(os.path.expanduser('~')+ "\\{}".format(search_term))
        directory_path = os.path.expanduser("~") + "\\{}".format(search_term)

        i = 1
        while True:
            s = directory_path + str(i)
            if os.path.exists(s) and os.path.isdir(s):
                i += 1
                continue
            break

        directory_path += str(i)

        print(directory_path)
        
        os.mkdir(directory_path)
        os.mkdir(directory_path + '\\music\\')
        os.mkdir(directory_path + '\\fonts\\')

        for file in os.listdir('fonts'):
            copyfile(f"fonts\\{file}", f"{directory_path}\\fonts\\{file}")
    
        copyfile('music.ogg', f'{directory_path}\\music\\song.ogg')
        
        return directory_path + '\\'
    
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            print("Creation of the project directory failed.")
            sys.exit(1)

        print("Other error")
    pass

def first(array):
    try:
        return array[0]
    except:
        return array

def init():
    while True:
        try:
            main()
            break
        except:
            main()

def main():
    search_term = input("Wikipedia search term: ")
    if len(search_term) == 0:
        print("Please enter a search term.")
        sys.exit(1)

    print("Avaiable prefixes:\n1. What is\n2. Who is\n3. The history of\n4. Learn more about")
    prefixes = ["What is", "Who is", "The history of", "Learn more about"]
    prefix = input("Prefix: ")
    if not prefix in "1234":
        print("Please enter a prefix.")
        sys.exit(1)

    project_directory = make_project_directory(search_term)
    prefix = prefixes[int(prefix) - 1]

    print("[*] Starting search robot...")
    search_robot = SearchRobot()
    search_result = search_robot.search(search_term)
    keywords_list = search_robot.get_keywords(search_result)
    for i in range(len(search_result)):
        print("[*] Sentence {0}: {1}".format(i + 1, search_result[i]))
        print("[*] Keywords: {0}\n".format(keywords_list[i]))

    print("[*] Starting image robot...")
    image_robot = ImageRobot(project_directory)
    images_list = []
    print(keywords_list)
    for keywords in keywords_list:
        print('here')
        get_img = image_robot.get_image(keywords, search_term)

        print(get_img)
        img = first(get_img)
        images_list.append(img)
        
        print("[*] Image saved in: " + str(img))

    print(images_list)
    print("[*] Renaming images...")
    images_list = image_robot.rename_files(images_list)

    print("[*] Converting images to JPG...")
    image_robot.convert_to_jpg(images_list)

    print("[*] Resizing images...")
    image_robot.resize(images_list)

    print("[*] Starting video robot...")
    video_robot = VideoRobot(search_result, project_directory, f'{project_directory}\\saida.mkv')
    video_robot.add_subtitles()
    video_robot.make_video()
    video_robot.add_music()

    print(search_result)
    print("[*] Backup files saved in: " + project_directory)

    option = input("Do you want to upload this video? (y/n)")

    if option in 'YySs':  
        print("[*] Starting upload robot...")
        upload_robot = UploadRobot()

        title = prefix + " " + search_term
        description = "\n\n".join(search_result)
        keywords = []

        for i in keywords_list:
            keywords += i

        keywords = ",".join(keywords)

        args = argparse.Namespace(
            auth_host_name="localhost",
            auth_host_port=[8080, 8090],
            category="27",
            description=description,
            file="{}/saida.mkv".format(project_directory),
            keywords=keywords,
            logging_level="ERROR",
            noauth_local_webserver=False,
            privacy_status="public",
            title=title)

        try:
            youtube = upload_robot.get_authenticated_service(args)

            print("[*] Uploading video...")
            try:
                upload_robot.initialize_upload(youtube, args)
            except HTTPError as e:
                error("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
        except:
            print("Error: Reached video upload limit per day.")

    else:
        play_video(os.path.join(project_directory, "saida.mkv"))

def error(string):
    print(string)
    print("Restarting program... in")
    time.sleep(1)
    print('1...')
    time.sleep(2)
    
    print('2...')
    time.sleep(2)
    print('3...')
    time.sleep(3)
    
    sys.stdout.flush()

    restart()
    input()
    exit(1)
    
def play_video(file):
    print(file)

    os.startfile(file)

def beauty_title():
    return\
'''
   _____ _       __       __  _     
  / ___/(_)___  / /____  / /_(_)____
  \__ \/ / __ \/ __/ _ \/ __/ / ___/
 ___/ / / / / / /_/  __/ /_/ / /__  
/____/_/_/ /_/\__/\___/\__/_/\___/  
                                    
'''

if __name__ == "__main__":
    os.system('color b1')
    print(beauty_title())
    print("Descricao: Robos como ajudantes de docentes na elaboracao de materiais audiovisuais")
    print("Autores: Boanerges Rodrigues & Gabriel Albuquerque\n")
    #nltk.download('punkt')
    main()
