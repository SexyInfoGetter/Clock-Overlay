import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
from tkinter import Toplevel, messagebox
import time

_HH, _MM, _SS = 0, 15, 0
uSize = 300 # size
uOfst = 10 # offset
uTrlc = 0.72
uBg_0 = "black"
uBg = "midnightblue"
uFg_0 = "#ffffff" #accent
uFg = "blue"
uAlert = "#ff0000"
_duration = _SS + _MM * 60 + _HH * 3600

class theClock:
    def __init__(self, theRoot, duration = 1):
        duration = 1 if duration <= 0 else duration
        self.t = duration
        self.t_0 = time.time()
        self.tEnd = False
        self.tPause = False
        self.t_Delta = 0

        self.root = theRoot
        
        self.v_S = uSize
        self.vFrame = tk.Frame(theRoot)
        self.vCnvs = tk.Canvas(
            self.vFrame, width=self.v_S, height=self.v_S,
            bg = uBg_0,
            highlightthickness=0
            )
        self.vBg = self.vCnvs.create_oval(
            uOfst, uOfst, self.v_S - uOfst, self.v_S - uOfst,
            fill = uBg, outline = uFg_0, width = 1
        )
        self.vArc = self.vCnvs.create_arc(
            uOfst, uOfst, self.v_S - uOfst, self.v_S - uOfst,
            start = 90, extent = 360, # default 
            fill = uFg, outline = uFg_0, width = 1
        )
        self.vLb = tk.Label(self.vFrame, text = "",
                             fg = uFg_0, font = ("Ubuntu Mono", 16),
                             bg = uBg_0
                             )

        self.bFrame = tk.Frame(theRoot, bg = uBg_0)
        self.bPause = tk.Button(
            self.bFrame,
            text = "⏯", width = 4, bg = uBg, fg = uFg_0,
            command = self.onTogglePause
        )
        self.bMenu = tk.Button(
            self.bFrame, 
            text="⚙",width = 4, bg = uBg, fg = uFg_0,
            command=lambda: theSetting(theRoot, self))
        self.bStart = tk.Button(
            self.bFrame,
            text = "↺", width = 4, bg = uBg, fg = uFg_0,
            command = self.onRestart
        )
        self.bPause.pack(fill = "x")
        self.bMenu.pack(fill = "x")
        self.bStart.pack(fill = "x")
        self.bFrame.pack(side = "left", fill = "both")
                
        self.vFrame.pack(side = "left")
        self.vLb.pack(fill ="x")
        self.vCnvs.pack(fill = "both", expand = 1)

        self.start(duration)
        self.vCnvs.bind("<Configure>", self.onResize)

        #debug        
        self.root.bind("<Escape>", lambda e: self.start(5)) 
        # self.root.bind("<KeyPress-[>", lambda e: self.updateArc(uFg, uFg_0))
        # self.root.bind("<KeyPress-]>", lambda e: self.updateArc(uBg, uBg))
        self.root.bind("<KeyPress-[>", lambda e: self.time__Pause())
        self.root.bind("<KeyPress-]>", lambda e: self.time__Resume())
        self.root.bind("<space>", lambda e: self.onTogglePause())

    def start(self, duration):
        self.t = duration
        self.t_0 = time.time()
        self.tPause = False
        self.updateArc(uFg, uFg_0)
        self.t_Delta = 0
        
        self.update()

    def update(self):
        self.root.attributes("-topmost", True)
        if self.tPause:
            return
        t_elapsed = self.t_Delta + (time.time() - self.t_0)
        t_ = max(0, self.t - t_elapsed) # Remaining time
        angle = 360 * (t_ / self.t)

        self.updateCnvs(angle = angle)
        if t_ > 0:
            self.root.after(50, self.update) # schedule
            T__int = int(t_)
            T__h = T__int // 3600
            T__m = (T__int % 3600) // 60
            T__s = (T__int % 60)
            self.updateLb(f"{T__h:02d}:{T__m:02d}:{T__s:02d}")
            self.tEnd = False
        else:
            self.updateLb("Time out")
            self.tEnd = True
            self.onTimeout()
            messagebox.showwarning("Time's up!", "Your timer has expired.")

    def time__Pause(self):
        if not self.tPause:
            self.t_Delta += time.time() - self.t_0
            self.tPause = True
            self.updateArc(uAlert, uFg_0)

    def time__Resume(self):
        if self.tPause:
            self.t_0 = time.time()
            self.tPause = False
            self.updateArc(uFg, uFg_0)
            self.update()  


    def updateCnvs(self, angle):
        self.vCnvs.itemconfig(self.vArc, extent = angle)
    
    def updateLb(self, text):
        self.vLb.config(text = text)

    def updateArc(self, color1 = uFg, color2 = uFg_0):
        self.vCnvs.itemconfig(self.vArc, fill = color1, outline = color2)
        
    

    def onResize(self, event):
        newSize = min(event.width, event.height)
        self.v_S = newSize
        self.vCnvs.coords(self.vBg ,
            uOfst, uOfst, self.v_S - uOfst, self.v_S - uOfst, 
        )
        self.vCnvs.coords(self.vArc ,
            uOfst, uOfst, self.v_S - uOfst, self.v_S - uOfst,
        )

    def onTimeout(self, blink = True):
        if self.tEnd:
            self.vCnvs.itemconfig(self.vBg, fill = "red" if blink else uBg)
            self.root.after(500, self.onTimeout, not blink)
        else:
            self.vCnvs.itemconfig(self.vBg, fill = uBg)           
            
    def onTogglePause(self):
        if self.tEnd:
            self.start(self.t)
        if self.tPause:
            self.time__Resume()
        else:
            self.time__Pause()

    def onRestart(self):
        if self.tPause or self.tEnd:
            self.start(self.t)
        else: # if midway, restart but not automatically start
            self.start(self.t)
            self.time__Pause()

class theSetting:
    def __init__(self, theRoot, theInstance):
        self.p_Clock = theInstance
        self.p_Parent = theRoot
        
        self.jTop = tk.Toplevel(self.p_Parent, bg = uBg_0)
        self.jTop.title("Setting")
        self.jTop.geometry(f"200x90+{x - 100}+{y - 100}") 

        self.jTop.transient(theRoot)
        self.jTop.lift()
        self.jTop.focus_force()
        self.jTop.grab_set()


        t0 = theInstance.t
        t_h = t0 // 3600
        t_m = (t0 % 3600) // 60
        t_s = t0 % 60

        self.j_timeFrame = tk.Frame(self.jTop, bg = uBg_0)
        self.j_timeFrame.pack()
        self.j_timeVar = [tk.StringVar(value = t_h),
                          tk.StringVar(value = t_m),
                          tk.StringVar(value = t_s)
                          ]
        self.j_timeEntries = []
        num = 1
        for t_Var in self.j_timeVar:
            t_Entr = tk.Entry(self.j_timeFrame, textvariable=t_Var, width = 5)
            t_Entr.grid(row = 2, column = num)
            num += 1
            t_Entr.bind("<Return>", lambda e: self.fApply())
            self.j_timeEntries.append(t_Entr)
        
        self.j_Apply = tk.Button(self.j_timeFrame, text="▷", width = 5,
                                command=self.fApply,
                                bg = uBg, fg = uFg_0)
        self.j_Apply.grid(row = 2, column = 5) 

        self.j_OpqVar = tk.DoubleVar(value=self.p_Parent.attributes("-alpha"))

        self.j_OpqSlider = tk.Scale(self.jTop, from_=0.1, to=1.0,
                                    resolution=0.05,
                                    orient="horizontal",
                                    variable=self.j_OpqVar,
                                    bg = uBg, fg = uFg_0,
                                    command=self.fApplyOpq)
        self.j_OpqSlider.pack()

        self.j_Color = tk.Button(self.jTop, text=":)", width = 5,
                                bg = uBg, fg = uFg_0,
                                command=self.fApplyColor)
        self.j_Color.pack()
       

    def fApply(self):
        try:
            total = int(self.j_timeEntries[0].get()) * 3600 + int(self.j_timeEntries[1].get()) * 60 + int(self.j_timeEntries[2].get())
            self.p_Clock.start(total)
        except ValueError:
            pass
        self.jTop.destroy()

    def fApplyOpq(self, value):
        self.p_Parent.attributes("-alpha", float(value))

    def fApplyColor(self):
        global uFg
        color = colorchooser.askcolor(title = "Clock color")
        if color[1]:
            uFg = color[1]
            self.p_Clock.updateArc(uFg, uFg_0)
   



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Time")
    root.attributes("-topmost", True)
    root.attributes("-alpha", uTrlc)
    try:
        root.iconbitmap(r"C:\Users\Aurora Borealis\Desktop\GAM - test\cockbruh\icon.ico")
    except tk.TclError:
        pass

    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = (screen_w - uSize - 100)
    y = (screen_h - uSize - 100)
    root.geometry(f"{uSize + 12}x{uSize}+{x}+{y}")    

    app = theClock(root, _duration)

    root.mainloop()