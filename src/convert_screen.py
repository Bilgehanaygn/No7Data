from tkinter import Label, Button, Toplevel
from tkinter.messagebox import showinfo, showerror




class Convert:
    def __init__(self, file_manager_instance):
        self.file_manager= file_manager_instance
        self.info_label = None
        self.file_loaded = False

    def load_data_helper(self, file_label):
        try:
            self.df = self.file_manager.load_data(file_label, self.convert_screen, show_success=False)
            self.file_manager.insert_tv(self.tv_c_1, self.df)
            if(self.info_label == None):
                self.info_label = Label(self.convert_screen, text = "Conversion is success. Download as either Excel or CSV by simply specifying the extension.")
                self.info_label.pack()
                self.info_label.place(relx=0.50, rely=0.57, anchor="center")
            self.file_loaded = True
        except:
            showerror("Upload Error", "Error while uploading file", parent=self.convert_screen)


    def download_file(self):
        if(self.file_loaded):
            out_path = self.file_manager.dialog_download(self.convert_screen)
            self.file_manager.download_file(self.convert_screen, self.df, out_path)

    def convert_screen(self,root, img):
        self.convert_screen = Toplevel(root)
        self.convert_screen.geometry("800x600")
        self.convert_screen.title("Convert File")
        self.convert_screen.iconphoto(False, img)

        self.open_area_1 = self.file_manager.create_open_area(self.convert_screen, 80, 290, 0.5, 0.7, anchor="center",
        frame_text="Upload First File", callback=self.load_data_helper)
        self.tv_c_1 = self.file_manager.create_treeview(self.convert_screen, 300, 500, 0.5, 0.275, anchor="center", frame_text="Data Frame 1")


        button_remove3 = Button(self.convert_screen, text="Downlaod", command=self.download_file, bg='#597b45')
        button_remove3.pack()
        button_remove3.place(rely=0.85, relx=0.5, width=125,height=40,anchor="center")
