import PySimpleGUI as sg

class Mastertemplate:
    def __init__(self):
        self.Col1 = sg.Column([[sg.Text('Question'), sg.Input()]])
        self.Col2 = sg.Column(
            [[sg.Text('Ans1'), sg.Input(), sg.Checkbox("")], [sg.Text('Ans2'), sg.Input(), sg.Checkbox("")]])
        self.Col3 = sg.Column([[sg.Text('Ans3'), sg.Input(), sg.Checkbox("")],
                        [sg.Text('Ans4'), sg.Input(), sg.Checkbox("")]])
        self.Col4 = sg.Column([[sg.Button("Next")], [sg.Button("Complete")]])
    def construct(self):
        layout = [[self.Col1], [self.Col2, self.Col3],[self.Col4]]
        return sg.Window('Window', layout)




objct1 = Mastertemplate()
objct1.construct().read()



