from tkinter import *
import tkinter.ttk as ttk
import os
import datetime
import csv
import sqlite3
from tkcalendar import DateEntry
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from pandas import DataFrame

parent = Tk()
screen_width = parent.winfo_screenwidth()
screen_height = parent.winfo_screenheight()
screensize = screen_height * screen_width
parent.geometry(f'{screen_width}x{screen_height}')
parent.title("Journal")
parent['bg'] = 'SteelBlue1'

############################################## STATS #############################################

def show_graph():
    num_dropdown.forget()
    label3.forget()
    label4.forget()
    label5.forget()
    num_menu1.forget()
    label6.forget()
    bBack_to_stats.forget()
    graph_menu.forget()
    bShowGraph.forget()
    
    y_axis = list()
    x_ticks = list()
    curr_date = start_date
    while(curr_date <= end_date):
        read_file = os.path.join(os.getcwd(), 'submissions', 'submission ' + str(curr_date) + '.csv')
        if os.path.exists(read_file):
            with open(read_file, newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=';', quotechar ='|')
                next(file_reader, None)
                next(file_reader, None)
                for row in file_reader:
                    if row[0] == num_option:
                        y_axis.append(int(row[score_dict[cat_option]]))
                        date = str(curr_date.month) + '/' + str(curr_date.day)
                        x_ticks.append(date)
            curr_date += datetime.timedelta(days = 1)  

    data = {'x_axis': x_ticks, 'y_axis': y_axis}
    df = DataFrame(data, columns = ['x_axis', 'y_axis'])

    figure = Figure(figsize = (6,5), dpi = 100)
    figure.tight_layout()

    add = figure.add_subplot(111)

    global canvas
    canvas = FigureCanvasTkAgg(figure, master = parent)
    canvas.get_tk_widget().pack(pady = (20,0))
    df = df[['x_axis', 'y_axis']].groupby('x_axis').sum()

    if graph_option == "Bar Graph":
        df.plot(kind = 'bar', legend = False, ax = add)

    elif graph_option == "Line Graph":
        df.plot(kind = 'line', legend = False, ax = add)

    toolbar = NavigationToolbar2Tk(canvas, parent)
    toolbar.update()
    toolbar.forget()
    bBacktoSelection.pack(pady = (50, 0))
    add.set_xlabel("Date of Submission")
    add.set_ylabel("{0}".format(cat_option))
    add.set_title("{0} of {1} for {2}".format(graph_option, cat_option, num_option))
def menu_num_option(value):
    global num_option 
    num_option = value

def menu_option1(value):
    global cat_option
    cat_option = value

def menu_option2(value):
    global graph_option
    graph_option = value

def view_graphs():
    label3.pack()
    bBacktoSelection.forget()
    canvas.get_tk_widget().destroy()
    label4.pack()
    label4.config(text = "Person")
    label3.config(text = "Build a graph from the options below.")
    label5.forget()
    from_cal.forget()
    bViewGraphs.forget()
    bViewText_category.forget()
    bViewText_person.forget()
    bMainMenu.forget()
    to_cal.forget()
    names_set = set()
    curr_date = start_date
    while(curr_date <= end_date):
        read_file = os.path.join(os.getcwd(), 'submissions', 'submission ' + str(curr_date) + '.csv')
        if os.path.exists(read_file):
            with open(read_file, newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=';', quotechar ='|')
                next(file_reader, None)
                next(file_reader, None)
                for row in file_reader:
                    names_set.add(row[0].lower())
            curr_date += datetime.timedelta(days = 1)   
    names_list = list(names_set)
    variable3 = StringVar(parent)
    variable1.set("                         ") 
    variable2.set("                         ") 
    variable3.set("                         ") 
    global num_dropdown               
    num_dropdown = OptionMenu(parent, variable3, *names_list, command=menu_num_option)
    num_dropdown.config(font = "Serif 14", bg = "white")
    num_menu = parent.nametowidget(num_dropdown.menuname)
    num_menu.config(font = "Serif 14", bg = "white")
    num_dropdown.pack()
    label5.config(text = "Category")
    label5.pack(pady = (50, 0))
    num_menu1.pack()
    label6.config(text = "Graph Type")
    label6.pack(pady = (50, 0))
    graph_menu.pack()
    bShowGraph.pack(pady = (50, 10))
    bBack_to_stats.pack()    

def show_listbox():
    text_menu.forget()
    from_cal.forget()
    to_cal.forget()
    bShowListbox.forget()
    bBack_to_stats.forget()
    bMainMenu.forget()
    curr_date = start_date
    text.pack()
    counter = 0
    label4.forget()
    option = text_dict[text_option]
    text.config(state = NORMAL)
    text.delete('1.0', END)
    label3.config(text = "Displaying results for '{0}'".format(text_option))
    while(curr_date <= end_date):
        read_file = os.path.join(os.getcwd(), 'submissions', 'submission ' + str(curr_date) + '.csv')
        if os.path.exists(read_file):
            with open(read_file, newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=';', quotechar ='|')
                next(file_reader, None)
                next(file_reader, None)
                for row in file_reader:
                    if (row[option] != 'N/A'):
                        text.insert(END, row[option] + '\n')
                        text.insert(END, row[0] + ' ' + str(curr_date) + '\n')
                        counter += 2
                        
            curr_date += datetime.timedelta(days = 1)

    for i in range(1, counter + 1, 4):
        tag1 = 'word{0}'.format(i)
        tag2 = 'word{0}'.format(i + 1)
        tag3 = 'word{0}'.format(i - 1)

        text.tag_add(tag1, str(i) + '.0', str(i + 1) + '.0')
        text.tag_config(tag1, background = "gainsboro", font = 'Serif 14')

        text.tag_add(tag2, str(i + 1) + '.0', str(i + 2) + '.0')
        text.tag_config(tag2, background = "gainsboro", font = 'Serif 10', justify = 'right')

        text.tag_add(tag3, str(i - 1) + '.0', str(i) + '.0')
        text.tag_config(tag3, background = "white", font = 'Serif 10', justify = 'right')
    
    text.tag_add("finaltag", str(counter) + '.0', str(counter + 1) + '.0')
    text.tag_config("finaltag", background = "white", font = 'Serif 10', justify = 'right')

    text.config(state = DISABLED)
    bBack_to_cal.pack()

def menu_option(value):
    global text_option 
    text_option = value

def view_text_cat():
    label3.config(text = "Please select the category of submissions you would like to view.")
    text.delete('1.0', END)
    bViewGraphs.forget()
    bViewText_category.forget()
    bViewText_person.forget()
    label4.config(text = "Category")
    label4.pack()
    text_menu.pack(side = TOP, pady = (0, 50))
    from_cal.forget()
    to_cal.forget()
    label5.forget()
    bBack_to_stats.pack(side= LEFT, padx = (575, 20))
    bShowListbox.pack(side = LEFT)
    text.forget()
    bBack_to_cal.forget()
    variable.set("                         ")
    
def person_stats(event):
    person_request = event.widget.get('1.0', 'end-1c')
    label4.forget()
    label5.forget()
    label6.forget()
    bMainMenu.forget()
    bBack_to_stats.forget()
    person_entry.forget()
    from_cal.forget()
    to_cal.forget()
    curr_date = start_date
    text.pack()
    counter = 0
    num_list = [3, 4, 5, 6, 13, 14, 15]
    label3.config(text = "Displaying results for {0}".format(person_request))
    text.config(state = NORMAL)
    text.delete('1.0', END)
    while(curr_date <= end_date):
        read_file = os.path.join(os.getcwd(), 'submissions', 'submission ' + str(curr_date) + '.csv')
        if os.path.exists(read_file):
            with open(read_file, newline='') as csvfile:
                file_reader = csv.reader(csvfile, delimiter=';', quotechar ='|')
                next(file_reader, None)
                next(file_reader, None)
                for row in file_reader:
                    if (row[0] == person_request.lower()):
                        for i in range(len(num_list)):
                            if (row[num_list[i]] != 'N/A'):
                                text.insert(END, row[num_list[i]] + '\n')
                                text.insert(END, num_dict[num_list[i]] + ' ' + str(curr_date) + '\n')

                                counter += 2
                        
            curr_date += datetime.timedelta(days = 1)

    for i in range(1, counter + 1, 4):
        tag1 = 'word{0}'.format(i)
        tag2 = 'word{0}'.format(i + 1)
        tag3 = 'word{0}'.format(i - 1)

        text.tag_add(tag1, str(i) + '.0', str(i + 1) + '.0')
        text.tag_config(tag1, background = "gainsboro", font = 'Serif 14')

        text.tag_add(tag2, str(i + 1) + '.0', str(i + 2) + '.0')
        text.tag_config(tag2, background = "gainsboro", font = 'Serif 10', justify = 'right')

        text.tag_add(tag3, str(i - 1) + '.0', str(i) + '.0')
        text.tag_config(tag3, background = "white", font = 'Serif 10', justify = 'right')
    
    text.tag_add("finaltag", str(counter) + '.0', str(counter + 1) + '.0')
    text.tag_config("finaltag", background = "white", font = 'Serif 10', justify = 'right')

    text.config(state = DISABLED)
    bBack_to_stats.pack(side = TOP, pady = (20, 0))

def to_cal_helper(event):
    global end_date
    end_date = to_cal.get_date()
    print(end_date)

def from_cal_helper(event):
    global start_date
    start_date = from_cal.get_date()
    print(start_date)
    to_cal.bind("<<DateEntrySelected>>", to_cal_helper)

def view_text_person():
    from_cal.forget()
    to_cal.forget()
    label3.config(text = "Please enter the name of the person you would like to view.")
    bViewGraphs.forget()
    bViewText_category.forget()
    bViewText_person.forget()
    label4.forget()
    label5.forget()
    label6.pack()
    person_entry.delete('1.0', END)
    person_entry.pack(side = TOP)
    bBack_to_stats.pack(side = TOP, pady = (50, 0))
    person_entry.bind("<Return>", person_stats)

def stats():
    bShowGraph.forget()
    num_dropdown.forget()
    num_menu1.forget()
    graph_menu.forget()
    bStats.forget()
    person_entry.forget()
    label4.forget()
    label5.forget()
    label6.forget()
    bSubmit.forget()
    label1.forget()
    bBack_to_stats.forget()
    bShowListbox.forget()
    from_cal.forget()
    to_cal.forget()
    text_menu.forget()
    text.forget()
    label3.config(text = "Please select a date range and choose what would you like to view.")
    label3.pack()
    label4.pack()
    from_cal.pack(side = TOP, pady = (0,50))
    label5.pack()
    to_cal.pack(side = TOP, pady = (0,50))
    from_cal.bind("<<DateEntrySelected>>", from_cal_helper)
    bMainMenu.pack(side = BOTTOM, pady = (50, 200))
    bViewGraphs.pack(side = LEFT, padx = 120)
    bViewText_category.pack(side = LEFT, padx = 100)
    bViewText_person.pack(side = LEFT, padx = 100)
    
################################################# SUBMIT ##########################################
def great():
    bGreat.forget()
    bNot_great.forget()
    label2.config(text ="I'm glad to hear it! Let's get started.")
    bOk.pack()

def not_great():
    bGreat.forget()
    bNot_great.forget()
    label2.config(text ="I'm sorry to hear you're not feeling so great.\nMaybe our work together will help us today. Let's get started")
    bOk.pack()

def create_file():
    bSubmit_yes.forget()
    bSubmit_no.forget()
    entry = open(name, "w")
    writer = csv.writer(entry, delimiter=';')
    writer.writerow(["Name", "Communal Strength", "Anxiety", "Gratitude", "Conflict", "Steps to feel more secure", "How addressed", "Consent", "Self Soothe (physically)", "Other Soothe (physically)", "Self Soothe (relationally)", "Other Soothe (relationally)", "Communication Score", "Appreciate Other", "Appreciate Self", "Support From Others"])
    entry.close()
    bStats.forget()
    bSubmit.forget()
    label1.forget()
    label2.config(text = "How are you today?", height = 5)
    label2.pack()
    bGreat.pack(side = LEFT, padx = (540, 30))
    bNot_great.pack(side = LEFT)

def submit():
    cwd = os.getcwd()
    now = datetime.datetime.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    global name
    name = os.path.join(cwd, 'submissions', 'submission ' + date + '.csv')
    if (os.path.exists(name)):
        label1.config(text = "You have already submitted today. Would you like to overwrite your previous submission?")
        bStats.forget()
        bSubmit.forget()
        bSubmit_no.pack(side = LEFT, padx = (575,50), pady = (0, 200))
        bSubmit_yes.pack(side = LEFT, pady = (0, 200))
    else:
        if (os.path.exists(os.path.join(cwd, 'submissions'))):
            create_file()
        else:
            os.makedirs(os.path.join(cwd, 'submissions'))
            create_file()

def end():
    bCont_no.forget()
    bCont_yes.forget()
    label2.config(pady = 0, height = 20, text = "It's important to remember that having anxious tendencies doesn't make you a bad person or unworthy of love.\nYou can have a secure relationship regardless of your inidividual insecurity score.\n\nRelationship security is earned through actions and behaviors that\nbuild both partners up and bring out the best in them.\nHaving a high insecurity score just means that you might encounter more challenges.\n\nThank you so much for working to understand yourself better\nand to work toward healthier and fulfilling relationships with the people in your life.\nSee you next week!")
    bEnd.pack()

def cont():
    label2.config(text = "Would you like to discuss another relationship?")
    gratitude_text = textbox1.get("1.0", END)
    gratitude_text = gratitude_text[:-1]
    support = textbox5.get("1.0", END)
    support = support[:-1]
    entry = open(name, "a+", newline='')
    writer = csv.writer(entry, delimiter = ";")
    lower_person = person.lower()
    row = [lower_person, cs, anxiety_level, gratitude_text, conflict_text, steps_to_secure, how_addressed, consent, ps_self, ps_other, rs_self, rs_other, communication_score, appreciate_other, appreciate_self_text, support]
    writer.writerow(row)
    entry.close()
    textbox1.delete("1.0", END)
    textbox1.forget()
    bGratitude.forget()
    textbox5.delete("1.0", END)
    textbox5.forget()
    bOutside_support.forget()
    bCont_yes.pack(side = LEFT, padx = (575, 20))
    bCont_no.pack(side = LEFT)

def outside_support():
    global appreciate_self_text
    appreciate_self_text = textbox4.get("1.0", 'end-1c')
    textbox4.delete("1.0", END)
    textbox4.forget()
    bAppreciate_self.forget()
    label2.config(text = "And finally, while self-compassion is a powerful tool, it is also important to seek out support from others.\nWhere do you feel you can get support at a time like this?")
    textbox5.pack()
    bOutside_support.pack(side = TOP, pady = 50)

def appreciate_self():
    global appreciate_other
    appreciate_other = textbox3.get("1.0", END)
    appreciate_other = appreciate_other[:-1]
    textbox3.delete("1.0", END)
    textbox3.forget()
    bAppreciate_person.forget()
    label2.config(text = "We still need to keep in mind self-compassion.\nWhat is one thing you appreciate about yourself today?\n")
    textbox4.pack()
    bAppreciate_self.pack(pady = 50)

def appreciate_person1():
    bNot_addressed.forget()
    global steps_to_secure
    steps_to_secure = textbox2.get("1.0", END)
    steps_to_secure = steps_to_secure[:-1]
    textbox2.delete("1.0", END)
    textbox2.forget()
    label2.config(text = "When it comes to anxious attachments,\nsometimes conflicts can overwhelm our sense of stability in the relationship.\nWe can ground ourselves through gratitude. What is one thing you appreciate about %s?" % person)
    textbox3.pack()
    bAppreciate_person.pack(pady = 50)

def gratitude():
    global conflict_text
    conflict_text = "N/A"
    global steps_to_secure
    steps_to_secure = "N/A"
    global how_addressed
    how_addressed = "N/A"
    global consent
    consent = "N/A"
    global ps_self
    ps_self = "N/A"
    global ps_other
    ps_other = "N/A"
    global rs_self
    rs_self = "N/A"
    global rs_other
    rs_other = "N/A"
    global communication_score
    communication_score = "N/A"
    global appreciate_other
    appreciate_other = "N/A"
    global appreciate_self_text
    appreciate_self_text = "N/A"
    global gratitude_text
    gratitude_text = "tochange"
    textbox5.insert("1.0", "N/A")
    label2.config(text = "I'm glad to hear things are going well with %s this week!\n Tell me more about the importance of this relationship in your life and why you're grateful for it." % person)
    bGratitude.pack()

def healthy_conclusion():
    bhealthy_conclusion.forget()
    global rs_other
    global healthy5_score
    if (cbYes.get() == 1):
        healthy5_score = 1
        rs_other = "1"
    else:
        healthy5_score = 0
        rs_other = "0"
    final_score = healthy1_score + healthy2_score + healthy3_score + healthy4_score + healthy5_score
    global communication_score
    communication_score = str(final_score)
    cbYes.set(0)
    cbNo.set(0)
    cbYes_healthy.forget()
    cbNo_healthy.forget()
    label2.config(pady = 50, text = "Remember, when you are close to someone,\nwhat you do or say around that person makes an impact, whether positive or negative.\n\nYour healthy communication score this week with %s is %i.\n\n Effective, health communication is possible for you,\nand developing these skills can help you develop and build trust and safety with %s." % (person, final_score, person))
    bNot_addressed.pack(pady = 50)

def healthy4():
    bhealthy4.forget()
    global rs_self
    global healthy4_score
    if (cbYes.get() == 1):
        healthy4_score = 1
        rs_self = "1"
    else:
        healthy4_score = 0
        rs_self = "0"
    cbYes.set(0)
    cbNo.set(0)
    label2.config(text = "And finally, how about %s.\nDid they take steps to soothe you, relationally?\n(reassuring the security of the relationship,\nresponsive to your emotional needs in the moment, practicing active listening.)" % person)
    bhealthy_conclusion.pack()

def healthy3():
    bhealthy3.forget()
    global ps_other
    global healthy3_score
    if (cbYes.get() == 1):
        healthy3_score = 1
        ps_other = "1"
    else:
        healthy3_score = 0
        ps_other = "0"
    cbYes.set(0)
    cbNo.set(0)
    label2.config(text = "Let's talk relationally.\nDid you take steps to soothe yourself, relationally?\n(using I-language, practicing active listening,\nstating needs constructively, giving emotions space without allowing them to dictate behavior.)")
    bhealthy4.pack()

def healthy2():
    bhealthy2.forget()
    global ps_self
    global healthy2_score
    if (cbYes.get() == 1):
        healthy2_score = 1
        ps_self = "1"
    else:
        healthy2_score = 0
        ps_self = "0"
    cbYes.set(0)
    cbNo.set(0)
    label2.config(text = "How about %s.\nDid they take steps to physically soothe you?\n(eye contact, facing the correct direction, physical closeness, sitting vs standing)" % person)
    bhealthy3.pack()

def healthy1():
    bhealthy1.forget()
    global consent
    global healthy1_score
    if (cbYes.get() == 1):
        healthy1_score = 1
        consent = "1"
    else:
        healthy1_score = 0
        consent = "0"
    cbYes.set(0)
    cbNo.set(0)
    label2.config(text = "Next, did you take steps to physically soothe yourself?\n(eye contact, facing the correct direction, physical closeness, sitting vs standing)")
    bhealthy2.pack()

def healthy_communication():
    bAddressed.forget()
    global how_addressed
    how_addressed = textbox25.get("1.0", 'end-1c')
    textbox25.delete("1.0", END)
    textbox25.forget()
    label2.config(pady = 50, text = "I'm glad you took steps to resolve this conflict.\nLet's talk about your process in terms of healthy communication.\nDid you ask for consent from %s before approaching the conflict?\n" % person)
    cbYes_healthy.pack()
    cbNo_healthy.pack()
    bhealthy1.pack()

def addressed():
    bYes.forget()
    bNo.forget()
    label2.config(pady = 50, height = 0, text = "I'm glad to hear it!\nIn your own words, how has the conflict been addressed?")
    textbox2.insert("1.0", "N/A")
    textbox25.pack()
    bAddressed.pack(pady = 50)

def self_comp2():
    bSelf2.forget()
    label2.config(text = "Zoom in on yourself during your conflict\nand repeat one or more of the following phrases:\nI see how you suffer just as anyone else does.\nMay you be happy.\nMay you be free from pain.\nAnything else that the you in the scene needs to hear in order to know that this difficulty is seen and acknowledged.\nLet me know when you're done.\n")
           
def self_comp1():
    bSelf.forget()
    label2.config(text = "Yes, self compassion is unfamiliar because you've learned to\ncondemn, criticize, or judge yourself when you learn something you don't like about yourself.\nLet's zoom in on how you reacted to your conflict.")
    bSelf2.pack()

def self_comp():
    label2.config(text= "Let's remember that if you've acted unpleasantly,\nyou're not doing it on purpose.\nYou're just expressing yourself in a way that's familiar to you and trying to get your needs met.")
    bSelf.pack()

def not_addressed():
    bYes.forget()
    bNo.forget()
    label2.config(text = "That's okay, you'll get there.\nWhat steps can you take to feel more secure in your relationship?\n")
    textbox2.pack()
    bNot_addressed.pack(side = TOP, pady = 50)
    global gratitude_text
    gratitude_text = "N/A"
    global how_addressed
    how_addressed = "N/A"
    global consent
    consent = "N/A"
    global ps_self
    ps_self = "N/A"
    global ps_other
    ps_other = "N/A"
    global rs_self
    rs_self = "N/A"
    global rs_other
    rs_other = "N/A"
    global communication_score
    communication_score = "N/A"
    
def compassion():
    bCompassion.forget()
    label2.config(height = 5, text = "Thank you for allowing yourself some space for self-compassion.\nHave you addressed this conflict?\n")
    bYes.pack(side = LEFT, padx = (575, 20))
    bNo.pack(side = LEFT)

def space():
    global conflict_text
    conflict_text = textbox15.get('1.0', END)
    conflict_text = conflict_text[:-1]
    textbox15.delete("1.0", END)
    textbox15.forget()
    label2.config(pady = 0, height = 20, text = "Wow, that sounds like it's been really hard for you.\nI definitely understand why you've been feeling some anxiety in the relationship,\nand I think it's important that we first take a moment to accept that feeling.\nLet me know when you've taken a moment to give yourself space for this.\n")
    bSpace.forget()
    bCompassion.pack()

def conflict():
    textbox15.pack()
    label2.config(text = "Conflicts can come in all shapes and sizes.\nPlease describe the conflict you've been experiencing and how it's been making you feel.\n(Feel free to discuss previous or ongoing conflicts and how they are impacting you now.)")
    bSpace.pack(side = TOP, pady = 50)
    
def get_anxiety(event):
    anxiety = int(event.widget.get('1.0', END))
    global anxiety_level
    anxiety_level = str(anxiety)
    entry1.delete('1.0',END)
    entry1.forget()
    textbox1.insert("1.0", "N/A")
    if (anxiety == 0):
        textbox1.delete("1.0", END)
        textbox1.pack()
        gratitude()
    else:
        conflict()
            
def anxiety_helper(communal_strength):
    entry1.delete('1.0', END)
    if (communal_strength >= 4):
        label2.config(text = "Wow, I'm glad to hear things are going well with %s this week.\nOn a scale of 1-5, to what extent have you felt anxiety this week in this relationship?\nPut 0 if you have felt none." % person)
        entry1.bind('<Return>', get_anxiety)
    elif (communal_strength < 4):
        label2.config(text = "I'm sorry to hear that things feel hard with %s this week.\nOn a scale of 1-5, to what extent have you felt anxiety this week in this relationship?\nPut 0 if you have felt none." % person)
        entry1.bind('<Return>', get_anxiety)

def get_communal(event):
    communal = int(event.widget.get('1.0', END))
    global cs
    cs = str(communal)
    entry1.delete('1.0',END)
    anxiety_helper(communal)

def person_helper():
    label2.config(text = "Great choice! On a scale of 1-5,what do you feel is your communal strength with %s?" % person)
    entry1.bind('<Return>', get_communal)

def get_person(event):
    global person
    person = event.widget.get('1.0', 'end-1c')
    if (person[0] == '\n'):
        person = person[1:]  
    entry1.delete("1.0", END)
    person_helper()

def analysis():
    bCont_yes.forget()
    bCont_no.forget()
    bOk.forget()
    bNo.forget()
    entry1.pack()
    label2.config(text = "Which relationship would you like to reflect on?")
    entry1.bind('<Return>', get_person)

####### MAIN MENU #########   
def start():
    from_cal.forget()
    to_cal.forget()
    label4.forget()
    label5.forget()
    label6.forget()
    label2.forget()
    label3.forget()
    bViewGraphs.forget()
    bViewText_category.forget()
    bViewText_person.forget()
    bMainMenu.forget()
    label1.config(text = "Hi there, what would you like to do today?")
    bSubmit_no.forget()
    bSubmit_yes.forget()
    bEnd.forget()
    label1.pack()
    bSubmit.pack(pady = 100)
    bStats.pack()
    

######################### SUBMISSIONS ###################################
label1 = Label(parent, text = "Hi Shayna, what would you like to do today?", bg = 'SteelBlue1', fg = 'snow', font= 'Serif 18 bold', height = 5)
label2 = Label(parent, height = 5, text = "How are you today?", bg = 'SteelBlue1', fg = 'snow', font = 'Serif 18 bold')

entry1 = Text(parent)    
entry1.config(width = 30, height = 1, font = 'Serif 16')

textbox1 = Text(parent, font = 'Serif 16', height = 15, width = 70)
textbox15 = Text(parent, font = 'Serif 16', height = 15, width = 70)
textbox2 = Text(parent, font = 'Serif 16', height = 15, width = 70)
textbox25 = Text(parent, font = 'Serif 16', height = 15, width = 70)
textbox3 = Text(parent, font = 'Serif 16', height = 15, width = 70)
textbox4 = Text(parent, font = 'Serif 16', height = 15, width = 70)
textbox5 = Text(parent, font = 'Serif 16', height = 15, width = 70)

bStats = Button(parent, text = "Check Stats", command = stats, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bSubmit = Button(parent, text = "Add Submission", command = submit, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bGreat = Button(parent, text = "Great", command=great, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bNot_great = Button(parent, text = "Not so great", command=not_great, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bOk = Button(parent, text = "Ok", command=analysis, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')

bSpace = Button(parent, text = "Next", command = space, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bNot_addressed = Button(parent, text = "Next", command = appreciate_person1, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bAppreciate_person = Button(parent, text = "Next", command = appreciate_self, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bYes = Button(parent, text = "Yes", command = addressed, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bNo = Button(parent, text = "No", command = not_addressed, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bSelf = Button(parent, text = "Next", command = self_comp1, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bSelf2 = Button(parent, text = "Next", command = self_comp2, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bCompassion = Button(parent, text = "Next", command = compassion, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bAppreciate_self = Button(parent, text = "Next", command = outside_support, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bOutside_support = Button(parent, text = "Next", command = cont, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bCont_yes = Button(parent, text = "Yes", command = analysis, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bCont_no = Button(parent, text = "No", command = end, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bEnd = Button(parent, text = "Done", command = start, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bGratitude = Button(parent, text = "Next", command = cont, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bAddressed = Button(parent, text = "Next", command = healthy_communication, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bhealthy1 = Button(parent, text = "Next", command = healthy1, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bhealthy2 = Button(parent, text = "Next", command = healthy2, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bhealthy3 = Button(parent, text = "Next", command = healthy3, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bhealthy4 = Button(parent, text = "Next", command = healthy4, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bhealthy_conclusion = Button(parent, text = "Next", command = healthy_conclusion, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bSubmit_yes = Button(parent, text = "Yes", command = create_file, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bSubmit_no = Button(parent, text = "No", command = start, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')

cbYes = IntVar()
cbNo = IntVar()
cbYes_healthy = Checkbutton(parent, text = "Yes", variable = cbYes, onvalue = 1, offvalue = 0, height = 2, width = 10, activebackground = 'SteelBlue1', bg = 'SteelBlue1', disabledforeground = 'snow', font = 'Serif 16 bold')
cbNo_healthy = Checkbutton(parent, text = "No", variable = cbNo, onvalue = 1, offvalue = 0, height = 2, width = 10, activebackground = 'SteelBlue1', bg = 'SteelBlue1', disabledforeground = 'snow', font = 'Serif 16 bold')



################################# STATS ###############################

label3 = Label(parent, height = 5, text = "What would you like to view?", bg = 'SteelBlue1', fg = 'snow', font = 'Serif 18 bold')
label4 = Label(parent, text = "From", bg = 'SteelBlue1', fg = 'snow', font = 'Serif 18 bold')
label5 = Label(parent, text = "To", bg = 'SteelBlue1', fg = 'snow', font = 'Serif 18 bold')
label6 = Label(parent, text = "Person", bg = 'SteelBlue1', fg = 'snow', font = 'Serif 18 bold')

from_cal = DateEntry(parent, width=12, background='SteelBlue1', foreground='white', borderwidth=5, font = 'Serif 16')
to_cal = DateEntry(parent, width=12, background='SteelBlue1', foreground='white', borderwidth=5, font = 'Serif 16')

bViewText_category = Button(parent, text = "View Text Submissions\n(by category)", command = view_text_cat, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bViewText_person = Button(parent, text = "View Text Submissions\n(by person)", command = view_text_person, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bViewGraphs = Button(parent, text = "View Graphical Data", command = view_graphs, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold', width = 20)
bShowListbox = Button(parent, text = "Next", command = show_listbox, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bShowGraph = Button(parent, text = "Next", command = show_graph, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bBack_to_cal = Button(parent, text = "Back", command = view_text_cat, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bBack_to_stats = Button(parent, text = "Back", command = stats, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bSubmit_person = Button(parent, text = "Submit", command = person_stats, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bMainMenu = Button(parent, text = "Return to Main Menu", command = start, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')
bBacktoSelection = Button(parent, text = "Back", command = view_graphs, bg = 'SteelBlue1', fg = 'snow', font = 'Serif 12 bold')


variable = StringVar(parent)
variable.set("                         ")
text_list = ["Gratitude Texts", "Conflict Descriptions", "Steps to Security", "How conflicts were addressed", "Appreciate Other", "Appreciate Self", "Support Elsewhere"]
text_dict = {"Gratitude Texts": 3, "Conflict Descriptions": 4, "Steps to Security": 5, "How conflicts were addressed": 6, "Appreciate Other": 13, "Appreciate Self": 14, "Support Elsewhere": 15}
num_dict = {3: "Gratitude Texts", 4: "Conflict Descriptions", 5: "Steps to Security", 6: "How conflicts were addressed", 13: "Appreciate Other", 14: "Appreciate Self", 15: "Support Elsewhere"}

score_list = ["Communal Strength", "Anxiety", "Communication Score"]
score_dict = {"Communal Strength": 1, "Anxiety": 2, "Communication Score": 12}
score_index_dict = {1: "Communal Strength", 2: "Anxiety", 12: "Communication Score"}

graph_list = ["Bar Graph", "Line Graph", "Scatter Plot"]


text_menu = OptionMenu(parent, variable, *text_list, command=menu_option)
text_menu.config(font = "Serif 14", bg = "white")
menu = parent.nametowidget(text_menu.menuname)
menu.config(font = "Serif 14", bg = "white")

variable1 = StringVar(parent)
variable1.set("                         ")

num_menu1 = OptionMenu(parent, variable1, *score_list, command=menu_option1)
num_menu1.config(font = "Serif 14", bg = "white")
menu1 = parent.nametowidget(num_menu1.menuname)
menu1.config(font = "Serif 14", bg = "white")

variable2 = StringVar(parent)
variable2.set("                         ")

graph_menu = OptionMenu(parent, variable2, *graph_list, command=menu_option2)
graph_menu.config(font = "Serif 14", bg = "white")
menu2 = parent.nametowidget(graph_menu.menuname)
menu2.config(font = "Serif 14", bg = "white")

person_entry = Text(parent)    
person_entry.config(width = 30, height = 1, font = 'Serif 16')

text = Text(parent, wrap = WORD, insertborderwidth = 5, spacing1 = 5, width = 75, height = 15, font = 'Serif 14')

figure = Figure(figsize = (5,4), dpi = 100)
canvas = FigureCanvasTkAgg(figure, master = parent)
num_dropdown = Label()

start()
parent.mainloop()

