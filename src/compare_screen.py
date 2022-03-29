from tkinter import Label, LabelFrame, Button, Entry, END, Toplevel
from tkinter.messagebox import showinfo, showerror
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gc
#import threading


class Compare:

    def __init__(self, file_manager_instance):
        self.special_chars = ['"', '*', '%', '$', '&', '!', '£']
        self.file_manager = file_manager_instance
        self.first_loaded = False
        self.second_loaded = False
        self.third_loaded = False
        self.fourth_loaded = False
        self.show_columns_button = False
        self.file_counter = 0
        self.match_button = None
        self.tv_c_result = None
        self.matched_df = None
        self.unmatched_df = None
        self.match_data = None
        self.unmatch_data = None
        self.matched_exist = False
        self.matched_exist = False
        self.unmatched_count = []
        self.number_of_fields = []

        self.show_columns_button = None
        self.file_frame_buttons = None

        self.given_cols_index = None
        self.column_numbers = None

        self.df_1 = None
        self.df_2 = None
        self.df_3 = None
        self.df_4 = None

        self.data_label_1 = None
        self.data_label_2 = None
        self.data_label_3 = None
        self.data_label_4 = None


    def download_matches(self):
        out_path = self.file_manager.dialog_download(self.compare_screen)
        if(out_path != ""):
            out_path = out_path.split(".")[0].lower()
            set_excel = True
            if(out_path.split('.')[len(out_path.split('.')) - 1] != 'xlsx' and out_path.split('.')[len(out_path.split('.')) - 1] != 'csv'):
                match_out_path = out_path + "-Matched" + ".xlsx"
                unmatched_out_path = out_path + "-Unmatched" + ".xlsx"
            else:
                if(out_path.split('.')[len(out_path.split('.')) - 1] == 'xlsx'):      
                    match_out_path = out_path + "-Matched" + ".xlsx"
                    unmatched_out_path = out_path + "-Unmatched" + ".xlsx"
                elif(out_path.split('.')[len(out_path.split('.')) - 1] == 'csv'):
                    match_out_path = out_path + "-Matched" + ".csv"
                    unmatched_out_path = out_path + "-Unmatched" + ".csv"
            try:
                if(set_excel):
                    showinfo("Success", "Excel file is downloading.", parent=self.compare_screen)
                    self.matched_df.to_excel(match_out_path, index=False)
                    self.unmatched_df.to_excel(unmatched_out_path, index=False)
                    showinfo("Success", "File downloaded.", parent=self.compare_screen)
                else:
                    showinfo("Success", "Excel file is downloading.", parent=self.compare_screen)
                    self.matched_df.to_excel(match_out_path, index=False)
                    self.unmatched_df.to_excel(unmatched_out_path, index=False)
                    showinfo("Success", "File downloaded.", parent=self.compare_screen)
            except:
                showerror("Error", "To download the files, please click on Matching and then Unmatching button.", parent=self.compare_screen)


    def plot_graphs(self):

        if(self.matched_exist):
            
            plot_matched_df = pd.DataFrame({'Matched' : [self.matched_df.shape[0]]}, index=['Matched'])
            plot_matched_df.plot(kind='bar', title="Number of matching items")
        
        if(self.unmatch_data!=None):

            plot_unmatched_df= pd.DataFrame({'File Names:' :['File 1', 'File 2', 'File 3', 'File 4'],
            'Values': self.unmatched_count})
            plot_unmatched_df.set_index('File Names:', inplace=True)    
            plot_unmatched_df.plot(kind='bar', title="Number of unmatching items for each file")

        plt.show()

    
    def find_matchings(self):
        i1 = pd.MultiIndex.from_frame(self.df_1.iloc[:,self.given_cols_index])
        i2 = pd.MultiIndex.from_frame(self.df_2.iloc[:,self.given_cols_index])
        self.matched_df = self.df_1[i1.isin(i2)]

        if(self.third_loaded):
            i0 = pd.MultiIndex.from_frame(self.matched_df.iloc[:,self.given_cols_index])
            i3 = pd.MultiIndex.from_frame(self.df_3.iloc[:,self.given_cols_index])

            self.matched_df = self.matched_df[i0.isin(i3)]
        
        if(self.fourth_loaded):
            i0 = pd.MultiIndex.from_frame(self.matched_df.iloc[:,self.given_cols_index])
            i4 = pd.MultiIndex.from_frame(self.df_4.iloc[:,self.given_cols_index])

            self.matched_df = self.matched_df[i0.isin(i4)]
        
        self.matched_exist = True


    def bring_matchings(self):
        if(not self.matched_exist):
            self.find_matchings()

        if(self.matched_df.shape[0] == 0):
            temp = pd.DataFrame({'MATCH RESULT: ':'NO ANY MATCHING ITEM!'}, index=[0])
            self.file_manager.insert_tv(self.tv_c_result, temp)
        else:
            self.file_manager.insert_tv(self.tv_c_result ,self.matched_df)

        if(self.match_data!=None):
            self.match_data.destroy

        self.match_data = Label(self.compare_screen, text="Matched: " + str(self.matched_df.shape[0]), font=('Helvatical bold',11))
        self.match_data.pack()
        self.match_data.place(relx=0.48, rely=0.83, anchor="ne")


    def bring_unmatchings(self):

        if(not self.matched_exist):
            self.find_matchings()
        
        self.unmatched_count.clear()

        i0 = pd.MultiIndex.from_frame(self.matched_df.iloc[:,self.given_cols_index])
        i1 = pd.MultiIndex.from_frame(self.df_1.iloc[:,self.given_cols_index])
        i2 = pd.MultiIndex.from_frame(self.df_2.iloc[:,self.given_cols_index])

        self.unmatched_df = self.df_1[~i1.isin(i0)]
        

        self.unmatched_count.append(self.unmatched_df.shape[0]) # append the num of unmatched in FIRST file to count list 

        self.unmatched_df = self.unmatched_df.append(self.df_2[~i2.isin(i0)])
        

        self.unmatched_count.append(self.unmatched_df.shape[0] - self.unmatched_count[0]) # append the num of unmatched in SECOND file to count list 
        
        third_exist = False # in order to find the difference between len of unmatched df after fourth df is checked and 
        # after third df is checked (we don't know if it is checked so third_exist notifies if it does.)
        if(self.third_loaded):
            i3 = pd.MultiIndex.from_frame(self.df_3.iloc[:,self.given_cols_index])
            
            self.unmatched_df = self.unmatched_df.append(self.df_3[~i3.isin(i0)])
            

            self.unmatched_count.append(self.unmatched_df.shape[0] - self.unmatched_count[1] - self.unmatched_count[0]) # append the num of unmatched in THIRD file to count list 
        else:
            self.unmatched_count.append(0) # if not loaded append 0

        if(self.fourth_loaded):
            i4 = pd.MultiIndex.from_frame(self.df_4.iloc[:,self.given_cols_index])
            self.unmatched_df = self.unmatched_df.append(self.df_4[~i4.isin(i0)])

            self.unmatched_count.append(self.unmatched_df.shape[0] - self.unmatched_count[2] - self.unmatched_count[1] - self.unmatched_count[0]) # append the num of unmatched in FOURTH file to count list 
        else:
            self.unmatched_count.append(0)


        #self.unmatched_df.drop_duplicates(keep="first", inplace=True)
        new_col = ["File 1" for i in range(self.unmatched_count[0])] + ["File 2" for i in range(self.unmatched_count[1])]
        if(self.third_loaded):
            new_col = new_col + ["File 3" for i in range(self.unmatched_count[2])] 
        if(self.fourth_loaded):
            new_col = new_col + ["File4 " for i in range(self.unmatched_count[3])]

        self.unmatched_df.insert(loc=0, column="Related File", value = new_col)

        if(self.unmatched_df.shape[0] == 0):
            temp2 = pd.DataFrame({'UNMATCHING RESULT: ':'NO ANY UNMATCHING ITEM!'}, index=[0])
            self.file_manager.insert_tv(self.tv_c_result, temp2)
        else:
            self.file_manager.insert_tv(self.tv_c_result, self.unmatched_df)

        if(self.unmatch_data!=None):
            self.unmatch_data.destroy()

        self.unmatch_data = Label(self.compare_screen, text="Unmatched: " + str(len(self.unmatched_df)), font=('Helvatical bold',11))
        self.unmatch_data.pack()
        self.unmatch_data.place(relx=0.48, rely=0.86, anchor="ne")
        

    def bring_compare_buttons(self):
        if(self.file_frame_buttons == None):
            self.file_frame_buttons = LabelFrame(self.compare_screen, text="Matching")
            self.file_frame_buttons.place(height=140, width=285, rely=0.80, relx=0.2675, anchor="sw")
        if(self.match_button == None):
            self.match_button = Button(self.file_frame_buttons, text='Matching', command=self.bring_matchings, bg='#5b86b0')
            self.match_button.pack()
            self.match_button.place(relx = 0.05, rely = 0.10, anchor = 'nw')

            self.unmatch_button = Button(self.file_frame_buttons, text='Unmatching', command=self.bring_unmatchings, bg='#5b86b0')
            self.unmatch_button.pack()
            self.unmatch_button.place(relx = 0.50, rely = 0.10, anchor = 'nw')

            self.download_button = Button(self.file_frame_buttons, text='Download Output', command=self.download_matches, bg='#597b45', fg='white')
            self.download_button.pack()
            self.download_button.place(relx = 0.50, rely = 0.45, anchor = 'nw')

            self.tv_c_result = self.file_manager.create_treeview(self.compare_screen, 275, 635, 0.99, 0.99, "se", "Result Screen")
            info_label = Label(self.file_frame_buttons, text="To download the files, please click on    \n Matching and then Unmatching button!")
            info_label.pack()
            info_label.place(relx = 0.02, rely = 0.98, anchor = 'sw')
            graph_button = Button(self.compare_screen, text='Get Graphs', command=self.plot_graphs, bg='#5b86b0')
            graph_button.pack()
            graph_button.place(relx = 0.175, rely = 0.85, anchor = 'nw')





    def bring_apply_field(self):
        
        apply_frame = LabelFrame(self.compare_screen, text="Apply Fields")
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

        def bring_compare_buttons_helper():
            columns_nums_str = e_columns.get().strip().split(" ")
            column_index_given = []

            try:
                for i in columns_nums_str:
                    if(int(i) > len(self.df_1.columns)):
                        raise Exception('apply index, get columns')

                    column_index_given.append(int(i)-1)
                self.given_cols_index = column_index_given
            except:
                showerror("Index Error", "Given index is out of bounds.", parent=self.compare_screen)
                return
            #Convert column nums to column names

            self.bring_compare_buttons()

        apply_button = Button(apply_frame, text='Apply Fields', command=bring_compare_buttons_helper, bg='#5b86b0')
        apply_button.pack()
        apply_button.place(relx = 0.585, rely = 0.70, anchor = 'sw')

        
    def is_field_nums_equal(self):
        current = self.number_of_fields[0]
        for i in self.number_of_fields:
            if(i!=current):
                return False
        return True


    def bring_column_nums(self):
        self.column_screen = Toplevel(self.compare_screen)
        self.column_screen.geometry("750x600")
        self.column_screen.title("Field Numbers")

        #Destroy childrens before adding new column names
        self.file_manager.destroy_children(self.column_numbers)

        self.column_numbers = LabelFrame(self.column_screen, text="Field Numbers -> Field Names")
        self.column_numbers.pack()
        self.column_numbers.place(height=550, width=720, relx=0.02,rely=0.035, anchor="nw")

        #Add new column names
        for i in range(len(self.df_1.columns)):
            label = Label(self.column_numbers, text = str(i+1) + " -> " + self.df_1.columns[i], anchor="nw")
            if(i<25):
                label.grid(sticky="w", row=i, column=0)
            elif(i>=25 and i<50):
                label.grid(sticky="w", row=i-25, column=1)
            elif(i>=50 and i<75):
                label.grid(sticky="w", row=i-50, column=2)
            elif(i>=75 and i<100):
                label.grid(sticky="w", row=i-75, column=3)

    def data_label(self, num_rows, relx, rely, is_first):
        if(is_first==1):
            if(self.data_label_1 != None):
                self.data_label_1["text"] = str(num_rows) + " rows are uploaded"
            else:
                self.data_label_1 = Label(self.compare_screen, text= str(num_rows) + " rows are uploaded.", font=('Helvatical bold',11))
                self.data_label_1.pack()
                self.data_label_1.place(relx=relx, rely=rely, anchor="nw")
        elif(is_first==2):
            if(self.data_label_2 != None):
                self.data_label_2["text"] = str(num_rows) + " rows are uploaded"
            else:
                self.data_label_2 = Label(self.compare_screen, text= str(num_rows) + " rows are uploaded.", font=('Helvatical bold',11))
                self.data_label_2.pack()
                self.data_label_2.place(relx=relx, rely=rely, anchor="nw")
        elif(is_first==3):
            if(self.data_label_3 != None):
                self.data_label_3["text"] = str(num_rows) + " rows are uploaded"
            else:
                self.data_label_3 = Label(self.compare_screen, text= str(num_rows) + " rows are uploaded.", font=('Helvatical bold',11))
                self.data_label_3.pack()
                self.data_label_3.place(relx=relx, rely=rely, anchor="nw")
        elif(is_first==4):
            if(self.data_label_4 != None):
                self.data_label_4["text"] = str(num_rows) + " rows are uploaded"
            else:
                self.data_label_4 = Label(self.compare_screen, text= str(num_rows) + " rows are uploaded.", font=('Helvatical bold',11))
                self.data_label_4.pack()
                self.data_label_4.place(relx=relx, rely=rely, anchor="nw")

    def load_data_helper(self, file_label, is_first):
        
        try:
            df = self.file_manager.load_data(file_label, self.compare_screen, show_success=False)
            
            if(is_first == 1):
                self.df_1 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_1,self.df_1)
                self.first_loaded = True
                self.data_label(self.df_1.shape[0], 0.0175, 0.38, 1)
                if(self.file_counter==0):
                    self.file_counter +=1
                elif(self.second_loaded and self.file_counter==1):
                    self.file_counter+=1
            elif(is_first==2):
                self.df_2 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_2,self.df_2)
                self.second_loaded = True
                self.data_label(self.df_2.shape[0], 0.2675, 0.38, 2)
                if(self.file_counter==0):
                    self.file_counter+=1
                elif(self.first_loaded and self.file_counter==1):
                    self.file_counter+=1
            elif(is_first==3):
                self.df_3 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_3,self.df_3)
                self.third_loaded = True
                self.data_label(self.df_3.shape[0], 0.5175, 0.38, 3)
            elif(is_first==4):
                self.df_4 = df.applymap(str)
                self.file_manager.insert_tv(self.tv_c_4,self.df_4)
                self.fourth_loaded = True
                self.data_label(self.df_4.shape[0], 0.7675, 0.40, 4)
            
            self.matched_exist = False
            self.number_of_fields.append(df.shape[1])



            showinfo("Success", "Loaded successfully.", parent=self.compare_screen)

            if(self.file_counter>=2):
                if(not self.is_field_nums_equal()):
                    showinfo("Attention", "Number of fields are not equal. Be careful specifiying field numbers.", 
                    parent=self.compare_screen)
                
            

            if(self.show_columns_button == None):
                if(self.first_loaded):
                    self.show_columns_button = Button(self.compare_screen, text='Show Fields', 
                    command=self.bring_column_nums, bg='#5b86b0')
                    self.show_columns_button.pack()
                    self.show_columns_button.place(relx = 0.095, rely = 0.85, anchor = 'nw')

            if(self.file_counter==2):
                    self.bring_apply_field()

            
            
        except ValueError:
            showerror("Information", "The file you have chosen is invalid", parent=self.compare_screen)
            return None
        except FileNotFoundError:
            showerror("Information", f"No such file as {file_label}", parent=self.compare_screen)
            return None

    def remove_file(self, file_num):
        if(file_num==3):
            self.third_loaded = False
            del[self.df_3]
            gc.collect()
            self.file_manager.clear_tv(self.tv_c_3)
        elif(file_num==4):
            self.fourth_loaded = False
            del[self.df_4]
            gc.collect()
            self.file_manager.clear_tv(self.tv_c_4)
        
        self.matched_exist = False


    def compare_screen(self,root):
        self.compare_screen = Toplevel(root)
        self.compare_screen.geometry("1350x700")
        self.compare_screen.title("Compare Files")

        self.open_area_1 = self.file_manager.create_open_area(self.compare_screen, 80, 290, 0.0175, 0.425, 
        frame_text="Upload First File", callback=self.load_data_helper, params=[1])
        self.open_area_2 = self.file_manager.create_open_area(self.compare_screen, 80, 290, 0.2675, 0.425, 
        frame_text="Upload Second File", callback=self.load_data_helper, params=[2])
        self.open_area_3 = self.file_manager.create_open_area(self.compare_screen, 80, 290, 0.5175, 0.425, 
        frame_text="Upload Third File", callback=self.load_data_helper, params=[3])
        self.open_area_4 = self.file_manager.create_open_area(self.compare_screen, 80, 290, 0.7675, 0.425, 
        frame_text="Upload Fourth File", callback=self.load_data_helper, params=[4])

        self.tv_c_1 = self.file_manager.create_treeview(self.compare_screen, 254, 290, 0.0175, 0)
        self.tv_c_2 = self.file_manager.create_treeview(self.compare_screen, 254, 290, 0.2675, 0)
        self.tv_c_3 = self.file_manager.create_treeview(self.compare_screen, 254, 290, 0.5175, 0)
        self.tv_c_4 = self.file_manager.create_treeview(self.compare_screen, 254, 290, 0.7675, 0)

        ##REMOVE BUTTONS
        button_remove3 = Button(self.open_area_3, text="Remove File", command=lambda: self.remove_file(3), bg='#5b86b0')
        button_remove3.pack()
        button_remove3.place(rely=0.46, relx=0.68)

        button_remove4 = Button(self.open_area_4, text="Remove File", command=lambda: self.remove_file(4), bg='#5b86b0')
        button_remove4.pack()
        button_remove4.place(rely=0.46, relx=0.68)


        


        
                
        
    