import PySimpleGUI as sg

quiz_lay = [
    [sg.Text("Quick Quiz Maker")],
    [sg.Text("Question: "), sg.InputText()],
    [sg.Text("Answer 1: "), sg.InputText(), sg.Text("Answer 2: "), sg.InputText()],
    [sg.Text("Answer 3: "), sg.InputText(),sg.Text("Answer 4: "), sg.InputText()],
    [sg.Button("Complete")],
    [sg.Button("Restart"), sg.Button("Next Question")],
    [sg.Button("End")]
]

window = sg.Window('Quiz Generator', quiz_lay)

while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED or event == 'End':
        break
    print("You entered", values[0])

window.close()