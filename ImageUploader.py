# LOADING MENU
import PySimpleGUI as sg
import io
import os
import shutil
from pathlib import Path
from PIL import Image

'''
23/5/21
This widget: 

Picks any file which is a PNG (can change this easily to have all Image Files such as JPEGs)
and converts the data back into the image and displays undeneath, the input fill dissapears
there will have to be a log of these files and the corresponding question they go with for example
you may make a quiz that doesn't have an image every question and obviously not implemented into the 
Quiz Gui.

Added a function (the copy line) which also adds the image to the image folder in the master folder. Makes it easier to 
share files between computers this way. I.e the loader would load up the image from the image folder instead of 
other computer files. 
'''



def image_open(image_name, window):
    image = Image.open(image_name)
    bio = io.BytesIO()
    image.thumbnail((400, 400))
    image.save(bio, format="PNG" or "JPEG")
    bio_info = bio.getvalue()
    window["IMAGE"].update(data=bio_info)
    return image_name

def choose_img():
    master_layout = [[sg.Input(key="-IMGINP-"), sg.FileBrowse("Browse"), sg.OK(key="OK")],
                     [sg.Image(key="IMAGE")], [sg.Button("DEL")]]

    window = sg.Window("", master_layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        elif event == "OK":
            check = False
            filename = values["-IMGINP-"]
            if os.path.exists(filename):
                save_name = os.path.basename(os.path.normpath(filename))
                shutil.copy(filename, "\QuizItems\.Image")
                image_open(f"C:/QuizItems/.Image/{save_name}", window)
                window["-IMGINP-"].update("")
            else:
                save_name = None

        elif event == "DEL":
            check = True
            window["IMAGE"].update("")
            try:
                file_path = f"/QuizItems/.Image/{Path(filename).stem}.png"
                os.remove(file_path)
                check = False
            except check == False:
                pass
        else:
            save_name = None
    window.close()
    return save_name

