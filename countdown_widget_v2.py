# LOADING MENU
import PySimpleGUI as sg
import time

text_element = [sg.Text('30', size=(8, 2), font=('Helvetica', 20),
                        justification='center', key='-timer-')]


def countdown(time_num, window):
    while time_num >= 0:
        window.refresh()
        window['-timer-'].update(time_num)
        time_num -= 1
        time.sleep(1)
