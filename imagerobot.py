#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from google_images_download import google_images_download
from PIL import Image

class ImageRobot():

    def __init__(self, project_directory):
        self.response = google_images_download.googleimagesdownload()
        self.download_directory = project_directory + 'images\\'

    def get_image(self, keywords, master_key):
        keywords = " ".join(keywords) + " " + master_key
        keywords = str(keywords.encode('ISO-8859-1', errors='ignore').decode('utf-8', errors='ignore'))

        arguments = {"keywords" : keywords, "limit" : 1, "print_urls" : True,
                "no_directory" : True, "size" : "large",
                "output_directory" : self.download_directory}

        print(arguments)
        print(keywords)

        return self.response.download(arguments)[0][keywords]

    def rename_files(self, files):
        new_files_list = []
        for i in range(len(files)):
            try:
                new_name = "{0}\\img{1}.jpg".format(self.download_directory, i)
                os.rename(files[i], new_name)
                new_files_list.append(new_name)
            except:
                continue

        return new_files_list

    def convert_to_jpg(self, files):
        for f in files:
            img = Image.open(f)
            rgb_img = img.convert("RGB")
            rgb_img.save(f)

    def resize(self, files):
        width = 1000
        height = 800
        
        for f in files:
            img = Image.open(f)
            new_img = img.resize((width, height), Image.ANTIALIAS)
            new_img.save(f)
