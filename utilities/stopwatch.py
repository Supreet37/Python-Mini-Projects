import tkinter as Tkinter
from datetime import datetime

counter = 0
running = False

def update_label(label):
    global counter, running
    if running:
        tt = datetime.utcfromtimestamp(counter)
        display = tt.strftime('%H:%M:%S')
        label['text'] = display
        counter += 1
        label.after(1000, update_label, label)

def Start(label):
    global running, counter
    if not running:
        running = True
        update_label(label)
        start['state'] = 'disabled'
        stop['state'] = 'normal'
        reset['state'] = 'normal'

def Stop():
    global running
    running = False
    start['state'] = 'normal'
    stop['state'] = 'disabled'
    reset['state'] = 'normal'

def Reset(label):
    global counter, running
    counter = 0
    label['text'] = '00:00:00'
    if not running:
        reset['state'] = 'disabled'

root = Tkinter.Tk()
root.title("Stopwatch")
root.minsize(width=250, height=70)

label = Tkinter.Label(root, text='00:00:00', fg='black', font='Verdana 30 bold')
label.pack()

f = Tkinter.Frame(root)
start = Tkinter.Button(f, text='Start', width=6, command=lambda: Start(label))
stop = Tkinter.Button(f, text='Stop', width=6, state='disabled', command=Stop)
reset = Tkinter.Button(f, text='Reset', width=6, state='disabled', command=lambda: Reset(label))

f.pack(anchor='center', pady=5)
start.pack(side='left')
stop.pack(side='left')
reset.pack(side='left')

root.mainloop()