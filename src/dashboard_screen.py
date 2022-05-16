from tkinter import Button, Toplevel
from tkinter.messagebox import showerror
import pandas_bokeh
import pandas as pd



class Dashboard:
    def __init__(self, file_manager_instance):
        self.file_manager= file_manager_instance
        self.info_label = None
        self.file_loaded = False

    def load_data_helper(self, file_label):
        try:
            self.df = self.file_manager.load_data(file_label, self.dashboard_screen, show_success=True, apply_str=False)
            self.file_manager.insert_tv(self.tv_c_1, self.df)
            self.file_loaded = True
        except:
            showerror("Upload Error", "Error while uploading file", parent=self.dashboard_screen)


    def create_dashboard(self):
        if(self.file_loaded):
            #dfi olustur
            #columnsu duzelt
            self.df.columns=['Sales Document','Created_on','Document_Date','Sales_Document_Type','Sales_Organization','Distribution_Channel','Division', 'Net_Value']

            #val countsi al
            myL = self.df[['Sales_Organization', 'Distribution_Channel', 'Division']].value_counts()

            #renklendirebilmek icin dict olustur
            sales_dictionary = {str(myL.index[i]) : myL.values[i] for i in range(len(myL))}
            df2 = pd.DataFrame(sales_dictionary, index=[0])

            ##BAR DICTE AYARLA
            p_bar = df2.plot_bokeh(kind="bar", colormap=["Purple", 'Orange', 'Red', 'Green'], show_figure=False)
            ##PIEDE DIREKT VER YENIDEN DICTE CEVIRME
            p_pie = myL.plot_bokeh(kind="pie",colormap=["Purple", 'Orange', 'Red', 'Green'],show_figure=False)


            temp_df = self.df[['Document_Date', 'Sales_Organization', 'Net_Value']]
            ##STACKED BAR CHART
            p_stack = temp_df.groupby(['Document_Date']).mean().plot_bokeh(kind='barh', stacked=True,colormap=["Purple", 'Orange', 'Red', 'Green'],show_figure=False)

            p_hist=self.df.plot_bokeh(kind='hist', histogram_type="stacked",bins=6,colormap=["Purple", 'Orange', 'Red', 'Green'], show_figure=False)


            pandas_bokeh.plot_grid([[p_bar, p_pie], [p_stack, p_hist]], width=700, height=500)

    def dashboard_screen(self,root, img):
        self.dashboard_screen = Toplevel(root)
        self.dashboard_screen.geometry("450x600")
        self.dashboard_screen.title("Create Dashboard")
        self.dashboard_screen.iconphoto(False, img)

        self.open_area_1 = self.file_manager.create_open_area(self.dashboard_screen, 80, 290, 0.5, 0.7, anchor="center",
        frame_text="Upload First File", callback=self.load_data_helper)
        self.tv_c_1 = self.file_manager.create_treeview(self.dashboard_screen, 300, 400, 0.5, 0.275, anchor="center", frame_text="Data Frame 1")


        button_remove3 = Button(self.dashboard_screen, text="Create Dashboard", command=self.create_dashboard, bg='#597b45')
        button_remove3.pack()
        button_remove3.place(rely=0.85, relx=0.5, width=125,height=40,anchor="center")
