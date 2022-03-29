from cProfile import label
from concurrent.futures import thread
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, ttk
from tkinter.messagebox import showinfo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import webbrowser
#from pandas_profiling import ProfileReport
#import pandas_profiling
import sweetviz as sv


class Data_Profiling:
    def __init__(self):
        self.label_file = None
        self.given_cols_index = None
        self.reset = True
        self.button_added = False
        self.field_frame = None
        
        

    def profiling_screen(self, root):
        self.profiling_screen = tk.Toplevel(root)
        self.profiling_screen.geometry("650x450")
        self.profiling_screen.title("Data Profiling")

        #OPEN AREA 1


        # Frame for open file dialog
        file_frame_1 = tk.LabelFrame(self.profiling_screen, text="Upload File")
        file_frame_1.place(height=80, width=285, rely=0.60, relx=0.025)

        # The file/file path text
        label_file_1 = ttk.Label(file_frame_1, text="No File Selected")
        label_file_1.place(rely=0, relx=0)

        # Buttons
        button1 = tk.Button(file_frame_1, text="Browse A File", command=lambda: self.file_dialog(label_file_1), bg='#5b86b0')
        button1.place(rely=0.46, relx=0.50)

        button2 = tk.Button(file_frame_1, text="Load A File", command=lambda: self.load_data(label_file_1), bg='#5b86b0')
        button2.place(rely=0.46, relx=0.15)

    """
    def profiling_report(self):
        
        if(self.reset):
            #profile = ProfileReport(self.df)
            profile = self.df.profile_report(title='NO7Data Profiling Report')
        else:
            #profile= ProfileReport(self.df)
            profile = self.df.iloc[:,self.given_cols_index].profile_report(title='NO7Data Profiling Report')
   
        # save the report as html file
        profile.to_file(output_file="NO7DataProfilingReport1.html")

        profile.to_file(output_file="NO7DataProfilingReport2.json")

        url = "NO7DataProfilingReport1.html"
        webbrowser.open(url)
    """

    def profiling_report(self):
        if(self.reset):
            report = sv.analyze(self.df)

        else:
            report = sv.analyze(self.df.iloc[:,self.given_cols_index])

        report.show_html('NO7DataProfilingReport.html')
    

    def reset_fields(self):
        self.reset = True
        e_columns.delete(0, tk.END)

    
    def apply_new_columns(self):
        columns_nums_str = e_columns.get().strip().split(" ")
        column_index_given = []


        try:
            for i in columns_nums_str:
                if(self.df.shape[1] < int(i)):
                    raise Exception("exception")
                else:
                    column_index_given.append(int(i)-1)
            self.given_cols_index = column_index_given

            self.reset = False
            
            if(not self.button_added):
                button_reset = tk.Button(self.profiling_screen, text="Reset Fields", command = self.reset_fields, padx=2, pady=5, bg='#597b45', fg='white')
                button_reset.pack()
                button_reset.place(rely=0.805,relx=0.785)
                self.button_added = True

        except:
            tk.messagebox.showerror("Index Error", "Given index is out of bounds.", parent=self.profiling_screen)

    
    def bring_fields(self):
        self.field_frame = tk.LabelFrame(self.profiling_screen, text="Column Numbers -> Column Names")
        self.field_frame.pack()
        self.field_frame.place(height=250, width=620, relx=0.025,rely=0.01, anchor="nw")

        for i in range(len(self.df.columns)):
            label = tk.Label(self.field_frame, text = str(i+1) + " -> " + self.df.columns[i], anchor="nw")
            if(i<11):
                label.grid(sticky="w", row=i, column=0)
            elif(i>=11 and i<22):
                label.grid(sticky="w", row=i-11, column=1)
            elif(i>=22 and i<33):
                label.grid(sticky="w", row=i-22, column=2)
            elif(i>=33 and i<44):
                label.grid(sticky="w", row=i-33, column=3)
            elif(i>=44 and i<55):        
                label.grid(sticky="w", row=i-44, column=4)


    def file_dialog(self, label_file):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        filename = filedialog.askopenfilename(initialdir="/", parent=self.profiling_screen,
                                            title="Select A File",
                                            filetype=(("xlsx files", "*.xlsx"),("All Files", "*.*")))
        label_file["text"] = filename
        return None

    def load_data(self, label_file):
        """If the file selected is valid this will load the file into the Treeview"""
        showinfo("Loading", "Excel file is loading, wait until loading is done.", parent=self.profiling_screen)
        file_path = label_file["text"]
        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".csv":
                self.df = pd.read_excel(excel_filename)
            else:
                self.df = pd.read_excel(excel_filename)
            
           

            showinfo("Success", "Loaded successfully.", parent=self.profiling_screen)
            button2 = tk.Button(self.profiling_screen, text="Report", command=self.profiling_report, padx=5, pady=5, bg='#597b45', fg='white')
            button2.pack()
            button2.place(relx = 0.09, rely = 0.80)

            self.apply_frame = tk.LabelFrame(self.profiling_screen, text="Apply Fields")
            self.apply_frame.pack()
            self.apply_frame.place(height=80, width=285, rely=0.60, relx=0.53)
            
            tk.Label(self.apply_frame, text="Field Numbers:").place(relx = 0.05, rely = 0.40, anchor = 'sw')


            global e_columns
            e_columns = tk.Entry(self.apply_frame)

            def handle_click(event):
                e_columns.delete(0, tk.END)

            e_columns.bind("<1>", handle_click)
            e_columns.place(relx = 0.40, rely = 0.40, anchor = 'sw')
            e_columns.insert(0, 'Ex:1 2 4 7')


            button1 = tk.Button(self.apply_frame, text="Apply Fields", command= self.apply_new_columns, bg='#5b86b0')
            button1.pack()
            button1.place(relx=0.58, rely=0.525, anchor='nw')

            self.bring_fields()




        except ValueError:
            tk.messagebox.showerror("Information", "The file you have chosen is invalid", parent=self.profiling_screen)
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Information", f"No such file as {file_path}", parent=self.profiling_screen)
            return None