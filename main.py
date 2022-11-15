from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from datetime import datetime as dt
import PySimpleGUI as sg
import numpy as np
import csv

#Declare global variables
fig = plt.figure(dpi = 96, figsize = (9,5))
fig.subplots_adjust(bottom=0.21, left=0.1, right=0.925)
temp1, temp2, temp3, temp4 = [], [], [], []
date, time = [], []

#Reset matplotlib figure
def resetFigure():
    plt.clf()
    plt.suptitle("Temp Data", fontsize = 20)
    plt.xlabel("Time",fontsize = 16)
    plt.ylabel("Temp (C)", fontsize = 16)
    plt.ylim(20,80)

#Update matplotlib graph
def updateFigure(filePath):

    #Open csv file
    with open(filePath) as f:
        reader = csv.reader(f)
        
        #TODO
        #Checks whether the number of columns is 6, otherwise the csv file will not be read
        ncol = len(next(reader))
        f.seek(0)
        if ncol != 6:
            sg.popup("The Column Count of the csv file doesn't match!"
                    + "\nPlease choose another file")
            pass

        #Read the data for each row and process it into a list
        for row in reader:

            #Skip the line if there is an empty value
            if not (row):
                continue
            
            #Timestamp data for time and date
            dateData = dt.strptime(row[0], "%m/%d/%Y")
            date.append(dateData)
            timeData = dt.strptime(row[1], "%I:%M:%S %p")
            time.append(timeData)

            #Graph subtitle
            plt.title(date[0].strftime("%d-%m-%Y") + " " 
                        + time[0].strftime("%I:%M:%S %p") + " Until " 
                        + date[-1].strftime("%d-%m-%Y") + " " 
                        + time[-1].strftime("%I:%M:%S %p"), fontsize=12)

            #Temp data
            dataTemp1 = float(row[2])
            temp1.append(dataTemp1)
            dataTemp2 = float(row[3])
            temp2.append(dataTemp2)
            dataTemp3 = float(row[4])
            temp3.append(dataTemp3)
            dataTemp4 = float(row[5])
            temp4.append(dataTemp4)

    #Take average of 8 data from time array for x axis ticker
    #If the data is less than 8 then the time ticker is not displayed
    XTickerSum = 8
    if len(time) >= XTickerSum:
        xTicker = []
        idx = []
        idx = np.round((np.linspace(0, len(time) - 1, XTickerSum))
                        .astype(int).tolist())
        for x in idx:
            xTicker.append(time[x].strftime("%I:%M:%S %p"))
        plt.xticks(ticks=idx, labels=xTicker, rotation=35)

    #If the temperature data is more than 80 degrees c, the graph is not displayed
    #Data over 1700 degrees c because the sensor is damaged or not installed
    if dataTemp1 <= 80:
        plt.plot(temp1, color="red", label="Temp 1")
    if dataTemp2 <= 80:
        plt.plot(temp2, color="green", label="Temp 2")
    if dataTemp3 <= 80:
        plt.plot(temp3, color="blue", label="Temp 3")
    if dataTemp4 <= 80:
        plt.plot(temp4, color="#cccc00", label="Temp 4")
    
    #Add legend for plot figure
    plt.legend()
    
    #Display the matplotlib figure on the PySimpleGUI canvas
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

    #Remove all list elements for the next figure
    date.clear()
    time.clear()
    temp1.clear()
    temp2.clear()
    temp3.clear()
    temp4.clear()

#PySimpleGUI window layout
sg.theme("DarkTeal6")
layout = [
    [sg.Canvas(key="-CANVAS-")],
    [sg.Input(key="-INPUT-",expand_x = True, disabled=True),
        sg.Button("Open File", key="-OPEN-"),
        sg.Button("Save Image", key="-SAVE-")
    ]
]

#Main Window
window = sg.Window("Data Logger", layout, location=(200,100), finalize = True)

#Matplotlib element connection to PySimpleGUI
figure_canvas_agg = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)

#Show blank figure
resetFigure()
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

#Main window loop
#try:
while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event == "-SAVE-":
        savePath = sg.popup_get_file("Save Image", 
                    file_types=(("Portable Network Graphics", "*.png"),), 
                    save_as=True, no_window=True)
        plt.savefig(savePath)
    
    if event == "-OPEN-":
        filePath = sg.popup_get_file("Open CSV File",
                    title="Open CSV File", 
                    file_types=(("Comma Separated Value", "*.csv"),),
                    no_window=True)
        if filePath:
            resetFigure()
            updateFigure(filePath)
            window["-INPUT-"].update(filePath)

#except Exception as e:
#    sg.popup_error_with_traceback(f"Terjadi Kesalahan!", e)

window.close()