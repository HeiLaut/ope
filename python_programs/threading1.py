#!/usr/bin/env python
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import serial
import time
import threading
import queue
from multiprocessing import Process, Value, Array
run = True
pause = True
data = ["0.0","0.0"]
def data():
    global run, pause, data
    ser = serial.Serial('COM6', baudrate = 9600)
    while run  == True:
            dat = str(ser.readline())[2:-5]
            data = dat.split(',')
            
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def gui():
    global run, pause, data
      
    t1 = threading.Thread(target = data, args = ())
    t1.start()
    # define the form layout
    layout = [[sg.Text('Serial Plotter', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Canvas(size=(640, 480), key='-CANVAS-')],
              [sg.Text(size=(40,2), key='-OUTPUT-', font = [25])],
              [sg.Button('Exit', size=(10, 2), pad=((280, 0), 3), font='Helvetica 14')],
              [sg.Button('toggle pause'), sg.Button('clear')],
              [sg.Text('Messintervall'), sg.Slider((1, 10),1,1,orientation="h",size=(20, 15),enable_events = True, key="SLIDER",)],
              [sg.Text('Crop'), sg.Slider((10, 1000),100,10,orientation="h",size=(20, 15),enable_events = True, key="SLIDER_CROP",)],
              [sg.MLine(default_text='A second multi-line', size=(35, 3),key ="DATA")]]
    values['DATA'] = "aha"
    # create the form and show it without the plot
    window = sg.Window('Demo Application - Embedding Matplotlib In PySimpleGUI', layout, finalize=True)

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
    while True:
        event, values = window.read(timeout=10)
        #print(datx , daty )
        
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
        
        if event == 'toggle pause':
            if pause  == False:
                pause  = True
            else:
                pause  = False
        if event == 'clear':
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
                fig_agg.draw()
    window.close()
    
if __name__ == '__main__':
    gui()
