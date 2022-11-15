from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt
from datetime import datetime as dt
import PySimpleGUI as sg
import numpy as np
import csv

#Deklarasi beberapa variabel global
fig = plt.figure(dpi = 96, figsize = (9,5))
fig.subplots_adjust(bottom=0.21, left=0.1, right=0.925)
temp1, temp2, temp3, temp4 = [], [], [], []
tanggal, waktu = [], []

#Atur ulang figure matplotlib
def resetFigure():
    plt.clf()
    plt.suptitle("Data Suhu", fontsize = 20)
    plt.xlabel("Waktu",fontsize = 16)
    plt.ylabel("Suhu (C)", fontsize = 16)
    plt.ylim(20,80)

#Update Grafik Matplotlib
def updateFigure(filePath):

    #Buka file csv
    with open(filePath) as f:
        reader = csv.reader(f)
        
        #TODO
        #Cek apakah jumlah kolom adalah 6, jika tidak maka file csv tidak dibaca
        ncol = len(next(reader))
        f.seek(0)
        if ncol != 6:
            sg.popup("Jumlah Kolom file csv tidak sesuai!"
                    + "\nMohon pilih kembali file")
            pass

        #Baca data tiap baris dan di proses menjadi list
        for row in reader:

            #Lewati baris jika ada nilai kosong
            if not (row):
                continue
            
            #Data timestamp waktu dan tanggal
            dataTanggal = dt.strptime(row[0], "%m/%d/%Y")
            tanggal.append(dataTanggal)
            dataWaktu = dt.strptime(row[1], "%I:%M:%S %p")
            waktu.append(dataWaktu)

            #Subjudul grafik
            plt.title(tanggal[0].strftime("%d-%m-%Y") + " " 
                        + waktu[0].strftime("%I:%M:%S %p") + " Sampai Dengan " 
                        + tanggal[-1].strftime("%d-%m-%Y") + " " 
                        + waktu[-1].strftime("%I:%M:%S %p"), fontsize=12)

            #Data suhu
            dataTemp1 = float(row[2])
            temp1.append(dataTemp1)
            dataTemp2 = float(row[3])
            temp2.append(dataTemp2)
            dataTemp3 = float(row[4])
            temp3.append(dataTemp3)
            dataTemp4 = float(row[5])
            temp4.append(dataTemp4)

    #ambil rata 8 data dari array waktu untuk ticker x axis
    #Jika data kurang dari 8 maka ticker waktu tidak ditampilkan
    jumlahXTicker = 8
    if len(waktu) >= jumlahXTicker:
        xTicker = []
        idx = []
        idx = np.round((np.linspace(0, len(waktu) - 1, jumlahXTicker))
                        .astype(int).tolist())
        for x in idx:
            xTicker.append(waktu[x].strftime("%I:%M:%S %p"))
        plt.xticks(ticks=idx, labels=xTicker, rotation=35)

    #Kalau data suhu lebih dari 80 derajat c, graph tidak ditampilkan
    #Data lebih dari 1700 derajat c karena sensor rusak atau belum terpasang
    if dataTemp1 <= 80:
        plt.plot(temp1, color="red", label="Temp 1")
    if dataTemp2 <= 80:
        plt.plot(temp2, color="green", label="Temp 2")
    if dataTemp3 <= 80:
        plt.plot(temp3, color="blue", label="Temp 3")
    if dataTemp4 <= 80:
        plt.plot(temp4, color="#cccc00", label="Temp 4")
    
    #Beri legend untuk plot figure
    plt.legend()
    
    #Tampilkan figure matplotlib pada kanvas PySimpleGUI
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack()

    #Hapus semua elemen list untuk figure selanjutnya
    tanggal.clear()
    waktu.clear()
    temp1.clear()
    temp2.clear()
    temp3.clear()
    temp4.clear()

#PySimpleGUI window layout
sg.theme("DarkTeal6")
layout = [
    [sg.Canvas(key="-CANVAS-")],
    [sg.Input(key="-INPUT-",expand_x = True, disabled=True),
        sg.Button("Buka File", key="-OPEN-"),
        sg.Button("Simpan Gambar", key="-SAVE-")
    ]
]

#Window utama
window = sg.Window("Data Logger", layout, location=(200,100), finalize = True)

#Koneksi elemen Matplotlib ke PySimpleGUI
figure_canvas_agg = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)

#Tampilkan blank figure
resetFigure()
figure_canvas_agg.draw()
figure_canvas_agg.get_tk_widget().pack()

#Loop window utama
#try:
while True:
    event,values = window.read()
    if event == sg.WIN_CLOSED:
        break
    
    if event == "-SAVE-":
        savePath = sg.popup_get_file("Simpan Gambar", 
                    file_types=(("Portable Network Graphics", "*.png"),), 
                    save_as=True, no_window=True)
        plt.savefig(savePath)
    
    if event == "-OPEN-":
        filePath = sg.popup_get_file("Buka File CSV",
                    title="Buka File CSV", 
                    file_types=(("Comma Separated Value", "*.csv"),),
                    no_window=True)
        if filePath:
            resetFigure()
            updateFigure(filePath)
            window["-INPUT-"].update(filePath)

#except Exception as e:
#    sg.popup_error_with_traceback(f"Terjadi Kesalahan!", e)

window.close()