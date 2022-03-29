from tkinter import filedialog, ttk, LabelFrame, Button, Scrollbar
from tkinter.messagebox import showinfo, showerror
import pandas as pd


class FileManager():

    def __init__(self):
        pass


    def dialog_upload(self, f_label, parent_screen):
        """This Function will open the file explorer and assign the chosen file path to label_file"""
        f_types = (('Excel or CSV', '*.xlsx'), ('Excel or CSV',"*.csv"), ('Excel or CSV',"*.xls"))
        filename = filedialog.askopenfilename(initialdir="/", parent=parent_screen, title="Select A File", filetypes= f_types)
        f_label["text"] = filename
        return None


    def dialog_download(self, parent_screen):
        f_types = [('All Files', '*.*'), ('xlsx files', '*.xlsx'), ('CSV files',"*.csv")]
        return filedialog.asksaveasfilename(initialdir="/", parent=parent_screen, title="Select location", filetype=f_types)


    def load_data(self, f_label, parent_screen, show_success):
        """If the file selected is valid this will load the file into the Treeview"""
        showinfo("Loading", "Excel file is loading, wait until loading is done.", parent=parent_screen)
        file_path = f_label["text"]
        try:
            excel_filename = r"{}".format(file_path)
            if excel_filename[-4:] == ".csv":
                df = pd.read_csv(excel_filename)
            else:
                df = pd.read_excel(excel_filename)
            
            df = df.applymap(str)
            if(show_success):
                showinfo("Success", "Loaded successfully.", parent=parent_screen)
            return df

        except ValueError:
            showerror("Information", "The file you have chosen is invalid", parent=parent_screen)
            return None
        except FileNotFoundError:
            showerror("Information", f"No such file as {file_path}", parent=parent_screen)
            return None




    #WIDGET#WIDGET#WIDGET#WIDGET#WIDGET#WIDGET




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
        label_file = ttk.Label(file_frame, text="No File Selected")
        label_file.place(rely=0, relx=0)

        default_params = [label_file]
        if(params[0] == ''):
            params=default_params
        else: # may need some edit
            params= default_params + params
            
            
        

        
        # Buttons
        button_browse = Button(file_frame, text=browse_text, command=lambda: self.dialog_upload(label_file, parent_screen), bg='#5b86b0')
        button_browse.pack()
        button_browse.place(rely=0.46, relx=0.30)
        
        button_load = Button(file_frame, text=load_text, command=lambda: callback(*params), bg='#5b86b0')
        button_load.pack()
        button_load.place(rely=0.46, relx=0.05)

        return file_frame


    def create_treeview(self, parent_screen, height, width, relx, rely, anchor="nw", frame_text="Excel Data", borderWidth=2):
        # Frame 1 for TreeView
        frame_c = LabelFrame(parent_screen, text=frame_text, borderwidth=borderWidth)
        frame_c.pack()
        frame_c.place(height=height, width=width, relx=relx, rely=rely, anchor=anchor)

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
