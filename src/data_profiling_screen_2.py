from statistics import correlation
from tkinter import Label, LabelFrame, Button, Toplevel, Entry, END
from tkinter.messagebox import showerror
import webbrowser
#from pandas_profiling import ProfileReport
#import pandas_profiling
import sweetviz as sv


class Data_Profiling:
    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance
        self.label_file = None
        self.given_cols_index = None
        self.reset = True
        self.data_loaded = False
        self.field_frame = None
        self.selected_fields_label_exist = False
        
        
    """
    
    def profiling_report(self):
        if(self.data_loaded):
        
            if(self.reset):
                #profile = ProfileReport(self.df)
                profile = self.df.profile_report(title='NO7Data Profiling Report', correlations=None)
            else:
                #profile= ProfileReport(self.df)
                profile = self.df.iloc[:,self.given_cols_index].profile_report(title='NO7Data Profiling Report', correlations=None)
    
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
            report = sv.analyze(self.df[self.df.columns[self.given_cols_index]])

        report.show_html('NO7DataProfilingReport.html')
    
    
    

    def show_selected_fields(self, given_text):
        if(not self.selected_fields_label_exist):
            self.selected_fields_label = Label(self.profiling_screen, text="Selected Fields: " + given_text, font=('Helvatical bold',11))
            self.selected_fields_label.pack()
            self.selected_fields_label.place(relx = 0.50, rely = 0.67)
            self.selected_fields_label_exist = True
        else:
            self.selected_fields_label["text"] = "Selected Fields: " + given_text
    

    def reset_fields(self):
        if(self.data_loaded):
            self.reset = True
            e_columns.delete(0, END)
            self.show_selected_fields("All Fields")

    
    def apply_new_columns(self):
        if(self.data_loaded):
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
                temp_text = "".join([str(elem)+"-" for elem in columns_nums_str])
                temp_text = temp_text[0:len(temp_text)-1]
                self.show_selected_fields(temp_text)

            except:
                showerror("Index Error", "Given index is out of bounds.", parent=self.profiling_screen)

    
    def bring_fields(self):
        self.field_frame = LabelFrame(self.profiling_screen, text="Field Numbers -> Field Names")
        self.field_frame.pack()
        self.field_frame.place(height=400, width=620, relx=0.99,rely=0, anchor="ne")

        for i in range(len(self.df.columns)):
            label = Label(self.field_frame, text = str(i+1) + " -> " + self.df.columns[i], anchor="nw")
            if(i<18):
                label.grid(sticky="w", row=i, column=0)
            elif(i>=18 and i<36):
                label.grid(sticky="w", row=i-18, column=1)
            elif(i>=36 and i<54):
                label.grid(sticky="w", row=i-36, column=2)
            elif(i>=54 and i<72):
                label.grid(sticky="w", row=i-54, column=3)
            elif(i>=72 and i<90):        
                label.grid(sticky="w", row=i-72, column=4)


    def load_data_helper(self, file_label):
        
        self.df = self.file_manager.load_data(file_label, self.profiling_screen, True)
        self.file_manager.insert_tv(self.tv_c_1, self.df)
        self.data_loaded = True
        self.bring_fields()
        e_columns.delete(0, END)
        e_columns.insert(0, 'Ex:1 2 4 7')



            



    def profiling_screen(self, root, img):
        self.profiling_screen = Toplevel(root)
        self.profiling_screen.geometry("1350x650")
        self.profiling_screen.title("Data Profiling")
        self.profiling_screen.iconphoto(False, img)

        self.open_area_1 = self.file_manager.create_open_area(self.profiling_screen, 80, 320, 0, 0.64, 
        frame_text="Upload File", callback=self.load_data_helper)
        self.tv_c_1 = self.file_manager.create_treeview(self.profiling_screen, 400, 700, 0, 0, frame_text = "Data Frame")

        button2 = Button(self.profiling_screen, text="Report", command=self.profiling_report, padx=5, pady=5, bg='#597b45', fg='white')
        button2.pack()
        button2.place(relx = 0.52, rely = 0.75, width=80, height=40)

        self.apply_frame = LabelFrame(self.profiling_screen, text="Select Fields")
        self.apply_frame.pack()
        self.apply_frame.place(height=120, width=285, rely=0.64, relx=0.25)
        
        Label(self.apply_frame, text="Field Numbers:").place(relx = 0.05, rely = 0.40, anchor = 'sw')


        global e_columns
        e_columns = Entry(self.apply_frame)

        def handle_click(event):
            e_columns.delete(0, END)

        e_columns.bind("<1>", handle_click)
        e_columns.place(relx = 0.40, rely = 0.40, anchor = 'sw')
        e_columns.insert(0, 'Ex:1 2 4 7')


        button1 = Button(self.apply_frame, text="Apply Fields", command= self.apply_new_columns, bg='#5b86b0')
        button1.pack()
        button1.place(relx=0.835, rely=0.80, anchor="se")

        button_reset = Button(self.apply_frame, text="Select All Fields", command = self.reset_fields, bg='#5b86b0')
        button_reset.pack()
        button_reset.place(rely=0.55,relx=0.15)
        self.button_added = True

        self.show_selected_fields("All Fields")

        