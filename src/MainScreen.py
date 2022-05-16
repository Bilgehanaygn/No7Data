"""
Author: Quantum ERP
No7Data.com
"""

from tkinter import Button, Tk, LabelFrame, Label, BOTH, Y, LEFT, Entry
from tkinter.messagebox import showinfo, showerror
from PIL import ImageTk, Image
import src.compare_screen as compare_screen
import src.data_profiling_screen as data_profiling_screen
import src.data_profiling_screen_2 as data_profiling_screen_2
import src.file_manager as file_manager
import src.duplicate_screen.duplicate_screen as duplicate_screen
import src.concatenate_screen as concatenate_screen
import src.cleansing_screen as cleansing_screen
import src.convert_screen as convert_screen
import src.dashboard_screen as dashboard_screen
import src.supervised_screen as supervised_screen


class MainScreen:
    def __init__(self):
        # initalise the tkinter GUI
        self.root = Tk()
        self.root.title('No7Data - Customer Master')

        self.img = ImageTk.PhotoImage(Image.open("images/No7Data.ico"))  # PIL solution
        self.root.iconphoto(False, self.img)
        self.img2 = ImageTk.PhotoImage(Image.open("images/No7Data.jpg").resize((300,200), Image.ANTIALIAS))
        self.root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.

        self.predefined_key = ""

        self.root.geometry("600x600")

        # Create a Label Widget to display the text or Image
        label = Label(self.root, image = self.img2)
        label.pack()
        label.place(relx=0.25,rely=0, width=300, height=200)

        copyright_label = Label(text="Copyright No7Data.com - 2022")
        copyright_label.pack()
        copyright_label.place(relx=0.5,rely=0.92, anchor="center")

        self.button_frame = LabelFrame(self.root)
        self.button_frame.pack()
        self.button_frame.place(relx=0.083, rely=0.35, width=500, height=300)

        #create temporarily key frame
        self.key_frame = LabelFrame(self.button_frame, width=270, height=180)
        self.key_frame.pack()
        self.key_frame.place(relx=0.5, rely=0.5, anchor="center")


        label_file = Label(self.key_frame, text="Key:")
        label_file.pack()
        label_file.place(rely=0.4, relx=0.15)

        e = Entry(self.key_frame, show="*")
        e.pack()
        e.place(relx=0.27, rely=0.4)

        button1 = Button(self.key_frame, text="Enter", command= lambda: self.check_key(e.get()), bg='#5DADE2')
        button1.pack()
        button1.place(rely=0.55, relx=0.40, width=80, height=30)

        self.root.mainloop()


    def check_key(self, given_key):
        if given_key == self.predefined_key:
            self.key_frame.destroy()
            showinfo("Success","Success!")
            self.key_success()
        else:
            showerror("Incorrect key!", "Incorrect key!")
        

    def key_success(self):

        ##ICONS

        self.cleaning_icon = ImageTk.PhotoImage(Image.open("images/cleaning_icon.jpg").resize((25,25)))

        self.file_manager_instance = file_manager.FileManager()

        button_add = Button(self.button_frame, text="   Data Cleansing", command=self.cleansing_screen_helper, bg='#63C346',
        image = self.cleaning_icon, compound=LEFT)
        button_add.pack()
        button_add.place(relx=0.08, rely=0.10, width=125, height=40, anchor="nw")

        button_profiling = Button(self.button_frame, text="Data Profiling 1", command=self.profiling_screen_helper, bg='#85deff')
        button_profiling.pack()
        button_profiling.place(relx=0.37, rely=0.10, width=125, height=40, anchor="nw")

        button_profiling_2 = Button(self.button_frame, text="Data Profiling 2", command=self.profiling_screen_helper_2, bg='#85deff')
        button_profiling_2.pack()
        button_profiling_2.place(relx=0.92, rely=0.10, width=125, height=40, anchor="ne")

        button_duplicates = Button(self.button_frame, text="Detect Duplicates", command=self.duplicate_screen_helper, bg='#5b86b0')
        button_duplicates.pack()
        button_duplicates.place(relx=0.08, rely=0.30, width=125, height=40, anchor="nw")

        button_compare = Button(self.button_frame, text="Compare Files", command=self.compare_screen_helper, bg='#5b86b0')
        button_compare.pack()
        button_compare.place(relx=0.37, rely=0.30, width=125, height=40, anchor="nw")

        button_cleansing = Button(self.button_frame, text="Concatenate Files", command=self.concatenate_screen_helper, bg='#5b86b0')
        button_cleansing.pack()
        button_cleansing.place(relx=0.92, rely=0.30, width=125, height=40, anchor="ne")

        button_dashboard = Button(self.button_frame, text="Create A Dashboard", command=self.dashboard_screen_helper, bg='#5b86b0')
        button_dashboard.pack()
        button_dashboard.place(relx=0.08, rely=0.50, width=125, height=40, anchor="nw")

        button_excel_to_csv = Button(self.button_frame, text="Convert File Format", command=self.convert_file_screen_helper, bg='#5b86b0')
        button_excel_to_csv.pack()
        button_excel_to_csv.place(relx=0.37, rely=0.50, width=125, height=40, anchor="nw")

        button_supervised = Button(self.button_frame, text="Supervised", command=self.supervised_screen_helper, bg='#5b86b0')
        button_supervised.pack()
        button_supervised.place(relx=0.92, rely=0.50, width=125, height=40, anchor="ne")


        """
        progress_button = Button(self.button_frame, text="Progress Bar", command=self.progress_bar_helper, bg='#5b86b0')
        progress_button.pack()
        progress_button.place(relx=0.95, rely=0.80, width=125, height=40, anchor="ne")
        """
    

    def profiling_screen_helper(self):
        profiling_instance = data_profiling_screen.Data_Profiling(self.file_manager_instance)
        profiling_instance.profiling_screen(self.root, self.img)

    def profiling_screen_helper_2(self):
        profiling_instance_2 = data_profiling_screen_2.Data_Profiling(self.file_manager_instance)
        profiling_instance_2.profiling_screen(self.root, self.img)

    def compare_screen_helper(self):
        compare_instance = compare_screen.Compare(self.file_manager_instance)
        compare_instance.compare_screen(self.root, self.img)

    def duplicate_screen_helper(self):
        duplicate_detector_instance = duplicate_screen.DuplicateDetector(self.file_manager_instance)
        duplicate_detector_instance.duplicate_screen(self.root, self.img)

    def concatenate_screen_helper(self):
        concatenate_screen_instance = concatenate_screen.Concatenate(self.file_manager_instance)
        concatenate_screen_instance.concatenate_screen(self.root, self.img)


    def cleansing_screen_helper(self):
        cleansing_screen_instance = cleansing_screen.Cleansing(self.file_manager_instance)
        cleansing_screen_instance.cleansing_screen(self.root, self.img)


    def convert_file_screen_helper(self):
        convert_file_instance = convert_screen.Convert(self.file_manager_instance)
        convert_file_instance.convert_screen(self.root, self.img)

    def dashboard_screen_helper(self):
        dashboard_screen_instance = dashboard_screen.Dashboard(self.file_manager_instance)
        dashboard_screen_instance.dashboard_screen(self.root, self.img)

    def supervised_screen_helper(self):
        supervised_screen_instance = supervised_screen.Supervised(self.file_manager_instance)
        supervised_screen_instance.supervised_screen(self.root, self.img)
    
    """
    def progress_bar_helper(self):
        file_manager_instance.progress_bar(self.root)
    """


    # Copyright No7Data.com - 2022