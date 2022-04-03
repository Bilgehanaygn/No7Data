from tkinter import Label, LabelFrame, Button, Entry, END, Toplevel
from tkinter.messagebox import showinfo, showerror
import pandas as pd



class Concatenate:
    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance
        self.first_loaded = False
        self.second_loaded = False
        self.third_loaded = False
        self.reference_loaded = False
        self.buttons_exist = False
        self.file_counter = 0
        self.column_numbers = None
        self.total_data = None
        
    
    def download_matched_helper(self):
        out_path = self.file_manager.dialog_download(self.concatenate_screen)
        self.file_manager.download_file(self.concatenate_screen, self.result_df, out_path)


    def download_unmatched_helper(self):
        try:
            i0 = pd.MultiIndex.from_frame(self.result_df)
            i1 = pd.MultiIndex.from_frame(self.df_1)
            i2 = pd.MultiIndex.from_frame(self.df_2)

            self.unmatched_df = self.df_1[~i1.isin(i0)]
            self.unmatched_df = self.unmatched_df.append(self.df_2[~i2.isin(i0)])


            if(self.third_loaded):
                i3 = pd.MultiIndex.from_frame(self.df_3)
                self.unmatched_df = self.unmatched_df.append(self.df_3[~i3.isin(i0)])

        except:
            showerror('No field selected', 'No field selected', parent=self.concatenate_screen)
        out_path = self.file_manager.dialog_download(self.concatenate_screen)
        self.file_manager.download_file(self.concatenate_screen, self.unmatched_df, out_path)

    def remove_file(self):
        if(self.third_loaded):
            self.third_loaded = False
            del[self.df_3]
            self.file_manager.clear_tv(self.tv_c_3)



    def bring_column_nums(self):
        self.column_screen = Toplevel(self.concatenate_screen)
        self.column_screen.geometry("750x600")
        self.column_screen.title("Field Numbers")


        
        self.column_numbers = LabelFrame(self.column_screen, text="Field Numbers -> Field Names")
        self.column_numbers.pack()
        self.column_numbers.place(height=550, width=720, relx=0.02,rely=0.035, anchor="nw")

        #Add new column names
        for i in range(len(self.reference_df.columns)):
            label = Label(self.column_numbers, text = str(i+1) + " -> " + self.reference_df.columns[i], anchor="nw")
            if(i<25):
                label.grid(sticky="w", row=i, column=0)
            elif(i>=25 and i<50):
                label.grid(sticky="w", row=i-25, column=1)
            elif(i>=50 and i<75):
                label.grid(sticky="w", row=i-50, column=2)
            elif(i>=75 and i<100):
                label.grid(sticky="w", row=i-75, column=3)

    def apply_button_action(self):
        others = self.reference_df[self.reference_df.duplicated(subset=[i for i in self.reference_df.columns if(i not in self.cols_names)], keep=False)]

        i0 = pd.MultiIndex.from_frame(others[self.cols_names])
        i1 = pd.MultiIndex.from_frame(self.df_1[self.cols_names])
        i2 = pd.MultiIndex.from_frame(self.df_2[self.cols_names])

        self.result_df = self.df_1[i1.isin(i0)]
        new_col = ["File 1" for i in range(self.result_df.shape[0])]
        
        self.result_df = self.result_df.append(self.df_2[i2.isin(i0)])
        new_col = new_col + ["File 2" for i in range(self.result_df.shape[0] - len(new_col))]
        print(new_col)
        if(self.third_loaded):
            i3 = pd.MultiIndex.from_frame(self.df_3[self.cols_names])
            self.result_df = self.result_df.append(self.df_3[i3.isin(i0)])
            new_col = new_col + ["File 3" for i in range (self.result_df.shape[0] - len(new_col))]

        self.result_df.insert(loc=0, column="Related File", value = new_col)
        
        self.result_df.sort_values(by=[self.result_df.columns[i] for i in range(self.result_df.shape[1])], inplace=True)
        self.file_manager.insert_tv(self.tv_c_result, self.result_df)

        self.download_button = Button(self.concatenate_screen, text='Download\nMatched File', command=self.download_matched_helper, 
        bg='#597b45', fg='white')
        self.download_button.pack()
        self.download_button.place(relx = 0.30, rely = 0.63, anchor = 'center')

        self.download_button = Button(self.concatenate_screen, text='Download\nUnmatched File', command=self.download_unmatched_helper, 
        bg='#597b45', fg='white')
        self.download_button.pack()
        self.download_button.place(relx = 0.40, rely = 0.63, anchor = 'center')

        if(self.total_data == None):
            self.total_data = Label(self.concatenate_screen, text="Total: " + str(self.result_df.shape[0]), font=('Helvatical bold',11))
            self.total_data.pack()
            self.total_data.place(relx=0.43, rely=0.78)
        else:
            self.total_data["text"] = text="Total: " + str(self.result_df.shape[0])


    def bring_apply_field(self):
        apply_frame = LabelFrame(self.concatenate_screen, text="Select Fields")
        apply_frame.pack()
        apply_frame.place(height=140, width=285, rely=0.80, relx=0.0175, anchor="sw")
        
        Label(apply_frame, text="Field Numbers:").place(relx = 0.05, rely = 0.40, anchor = 'sw')

        Label(apply_frame, text="Make sure fields headings are identical!").place(relx = 0.05, rely = 0.95, anchor = 'sw')

        
        e_columns = Entry(apply_frame)
        

        def handle_click(event):
            e_columns.delete(0, END)

        e_columns.bind("<1>", handle_click)
        e_columns.place(relx = 0.40, rely = 0.40, anchor = 'sw')
        e_columns.insert(0, 'Ex:1 2 4 7')

        def apply_button_helper():
            columns_nums_str = e_columns.get().strip().split(" ")
            column_index_given = []
            self.cols_names = []


            try:
                for i in columns_nums_str:
                    if(int(i) > len(self.df_1.columns)):
                        raise Exception('apply index, get columns')

                    column_index_given.append(int(i)-1)
                    self.cols_names.append(self.reference_df.columns[int(i)-1])
                self.given_cols_index = column_index_given
            except:
                showerror("Index Error", "Given index is out of bounds.", parent=self.concatenate_screen)
                return
            
            self.apply_button_action()

        self.tv_c_result = self.file_manager.create_treeview(self.concatenate_screen, 265, 635, 0.99, 0.99, "se", "Result Screen")

        apply_button = Button(apply_frame, text='Apply Fields', command=apply_button_helper, bg='#5b86b0')
        apply_button.pack()
        apply_button.place(relx = 0.56, rely = 0.70, anchor = 'sw')

        self.show_columns_button = Button(apply_frame, text='Show Fields', 
                    command=self.bring_column_nums, bg='#5b86b0')
        self.show_columns_button.pack()
        self.show_columns_button.place(relx = 0.05, rely = 0.70, anchor = 'sw')





    def load_data_helper(self, file_label, is_first):
        try:
            df = self.file_manager.load_data(file_label, self.concatenate_screen, show_success=False)
            
            if(is_first == 1):
                self.df_1 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_1,self.df_1)
                self.first_loaded = True
                if(self.file_counter==0):
                    self.file_counter +=1
                elif(self.second_loaded and self.file_counter==1):
                    self.file_counter+=1
            elif(is_first==2):
                self.df_2 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_2,self.df_2)
                self.second_loaded = True
                if(self.file_counter==0):
                    self.file_counter+=1
                elif(self.first_loaded and self.file_counter==1):
                    self.file_counter+=1
            elif(is_first==3):
                self.df_3 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_3,self.df_3)
                self.third_loaded = True
            elif(is_first==4):
                self.reference_df = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_4,self.reference_df)
                self.reference_loaded = True

            showinfo("Success", "Loaded successfully.", parent=self.concatenate_screen)


            if(self.file_counter==2 and self.reference_loaded and not self.buttons_exist):
                self.buttons_exist = True
                self.bring_apply_field()


        except ValueError:
            showerror("Information", "The file you have chosen is invalid", parent=self.concatenate_screen)
            return None
        except FileNotFoundError:
            showerror("Information", f"No such file as {file_label}", parent=self.concatenate_screen)
            return None


    def concatenate_screen(self,root, img):
        self.concatenate_screen = Toplevel(root)
        self.concatenate_screen.geometry("1350x650")
        self.concatenate_screen.title("Concatenate Files")
        self.concatenate_screen.iconphoto(False, img)


        self.open_area_1 = self.file_manager.create_open_area(self.concatenate_screen, 80, 285, 0.0175, 0.425, 
        frame_text="Upload First File", callback=self.load_data_helper, params=[1])
        self.open_area_2 = self.file_manager.create_open_area(self.concatenate_screen, 80, 285, 0.2675, 0.425, 
        frame_text="Upload Second File", callback=self.load_data_helper, params=[2])
        self.open_area_3 = self.file_manager.create_open_area(self.concatenate_screen, 80, 285, 0.5175, 0.425, 
        frame_text="Upload Third File", callback=self.load_data_helper, params=[3])
        self.open_area_4 = self.file_manager.create_open_area(self.concatenate_screen, 80, 285, 0.7675, 0.425, 
        frame_text="Upload Reference File", callback=self.load_data_helper, params=[4])
        self.open_area_4["bg"] = "#D4E1FF"

        self.tv_c_1 = self.file_manager.create_treeview(self.concatenate_screen, 254, 290, 0.0175, 0, frame_text="Data Frame 1")
        self.tv_c_2 = self.file_manager.create_treeview(self.concatenate_screen, 254, 290, 0.2675, 0, frame_text="Data Frame 2" )
        self.tv_c_3 = self.file_manager.create_treeview(self.concatenate_screen, 254, 290, 0.5175, 0, frame_text="Data Frame 3")
        self.tv_c_4 = self.file_manager.create_treeview(self.concatenate_screen, 254, 290, 0.7675, 0, frame_text = "Reference File",
        borderWidth=10, reference=True)
        

        button_remove = Button(self.open_area_3, text="Remove File", command=lambda: self.remove_file(), bg='#5b86b0')
        button_remove.pack()
        button_remove.place(rely=0.46, relx=0.68)
        