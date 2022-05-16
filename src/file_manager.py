from tkinter import filedialog, ttk, LabelFrame, Button, Scrollbar, Toplevel, HORIZONTAL, Label
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Progressbar
import pandas as pd
import numpy as np


class FileManager():

    def __init__(self):
        pass


    def dialog_upload(self, f_label, parent_screen):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        f_types = (('Excel, CSV or TXT', '*.xlsx'), ('Excel, CSV or TXT',"*.csv"), ('Excel, CSV or TXT',"*.txt"), ('Excel, CSV or TXT',"*.TXT"))
        filename = filedialog.askopenfilename(initialdir="/", parent=parent_screen, title="Select A File", filetypes= f_types)
        f_label["text"] = filename
        return None


    def download_file(self, parent_screen, given_df, out_path):
        if(out_path != ""):
            if(out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'xlsx' and out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'csv'):
                out_path = out_path + '.xlsx'
                given_df.to_excel(out_path, index=False)
            else:
                if(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'xlsx'):      
                    showinfo("Success", "Excel file is downloading.", parent=parent_screen)
                    given_df.to_excel(out_path, index=False)
                elif(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'csv'):
                    showinfo("Success", "CSV file is downloading.", parent=parent_screen)
                    given_df.to_csv(out_path, index=False)
            showinfo("Success", "File downloaded.", parent=parent_screen)


    def dialog_download(self, parent_screen):
        f_types = [('All Files', '*.*'), ('xlsx files', '*.xlsx'), ('CSV files',"*.csv")]
        return filedialog.asksaveasfilename(initialdir="/", parent=parent_screen, title="Select location", filetype=f_types)

    def process_frame(self, df):
        # process data frame
        return len(df)

    def load_data(self, f_label, parent_screen, show_success, apply_str=True):
        """If the file selected is valid this will load the file into the Treeview"""
        showinfo("Loading", "Excel file is loading, wait until loading is done.", parent=parent_screen)
        file_path = f_label["text"]
        try:
            filename = r"{}".format(file_path)
            if filename[-4:] == ".txt" or filename[-4:] == ".TXT":
                df = pd.read_csv(filename, delimiter = '|')
            elif filename[-4:] == ".csv":
                df = pd.read_csv(filename)
            else:
                df = pd.read_excel(filename)
            if(df.shape[0] >1000000000 or df.shape[1] > 10000):
                raise Exception
            if(apply_str):
                df = df.applymap(str)
                df = df.replace(r'^\s*$', 'nan', regex=True)
            if(show_success):
                showinfo("Success", "Loaded successfully.", parent=parent_screen)
            return df

        except ValueError:
            showerror("Information", "The file you have chosen is invalid", parent=parent_screen)
            return None
        except FileNotFoundError:
            showerror("Information", f"Please select a file.", parent=parent_screen)
            return None
        except Exception:
            showerror("Demo Version Limitations", "Demo version is limited with 100 rows and 10 columns.", parent=parent_screen)
            return None




    #WIDGET#WIDGET#WIDGET#WIDGET#WIDGET#WIDGET


    def progress_bar(self, root):
        progress_bar = Toplevel(root)
        progress_bar.geometry("250x125")
        progress_bar.title("Progress.")

        label1 = Label(progress_bar, text="Loading...")
        label1.pack()
        label1.place(relx=0.4, rely=0.5)

        pb1 = Progressbar(progress_bar, orient=HORIZONTAL, length=100, mode='indeterminate')
        pb1.pack()
        pb1.place(relx=0.25, rely=0.20)



    def insert_tv(self, tv_given, df):

        self.clear_tv(tv_given)

        tv_given["column"] = list(df.columns)
        tv_given["show"] = "headings"

        for column in tv_given["columns"]:
            tv_given.heading(column, text=column) # let the column heading = column name

        df_rows = df.to_numpy().tolist() # turns the dataframe into a list of lists
        
        for row in df_rows:
            tv_given.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        tv_given.insert("", "end", values="") # add 1 empty item so tv shows items properly

    
    def clear_tv(self, tv_given):
        tv_given.delete(*tv_given.get_children())
        return None
    
    def destroy_children(self, frame):
        if(not isinstance(frame, type(None))):
            for child in frame.winfo_children():
                child.destroy()

    
    def create_open_area(self, parent_screen, height, width, relx, rely, anchor="nw", frame_text="Upload File", 
    browse_text="Browse A File", load_text="Load File", show_success=True, callback=load_data, params=['']):
        file_frame = LabelFrame(parent_screen, text=frame_text)
        file_frame.place(height=height, width=width, relx=relx, rely=rely, anchor=anchor)
        

        # The file/file path text
        label_file = Label(file_frame, text="No File Selected")
        label_file.place(rely=0, relx=0)

        default_params = [label_file]
        if(params[0] == ''):
            params=default_params
        else: # may need some edit
            params= default_params + params

        
        # Buttons
        button_browse = Button(file_frame, text=browse_text, command=lambda: self.dialog_upload(label_file, parent_screen), bg='#5b86b0')
        button_browse.pack()
        button_browse.place(rely=0.46, relx=0.05)
        
        button_load = Button(file_frame, text=load_text, command=lambda: callback(*params), bg='#5b86b0')
        button_load.pack()
        button_load.place(rely=0.46, relx=0.38)

        return file_frame


    def create_treeview(self, parent_screen, height, width, relx, rely, anchor="nw", frame_text="Data Frame", borderWidth=2, reference=False):
        # Frame 1 for TreeView
        frame_c = LabelFrame(parent_screen, text=frame_text, borderwidth=borderWidth)
        frame_c.pack()
        frame_c.place(height=height, width=width, relx=relx, rely=rely, anchor=anchor)
        if(reference):
            frame_c["font"] = ('Helvatical bold',11)
            frame_c["bg"] = "#D4E1FF"

        ## Treeview Widget
        style = ttk.Style(parent_screen)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="silver")
        tv_c = ttk.Treeview(frame_c)
        
        
        
        tv_c.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame_c_1).

        treescrolly1 = Scrollbar(frame_c, orient="vertical", command=tv_c.yview) # command means update the yaxis view of the widget
        treescrollx1 = Scrollbar(frame_c, orient="horizontal", command=tv_c.xview) # command means update the xaxis view of the widget
        tv_c.configure(xscrollcommand=treescrollx1.set, yscrollcommand=treescrolly1.set) # assign the scrollbars to the Treeview Widget
        treescrollx1.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
        treescrolly1.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

        return tv_c
