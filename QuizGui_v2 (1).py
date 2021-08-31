'''
Title: QuizGUI v0.1a2
Author: Jake Brooks & Max Carberry
Date: 12 MAY 21
'''
import PySimpleGUI as sg
import ImageUploader as IU
import countdown_widget_v2 as cw
#TODO Blank question field


class Mastertemplate:
    # Basic Menu Layout
    # Basic Question Jumping Layout
    '''
    attributes are constructed for window layout
    '''

    def __init__(self):
        self.question = [[sg.Text('Question', key='-QTxt-'), sg.Input(key='-QIN-')],
                         [sg.Image(key='IMAGE'), cw.text_element[0]],
                         [sg.Button('Upload Image', key='-img-'), sg.Button('Delete', key='-img_del-')]]
        self.answers = [[sg.Text('Ans1', key='-Ans1Txt-'), sg.Input(key='-Ans1-'), sg.Checkbox("", key="-C1-")],
                        [sg.Text('Ans2', key='-Ans2Txt-'), sg.Input(key='-Ans2-'), sg.Checkbox("", key="-C2-")]]
        self.nxt_ans = [[sg.Text('Ans3', key='-Ans3Txt-'), sg.Input(key='-Ans3-'), sg.Checkbox("", key="-C3-")],
                        [sg.Text('Ans4', key='-Ans4Txt-'), sg.Input(key='-Ans4-'), sg.Checkbox("", key="-C4-")]]
        self.move = [[sg.Button("Next"), sg.Button("Save")]]

        # Jump to Section

        # Edit Function
        # Timer, Edit Fields, Give Points

    def construct(self):
        layout =[[sg.Frame('The Slide', [[sg.Column([[sg.Column(self.question)],
                              [sg.Column(self.answers), sg.Column(self.nxt_ans)],
                              ], element_justification='center'
                    )], [sg.Column(self.move)]], key='-SLIDE-')]]
        return layout

    def question_select(self, q_amount, extra=0):
        auto_button_gen = False
        blanks = [[None, ]] * extra
        first_button = (len(blanks) - extra) + 1
        q_amount.extend(blanks)
        buttons = []
        for num, val in enumerate(q_amount, 1):
            if val[0] == None:
                button_text = 'Unused'
                if num != first_button:
                    auto_button_gen = True
            else:
                button_text = val[0]
            buttons.append([sg.Button('%s) %s' % (num, button_text),  # new change - changed val[2] to val[0]
                                      key='-%s-' % num,
                                      disabled=auto_button_gen
                                      )])
        return sg.Column(buttons, key='-jump-', scrollable=True,
                         vertical_scroll_only=True)

    def slide_fill(self, window, q_list, disable=True):
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
        ans_list = q_list[2]
        tuple(map(lambda x: window[f'-Ans{x[0]}-'].update(str(x[1]), disabled=disable), enumerate(ans_list, 1)))

    def next_question(self, position, TempList, input, pos_change=1):
        try:
            TempList[position - 1] = input
            position += pos_change
        except IndexError:
            TempList.append(input)
            position += pos_change
        return position, TempList

    def string_to_list(self, TempList):
        a = map(lambda x: (*x.strip('\n').split(':'),), TempList)
        a = (tuple(val[2].strip(')(\'').split(',')) for val in a)
        return list(a)

    def key_filter(self, event):
        key_filter = filter(lambda x: True if x != '-' else False, event)# new change, changed to tuples
        key_filter = ''.join(key_filter)
        position = int(key_filter)
        return position

class Input(Mastertemplate):
    def __init__(self):
        super(Input, self).__init__()

    def window_update(self, window, TempList):
        new_layout = Mastertemplate().construct()
        new_layout[0].append(sg.Frame('Question Selection', [[self.question_select(TempList, extra=10)]]))
        new_layout[0].insert(0, self.options())
        window.close()
        new_window = sg.Window('Editor', new_layout, finalize=True, resizable=True)
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
        return new_window

    def save_to_file(self, save_list, metadata):
        new_format = ('%s:%s:%s\n' % (val[0], val[1], val[2]) for val in save_list if
                      val[0] != None)
        with open('Example.txt', 'w') as file:
            file.writelines(new_format)
            file.write(str(metadata))

    def options(self):
        slide_options = [[sg.Button('Blank Slide')], [sg.Button('Delete Slide')],
                         [sg.Button('Slide Time Limit'), sg.Text(key='-time-', size=(2, 1))],
                         [sg.Button('Swap Slides'), sg.Text("Separate values with a ','")],
                         [sg.Button('Slide Points'), sg.Text(key='-pts-')], [sg.Input(key='master_input')]]
        general_options = [[sg.Button('Blank all slides', key='-clear-')],
                           [sg.Button('Delete all Slides', key='-del_slides-')],
                           [sg.Button('General Time limit', key='-gen_time-')],
                           [sg.Button('Points for all slides', key='-all_pts-')],
                           [sg.Button('Exit')], [sg.Input(key='master_input2')]]
        tab_layout = [[sg.Tab(title='Slide options', layout=slide_options), sg.Tab(title='General options',
                                                                                   layout=general_options)]]
        return sg.Frame('Options', [[sg.TabGroup(layout=tab_layout), ]])

    def correct_ans(self, values):
        cor_ans = []
        count = 0
        for i in values.items():
            if type(i[1]) is bool:
                count+= 1
                if i[1] is True:
                    cor_ans.append(count)
        current_input = [values["-QIN-"], cor_ans, (values["-Ans1-"], values["-Ans2-"],
                        values["-Ans3-"], values["-Ans4-"])]
        return current_input

    def blank_slide(self, window):
        window['-QIN-'].update('')
        tuple(map(lambda val: window[f'-Ans{val}-'].update(''), range(1, 5)))

    def UseInputVals(self):
        layout = self.construct()
        TempList = []
        num_of_buttons = 10
        selector_column = self.question_select(TempList, extra=10)
        options_frame = self.options()
        layout[0].append(sg.Frame('Question Selection', [[selector_column]]))  # New change Question selector frame
        layout[0].insert(0, options_frame)  # New change added options frame
        window = sg.Window('Editor', layout, finalize=True)
        check = 0
        position = 1
        max_position = 0
        blank_mode = False
        default_settings = [20, 4, None, 1]
        metadata = {}
        while True:
            try:
                metadata[position]
            except KeyError:
                metadata[position] = [*default_settings, ]
            window['-SLIDE-'].update(f'You are viewing slide {position}')
            window['-time-'].update(metadata[position][0])
            window['-timer-'].update(metadata[position][0])
            window['-pts-'].update(metadata[position][3])
            if metadata[position][2] == None:
                window['IMAGE'].update('')
            else:
                IU.image_open(f"C:/QuizItems/.Image/{metadata[position][2]}", window)
            #TODO Add check box state remembering(on/off)
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
            elif event == sg.WIN_CLOSED:
                break
            else:
                current_input = self.correct_ans(values)
                if event == "Next":
                    check = 0
                    position, TempList = self.next_question(position, TempList, current_input)
                    if position > num_of_buttons:
                        new_window = self.window_update(window, TempList)
                        window.close()
                        window = new_window
                        window[f'-{position - 1}-'].update('%s) %s' % (position - 1, TempList[position - 2][0]),
                                                           visible=True, disabled=False)
                        num_of_buttons += 10
                        window[f'-{position}-'].update(disabled=False)
                    else:
                        window[f'-{position - 1}-'].update('%s) %s' % (position - 1, TempList[position - 2][0])
                                      ,visible=True, disabled=False)
                        self.slide_fill(window, TempList[position - 2], disable=False)
                    if position >= max_position:
                        # TODO need to add the metadata saving to when not going above max position
                        blank_mode = True
                        max_position = position

                    else:
                        blank_mode = False
                        self.slide_fill(window, TempList[position - 1], disable=False)
                elif event == "Save":
                    check = 1
                    self.next_question(position, TempList, current_input, pos_change=0)
                    self.save_to_file(TempList, metadata)
                    pass
                elif event == '-img-':
                    save_name = IU.choose_img()
                    metadata[position][2] = save_name
                elif event == '-img_del-':
                    window['IMAGE'].update('')
                    metadata[position][2] = None
                elif event == 'Blank Slide':
                    self.blank_slide(window)
                    TempList[position-1] = ['', [], ('', '', '', '')]
                elif event == 'Delete Slide':
                    del TempList[position-1]
                    if max_position > 0:
                        window[f'-{max_position-1}-'].update(f'{position-1}) Unused', disabled=True)
                        max_position -=1
                    else:
                        max_position= 1
                        window[f'-{max_position}-'].update(f'{position-1}) Unused',disabled=True)
                        max_position -= 1
                    if TempList[position-1][0] == None:
                        self.blank_slide(window)
                        position -=1
                        max_position = position
                    else:
                        self.slide_fill(window, TempList[position-1], disable=False)
                elif event == 'Slide Time Limit':
                    metadata[position][0]= values['master_input']
                elif event == 'Slide Points':
                    metadata[position][3]= values['master_input']
                elif event == 'Swap Slides':
                    swap = values['master_input'].split(',')
                    if len(swap) != 2 or int(swap[1]) > max_position-1 or int(swap[0]) > max_position-1:
                        sg.popup('You have entered in the information incorrectly,\n'
                                 '-You may have forgot to separate with a , (comma)\n'
                                 '-Tried to swap more than two slides at a time\n'
                                 '-You entered slide numbers which don\'t exist /are unused\n', title='Input Error')
                        continue
                    frst_slide = TempList[int(swap[0])-1]
                    scd_slide = TempList[int(swap[1])-1]
                    TempList[int(swap[0])-1] = scd_slide
                    TempList[int(swap[1])-1] = frst_slide
                    self.slide_fill(window, TempList[position-1], disable=False)
                elif event == '-clear-':
                    for num in range(0, max_position-1):
                        self.blank_slide(window)
                        TempList[num] = ['', [], ('', '', '', '')]
                elif event == '-del_slides-':
                    Templist= []
                    for num in range(0, max_position-1):
                        window[f'-{max_position - 1}-'].update(disabled=True)
                        window[f'-{num + 1}-'].update(f'{num + 1})Unused')
                        max_position -=1
                    window[f'-{1}-'].update(f'{1})Unused', disabled=False)
                    position = 1
                    max_position =position
                    self.blank_slide(window)
                elif event == '-gen_time-':
                    print('gen time has fired')
                    for num in range(0, max_position-1):
                        metadata[num][0] = values['master_input2']
                elif event == '-all_pts-':
                    print('all pts fired')
                    for num in range(0, max_position-1):
                        metadata[num][3] = values['master_input2']
                else:
                    #metadata[position] = default_settings
                    TempList[position-1] = current_input
                    position = self.key_filter(event)
                    self.slide_fill(window, TempList[position - 1], disable=False)
                if blank_mode == True:
                    self.blank_slide(window)
                    window['IMAGE'].update('')
                    for i in range(1,5):
                        window[f'-C{i}-'].update('')
                blank_mode = False

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
            metadata = dict(question_list.pop(-1))
            question_list = (*self.string_to_list(question_list),)
        return question_list, metadata

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
        question_list, metadata = self.Q_process()
        print(type(metadata))
        window = sg.Window('Jake\'s Quiz', layout, finalize=True)
        key_num = len(question_list)
        q_position = 1
        window['Save'].update(visible=False, disabled=True)
        window['-img-'].update(visible=False, disabled=True)
        window['-img_del-'].update(visible=False, disabled=True)
        #TODO Fix converting dictionary to string
        while True:
            window['-SLIDE-'].update(f'You are viewing slide {q_position}')
            if metadata[q_position][2] == None:
                window['IMAGE'].update('')
            else:
                IU.image_open(f"C:/QuizItems/.Image/{metadata[q_position][2]}", window)
            self.slide_fill(window, question_list[q_position])
            event, values = window.read()

            if event == sg.WIN_CLOSED:
                break

            elif q_position >= key_num:
                window['Next'].update(disabled=True)
                sg.Popup('That was the last question!')
                q_position = 1
                pass

            elif event == 'Next':
                q_position += 1
                pass

            else:
                q_position = self.key_filter(event)
                pass

            if q_position < key_num:
                window['Next'].update(disabled=False)


## Temporary so I didn't have to mess around with the QuizLoader
# f = Input()
# f.UseInputVals()

j = Qreader()
j.start_up()
