from tkinter import Toplevel, LabelFrame, Label, Entry, END, Button
from tkinter.messagebox import showerror, showinfo
import pandas as pd


class Cleansing():
    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance
        self.difference= ""
        self.last_process= "-"
        self.field_selected = False
        self.selected_columns = []
        self.data_loaded = False
        self.removed_df_exist = False

    def convert_to_str(self):
        if(self.field_selected):
            if(not self.df.empty):
                try:
                    self.pre_df = self.df.copy()
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(str) 
                    showinfo("Success", "Successfully converted.", parent=self.cleansing_screen)
                    self.file_manager.insert_tv(self.tv_c_1,self.df)
                    self.difference = "-"
                    self.last_process = 'Convert to String'
                    self.bring_answer_frame()
                except:
                    showerror("Error", "Error while converting to string!", parent=self.cleansing_screen)

    def convert_to_int(self):
        if(self.field_selected):
            if(not self.df.empty):
                try:
                    self.pre_df = self.df.copy()
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(float) 
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].fillna(-1)
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype("Int32") 
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(str)
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].replace('-1', "nan")
                    
                    showinfo("Success", "Successfully converted.", parent=self.cleansing_screen)
                    self.file_manager.insert_tv(self.tv_c_1,self.df)
                    self.difference = "-"
                    self.last_process = 'Convert to Integer'
                    self.bring_answer_frame()
                except:
                    showerror("Error", "Given fields contains alphanumeric values!", parent=self.cleansing_screen)

    def convert_to_float(self):
        if(self.field_selected):
            if(not self.df.empty):
                try:
                    self.pre_df = self.df.copy()
                    self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(float) 
                    showinfo("Success", "Successfully converted.", parent=self.cleansing_screen)
                    self.file_manager.insert_tv(self.tv_c_1,self.df)
                    self.difference = "-"
                    self.last_process = 'Convert to Float'
                    self.bring_answer_frame()
                except:
                    showerror("Error", "Given fields contains alphanumeric values!", parent=self.cleansing_screen)

    
    def remove_nans(self):
        if(self.field_selected):
            if(not self.df.empty):
                def contains_nan(row):
                    for i in row:
                        if(i=="nan"):
                            return False
                        if(pd.isna(i)):
                            return False
                    return True
            
                i0 = pd.MultiIndex.from_frame(self.df) # before action
                self.pre_df = self.df.copy() # copy old df
                count1 = self.df.shape[0]
                self.df = self.df[[contains_nan(i) for i in self.df[self.selected_columns].values]]
                self.file_manager.insert_tv(self.tv_c_1, self.df)
                self.difference = str(count1-self.df.shape[0])
                self.last_process = 'Remove NaNs'
                i1 = pd.MultiIndex.from_frame(self.df) # after action
                self.removed_df = self.pre_df[~i0.isin(i1)] # before after difference
                self.removed_df_exist = True
                self.bring_answer_frame()



    def fill_nans_zero(self):
        if(self.field_selected):
            if(not self.df.empty):
                self.pre_df = self.df.copy()
                self.df[self.selected_columns] = self.df[self.selected_columns].replace('nan',0)
                self.file_manager.insert_tv(self.tv_c_1, self.df)
                self.difference = "-"
                self.last_process = 'Fill NaNs With "0"'
                self.bring_answer_frame()

    def fill_nans_str(self):
        if(self.field_selected):
            if(not self.df.empty):
                self.pre_df = self.df.copy()
                self.df[self.selected_columns] = self.df[self.selected_columns].replace('nan', ' ')
                self.file_manager.insert_tv(self.tv_c_1, self.df)
                self.difference = "-"
                self.last_process = 'Fill NaNs With " "'
                self.bring_answer_frame()


    def duplicates_first(self):
        if(self.field_selected):
            if(not self.df.empty):
                i0 = pd.MultiIndex.from_frame(self.df) # before action
                self.pre_df = self.df.copy() # copy old df
                count1 = self.df.shape[0]
                self.df.drop_duplicates(subset=self.selected_columns, keep="first", inplace=True)
                self.file_manager.insert_tv(self.tv_c_1, self.df)
                self.difference = str(count1-self.df.shape[0])
                self.last_process = "Remove Duplicates (Keep First Occurrence)"
                i1 = pd.MultiIndex.from_frame(self.df) # after action
                self.removed_df = self.pre_df[~i0.isin(i1)] # before after difference
                self.removed_df_exist = True
                self.bring_answer_frame()

    def duplicates_last(self):
        if(self.field_selected):
            if(not self.df.empty):
                i0 = pd.MultiIndex.from_frame(self.df) # before action
                self.pre_df = self.df.copy() # copy old df
                count1 = self.df.shape[0]
                self.df.drop_duplicates(subset=self.selected_columns, keep="last", inplace=True)
                self.file_manager.insert_tv(self.tv_c_1, self.df)
                self.difference = str(count1-self.df.shape[0])
                self.last_process = "Remove Duplicates (Keep Last Occurrence)"
                i1 = pd.MultiIndex.from_frame(self.df) # after action
                self.removed_df = self.pre_df[~i0.isin(i1)] # before after difference
                self.removed_df_exist = True
                self.bring_answer_frame()

    def duplicates_all(self):
        if(self.field_selected):
            if(not self.df.empty):
                i0 = pd.MultiIndex.from_frame(self.df) # before action
                self.pre_df = self.df.copy() # copy old df
                count1 = self.df.shape[0]
                self.df.drop_duplicates(subset=self.selected_columns, keep=False, inplace=True)
                self.file_manager.insert_tv(self.tv_c_1, self.df)
                self.difference = str(count1-self.df.shape[0])
                self.last_process = "Remove Duplicates (Don't Keep Any)"
                i1 = pd.MultiIndex.from_frame(self.df) # after action
                self.removed_df = self.pre_df[~i0.isin(i1)] # before after difference
                self.removed_df_exist = True
                self.bring_answer_frame()




    def download_removed_helper(self):
        if(self.removed_df_exist):
            out_path = self.file_manager.dialog_download(self.cleansing_screen)
            self.file_manager.download_file(self.cleansing_screen, self.removed_df, out_path)




    def download_cleaned(self):
        out_path = self.file_manager.dialog_download(self.cleansing_screen)
        if(out_path != ""):
            if("." in out_path):
                if(out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'xlsx' and out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'csv'):
                    out_path = out_path + '.xlsx'
                    self.df.to_excel(out_path, index=False)
                else:
                    if(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'xlsx'):      
                        
                        self.df.to_excel(out_path, index=False)
                        showinfo("Success", "Excel file is downloading.", parent=self.cleansing_screen)
                    elif(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'csv'):
                        self.df.to_csv(out_path, index=False)
                        showinfo("Success", "CSV file is downloading.", parent=self.cleansing_screen)
            else:
                out_path = out_path + '.xlsx'
                self.df.to_excel(out_path, index=False)
                showinfo("Success", "Excel file is downloading.", parent=self.cleansing_screen)
            showinfo("Success", "File downloaded.", parent=self.cleansing_screen)
    

    def bring_answer_frame(self):
        self.label1["text"] = "Last Process: " + self.last_process
        self.label2["text"] = "Removed Rows: " + self.difference

    
    def select_fields_some(self):
        if(self.data_loaded):
            columns_nums_str = self.e_columns.get().strip().split(" ")
            column_index_given = []
        
            try:
                for i in columns_nums_str:
                    if(int(i) > len(self.df.columns)):
                        raise Exception('apply index, get columns')

                    column_index_given.append(int(i)-1)

                self.given_cols_index = column_index_given
                self.selected_columns = [self.df.columns[i] for i in self.given_cols_index]

                self.selected_fields_text = "".join([str(elem)+"-" for elem in columns_nums_str])
                self.selected_fields_text = self.selected_fields_text[0:len(self.selected_fields_text)-1]
                self.selected_fields_text = "Selected Fields: " + self.selected_fields_text

                self.selected_fields_label["text"] = self.selected_fields_text
                self.selected_fields_label["fg"] = "black"
                self.field_selected = True
            
            except:
                showerror("Index Error", "Given index is out of bounds.", parent=self.cleansing_screen)
                return
            
    def undo(self):
        self.df = self.pre_df
        self.file_manager.insert_tv(self.tv_c_1, self.df)
        #change last process data
        self.label1["text"] = "Last Process: -"
        self.label2["text"] = "Removed Rows: "



    def select_fields_all(self):
        if(self.data_loaded):
            self.given_cols_index = []
            for i in range(self.df.shape[1]):
                self.given_cols_index.append(i)
            self.selected_columns = [self.df.columns[i] for i in self.given_cols_index]
            self.selected_fields_label["text"] = "Selected Fields: All Fields"
            self.selected_fields_label["fg"] = "black"
            self.field_selected = True


    def bring_column_nums(self):
        if(self.data_loaded):
            self.column_screen = Toplevel(self.cleansing_screen)
            self.column_screen.geometry("750x600")
            self.column_screen.title("Field Numbers")

            #Destroy childrens before adding new column names
            self.file_manager.destroy_children(self.column_screen)

            column_numbers = LabelFrame(self.column_screen, text="Field Numbers -> Field Names")
            column_numbers.pack()
            column_numbers.place(height=550, width=720, relx=0.02,rely=0.035, anchor="nw")

            #Add new column names
            for i in range(len(self.df.columns)):
                label = Label(column_numbers, text = str(i+1) + " -> " + self.df.columns[i], anchor="nw")
                if(i<25):
                    label.grid(sticky="w", row=i, column=0)
                elif(i>=25 and i<50):
                    label.grid(sticky="w", row=i-25, column=1)
                elif(i>=50 and i<75):
                    label.grid(sticky="w", row=i-50, column=2)
                elif(i>=75 and i<100):
                    label.grid(sticky="w", row=i-75, column=3)



    def load_data_helper(self, file_label):
        self.df = self.file_manager.load_data(file_label, self.cleansing_screen, True)
        self.label_shape['text'] = str(self.df.shape[0]) + " rows uploaded."
        self.file_manager.insert_tv(self.tv_c_1, self.df)
        
        self.data_loaded = True
        self.field_selected = False
        self.selected_fields_label["text"] = "Selected Fields: No Field Selected!"
        self.selected_fields_label["font"] = ('Helvatical bold',13)
        self.selected_fields_label["fg"] = "red"
        self.label1["text"] = "Last Process: -"
        self.label2["text"] = "Removed Rows: "
        self.e_columns.delete(0, END)
        self.e_columns.insert(0, 'Ex:1 2 4 7')

    def find_nans(self):
        print('will fill')
        


    def cleansing_screen(self, root, img):
        self.cleansing_screen = Toplevel(root)
        self.cleansing_screen.geometry("1350x650")
        self.cleansing_screen.title("Data Cleansing")
        self.cleansing_screen.iconphoto(False, img)

        self.open_area_1 = self.file_manager.create_open_area(self.cleansing_screen, 80, 320, 0, 0.64, 
        frame_text="Upload File", callback=self.load_data_helper)
        self.tv_c_1 = self.file_manager.create_treeview(self.cleansing_screen, 400, 700, 0, 0, frame_text="Data Frame")

        self.selected_fields_label = Label(self.cleansing_screen, text="Selected Fields: No Field Selected!", font=('Helvatical bold',13), fg="red")
        self.selected_fields_label.pack()
        self.selected_fields_label.place(relx = 0.65, rely = 0.06)

        self.answer_frame = LabelFrame(self.cleansing_screen)
        self.answer_frame.pack()
        self.answer_frame.place(height=150, width=500, relx=0.60, rely=0.70, anchor="nw")
        
        self.label1 = Label(self.answer_frame, text="Last Process: " + self.last_process, font=('Helvatical bold',11))
        self.label1.pack()
        self.label1.place(relx=0.025, rely=0.10)
        
        self.label2 = Label(self.answer_frame, text="Removed Rows: " + self.difference, font=('Helvatical bold',11))
        self.label2.pack()
        self.label2.place(relx=0.025, rely=0.35)
        self.answer_frame_exist=True

        self.download_button = Button(self.answer_frame, text='Download\nCleansed Data', command=self.download_cleaned, 
        bg='#597b45', fg='white')
        self.download_button.pack()
        self.download_button.place(relx = 0.075, rely = 0.60, width=125, height=40, anchor = 'nw')

        self.download_button = Button(self.answer_frame, text='Download\nRemoved Data', command=self.download_removed_helper, 
        bg='#597b45', fg='white')
        self.download_button.pack()
        self.download_button.place(relx = 0.375, rely = 0.60, width=125, height=40, anchor = 'nw')

        self.undo_button = Button(self.answer_frame, text='Undo', command=self.undo, 
        bg='#597b45', fg='white')
        self.undo_button.pack()
        self.undo_button.place(relx = 0.675, rely = 0.60, width=125, height=40, anchor = 'nw')

        self.cleansing_buttons_frame = LabelFrame(self.cleansing_screen)
        self.cleansing_buttons_frame.pack()
        self.cleansing_buttons_frame.place(height=300, width=550, relx=0.55,rely=0.15, anchor="nw")

        ##Convert buttons
        
        convert_str_button = Button(self.cleansing_buttons_frame, text='Convert to String', command=self.convert_to_str, bg='#5b86b0')
        convert_str_button.pack()
        convert_str_button.place(relx = 0.075, rely = 0.10, width=125, height=40, anchor = 'nw')

        convert_int_button = Button(self.cleansing_buttons_frame, text='Convert to Integer', command=self.convert_to_int, bg='#5b86b0')
        convert_int_button.pack()
        convert_int_button.place(relx = 0.375, rely = 0.10, width=125, height=40,anchor = 'nw')

        convert_float_button = Button(self.cleansing_buttons_frame, text='Convert to Float', command=self.convert_to_float, bg='#5b86b0')
        convert_float_button.pack()
        convert_float_button.place(relx = 0.675, rely = 0.10, width=125, height=40,anchor = 'nw')

        ##NAN HANDLING

        remove_nan_button = Button(self.cleansing_buttons_frame, text="Remove NaNs", command=self.remove_nans, bg='#5b86b0')
        remove_nan_button.pack()
        remove_nan_button.place(relx = 0.075, rely = 0.30, width=125, height=40, anchor = 'nw')

        convert_int_button = Button(self.cleansing_buttons_frame, text='Fill NaNs with 0', command=self.fill_nans_zero, bg='#5b86b0')
        convert_int_button.pack()
        convert_int_button.place(relx = 0.375, rely = 0.30, width=125, height=40,anchor = 'nw')

        convert_float_button = Button(self.cleansing_buttons_frame, text='Fill NaNs with " "', command=self.fill_nans_str, bg='#5b86b0')
        convert_float_button.pack()
        convert_float_button.place(relx = 0.675, rely = 0.30, width=125, height=40,anchor = 'nw')

        ##DUPLICATES HANDLING

        remove_duplicates_first = Button(self.cleansing_buttons_frame, text="Remove Duplicates\n(Keep First Occurence)", command=self.duplicates_first, bg='#5b86b0')
        remove_duplicates_first.pack()
        remove_duplicates_first.place(relx = 0.075, rely = 0.50, width=125, height=40, anchor = 'nw')

        remove_duplicates_last = Button(self.cleansing_buttons_frame, text="Remove Duplicates\n(Keep Last Occurence)", command=self.duplicates_last, bg='#5b86b0')
        remove_duplicates_last.pack()
        remove_duplicates_last.place(relx = 0.375, rely = 0.50, width=125, height=40,anchor = 'nw')

        remove_duplicates_all = Button(self.cleansing_buttons_frame, text="Remove Duplicates\n(Don't Keep Any)", command=self.duplicates_all, bg='#5b86b0')
        remove_duplicates_all.pack()
        remove_duplicates_all.place(relx = 0.675, rely = 0.50, width=125, height=40,anchor = 'nw')


        find_nan_button = Button(self.cleansing_buttons_frame, text="Find NaNs", command=self.find_nans, bg='#5b86b0')
        find_nan_button.pack()
        find_nan_button.place(relx = 0.075, rely = 0.70, width=125, height=40, anchor = 'nw')


        apply_frame = LabelFrame(self.cleansing_screen, text="Select Fields")
        apply_frame.pack()
        apply_frame.place(height=150, width=285, relx=0.28, rely=0.64)
        
        Label(apply_frame, text="Field Numbers:").place(relx = 0.05, rely = 0.20, anchor = 'sw')

        Label(apply_frame, text='To select all fields, tap to "Select All".').place(relx = 0.05, rely = 0.95, anchor = 'sw')


        self.e_columns = Entry(apply_frame)

        def handle_click(event):
            self.e_columns.delete(0, END)

        self.e_columns.bind("<1>", handle_click)
        self.e_columns.place(relx = 0.40, rely = 0.20, anchor = 'sw')
        self.e_columns.insert(0, 'Ex:1 2 4 7')

        apply_button = Button(apply_frame, text='Apply Fields', command=self.select_fields_some, bg='#5b86b0')
        apply_button.pack()
        apply_button.place(relx = 0.57, rely = 0.45, anchor = 'sw')

        self.select_all_fields_button = Button(apply_frame, text='Select All Fields', command=self.select_fields_all, bg='#5b86b0')
        self.select_all_fields_button.pack()
        self.select_all_fields_button.place(relx = 0.05, rely = 0.45, anchor = 'sw')

        self.show_columns_button = Button(apply_frame, text='Show Fields', command=self.bring_column_nums, bg='#5b86b0')
        self.show_columns_button.pack()
        self.show_columns_button.place(relx = 0.05, rely = 0.70, anchor = 'sw')

        self.label_shape = Label(self.cleansing_screen, text = ("- Rows Uploaded."))
        self.label_shape.pack()
        self.label_shape.place(relx=0, rely=0.78)
