import PySimpleGUI as sg


sg.theme_background_color('#E4F3F5')
#
# [Psg.FileBrowse('Browse'), Psg.Button('Submit', key='-OPEN-')]




def CreateNewFile():
    '''
    Function to allow user to make a new file, can make this same colour as the rest at another time as well, this then
    opens the NewGame Function
    '''
    create_layout = [[sg.Text("Create New File Name"),sg.Input(key="-FILNAM-"),sg.Text(".txt")],
                     [sg.Button("Submit")]]

    cnf_window = sg.Window("Create New File",create_layout,finalize=True)

    while True:
        event, values = cnf_window.read()
        if event == sg.WIN_CLOSED:
            StartMenu()
            break
        elif event == "Submit":
            new_file = open("{0}.txt".format(values["-FILNAM-"]), "a")
            NewGame(new_file)
            return new_file




        cnf_window.close()



def NewGame(file):
    list_test  = []
    # count = 0





    '''
    Mucked around with a lot of parameters but have made a really simple stripped back input window we want
    I also don't want there to be two seperate frames as you can see when you click on them. Non functional yet.
    Just allows you to open window.
    Now writes to file Question and Answers
    '''
    frames_q = [[sg.Frame("Question",[[sg.Text("Input Question:",text_color='Black',background_color=sg.theme_background_color())
                                          ,sg.Input(key="-QIN-")]],title_color='Black',background_color=sg.theme_background_color())]]
    frames_ans1 = [[sg.Frame("Answers",[[sg.Text("Input Answer 1:",text_color='Black',background_color=sg.theme_background_color()),
                                         sg.Input(key="A1"),sg.Checkbox('Correct?',text_color='Black', default=False,key="-Ans1-",background_color=sg.theme_background_color()),
                                         sg.Text("Input Answer 2:",text_color='Black',background_color=sg.theme_background_color()),sg.Input(key="A2"),
                                         sg.Checkbox("Correct?",text_color='Black',default=False,key= "-Ans2-",background_color=sg.theme_background_color())]],background_color=sg.theme_background_color(),title_color='Black')],
                  [sg.Frame("",[[sg.Text("Input Answer 3:",text_color='Black',background_color=sg.theme_background_color()),sg.Input(key="A3"),
                                 sg.Checkbox('Correct?',text_color='Black', default=False,key="-Ans3-",
                                             background_color=sg.theme_background_color()),sg.Text("Input Answer 4:",text_color='Black',background_color=sg.theme_background_color()),sg.Input(key="A4"),
                                 sg.Checkbox("Correct?",text_color='Black',default=False,key= "-Ans4-",background_color=sg.theme_background_color())]],background_color=sg.theme_background_color())]]

    #editor_frame = add_editor(count)
    layout = [[sg.Column(frames_q)],#[sg.Column(editor_frame)],
             [sg.Column(frames_ans1)],
              [sg.Input("Type Question Number Here", key="-QNUM-")],
              [sg.Button("Submit"),sg.Button("Next")],[sg.Button("Complete"),sg.Button("Go Back")],
              [sg.Text(" When done Press Complete, Press Submit before Next to not lose Questions", key= "-TXTFIELD-")]]

    ng_window = sg.Window('New Quiz',layout,finalize=True,background_color=(sg.theme_background_color()))
    while True:
        event, values = ng_window.read()
        if event == sg.WIN_CLOSED:
            break
        ans = filter(lambda x: type(x[1]) is not None, values.items())

        cor_ans = 'no ans'
        for i in list(ans):
            key = i[0]
            print(i[0])
            if values[i][0] is True:
                cor_ans = i
            else:
                pass


        if event == "Submit":
            #Open Editing Buttons (i.e click on button takes you back to questions)
            evaluated_string = ":" + str(cor_ans) + ":" + values["-QIN-"] + ":" + values["A1"] + ":" + values["A2"]+ ":" + values["A3"] + ":" + values["A4"] +'\n'
            if evaluated_string not in file.readlines():
                file.write(evaluated_string)
            else:
                continue

        elif event == "Next":
            NewGame(file)
        # elif event == "Edit":
        #     information = StringSplitter(file.readlines()[int("-QNUM-")])
        #     information[0] = values["-QIN-"]
        #     information[1] = values["-A1-"]
        #     information[2] = values["-A2-"]
        #     information[3] = values["-A3-"]
        #     information[4] = values["-A4-"]
        #     ng_window[information[0:4]].update(event)


        elif event == "Complete":
            file.close()
            Intermediate_Window(file)
            break

    ng_window.close()


# def add_editor(list_test):
#     return [[sg.Button("Question %d" % num)] for num in enumerate(list_test, 1)]





def StringSplitter(argument):
    f = argument.replace("\n","")
    list_information = f.split(":")



    #print(list_information)
    return list_information



def LoadMenu():
    a = sg.popup_yes_no("Load File",title="Load")
    if a == "Yes":
        select_File = sg.PopupGetFile('Please Select File', title="Loader",no_window=True)

        file1 = open(select_File)
        information = file1.read()

        #print('Function only prints the list_info for now',list_information)
        return StringSplitter(information)
    elif a == "No":
        StartMenu()
    elif a == sg.WIN_CLOSED:
        StartMenu()
    else:
        print("Error.")

def LoadQuiz(file):
    file_load = open(file)
    information = file_load.read()



def Intermediate_Window(file):
    int_layout = [[sg.Text("Would you like to:")],[sg.Button("Start Quiz")],
                  [sg.Button("Load Another Quiz")], sg.Button("Exit")]


    int_window = sg.Window("",int_layout,finalize=True,background_color=sg.theme_background_color())

    while True:
        event,values = int_window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Start Quiz":
            LoadQuiz(file)
        elif event == "Load Another Quiz":
            LoadMenu()

        int_window.close()




def StartMenu():
    '''
    Functional, Obviously the image will not work for you so you can just comment it out for now. And possibly in the
    future we find how to keep the image across every computer (something like a folder of things downloads
    that it can look in when this script is run that holds the image within it?) The commented out Window.Maximize func.
    can be used however, I have not moved things around from 0,0 so not really any point you just get a large screen
    with all the stuffs in the left hand corner. 
    '''
    layout = [[sg.Image(r'D:\PycharmProjects\QUIZgui\Logo.png', background_color=(sg.theme_background_color()))],
              [sg.Button('Load Game')],
              [sg.Button('Create New Game')],
              [sg.Button('Add to Existing Game')]]

    Window = sg.Window('', layout, finalize=True, background_color=(sg.theme_background_color()))
    # Window.Maximize()
    while True:
        event, values = Window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Load Game':
            LoadMenu()
            break
        elif event == "Create New Game":
            CreateNewFile()
            break

    Window.close()

StartMenu()










