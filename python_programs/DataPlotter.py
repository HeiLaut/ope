#!/usr/bin/env python
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import serial
import time
import threading
from multiprocessing import Process, Value, Array
import random
import csv
sg.theme("DarkTeal2")
#import pyautogui //to get the Position of the mouse
run = True
pause = True
data = ["0.0","0.0"]
def get_data():
    global run, pause, data
    ser = serial.Serial('COM6', baudrate = 9600)
    #i = 0
    while run  == True:
        #time.sleep(0.05)
        #i+=1
        #data = [i, random.randint(0,10)]

        dat = str(ser.readline())[2:-5]
        data = dat.split(',')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def output(x,y):# überführt Koordinaten in eine Liste mit beiden Werten durch Tabularor getrennt
    outp = []

    for i in range(len(x)):
        outp.append(f"{str(x[i])}, \t \t{str(y[i])}")

    return outp
def csv_out(x,y,folder):
    csv_o = []
    with open(f'{folder}/tables.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        csv_o = list(zip(x,y))
        for row in csv_o:
            writer.writerow(row)

def gui():
    global run, pause, data

    t1 = threading.Thread(target = get_data, args = ())
    t1.start()
    # define the form layout
    layout = [[sg.Text('Data Plot', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS-'),sg.Listbox(values = [], key = '-LISTOUT-', size=(30, 25))],
              [sg.Text(size=(40,2), key='-OUTPUT-', font = [25]), sg.Button('Export csv', disabled = True), sg.InputText(key = "-FOLDERTEXT-"),sg.FolderBrowse(key = "-FOLDER-")],
              [sg.Button('Start/Stop'), sg.Button('Löschen')],
              [sg.Text('Messintervall'), sg.Slider((1, 10),1,1,orientation="h",size=(20, 15),enable_events = True, key="SLIDER",)],
              [sg.Text('Crop'), sg.Slider((10, 1000),100,10,orientation="h",size=(20, 15),enable_events = True, key="SLIDER_CROP",)],
              [sg.Button('Exit', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')]
               ]

    # create the form and show it without the plot
    window = sg.Window('Serial Plotter', layout, finalize=True)

    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.TKCanvas
    # draw the intitial scatter plot
    fig, ax = plt.subplots()
    ax.grid(True)
    fig_agg = draw_figure(canvas, fig)
    x = []
    y = []
    i = 0
    n = 5
    #folder = None
    while True:

        #print(pyautogui.position())
        event, values = window.read(timeout=10)

        datx = float(data[0])
        daty = float(data[1])

        window['-OUTPUT-'].update(f"t = {datx}\n F = {daty }")

        i = int(datx*100)

        if event in ('Exit', None):
            pause  = True
            run  = False
            t1.join()
            break

        n = values['SLIDER']
        crop = int(values['SLIDER_CROP'])
        if event == "-FOLDER-":
            window.FindElement('-FOLDERTEXT-').update(values["-FOLDER-"])

        folder = values["-FOLDER-"]

        if folder != '':
            window.FindElement('Export csv').update(disabled = False)
        if event == 'Export csv':
            csv_out(x,y,folder)

        if event == 'Start/Stop':
            if pause  == False:
                pause  = True
            else:
                pause  = False
        if event == 'Löschen':
            x = []
            y = []
            ax.cla()
            ax.grid(True)
            ax.plot(x,y)
            fig_agg.draw()

        if pause  == False:
            if i%n == 0:
                y.append(float(daty))
                x.append(float(datx))
                x = x[-crop:]
                y = y[-crop:]
                ax.cla()
                ax.grid(True)
                ax.plot(x,y)
                #ax.plot(105,200,'ro')
                fig_agg.draw()
            window.FindElement('-LISTOUT-').Update(values=output(x,y))
        elif pause == True:
            if values['-LISTOUT-'] ==[]:
                pass
            else:
                mark = values['-LISTOUT-'][0]
                markxy = mark.split(',')
                ax.cla()
                ax.grid(True)
                ax.plot(x,y)
                ax.plot(float(markxy[0]),float(markxy[1]),'ro')
                fig_agg.draw()


    window.close()



if __name__ == '__main__':
    gui()
