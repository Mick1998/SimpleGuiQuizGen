import PySimpleGUI as sg

class Mastertemplate:
    # Basic Menu Layout
    # Basic Question Jumping Layout
    '''
    attributes are constructed for window layout
    '''

    def __init__(self):
        self.question = [[sg.Text('Question', key='QTxt'), sg.Input(key='-QIN-')]]
        self.answers = [[sg.Text('Ans1', key='Ans1Txt'), sg.Input(key='-Ans1-'), sg.Checkbox("")],
                        [sg.Text('Ans2', key='Ans2Txt'), sg.Input(key='-Ans2-'), sg.Checkbox("")]]
        self.nxt_ans = [[sg.Text('Ans3', key='Ans3Txt'), sg.Input(key='-Ans3-'), sg.Checkbox("")],
                        [sg.Text('Ans4', key='Ans4Txt'), sg.Input(key='-Ans4-'), sg.Checkbox("")]]
        self.move = [[sg.Button("Next", key='-Next-')], [sg.Button("Complete")]]

    def construct(self):
        layout = [[sg.Frame('The slide', [[sg.Column(self.question)],
                                          [sg.Column(self.answers), sg.Column(self.nxt_ans)],
                                          [sg.Column(self.move)]])]]
        return layout

    def question_select(self, q_amount):  # do i need to get rid of the self parameter here?
        buttons = [[sg.Button('%s) %s' % (num, val[2]), key='-%s-' % (num))] for num, val in enumerate(q_amount, 1)]
        return sg.Column(buttons, key='-jump-')


class Input(Mastertemplate):

    def __init__(self):
        super(Input, self).__init__()

    def UseInputVals(self):
        layout = self.construct()
        TempList = []
        select_keys = [f'-Ans{val}-' for val in range(1, 5)] #temporarily hardcoded
        layout[0].append(sg.Frame('Question Selection', [[self.question_select(TempList)]]))
        '''
        The immediately above adds the question selector frame 
        '''
        window = sg.Window('Editor', layout, finalize=True)
        # events, values = window.read(close=False)
        # select_keys = [val for val in values.keys() if type(val) != int]
        # window.close()
        '''
        Obvs since the keys stay the same we could hard code the list, but i thought this might be better if we end up 
        having variable numbers of answers
        
        For some reason the commented out method of read the keys from the window directly broke the rest of the 
        code as since it closed the window, starting the loop meant that the sg.WIN_CLOSED condition was fuilled in
        the if statement
        '''
        check = 0

        while True:
            event, values = window.read()

            if event == sg.WIN_CLOSED and check == 0:
                popup = sg.popup_yes_no("You haven't Saved File. Do you want to Save?")
                if popup == "Yes":
                    file_one = open("Example.txt", "w+")
                    file_one.writelines(TempList)
                    file_one.close()
                    break
                else:
                    break
            else:
                try:
                    cor_ans = list(filter(lambda x: x[1] is True, values.items()))[0][0]
                except IndexError:
                    cor_ans = 1
                num = cor_ans
                var = "%s:%s:%s\n" % (
                    num, values["-QIN-"], (values["-Ans1-"], values["-Ans2-"], values["-Ans3-"], values["-Ans4-"]))

                if event == "-Next-":
                    check = 0
                    TempList.append(var)
                    window['-QIN-'].update('')
                    for key in select_keys: #Couldn't figure out how to turn this into a list comprehension
                        window[key].update('')
                    new_instance = Mastertemplate()
                    new_layout = new_instance.construct()
                    new_layout[0].append(sg.Frame('Question Selection', [[self.question_select(TempList)]]))
                    window = sg.Window('Editor', new_layout, finalize=True)
                    '''
                    I had to create a new instance of the mastertemplate class so that it has new memory address
                    for each element and can therefore be reused in the PySimpleGui window.
                    
                    This does mean everytime next is pressed not only do we have to generate a new window but also
                    new instances of the Mastertemplate class, I think this is probably inefficient.
                    
                    One workaround could be to get the user to select the number of questions they want at the start
                    then we can have the buttons invisible until the matching slide number to the button number has 
                    been filled. Then we only need to generate new instances and window layouts if the user decides
                    to add more than they originally wanted instead of everytime next is hit.  
                    '''
                    pass

                # elif event == "Edit":
                #     #something about buttons from Jakes Class here = Jed
                #     Input.UseInputVals(self)
                #     TempList[Jed].replace(TempList[Jed],var)

                elif event == "Save":
                    check = 1
                    file_one = open("Example.txt", "w+")
                    file_one.writelines(TempList)
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

    def __init__(self):  # I think you don't need to do this, is it for pep8?
        Mastertemplate.__init__(self)

    def Q_process(self):
        """
        This method returns the selected questions as a list containing lists of answers,
        questions and correct answers for each questions
        It props the user to select a file which it then process's to get said list of
        lists

        """
        select_file = sg.PopupGetFile('Please Select File', title="Loader", no_window=True)
        with open(select_file) as questions:
            question_list = questions.readlines()
            question_list = map(lambda x: x.split(':'), question_list)
        return tuple(question_list)  # since this is a reader can i have it return a tuple?

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
        keys = ['-Ans%s-' % (val) for val in range(1, key_num + 1)]
        ans_list = q_list[qnum - 1]
        window['-QIN-'].update(ans_list[2], disabled=True)
        list(map(lambda key_index: window[key_index[1]].update(ans_list[key_index[0]], disabled=True),
                 enumerate(keys, 3)))
        # For some reason you have to cast the map object as a list to make it work unsure why, also unusure
        # If this is any faster than a normal loop

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
            # I dislike all the conditionals i had to use here
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
                instead of filtering out the '-' maybe just make the keys not have '-'?
                '''
                key_filter = list(filter(lambda x: True if x != '-' else False, event))
                q_num = list(map(int, key_filter))[0]
                pass

            if q_num < key_num:
                window['-Next-'].update(disabled=False)

#
# read = Qreader()
# read.start_up()
