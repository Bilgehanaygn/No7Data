from tkinter import Toplevel
from tkinter.messagebox import showerror, showinfo



class CreateReference():
    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance


    def create_reference_screen(self, root, img):
        self.reference_screen = Toplevel(root)
        self.reference_screen.geometry("1350x650")
        self.reference_screen.title("Reference File Generator")
        self.reference_screen.iconphoto(False, img)

        self.open_area_1 = self.file_manager.create_open_area(self.reference_screen, 80, 320, 0, 0.64, 
        frame_text="Upload File", callback=self.load_data_helper)
        self.tv_c_1 = self.file_manager.create_treeview(self.reference_screen, 400, 700, 0, 0)
        
        
        
        

