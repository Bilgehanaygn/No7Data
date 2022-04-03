"""
Author: Quantum ERP
No7Data.com
"""

from tkinter import Button, Tk, LabelFrame, Label, BOTH, Y, LEFT
from PIL import ImageTk, Image
import src.compare_screen as compare_screen
import src.data_profiling_screen as data_profiling_screen
import src.file_manager as file_manager
import src.duplicate_screen.duplicate_screen as duplicate_screen
import src.concatenate_screen as concatenate_screen
import src.cleansing_screen as cleansing_screen
import src.create_reference_screen as create_reference_screen
import src.convert_screen as convert_screen


# initalise the tkinter GUI
root = Tk()
root.title('No7Data - Data Analysis V4.7')

img = ImageTk.PhotoImage(Image.open("images/No7Data.ico"))  # PIL solution
root.iconphoto(False, img)
img2 = ImageTk.PhotoImage(Image.open("images/No7Data.jpg").resize((300,200), Image.ANTIALIAS))
root.geometry("400x600")
root.pack_propagate(False) # tells the root to not let the widgets inside it determine its size.

##ICONS

cleaning_icon = ImageTk.PhotoImage(Image.open("images/cleaning_icon.jpg").resize((25,25)))



def display_image():

    # Create a Label Widget to display the text or Image
    label = Label(root, image = img2)
    label.pack()
    label.place(relx=0.125,rely=0, width=300, height=200)

    copyright_label = Label(text="Copyright No7Data.com - 2022")
    copyright_label.pack()
    copyright_label.place(relx=0.5,rely=0.92, anchor="center")
    

def profiling_screen_helper():
    profiling_instance = data_profiling_screen.Data_Profiling(file_manager_instance)
    profiling_instance.profiling_screen(root, img)

def compare_screen_helper():
    compare_instance = compare_screen.Compare(file_manager_instance)
    compare_instance.compare_screen(root, img)

def duplicate_screen_helper():
    duplicate_detector_instance = duplicate_screen.DuplicateDetector(file_manager_instance)
    duplicate_detector_instance.duplicate_screen(root, img)

def concatenate_screen_helper():
    concatenate_screen_instance = concatenate_screen.Concatenate(file_manager_instance)
    concatenate_screen_instance.concatenate_screen(root, img)


def cleansing_screen_helper():
    cleansing_screen_instance = cleansing_screen.Cleansing(file_manager_instance)
    cleansing_screen_instance.cleansing_screen(root, img)


def create_reference_screen_helper():
    create_reference_instance = create_reference_screen.CreateReference(file_manager_instance)
    create_reference_instance.create_reference_screen(root, img)

def convert_file_screen_helper():
    convert_file_instance = convert_screen.Convert(file_manager_instance)
    convert_file_instance.convert_screen(root, img)



file_manager_instance = file_manager.FileManager()
"""
def progress_bar_helper():
    file_manager_instance.progress_bar(root)
"""

display_image()

button_frame = LabelFrame(root)
button_frame.pack()
button_frame.place(relx=0.125, rely=0.375, width=300, height=300)

button_add = Button(button_frame, text="   Data Cleansing", command=cleansing_screen_helper, bg='#63C346',
image = cleaning_icon, compound=LEFT)
button_add.pack()
button_add.place(relx=0.05, rely=0.10, width=125, height=40, anchor="nw")

button_profiling = Button(button_frame, text="Data Profiling", command=profiling_screen_helper, bg='#5b86b0')
button_profiling.pack()
button_profiling.place(relx=0.95, rely=0.10, width=125, height=40, anchor="ne")

button_duplicates = Button(button_frame, text="Detect Duplicates", command=duplicate_screen_helper, bg='#5b86b0')
button_duplicates.pack()
button_duplicates.place(relx=0.05, rely=0.30, width=125, height=40, anchor="nw")

button_compare = Button(button_frame, text="Compare Files", command=compare_screen_helper, bg='#5b86b0')
button_compare.pack()
button_compare.place(relx=0.95, rely=0.30, width=125, height=40, anchor="ne")


button_cleansing = Button(button_frame, text="Concatenate Files", command=concatenate_screen_helper, bg='#5b86b0')
button_cleansing.pack()
button_cleansing.place(relx=0.95, rely=0.50, width=125, height=40, anchor="ne")

button_reference = Button(button_frame, text="Create A Dashboard", command=create_reference_screen_helper, bg='#5b86b0')
button_reference.pack()
button_reference.place(relx=0.05, rely=0.50, width=125, height=40, anchor="nw")


button_excel_to_csv = Button(button_frame, text="Convert File Format", command=convert_file_screen_helper, bg='#5b86b0')
button_excel_to_csv.pack()
button_excel_to_csv.place(relx=0.05, rely=0.70, width=125, height=40, anchor="nw")



"""
progress_button = Button(button_frame, text="Progress Bar", command=progress_bar_helper, bg='#5b86b0')
progress_button.pack()
progress_button.place(relx=0.95, rely=0.80, width=125, height=40, anchor="ne")
"""


root.mainloop()


# Copyright No7Data.com - 2022