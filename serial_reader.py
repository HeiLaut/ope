import serial
import time
import PySimpleGUI as sg

ser = serial.Serial('/dev/ttyUSB0', baudrate = 9600)
layout = [[sg.Text("Daten:", font = [25])],
          [sg.Text(size=(40,2), key='-OUTPUT-', font = [25])],
          [sg.Button('Ok'), sg.Button('Quit')]]
          
window = sg.Window('Datenanzeige', layout)


while True:
    data = str(ser.readline())[2:-5]
    event, values = window.read(timeout = 1)

    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    window['-OUTPUT-'].update(data)
    


ser.close()
window.close()
