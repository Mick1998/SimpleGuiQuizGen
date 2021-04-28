import PySimpleGUI as sg


class Mastertemplate:
    #Basic Menu Layout
    #Basic Question Jumping Layout
    '''
    attributes are constructed for window layout
    '''
    def __init__(self):
        self.__Col1 = sg.Column([[sg.Text('Question'), sg.Input(key="-QIN-")]])
        self.__Col2 = sg.Column(
            [[sg.Text('Ans1'), sg.Input(key="-A1-"), sg.Checkbox("")],
             [sg.Text('Ans2'), sg.Input(key="-A2-"), sg.Checkbox("")]])
        self.__Col3 = sg.Column([[sg.Text('Ans3'), sg.Input(key="-A3-"), sg.Checkbox("")],
                                 [sg.Text('Ans4'), sg.Input(key="-A4-"), sg.Checkbox("")]])
        self.__Col4 = sg.Column([[sg.Button("Next")], [sg.Button("Save"), sg.Button("Edit")]])





    def construct(self):
        '''
        Construct Window
        '''
        layout = [[self.__Col1], [self.__Col2, self.__Col3], [self.__Col4]]
        return sg.Window('Window', layout)








class Input(Mastertemplate):

    def __init__(self):
        super(Input, self).__init__()

    def UseInputVals(self):

        objct1 = Mastertemplate().construct()
        tempList = []
        check = 0
        while True:
            event, values = objct1.read()

            if event == sg.WIN_CLOSED:
                if check == 0:
                    popup = sg.popup_yes_no("You haven't Saved File. Do you want to Save?")
                    if popup == "Yes":
                        file_one = open("Example.txt", "w+")
                        file_one.writelines(tempList)
                        file_one.close()
                        break
                    else:
                        break
            else:
                cor_ans = list(filter(lambda x: x[1] is True, values.items()))
                num = [a[0]for a in cor_ans]
                var = "%s:%s:%s\n" % (num, values["-QIN-"], (values["-A1-"], values["-A2-"], values["-A3-"], values["-A4-"]))

                if event == "Next":
                    check = 0
                    tempList.append(var)
                    print(tempList)

                # elif event == "Edit":
                #     #something about buttons from Jakes Class here = Jed
                #     Input.UseInputVals(self)
                #     tempList[Jed].replace(tempList[Jed],var)

                elif event == "Save":
                    check += 1
                    file_one = open("Example.txt", "w+")
                    file_one.writelines(tempList)
                    file_one.close()





f = Input()
f.UseInputVals()


class Qreader(Mastertemplate):
    """
    This class allows the startup of a loaded game, and integrates
    the question_select method from its parent class Mastertemplate to jump questions
    It allows the player to run through the questions and tick the correct box without letting
    said player edit questions or answers.

    Since the example input question has a : at the start when it is split it makes an extra space
    at the start of the list, this may be changed at some point and if so index numbers need to be
    changed to reflect that.
    """

    def __init__(self):
        Mastertemplate.__init__(self)

    def Q_process(self):
        """
        This method returns the selected questions as a list containing lists of answers,
        questions and correct answers for each questions
        It props the user to select a file which it then process's to get said list of
        lists

        """
        select_File = sg.PopupGetFile('Please Select File', title="Loader", no_window=True)
        with open(select_File) as questions:
            question_list = questions.readlines()
            question_list = map(lambda x: x.split(':'), question_list)
        return tuple(question_list) #since this is a reader can i have it return a tuple?

    def slide_fill(self, qnum, window, q_list, key_num):
        """
        This method fills in each slide with the appropriate text for the question, ans1, ans2, ans3
        and ans4 slots based on what question the user is on, which is passed to the method through
        the qnum parameter.
        It intakes the list containing all answers and questions and then selects the appropriate
        question(which also contain answers) by indexing with qnum since the list is in the order
        the questions are. Then each element is updated as appropriate from the selected question.

        The keys for each answer are numerical, so ans1 has the key -Ans1-, ans2 has the key -Ans2-
        and so on. In order to generate the keys the method ranges from 1 to the key_num , which is
        the length of q_list generating a list of keys to use to access elements.

        This does mean every time the slide fill is called it repeatedly generates the keys again, so
        maybe better to do this outside the method and pass it as a parameter?
        """
        keys = ['-Ans%s-'%(val) for val in range(1, key_num+1)]
        ans_list = q_list[qnum - 1]
        window['-QIN-'].update(ans_list[2], disabled=True)
        for num, i in enumerate(keys, 3):
            window[i].update(ans_list[num], disabled=True)
        # map(lambda x: window[x].update('hello', disabled=True), keys) #messed around with trying to use map


    def start_up(self):
        """
        This is the main method of the class and is the one called to generate the actual GUI,
        it forms together the base slide format which it inherits the method for from its parent
        class. It then combines this with a question selector from the Maststertemplate class
        method self.question_select() all into one window.

        It calls its own Q_process method to generate the list of questions(and their answers!) in
        order to build the self.question_select() based on the question bank selected.

        Then in a while loop it fills the slide based on what the current qnum variable value is
        if the user presses next or selects a question from the question selector the qnum is set
        to the question number the user has moved to and passes to the next iteration.

        Once this pass has happened while loop resets to the top and redoes the slide_fill method
        with the new qnum.

        """
        layout = self.construct()
        q_list = self.Q_process()
        select_column = self.question_select(q_list)
        layout[0].append(sg.Frame('Question Select', [[select_column]]))
        window = sg.Window('Jake\'s Quiz', layout, finalize=True)
        key_num = len(q_list)
        q_num = 1
        while True:
            #I dislike all the conditionals i had to use here
            self.slide_fill(q_num, window, q_list, key_num)
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break

            elif q_num >= key_num:
                window['-Next-'].update(disabled=True)
                sg.Popup('That was the last question!')
                q_num = 1
                pass

            elif event == '-Next-':
                q_num += 1
                pass

            else:
                '''
                instead of filtering out the '-' maybe just may the keys not have '-'?
                '''
                key_filter = list(filter(lambda x: True if x != '-' else False, event))
                q_num = list(map(int, key_filter))[0]
                pass

            if q_num < key_num:
                window['-Next-'].update(disabled=False)
        return 'success'


#need a function which deletes list as to not mess up the list function when you save and then edit and save? - Maybe



