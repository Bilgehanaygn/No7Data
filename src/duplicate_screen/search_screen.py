from tkinter import Label, Toplevel, Entry, Button
from tkinter.messagebox import showerror, showinfo
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



class SearchScreen():
  def __init__(self, file_manager_instance, df):
    self.file_manager = file_manager_instance
    self.df = df
    self.match_label = None
    self.search_result_set = False

  def is_empty(self, list):
    for i in list:
      if(i.strip() !=""):
        return False
    return True
  
  def search(self):
    given_columns = []
    related_column_index = []


    given_columns.append(self.c1.get())
    given_columns.append(self.c2.get())
    given_columns.append(self.c3.get())
    given_columns.append(self.c4.get())
    given_columns.append(self.c5.get())
    given_columns.append(self.c6.get())
    given_columns.append(self.c7.get())
    given_columns.append(self.c8.get())

    for i in given_columns:
      if(i.strip() != ""):
          related_column_index.append([int(i.strip()) - 1])
      else:
          related_column_index.append([""])

    
    #realted column index append e.get.split(",")

    related_column_index[0].append(self.e1.get().split('-'))
    related_column_index[1].append(self.e2.get().split('-'))
    related_column_index[2].append(self.e3.get().split('-'))
    related_column_index[3].append(self.e4.get().split('-'))
    related_column_index[4].append(self.e5.get().split('-'))
    related_column_index[5].append(self.e6.get().split('-'))
    related_column_index[6].append(self.e7.get().split('-'))
    related_column_index[7].append(self.e8.get().split('-'))

    related_column_index[0].append(self.exact1.get())
    related_column_index[1].append(self.exact2.get())
    related_column_index[2].append(self.exact3.get())
    related_column_index[3].append(self.exact4.get())
    related_column_index[4].append(self.exact5.get())
    related_column_index[5].append(self.exact6.get())
    related_column_index[6].append(self.exact7.get())
    related_column_index[7].append(self.exact8.get())

    not_null_related_column = []

    for i in related_column_index:
      if(not self.is_empty(i[1]) and i[2].strip() != ""):
        showerror('Error','Cannot specify both: exact value and containing value.', parent=self.search_screen)
        return
      if((not self.is_empty(i[1]) or i[2].strip()!="") and (i[0] != "")):
        not_null_related_column.append(i)
    
    self.search_result_set = True

    search_result_exist = False
    for item in not_null_related_column:
      inside_item = False
      if(not self.is_empty(item[1])):
          for iter in item[1]:
            if(not search_result_exist):
              self.search_result = self.df[self.df[self.df.columns[item[0]]].str.contains(iter, na=False, case=False)]
              search_result_exist = True
              inside_item=True
            else:
              if(inside_item):
                self.search_result = pd.concat([self.search_result, self.df[self.df[self.df.columns[item[0]]].str.contains(iter, na=False, case=False)]], axis=0)
              else:
                self.search_result = self.search_result[self.search_result[self.df.columns[item[0]]].str.contains(iter, na=False, case=False)]
                inside_item = True
      elif(item[2]!=''):
        if(not search_result_exist):
          self.search_result = self.df[self.df[self.df.columns[item[0]]].str.lower() == item[2].lower()]
        else:
          self.search_result = self.search_result[self.search_result[self.df.columns[item[0]]].str.lower() == item[2].lower()]

      search_result_exist = True

    
    
    if(search_result_exist):
      self.file_manager.insert_tv(self.search_tv, self.search_result)

      if(self.match_label == None):
          self.match_label = Label(self.search_screen, font=('Helvatical bold',12))
          self.match_label.pack()
          self.match_label.place(relx = 0.81, rely = 0.60, anchor = 'center')

      if(self.search_result.shape[0] == 0):
        temp = pd.DataFrame({'Search Result: ':'NO ITEM FOUND!'}, index=[0])
        self.file_manager.insert_tv(self.search_tv, temp)
        
        self.match_label["text"] = "No item matches the given values."
      else:
        self.match_label["text"] = str(self.search_result.shape[0]) + " item matches the given values."

  def reset(self):
    self.file_manager.insert_tv(self.search_tv, self.df)
    if(self.match_label!=None):
      self.match_label["text"] = "State: Reset"

  def download_helper(self):
    out_path = self.file_manager.dialog_download(self.search_screen)
    if(out_path != ""):
        if("." in out_path):
            if(out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'xlsx' and out_path.split('.')[len(out_path.split('.')) - 1].lower() != 'csv'):
                out_path = out_path + '.xlsx'
                self.search_result.to_excel(out_path, index=False)
            else:
                if(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'xlsx'):      
                    
                    self.search_result.to_excel(out_path, index=False)
                    showinfo("Success", "Excel file is downloading.", parent=self.search_screen)
                elif(out_path.split('.')[len(out_path.split('.')) - 1].lower() == 'csv'):
                    self.search_result.to_csv(out_path, index=False)
                    showinfo("Success", "CSV file is downloading.", parent=self.search_screen)
        else:
            out_path = out_path + '.xlsx'
            self.search_result.to_excel(out_path, index=False)
            showinfo("Success", "Excel file is downloading.", parent=self.search_screen)
        showinfo("Success", "File downloaded.", parent=self.search_screen)


  def func(self, pct, allvalues):
    absolute = int(round(pct / 100.*np.sum(allvalues)))

    return "{:d}".format(absolute)


  def get_graphs(self):
    if(self.search_result_set):
      if(self.search_result.shape[0] != 0):
     
        plt.subplot(1, 2, 1)
        plt.pie([self.search_result.shape[0], self.df.shape[0] - self.search_result.shape[0]],labels=['Search Result', 'Remaining'],
        startangle=90, shadow=True,explode=(0.1, 0.1), autopct='%1.2f%%')
        plt.title('Percentages of Search Result\n', fontsize = 12)
        plt.axis('equal')

        plt.subplot(1,2,2)
        plt.pie([self.search_result.shape[0], self.df.shape[0] - self.search_result.shape[0]], labels=['Search Result', 'Remaining'],
        startangle=90, shadow=True,explode=(0.1, 0.1), autopct= lambda pct: self.func(pct, [self.search_result.shape[0], self.df.shape[0] - self.search_result.shape[0]]))
        plt.title('Counts of Search Result\n', fontsize = 12)
        plt.axis('equal')

        plt.subplots_adjust(wspace=0.6, hspace=0.4)
        plt.show()

    else:
      showerror('Error','No search result exists.',parent=self.search_screen)

  
  def bring_widgets(self):
    self.search_tv = self.file_manager.create_treeview(self.search_screen, 250, 750, 0.055, 0)
    info_text = "If an entry area is not filled, it will not be included in the query. If you want to enter an empty value or"
    info_text = info_text + ' null value simply type "nan".'
    info_label = Label(self.search_screen, text=info_text)
    info_label.pack()
    info_label.place(relx = 0.10, rely = 0.39, anchor = 'sw')

    reset_button = Button(self.search_screen, text='Reset', command=self.reset, padx=6, pady=6, bg='#597b45', fg='white')
    reset_button.pack()
    reset_button.place(relx = 0.835, rely = 0.70, anchor = 'sw')

    get_graphs = Button(self.search_screen, text='Get Graphs', command=self.get_graphs, padx=6, pady=6, bg='#597b45', fg='white')
    get_graphs.pack()
    get_graphs.place(relx = 0.73, rely = 0.70, anchor = 'sw')

    download_button = Button(self.search_screen, text='Download Results', command=self.download_helper, pady=6, bg='#597b45', fg='white')
    download_button.pack()
    download_button.place(relx = 0.73, rely = 0.80, width=140, anchor = 'sw')


    label1 = Label(self.search_screen, text="Specify Field Numbers")
    label1.pack()
    label1.place(relx = 0.06, rely = 0.47, anchor = 'sw')
    label2 = Label(self.search_screen, text="Fuzzy Search")
    label2.pack()
    label2.place(relx = 0.25, rely = 0.47, anchor = 'sw')
    label3 = Label(self.search_screen, text="Specify Exact Value")
    label3.pack()
    label3.place(relx=0.47, rely=0.47, anchor='sw')

    self.c1 = Entry(self.search_screen, width=5)
    self.c1.pack()
    self.c1.place(relx = 0.11, rely = 0.51, anchor='sw')
    self.e1 = Entry(self.search_screen)
    self.e1.pack()
    self.e1.place(relx = 0.23, rely = 0.51, anchor='sw')
    self.exact1 = Entry(self.search_screen)
    self.exact1.pack()
    self.exact1.place(relx = 0.46, rely = 0.51, anchor='sw')

    self.c2 = Entry(self.search_screen, width=5)
    self.c2.pack()
    self.c2.place(relx = 0.11, rely = 0.55, anchor = 'sw')
    self.e2 = Entry(self.search_screen)
    self.e2.pack()
    self.e2.place(relx = 0.23, rely = 0.55, anchor = 'sw')
    self.exact2 = Entry(self.search_screen)
    self.exact2.pack()
    self.exact2.place(relx = 0.46, rely = 0.55, anchor='sw')
    
    self.c3 = Entry(self.search_screen, width=5)
    self.c3.pack()
    self.c3.place(relx = 0.11, rely = 0.59, anchor = 'sw')
    self.e3 = Entry(self.search_screen)
    self.e3.pack()
    self.e3.place(relx = 0.23, rely = 0.59, anchor = 'sw')
    self.exact3 = Entry(self.search_screen)
    self.exact3.pack()
    self.exact3.place(relx = 0.46, rely = 0.59, anchor='sw')

    self.c4 = Entry(self.search_screen, width=5)
    self.c4.pack()
    self.c4.place(relx = 0.11, rely = 0.63, anchor = 'sw')
    self.e4 = Entry(self.search_screen)
    self.e4.pack()
    self.e4.place(relx = 0.23, rely = 0.63, anchor = 'sw')
    self.exact4 = Entry(self.search_screen)
    self.exact4.pack()
    self.exact4.place(relx = 0.46, rely = 0.63, anchor='sw')

    self.c5 = Entry(self.search_screen, width=5)
    self.c5.pack()
    self.c5.place(relx = 0.11, rely = 0.67, anchor = 'sw')
    self.e5 = Entry(self.search_screen)
    self.e5.pack()
    self.e5.place(relx = 0.23, rely = 0.67, anchor = 'sw')
    self.exact5 = Entry(self.search_screen)
    self.exact5.pack()
    self.exact5.place(relx = 0.46, rely = 0.67, anchor='sw')

    self.c6 = Entry(self.search_screen, width=5)
    self.c6.pack()
    self.c6.place(relx = 0.11, rely = 0.71, anchor = 'sw')
    self.e6 = Entry(self.search_screen)
    self.e6.pack()
    self.e6.place(relx = 0.23, rely = 0.71, anchor = 'sw')
    self.exact6 = Entry(self.search_screen)
    self.exact6.pack()
    self.exact6.place(relx = 0.46, rely = 0.71, anchor='sw')

    self.c7 = Entry(self.search_screen, width=5)
    self.c7.pack()
    self.c7.place(relx = 0.11, rely = 0.75, anchor = 'sw')
    self.e7 = Entry(self.search_screen)
    self.e7.pack()
    self.e7.place(relx = 0.23, rely = 0.75, anchor = 'sw')
    self.exact7 = Entry(self.search_screen)
    self.exact7.pack()
    self.exact7.place(relx = 0.46, rely = 0.75, anchor='sw')

    self.c8 = Entry(self.search_screen, width=5)
    self.c8.pack()
    self.c8.place(relx = 0.11, rely = 0.79, anchor = 'sw')
    self.e8 = Entry(self.search_screen)
    self.e8.pack()
    self.e8.place(relx = 0.23, rely = 0.79, anchor = 'sw')
    self.exact8 = Entry(self.search_screen)
    self.exact8.pack()
    self.exact8.place(relx = 0.46, rely = 0.79, anchor='sw')

    self.c9 = Entry(self.search_screen, width=5)
    self.c9.pack()
    self.c9.place(relx = 0.11, rely = 0.83, anchor = 'sw')
    self.e9 = Entry(self.search_screen)
    self.e9.pack()
    self.e9.place(relx = 0.23, rely = 0.83, anchor = 'sw')
    self.exact9 = Entry(self.search_screen)
    self.exact9.pack()
    self.exact9.place(relx = 0.46, rely = 0.83, anchor='sw')

    self.c10 = Entry(self.search_screen, width=5)
    self.c10.pack()
    self.c10.place(relx = 0.11, rely = 0.87, anchor = 'sw')
    self.e10 = Entry(self.search_screen)
    self.e10.pack()
    self.e10.place(relx = 0.23, rely = 0.87, anchor = 'sw')
    self.exact10 = Entry(self.search_screen)
    self.exact10.pack()
    self.exact10.place(relx = 0.46, rely = 0.87, anchor='sw')

    search_button = Button(self.search_screen, text='Search', command=self.search, padx=6, pady=6, bg='#597b45', fg='white')
    search_button.pack()
    search_button.place(relx = 0.25, rely = 0.95, anchor = 'sw')



  def search_screen(self, root, img):
    self.search_screen = Toplevel(root)
    self.search_screen.geometry("850x700")
    self.search_screen.title("Search For Duplicate")
    self.search_screen.iconphoto(False, img)

    self.bring_widgets()
  
