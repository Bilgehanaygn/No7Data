"""
Author: Quantum ERP
No7Data.com
"""

from os import dup
from tkinter import Toplevel, LabelFrame, Button, Label, Entry, END
import pandas as pd
from tkinter.messagebox import showerror, showinfo
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import use

from src.duplicate_screen import search_screen
use('TkAgg')



class DuplicateDetector():

    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance
        self.file_loaded = False
        self.columns_specified = False
        self.e_columns = None
        self.given_cols_index = None
        self.frame_col_nums = None

    def stats_window(self):
        new = Toplevel(self.duplicate_screen)
        new.geometry("500x500")
        new.title("Stats Window")
                
        
        stats_frame = LabelFrame(new, text="Stats And Max Duplicate Data")
        stats_frame.pack()
        stats_frame.place(height=500, width=500)
        
        try:
            label1 = Label(stats_frame, text = ("Unique rows in dataset : " + str(self.is_duplicate.value_counts()[0])))
            label1.grid(row=0, column=0, sticky="w")
        except:
            label1 = Label(stats_frame, text = ("Unique rows in dataset : 0"))
            label1.grid(row=0, column=0, sticky="w")
        try:
            label2 = Label(stats_frame, text = ("Duplicate rows in dataset : " + str(self.is_duplicate.value_counts()[1])))
            label2.grid(row=1, column=0, sticky="w")
        except:
            label2 = Label(stats_frame, text = ("Duplicate rows in dataset : 0"))
            label2.grid(row=1, column=0, sticky="w")
        
        max_duplicate_data = self.duplicate_df.groupby([self.df.columns[i] for i in self.given_cols_index], dropna=False).size().idxmax()
        

        occurrence = self.duplicate_df.groupby([self.df.columns[i] for i in self.given_cols_index], dropna=False).size().max()
        
        iter = 0
        myText = ""
        for i in self.given_cols_index:
            myText = myText + (str(i+1) + ': ' + str(max_duplicate_data[iter]) + "\n")
            iter = iter + 1
        myText = 'Number Of Occurrence: ' + str(occurrence) + "\n" + myText
        myText = '--Max Duplicate Data--\n' + myText
        label3 = Label(stats_frame, text=myText)
        label3.grid(row=5, column=0)


    def get_duplicates(self):
        self.is_duplicate = self.df.duplicated(subset = [self.df.columns[i] for i in self.given_cols_index], keep=False)
        self.duplicate_df = self.df[self.is_duplicate]
        if(self.duplicate_df.shape[0] == 0):
            temp = pd.DataFrame({'Duplicates':'NO ANY DUPLICATE!'}, index=[0])
            self.file_manager.insert_tv(self.tv_1, temp)
        else:
            self.file_manager.insert_tv(self.tv_1, self.duplicate_df)


    def enable_stat_buttons(self):
        columns_nums_str = self.e_columns.get().strip().split(" ")
        column_index_given = []

        try:
            for i in columns_nums_str:
                if(int(i) > len(self.df.columns)):
                    raise Exception('apply index, get columns')

                column_index_given.append(int(i)-1)

            self.given_cols_index = column_index_given

            self.graph_button["state"] = "normal"
            self.stats_button["state"] = "normal"
            self.download_button["state"] = "normal"
            self.graph_button["bg"] = "#597b45"
            self.stats_button["bg"] = "#597b45"
            self.download_button["bg"] = "#597b45"

            self.get_duplicates()

        except:
            showerror("Index Error", "Given index is out of bounds", parent=self.duplicate_screen)
            return


    def download_duplicates(self):
        out_path = self.file_manager.dialog_download(self.duplicate_screen)
        if(out_path != ""):
            if(out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'xlsx' and out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'csv'):
                out_path = out_path + '.xlsx'
            else:
                if(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'xlsx'):      
                    showinfo("Success", "Excel file is downloading.", parent=self.duplicate_screen)
                    self.self.duplicate_df.to_excel(out_path, index=False)
                elif(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'csv'):
                    showinfo("Success", "CSV file is downloading.", parent=self.duplicate_screen)
                    self.duplicate_df.to_csv(out_path, index=False)
            showinfo("Success", "File downloaded.", parent=self.duplicate_screen)


    def func(self, pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:d}".format(absolute)


    def plot_graphs(self):
        plt.subplot(1, 2, 1)
        plt.pie(self.is_duplicate.value_counts(), labels=['Not Duplicate', 'Duplicate'],
        startangle=90, shadow=True,explode=(0.1, 0.1), autopct='%1.2f%%')
        plt.title('Percentage of duplicate rows \n', fontsize = 12)
        plt.axis('equal')

        plt.subplot(1,2,2)
        plt.pie(self.is_duplicate.value_counts(), labels=['Not Duplicate', 'Duplicate'],
        startangle=90, shadow=True,explode=(0.1, 0.1), autopct= lambda pct: self.func(pct, self.is_duplicate.value_counts()))
        plt.title('Number of duplicate rows \n', fontsize = 12)
        plt.axis('equal')
        
        plt.show()

    def bring_apply_field(self):
        apply_frame = LabelFrame(self.duplicate_screen, text="Apply Fields")
        apply_frame.pack()
        apply_frame.place(height=140, width=300, rely=0.975, relx=0.002, anchor="sw")

        Label(apply_frame, text="Field Numbers:").place(relx = 0.05, rely = 0.40, anchor = 'sw')
        apply_button = Button(apply_frame, text='Apply Fields', command = self.enable_stat_buttons, bg='#5b86b0')
        apply_button.pack()
        apply_button.place(relx = 0.55, rely = 0.70, anchor = 'sw')

        self.e_columns = Entry(apply_frame)

        def handle_click(event):
            self.e_columns.delete(0, END)

        self.e_columns.bind("<1>", handle_click)
        self.e_columns.place(relx = 0.40, rely = 0.40, anchor = 'sw')
        self.e_columns.insert(0, 'Ex:1 2 4 7')

        
    def init_search_screen(self):
        search_instance = search_screen.SearchScreen(self.file_manager, self.df)
        search_instance.search_screen(self.duplicate_screen)


    def bring_buttons(self):
        if(not self.frame_col_nums==None):
            self.file_manager.destroy_children(self.frame_col_nums)

        self.frame_col_nums = LabelFrame(self.duplicate_screen, text="Field Number -> Field Name")
        self.frame_col_nums.pack()
        self.frame_col_nums.place(height=610, width=500, rely= 0, relx = 0.998, anchor="ne")

        for i in range(len(self.df.columns)):
            label = Label(self.frame_col_nums, text = str(i+1) + " -> " + self.df.columns[i], anchor="nw")
            if(i<28):
                label.grid(sticky="w", row=i, column=0)
            elif(i>=28 and i<56):
                label.grid(sticky="w", row=i-28, column=1)
            elif(i>=56 and i<84):
                label.grid(sticky="w", row=i-56, column=2)
            elif(i>=84 and i<112):
                label.grid(sticky="w", row=i-84, column=3)

        self.bring_apply_field()

        self.buttons_frame = LabelFrame(self.duplicate_screen)
        self.buttons_frame.pack()
        self.buttons_frame.place(rely=0.975, relx=0.30, anchor="sw", height = 140, width=200)

        self.search_button = Button(self.buttons_frame, text='Search New Data\nFor Duplicate', command=self.init_search_screen, bg='#597b45', fg='white')
        self.search_button.pack()
        self.search_button.place(relx = 0.5, rely = 0.20, anchor = 'center')

        self.download_button = Button(self.buttons_frame, text='Download\nDuplicates', command=self.download_duplicates, 
        state="disabled", bg='#40E0D0', fg='white')
        self.download_button.pack()
        self.download_button.place(relx = 0.5, rely = 0.80, anchor = 'center', width=120)

        self.graph_button = Button(self.buttons_frame, text="Get Graphs", command=self.plot_graphs,
        state="disabled", bg='#40E0D0', fg='white')
        self.graph_button.pack()
        self.graph_button.place(relx = 0.10, rely = 0.43, anchor = 'nw')

        self.stats_button = Button(self.buttons_frame, text='Get Stats', command=self.stats_window,
        state="disabled", bg='#40E0D0', fg='white', padx=7)
        self.stats_button.pack()
        self.stats_button.place(relx = 0.90, rely = 0.43, anchor = 'ne')
        
        

    def load_helper(self, file_label):
        try:
            self.df = self.file_manager.load_data(file_label, self.duplicate_screen, show_success=True)
            self.file_manager.insert_tv(self.tv_1, self.df)
            self.bring_buttons()
        except:
            showerror("Information", "The file you have chosen is invalid", parent=self.duplicate_screen)
            return None



    def duplicate_screen(self, root):
        self.duplicate_screen = Toplevel(root)
        self.duplicate_screen.geometry("1350x650")
        self.duplicate_screen.title("Detect Duplicates")

        self.open_area_1 = self.file_manager.create_open_area(self.duplicate_screen, 80, 300, 0.002, 0.60, callback=self.load_helper)
        self.tv_1 = self.file_manager.create_treeview(self.duplicate_screen, 350, 650, 0.00, 0.00)

        
