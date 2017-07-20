#!/usr/bin/python3

"""tuner.py: example of graphical interface for real-time tuning of the paramenters"""

import sys

sys.path.insert(0, '../../libs')
from KinseiTuner import *
import gui
from tooltip import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *

__author__ = "Francesco Pessolano"
__copyright__ = "Copyright 2017, Xetal nv"
__license__ = "MIT"
__version__ = "0.9.0"
__maintainer__ = "Francesco Pessolano"
__email__ = "francesco@xetal.eu"
__status__ = "development"
__requiredfirmware__ = "july2017 or later"

# tips for commands

BA = "Indicates the minimum difference between the background temperature and the measured one in order to " \
     "consider this a person "
BT = "Represents the weight of the new background temperature versus the old one when caculating the new " \
     "background temperature"
TT = "Represents the minimum background temperature with the respect of the average room temperature"
FBT = "This threshold must be high enough to clean the fusion. Increase to reduce noise, decrease to increase samples"
FCF = "The higher the value, the greater priority is given to positions detected by more sensors"
FT = "The position temperature and the background must have a difference greater this threshold" \
     "to be considered a person position candidate"

SEND = "Sends configuration to the device"
FREEZE = "Stores current configuration as start override"
UNFREEZE = "Removes current start override, resetting to factory default"
BGRESET = "Reset the temperature background"
DISCARD = "Discards any change made from application start"


# Support functions
def popUpOk():
    messagebox.showinfo("Information", "Operation was succesfull")


def popUpNotOk():
    messagebox.showinfo("Error", "Operation has failed")


# this class shows how to visualise tracking with tkinter

class TunerGui:
    def __init__(self):
        self.demoKit = None
        self.ip = None
        self.connected = False
        self.canvas = None
        self.config = None
        self.master = None
        self.scales = []

    def connect(self, ip):
        try:
            self.demoKit = KinseiTuner(ip)
            self.connected = self.demoKit.serverConnected
            self.config = self.demoKit.readFullConfiguration()
            self.ip = ip
        except:
            self.connected = False

    def isConnected(self):
        return self.connected

    # this function set-up the canvas and let the tracking start
    def start(self):

        if self.connected:
            self.master = Tk()
            self.master.title("Kinsei Tuner Demo: " + self.ip)

            # bind escape to terminate
            self.master.bind('<Escape>', quit)

            menubar = Menu(self.master)
            filemenu = Menu(menubar, tearoff=0)
            filemenu.add_command(label="Load", command=self.loadConfig)
            filemenu.add_command(label="Save", command=self.saveConfig)
            filemenu.add_separator()
            filemenu.add_command(label="Exit", command=self.master.quit)

            # helpmenu = Menu(menubar, tearoff=0)

            menubar.add_cascade(label="File", menu=filemenu)
            # menubar.add_cascade(label="Help", menu=helpmenu)
            self.master.config(menu=menubar)

            frameSliders = Frame(self.master)
            frameButtons = Frame(self.master)
            frameSliders.pack(padx=20, pady=20)
            frameButtons.pack(padx=20, pady=20)

            wraplength = 200

            labelBA = Label(frameSliders, text="Background Alfa")
            labelBA.grid(row=1, column=0, sticky=E, padx=5)
            backgroundAlfa = Scale(frameSliders, orient=HORIZONTAL, length=450, width=20, digits=3, \
                                   from_=0.1, to=1.0, resolution=0.01)
            backgroundAlfa.grid(row=1, column=3)
            backgroundAlfa.set(self.config[0])
            self.scales.append(backgroundAlfa)
            Tooltip(labelBA, text=BA, wraplength=wraplength)

            labelBT = Label(frameSliders, text="Background Threshold")
            labelBT.grid(row=2, column=0, sticky=E, padx=5)
            backgroundThreshold = Scale(frameSliders, orient=HORIZONTAL, length=450, width=20, digits=4, \
                                        from_=0.1, to=10.0, resolution=0.01)
            backgroundThreshold.grid(row=2, column=3)
            backgroundThreshold.set(self.config[1])
            self.scales.append(backgroundThreshold)
            Tooltip(labelBT, text=BT, wraplength=wraplength)

            labelTT = Label(frameSliders, text="Temperature Threshold")
            labelTT.grid(row=3, column=0, sticky=E, padx=5)
            temperatureThreshold = Scale(frameSliders, orient=HORIZONTAL, length=450, width=20, digits=4, \
                                         from_=-10.0, to=10.0, resolution=0.01)
            temperatureThreshold.grid(row=3, column=3)
            temperatureThreshold.set(self.config[2])
            self.scales.append(temperatureThreshold)
            Tooltip(labelTT, text=TT, wraplength=wraplength)

            labelFBT = Label(frameSliders, text="Fusion Background Threshold")
            labelFBT.grid(row=4, column=0, sticky=E, padx=5)
            fusionBackgroundThreshold = Scale(frameSliders, orient=HORIZONTAL, length=450, width=20, digits=4, \
                                              from_=0.1, to=10.0, resolution=0.01)
            fusionBackgroundThreshold.grid(row=4, column=3)
            fusionBackgroundThreshold.set(self.config[3])
            self.scales.append(fusionBackgroundThreshold)
            Tooltip(labelFBT, text=FBT, wraplength=wraplength)

            labelFCF = Label(frameSliders, text="Fusion Consensum Factor")
            labelFCF.grid(row=5, column=0, sticky=E, padx=5)
            fusionConsensumFactor = Scale(frameSliders, orient=HORIZONTAL, length=450, width=20, digits=3, \
                                          from_=0.1, to=5.0, resolution=0.01)
            fusionConsensumFactor.grid(row=5, column=3)
            fusionConsensumFactor.set(self.config[4])
            self.scales.append(fusionConsensumFactor)
            Tooltip(labelFCF, text=FCF, wraplength=wraplength)

            labelFT = Label(frameSliders, text="Fusion Threshold")
            labelFT.grid(row=6, column=0, sticky=E, padx=5)
            fusionThreshold = Scale(frameSliders, orient=HORIZONTAL, length=450, width=20, digits=4,
                                    from_=0.1, to=10.0, resolution=0.01)
            fusionThreshold.grid(row=6, column=3)
            fusionThreshold.set(self.config[5])
            self.scales.append(fusionThreshold)
            Tooltip(labelFT, text=FT, wraplength=wraplength)

            bSend = Button(frameButtons, text='SEND', width=8, command=self.sendConfig)
            bSend.pack(side=LEFT, padx=5, pady=5)
            Tooltip(bSend, text=SEND, wraplength=wraplength)

            bFreeze = Button(frameButtons, text='FREEZE', width=8, command=self.freezeConfig)
            bFreeze.pack(side=LEFT, padx=5, pady=5)
            Tooltip(bFreeze, text=FREEZE, wraplength=wraplength)

            bUnfreeze = Button(frameButtons, text='UNFREEZE', width=8, command=self.unfreezeConfig)
            bUnfreeze.pack(side=LEFT, padx=5, pady=5)
            Tooltip(bUnfreeze, text=UNFREEZE, wraplength=wraplength)

            bBgreset = Button(frameButtons, text='BGRESET', width=8, command=self.bgReset)
            bBgreset.pack(side=LEFT, padx=5, pady=5)
            Tooltip(bBgreset, text=BGRESET, wraplength=wraplength)

            bDiscard = Button(frameButtons, text='DISCARD', width=8, command=self.discard)
            bDiscard.pack(side=LEFT, padx=5, pady=5)
            Tooltip(bDiscard, text=DISCARD, wraplength=wraplength)

    def sendConfig(self):  # check negatives again!
        newConfig = []
        for i in range(0, len(self.config)):
            newConfig.append(self.scales[i].get())
        if self.demoKit.writeFullConfiguration(newConfig):
            popUpOk()
        else:
            popUpNotOk()

    def saveConfig(self):
        self.master.filename = filedialog.asksaveasfilename(initialdir="/", title="Select file",
                                                            filetypes=(("config files", "*.cfg"), ("all files", "*.*")))
        with (open(self.master.filename, 'w')) as saveFile:
            for i in range(0, len(self.scales)):
                saveFile.write(str(self.scales[i].get()) + "\n")

    def loadConfig(self):
        self.master.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                          filetypes=(("config files", "*.cfg"), ("all files", "*.*")))
        with (open(self.master.filename, 'r')) as loadFile:
            for i in range(0, len(self.scales)):
                data = float(loadFile.readline().strip('\n'))
                self.scales[i].set(data)

    def discard(self):
        for i in range(0, len(self.config)):
            self.scales[i].set(self.config[i])

    def bgReset(self):
        if messagebox.askyesno('Reset Background', "Make sure nobody is in front of the device. Continue?", \
                               icon=messagebox.QUESTION, default=messagebox.YES):
            if self.demoKit.resetBackground():
                popUpOk()
            else:
                popUpNotOk()

    def freezeConfig(self):  # wait new fw
        if self.demoKit.saveOveride():
            popUpOk()
        else:
            popUpNotOk()

    def unfreezeConfig(self):  # wait new fw
        if self.demoKit.removeOveride():
            popUpOk()
        else:
            popUpNotOk()


def start():
    root = Tk()
    device = TunerGui()
    gui.StartGUI(root, device)
    root.mainloop()


if __name__ == "__main__":
    start()
