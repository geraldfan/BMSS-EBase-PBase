import tkinter as tk  # python 3
from tkinter import font as tkfont, filedialog, BOTTOM, LEFT  # python 3
import PBase
import EBase


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("EBase/PBase")
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, EBasePage, PBasePage, PBaseExcelPage, PBaseEntryPage, PBaseEntryPageTwo,
                  PBaseEntryPageThree, SuccessPage):
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

    def get_page(self, page_class):
        return self.frames[page_class]


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
        label = tk.Label(self, text="Select method of entry", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        excelButton = tk.Button(self, text="Parse Excel",
                                command=lambda: controller.show_frame("PBaseExcelPage"))
        entryButton = tk.Button(self, text="Enter a new entry",
                                command=lambda: controller.show_frame("PBaseEntryPage"))
        excelButton.pack()
        entryButton.pack()


class PBaseEntryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name = tk.StringVar()
        self.name.set("")
        self.location = tk.StringVar()
        self.location.set("")
        self.plasmid_origin_antibiotics = tk.StringVar()
        self.plasmid_origin_antibiotics.set("")
        self.contributor = tk.StringVar()
        self.contributor.set("")
        self.dna_sequence = tk.StringVar()
        self.dna_sequence.set("")
        self.size = tk.StringVar()
        self.size.set("")
        self.benchling = tk.StringVar()
        self.benchling.set("")

        name_label = tk.Label(self, text="Name")
        ent_name = tk.Entry(self, textvariable=self.name, width=50)
        location_label = tk.Label(self, text="Location")
        ent_location = tk.Entry(self, textvariable=self.location, width=50)
        plasmid_origin_antibiotics_label = tk.Label(self, text="Plasmid Origin Antibiotics")
        ent_plasmid_origin_antibiotics = tk.Entry(self, textvariable=self.plasmid_origin_antibiotics, width=50)
        contributor_label = tk.Label(self, text="Contributor")
        ent_contributor = tk.Entry(self, width=50)
        dna_sequence_label = tk.Label(self, text="DNA Sequence")
        ent_dna_sequence = tk.Entry(self, textvariable=self.dna_sequence, width=50)
        size_label = tk.Label(self, text="Size")
        ent_size = tk.Entry(self, textvariable=self.size, width=50)
        benchling_label = tk.Label(self, text="Benchling")
        ent_benchling = tk.Entry(self, textvariable=self.benchling, width=50)

        name_label.grid(row=0, column=0, sticky="e")
        ent_name.grid(row=0, column=1)
        location_label.grid(row=1, column=0, sticky="e")
        ent_location.grid(row=1, column=1)
        plasmid_origin_antibiotics_label.grid(row=2, column=0, sticky="e")
        ent_plasmid_origin_antibiotics.grid(row=2, column=1)
        contributor_label.grid(row=3, column=0, sticky="e")
        ent_contributor.grid(row=3, column=1)
        dna_sequence_label.grid(row=5, column=0, sticky="e")
        ent_dna_sequence.grid(row=5, column=1)
        size_label.grid(row=6, column=0, sticky="e")
        ent_size.grid(row=6, column=1)
        benchling_label.grid(row=7, column=0, sticky="e")
        ent_benchling.grid(row=7, column=1)

        nextButton = tk.Button(self, width=30, text="Next",
                               command=lambda: controller.show_frame("PBaseEntryPageTwo"))
        nextButton.grid(row=8, column=0)
        button = tk.Button(self, width=30, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=8, column=1, sticky="se")

    def add_to_pbase(self, ent_name, ent_location, ent_plasmid_origin_antibiotics,
                     ent_contributor, ent_plasmid_details, ent_dna_sequence,
                     ent_size, ent_benchling, ent_reference, ent_quantity,
                     ent_remarks, ent_description, controller):
        PBase.read_entry(ent_name.get(), ent_location.get(), ent_plasmid_origin_antibiotics.get(),
                         ent_contributor.get(), ent_plasmid_details.get(), ent_dna_sequence.get(),
                         ent_size.get(), ent_benchling.get(), ent_reference.get(), ent_quantity.get(),
                         ent_remarks.get(), ent_description.get())

        controller.show_frame("SuccessPage")


class PBaseEntryPageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.set1_promoter = tk.StringVar()
        self.set1_promoter.set("")
        self.set1_rbs = tk.StringVar()
        self.set1_rbs.set("")
        self.set1_goi = tk.StringVar()
        self.set1_goi.set("")
        self.set1_terminator = tk.StringVar()
        self.set1_terminator.set("")
        self.set2_promoter = tk.StringVar()
        self.set2_promoter.set("")
        self.set2_rbs = tk.StringVar()
        self.set2_rbs.set("")
        self.set2_goi = tk.StringVar()
        self.set2_goi.set("")
        self.set2_terminator = tk.StringVar()
        self.set2_terminator.set("")
        self.set3_promoter = tk.StringVar()
        self.set3_promoter.set("")
        self.set3_rbs = tk.StringVar()
        self.set3_rbs.set("")
        self.set3_goi = tk.StringVar()
        self.set3_goi.set("")
        self.set3_terminator = tk.StringVar()
        self.set3_terminator.set("")

        set1_promoter_label = tk.Label(self, text="Set 1 Promoter")
        ent_set1_promoter = tk.Entry(self, textvariable=self.set1_promoter, width=50)
        set1_rbs_label = tk.Label(self, text="Set 1 RBS")
        ent_set1_rbs = tk.Entry(self, textvariable=self.set1_rbs, width=50)
        set1_goi_label = tk.Label(self, text="Set 1 GOI")
        ent_set1_goi = tk.Entry(self, textvariable=self.set1_goi, width=50)
        set1_terminator_label = tk.Label(self, text="Set 1 Terminator")
        ent_set1_terminator = tk.Entry(self, textvariable=self.set1_terminator, width=50)
        set2_promoter_label = tk.Label(self, text="Set 2 Promoter")
        ent_set2_promoter = tk.Entry(self, textvariable=self.set2_promoter, width=50)
        set2_rbs_label = tk.Label(self, text="Set 2 RBS")
        ent_set2_rbs = tk.Entry(self, textvariable=self.set2_rbs, width=50)
        set2_goi_label = tk.Label(self, text="Set 2 GOI")
        ent_set2_goi = tk.Entry(self, textvariable=self.set2_goi, width=50)
        set2_terminator_label = tk.Label(self, text="Set 2 Terminator")
        ent_set2_terminator = tk.Entry(self, textvariable=self.set2_terminator, width=50)
        set3_promoter_label = tk.Label(self, text="Set 3 Promoter")
        ent_set3_promoter = tk.Entry(self, textvariable=self.set3_promoter, width=50)
        set3_rbs_label = tk.Label(self, text="Set 3 RBS")
        ent_set3_rbs = tk.Entry(self, textvariable=self.set3_rbs, width=50)
        set3_goi_label = tk.Label(self, text="Set 3 GOI")
        ent_set3_goi = tk.Entry(self, textvariable=self.set3_goi, width=50)
        set3_terminator_label = tk.Label(self, text="Set 3 Terminator")
        ent_set3_terminator = tk.Entry(self, textvariable=self.set3_terminator, width=50)

        set1_promoter_label.grid(row=0, column=0, sticky="e")
        ent_set1_promoter.grid(row=0, column=1)
        set1_rbs_label.grid(row=1, column=0, sticky="e")
        ent_set1_rbs.grid(row=1, column=1)
        set1_goi_label.grid(row=2, column=0, sticky="e")
        ent_set1_goi.grid(row=2, column=1)
        set1_terminator_label.grid(row=3, column=0, sticky="e")
        ent_set1_terminator.grid(row=3, column=1)
        set2_promoter_label.grid(row=4, column=0, sticky="e")
        ent_set2_promoter.grid(row=4, column=1)
        set2_rbs_label.grid(row=5, column=0, sticky="e")
        ent_set2_rbs.grid(row=5, column=1)
        set2_goi_label.grid(row=6, column=0, sticky="e")
        ent_set2_goi.grid(row=6, column=1)
        set2_terminator_label.grid(row=7, column=0, sticky="e")
        ent_set2_terminator.grid(row=7, column=1)
        set3_promoter_label.grid(row=8, column=0, sticky="e")
        ent_set3_promoter.grid(row=8, column=1)
        set3_rbs_label.grid(row=9, column=0, sticky="e")
        ent_set3_rbs.grid(row=9, column=1)
        set3_goi_label.grid(row=10, column=0, sticky="e")
        ent_set3_goi.grid(row=10, column=1)
        set3_terminator_label.grid(row=11, column=0, sticky="e")
        ent_set3_terminator.grid(row=11, column=1)

        button = tk.Button(self, width=30, text="Next",
                           command=lambda: controller.show_frame("PBaseEntryPageThree"))
        button.grid(row=12, column=0, sticky="sw")

        button = tk.Button(self, width=30, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=12, column=1, sticky="se")


class PBaseEntryPageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.reference = tk.StringVar()
        self.reference.set("")
        self.quantity = tk.StringVar()
        self.quantity.set("")
        self.remarks = tk.StringVar()
        self.remarks.set("")
        self.description = tk.StringVar()
        self.description.set("")
        page1 = self.controller.get_page("PBaseEntryPage")
        page2 = self.controller.get_page("PBaseEntryPageTwo")

        reference_label = tk.Label(self, text="References/Publication")
        ent_reference = tk.Entry(self, textvariable=self.reference, width=50)
        quantity_label = tk.Label(self, text="Quantity")
        ent_quantity = tk.Entry(self, textvariable=self.quantity, width=50)
        remarks_label = tk.Label(self, text="Remarks")
        ent_remarks = tk.Entry(self, textvariable=self.remarks, width=50)
        description_label = tk.Label(self, text="Description/Purpose")
        ent_description = tk.Entry(self, textvariable=self.description, width=50)

        reference_label.grid(row=0, column=0, sticky="e")
        ent_reference.grid(row=0, column=1)
        quantity_label.grid(row=1, column=0, sticky="e")
        ent_quantity.grid(row=1, column=1)
        remarks_label.grid(row=2, column=0, sticky="e")
        ent_remarks.grid(row=2, column=1)
        description_label.grid(row=3, column=0, sticky="e")
        ent_description.grid(row=3, column=1)

        button = tk.Button(self, width=30, text="Add to database",
                           command=lambda: self.add_to_pbase(controller, page1, page2, ent_reference.get(),
                                                             ent_quantity.get(), ent_remarks.get(),
                                                             ent_description.get()))
        button.grid(row=4, column=0, sticky="sw")

        button = tk.Button(self, width=30, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=4, column=1, sticky="se")

    def add_to_pbase(self, controller, page1, page2, reference, quantity, remarks, description):
        plasmid_details = self.create_plasmid_details_dict(controller, page2)

        PBase.read_entry(page1.name.get(), page1.location.get(), page1.plasmid_origin_antibiotics.get(),
                         page1.contributor.get(), str(plasmid_details), page1.dna_sequence.get(), page1.size.get(),
                         page1.benchling.get(), reference, quantity, remarks, description)
        controller.show_frame("SuccessPage")

    def create_plasmid_details_dict(self, controller, page2):
        plasmid_details_dict = {}
        set1 = []
        set2 = []
        set3 = []
        set1_nested = {}
        set2_nested = {}
        set3_nested = {}

        set1_nested['Promoter'] = page2.set1_promoter.get()
        set1_nested['RBS'] = page2.set1_rbs.get()
        set1_nested['GOI'] = page2.set1_goi.get()
        set1_nested['Terminator'] = page2.set1_terminator.get()
        set1.append(set1_nested)
        set2_nested['Promoter'] = page2.set2_promoter.get()
        set2_nested['RBS'] = page2.set2_rbs.get()
        set2_nested['GOI'] = page2.set2_goi.get()
        set2_nested['Terminator'] = page2.set2_terminator.get()
        set2.append(set2_nested)
        set3_nested['Promoter'] = page2.set3_promoter.get()
        set3_nested['RBS'] = page2.set3_rbs.get()
        set3_nested['GOI'] = page2.set3_goi.get()
        set3_nested['Terminator'] = page2.set3_terminator.get()
        set3.append(set3_nested)

        for variable in ["set1", "set2", "set3"]:
            plasmid_details_dict[variable] = eval(variable)

        return plasmid_details_dict


class PBaseExcelPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        lastRowId_label = tk.Label(self, text="Last Row ID")
        ent_lastRowId = tk.Entry(self, width=50)
        sheet_label = tk.Label(self, text="Sheet name")
        ent_sheet = tk.Entry(self, width=50)
        contributor_label = tk.Label(self, text="Contributor")
        ent_contributor = tk.Entry(self, width=50)

        lastRowId_label.grid(row=0, column=0, sticky="e")
        ent_lastRowId.grid(row=0, column=1)
        sheet_label.grid(row=1, column=0, sticky="e")
        ent_sheet.grid(row=1, column=1)
        contributor_label.grid(row=2, column=0, sticky="e")
        ent_contributor.grid(row=2, column=1, sticky="e")

        button = tk.Button(self, width=30, text="Select file and Add to database",
                           command=lambda: self.file_select(ent_lastRowId, ent_sheet, ent_contributor, controller))
        button.grid(row=3, column=0, sticky="sw")

        button = tk.Button(self, width=30, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3, column=1, sticky="se")

    def file_select(self, ent_lastRowId, ent_sheet, ent_contributor, controller):
        root = tk.Tk()
        root.withdraw()
        fTyp = [('', '* .xlsx')]
        iDir = r'path to the folder you want to reference'
        filename = filedialog.askopenfilename(filetype=fTyp, initialdir=iDir)
        self.add_to_pbase(filename, ent_lastRowId.get(), ent_sheet.get(), ent_contributor.get())
        controller.show_frame("SuccessPage")

    def add_to_pbase(self, filename, lastRowId, sheet, contributor):
        PBase.read(filename, lastRowId, sheet, contributor)


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
