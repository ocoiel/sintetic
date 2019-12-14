import cv2
import numpy as np
import os
import textwrap
import moviepy.editor as mvpy
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from os.path import isfile, join

class VideoRobot:
    def __init__(self, sentences, pathIn, pathOut):
        self.pathIn  = pathIn
        self.pathOut = pathOut
        self.fps = 0.08

        self.sentences = sentences

    # -- getters --
    
    def get_path(self, directory):
        return self.pathIn + directory + '\\'

    def get_files(self, path):
        files = [file for file in os.listdir(path) if isfile(join(path, file))]

        # 'img0.jpg'..'imgN.jpg'
        files.sort(key = lambda x: x[4:-4])

        return files

    def get_font(self, name):
        pathFonts = self.get_path('fonts')

        listdir = os.listdir(pathFonts)
        fonts = []

        for file in listdir:
            fullPath = pathFonts + file
            fonts.append(file)
            

        if len(fonts) == 0:
            return None
        
        my_fonts = sorted([join(pathFonts, font) for font in fonts if (name in font)])

        if len(my_fonts) == 0:
            return fonts[0]


        return my_fonts[0]

    # -- utility --

    def wrap_sentence(self, sentence):
        return textwrap.wrap(sentence, width = 35)
    
    def add_subtitles(self):
        pathImages = self.get_path('images')
        
        sentences = self.sentences
        files = self.get_files(pathImages)
        length = len(files)

        for i in range(0, length):
            file = files[i]
            sentence = sentences[i]
            
            filename = pathImages + file
            
            img = Image.open(join(pathImages, file))
            draw = ImageDraw.Draw(img)

            font_file = self.get_font("arial")
            font = ImageFont.truetype(font_file, 40)
            width, height = position = (40, 100)
            txt_color = 'white'
            outl_color = 'black'
            outl_amount = 3

            sentence = sentences[i]
            lines = self.wrap_sentence(sentence)

            for line in lines:
                line = line.strip()

                self.outline(draw, (width, height), line, font, txt_color, outl_color, outl_amount)

                w, h = font.getsize(line)

                height += (h + outl_amount)

            img.save(filename)

        print('subtitles added!')

    def outline(self, draw, size, line, font, txt_color, outl_color, outl_amount):
        (x, y) = size

        for adj in range(outl_amount):
            #move right
            draw.text((x-adj, y), line, font=font, fill=outl_color)
            #move left
            draw.text((x+adj, y), line, font=font, fill=outl_color)
            #move up
            draw.text((x, y+adj), line, font=font, fill=outl_color)
            #move down
            draw.text((x, y-adj), line, font=font, fill=outl_color)
            #diagnal left up
            draw.text((x-adj, y+adj), line, font=font, fill=outl_color)
            #diagnal right up
            draw.text((x+adj, y+adj), line, font=font, fill=outl_color)
            #diagnal left down
            draw.text((x-adj, y-adj), line, font=font, fill=outl_color)
            #diagnal right down
            draw.text((x+adj, y-adj), line, font=font, fill=outl_color)

            draw.text((x,y), line, font=font, fill=txt_color)

    def make_video(self):
        pathImages = self.get_path('images')
        
        pathOut = self.pathOut
        fps = self.fps
        
        frames = []
        files = self.get_files(pathImages)
        size = 0

        for i in range(len(files)):
            filename = pathImages + files[i]
            print(f'filename: {filename}')

            img = cv2.imread(filename)
            height, width, layers = img.shape
            size = (width, height)

            frames.append(img)

        out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

        for i in range(len(frames)):
            out.write(frames[i])

        out.release()

    def add_music(self):
        pathOut = self.pathOut
        song_path = self.get_path('music')
        
        clip = mvpy.VideoFileClip(pathOut)
        print(join(song_path, 'song.ogg'))
        song = mvpy.AudioFileClip(join(song_path, 'song.ogg')).set_duration(clip.duration)

        final_video = clip.set_audio(song)

        final_video.write_videofile(self.pathOut,fps=0.08,codec='mpeg4', audio_codec='libvorbis')
        print('done')

def main():
    vr = VideoRobot(sentences, 'C:\\Users\\Administrador\\', 'C:\\Users\\Administrador\\saida.mkv')

    vr.add_subtitles()
    vr.make_video()
    vr.add_music()


if __name__ == '__main__':
    main()
