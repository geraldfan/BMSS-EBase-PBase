import tkinter as tk  # python 3
from tkinter import font as tkfont, filedialog, BOTTOM, LEFT  # python 3
import PBase
import EBase


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, EBasePage, PBasePage, SuccessPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Select the database", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="EBase",
                            command=lambda: controller.show_frame("EBasePage"))
        button2 = tk.Button(self, text="PBase",
                            command=lambda: controller.show_frame("PBasePage"))
        button1.pack()
        button2.pack()


class EBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lastRowId_label = tk.Label(self, text="Last Row ID")
        ent_lastRowId = tk.Entry(self, width=50)
        lastColId_label = tk.Label(self, text="Last Col ID")
        ent_lastColId = tk.Entry(self, width=50)

        lastRowId_label.grid(row=0, column=0, sticky="e")
        ent_lastRowId.grid(row=0, column=1)
        lastColId_label.grid(row=1, column=0, sticky="e")
        ent_lastColId.grid(row=1, column=1)

        button = tk.Button(self, width=30, text="Select file and Add to database",
                           command=lambda: self.file_select(ent_lastRowId, ent_lastColId, controller))
        button.grid(row=2, column=0, sticky="sw")

        button = tk.Button(self, width=30, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=1, sticky="se")

    def file_select(self, ent_lastRowId, ent_lastColId, controller):
        root = tk.Tk()
        root.withdraw()
        fTyp = [('', '* .xlsx')]
        iDir = r'path to the folder you want to reference'
        filename = filedialog.askopenfilename(filetype=fTyp, initialdir=iDir)
        self.add_to_ebase(filename, ent_lastRowId.get(), ent_lastColId.get())
        controller.show_frame("SuccessPage")

    def add_to_ebase(self, filename, lastRowId, lastColId):
        EBase.read(filename, lastRowId, lastColId)


class PBasePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lastRowId_label = tk.Label(self, text="Last Row ID")
        ent_lastRowId = tk.Entry(self, width=50)
        sheet_label = tk.Label(self, text="Sheet name")
        ent_sheet = tk.Entry(self, width=50)

        lastRowId_label.grid(row=0, column=0, sticky="e")
        ent_lastRowId.grid(row=0, column=1)
        sheet_label.grid(row=1, column=0, sticky="e")
        ent_sheet.grid(row=1, column=1)


        button = tk.Button(self, width=30, text="Select file and Add to database",
                           command=lambda: self.file_select(ent_lastRowId, ent_sheet, controller))
        button.grid(row=2, column=0, sticky="sw")

        button = tk.Button(self, width=30, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=2, column=1, sticky="se")

    def file_select(self, ent_lastRowId, ent_sheet, controller):
        root = tk.Tk()
        root.withdraw()
        fTyp = [('', '* .xlsx')]
        iDir = r'path to the folder you want to reference'
        filename = filedialog.askopenfilename(filetype=fTyp, initialdir=iDir)
        self.add_to_ebase(filename, ent_lastRowId.get(), ent_sheet.get())
        controller.show_frame("SuccessPage")

    def add_to_ebase(self, filename, lastRowId, sheet):
        PBase.read(filename, lastRowId, sheet)

class SuccessPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Data added successfully.", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, width=20, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        exit_button = tk.Button(self, width=20, text="Exit",
                                command=lambda: self.quit())
        exit_button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
