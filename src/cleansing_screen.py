from tkinter import Toplevel, LabelFrame, Label, Entry, END, Button
from tkinter.messagebox import showerror, showinfo


class Cleansing():
    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance
        self.column_screen = None
        self.selected_fields_label = None
        self.cleansing_buttons_exist = False


    def convert_to_str(self):
        try:
            self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(str) 
            showinfo("Success", "Successfully converted.", parent=self.cleansing_screen)
            self.file_manager.insert_tv(self.tv_c_1,self.df)
        except:
            showerror("Error", "Error while converting to string!", parent=self.cleansing_screen)

    def convert_to_int(self):
        try:
            self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(int) 
            showinfo("Success", "Successfully converted.", parent=self.cleansing_screen)
            self.file_manager.insert_tv(self.tv_c_1,self.df)
        except:
            showerror("Error", "Error while converting to int!", parent=self.cleansing_screen)

    def convert_to_float(self):
        try:
            self.df[self.df.columns[self.given_cols_index]] = self.df[self.df.columns[self.given_cols_index]].astype(float) 
            showinfo("Success", "Successfully converted.", parent=self.cleansing_screen)
            self.file_manager.insert_tv(self.tv_c_1,self.df)
        except:
            showerror("Error", "Error while converting to float!", parent=self.cleansing_screen)


    def download_cleaned(self):
        out_path = self.file_manager.dialog_download(self.cleansing_screen)
        if(out_path != ""):
            if(out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'xlsx' or out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'csv'):
                out_path = out_path + '.xlsx'
            else:
                if(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'xlsx'):      
                    showinfo("Success", "Excel file is downloading.", parent=self.cleansing_screen)
                    self.df.to_excel(out_path, index=False)
                elif(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'csv'):
                    showinfo("Success", "CSV file is downloading.", parent=self.cleansing_screen)
                    self.df.to_csv(out_path, index=False)
            showinfo("Success", "File downloaded.", parent=self.cleansing_screen)
            

    def bring_cleansing_buttons(self):
        
        self.cleansing_buttons_frame = LabelFrame(self.cleansing_screen)
        self.cleansing_buttons_frame.pack()
        self.cleansing_buttons_frame.place(height=300, width=550, relx=0.55,rely=0.15, anchor="nw")
        
        convert_str_button = Button(self.cleansing_buttons_frame, text='Convert to String', command=self.convert_to_str, bg='#5b86b0')
        convert_str_button.pack()
        convert_str_button.place(relx = 0.075, rely = 0.10, width=125, height=40, anchor = 'nw')

        convert_int_button = Button(self.cleansing_buttons_frame, text='Convert to Integer', command=self.convert_to_int, bg='#5b86b0')
        convert_int_button.pack()
        convert_int_button.place(relx = 0.375, rely = 0.10, width=125, height=40,anchor = 'nw')

        convert_float_button = Button(self.cleansing_buttons_frame, text='Convert to Float', command=self.convert_to_float, bg='#5b86b0')
        convert_float_button.pack()
        convert_float_button.place(relx = 0.675, rely = 0.10, width=125, height=40,anchor = 'nw')

        self.download_button = Button(self.cleansing_buttons_frame, text='Download\nCleansed Data', command=self.download_cleaned, 
        bg='#597b45', fg='white')
        self.download_button.pack()
        self.download_button.place(relx = 0.5, rely = 0.80, anchor = 'center')




    
    def apply_fields_act(self):
        columns_nums_str = self.e_columns.get().strip().split(" ")
        column_index_given = []
        
        try:
            for i in columns_nums_str:
                if(int(i) > len(self.df.columns)):
                    raise Exception('apply index, get columns')

                column_index_given.append(int(i)-1)

            self.given_cols_index = column_index_given

            selected_fields_text = "".join([str(elem)+"-" for elem in columns_nums_str])
            selected_fields_text = selected_fields_text[0:len(selected_fields_text)-1]
            selected_fields_text = "Selected Fields: " + selected_fields_text

            if(self.selected_fields_label == None):
                self.selected_fields_label = Label(self.cleansing_screen, text=selected_fields_text, font=('Helvatical bold',11))
                self.selected_fields_label.pack()
                self.selected_fields_label.place(relx = 0.7, rely = 0.05)
            else:
                self.selected_fields_label["text"] = selected_fields_text

            if(not self.cleansing_buttons_exist):
                self.bring_cleansing_buttons()

        except:
            showerror("Index Error", "Given index is out of bounds.", parent=self.cleansing_screen)
            return

    
    def bring_column_nums(self):
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
       




    def bring_apply_field(self):
        apply_frame = LabelFrame(self.cleansing_screen, text="Apply Fields")
        apply_frame.pack()
        apply_frame.place(height=140, width=285, relx=0.28, rely=0.64)
        
        Label(apply_frame, text="Field Numbers:").place(relx = 0.05, rely = 0.40, anchor = 'sw')

        Label(apply_frame, text="Make sure fields headings are identical!").place(relx = 0.05, rely = 0.95, anchor = 'sw')



        self.e_columns = Entry(apply_frame)

        def handle_click(event):
            self.e_columns.delete(0, END)

        self.e_columns.bind("<1>", handle_click)
        self.e_columns.place(relx = 0.40, rely = 0.40, anchor = 'sw')
        self.e_columns.insert(0, 'Ex:1 2 4 7')

        apply_button = Button(apply_frame, text='Apply Fields', command=self.apply_fields_act, bg='#5b86b0')
        apply_button.pack()
        apply_button.place(relx = 0.585, rely = 0.70, anchor = 'sw')

        self.show_columns_button = Button(self.cleansing_screen, text='Show Fields', command=self.bring_column_nums, bg='#5b86b0')
        self.show_columns_button.pack()
        self.show_columns_button.place(relx = 0.30, rely = 0.90, anchor = 'nw')



    def load_data_helper(self, file_label):

        self.df = self.file_manager.load_data(file_label, self.cleansing_screen, True)
        self.file_manager.insert_tv(self.tv_c_1, self.df)

        self.bring_apply_field()


    def cleansing_screen(self, root):
        self.cleansing_screen = Toplevel(root)
        self.cleansing_screen.geometry("1350x650")
        self.cleansing_screen.title("Data Cleansing")

        self.open_area_1 = self.file_manager.create_open_area(self.cleansing_screen, 80, 320, 0, 0.64, 
        frame_text="Upload File", callback=self.load_data_helper)
        self.tv_c_1 = self.file_manager.create_treeview(self.cleansing_screen, 400, 700, 0, 0)