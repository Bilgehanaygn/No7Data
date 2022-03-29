from tkinter import Label, Toplevel, Entry, Button
import pandas as pd



class SearchScreen():
  def __init__(self, file_manager_instance, df):
    self.file_manager = file_manager_instance
    self.df = df
    self.match_label = None

  
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

    related_column_index[0].append(self.e1.get())
    related_column_index[1].append(self.e2.get())
    related_column_index[2].append(self.e3.get())
    related_column_index[3].append(self.e4.get())
    related_column_index[4].append(self.e5.get())
    related_column_index[5].append(self.e6.get())
    related_column_index[6].append(self.e7.get())
    related_column_index[7].append(self.e8.get())

    not_null_related_column = []

    for i in related_column_index:
      if((i[1].strip() != "") and (i[0] != "")):
          not_null_related_column.append(i)

    search_result_exist = False

    for item in not_null_related_column:
      if(not search_result_exist):
        search_result = self.df[self.df[self.df.columns[item[0]]].str.contains(item[1], na=False, case=False)]

      else:
        search_result = search_result[search_result[self.df.columns[item[0]]].str.contains(item[1], na=False, case=False)]


      search_result_exist = True
    
    if(search_result_exist):
      self.file_manager.insert_tv(self.search_tv, search_result)

      if(self.match_label == None):
          self.match_label = Label(self.search_screen)
          self.match_label.pack()
          self.match_label.place(relx = 0.60, rely = 0.60, anchor = 'sw')

      if(search_result.shape[0] == 0):
        temp = pd.DataFrame({'Search Result: ':'NO ITEM FOUND!'}, index=[0])
        self.file_manager.insert_tv(self.search_tv, temp)
        
        self.match_label["text"] = "No item matches the given values."
      else:
        self.match_label["text"] = str(search_result.shape[0]) + " item matches the given values."


  
  def bring_widgets(self):
    self.search_tv = self.file_manager.create_treeview(self.search_screen, 250, 750, 0, 0)
    info_text = "! If an entry area is not filled, it will not be included in the query. If you want to enter an empty value or"
    info_text = info_text + ' null value simply type "nan".'
    info_label = Label(self.search_screen, text=info_text)
    info_label.pack()
    info_label.place(relx = 0.07, rely = 0.45, anchor = 'sw')
    label1 = Label(self.search_screen, text="Specify Field Numbers")
    label1.pack()
    label1.place(relx = 0.19, rely = 0.53, anchor = 'sw')
    label2 = Label(self.search_screen, text="Specify Value")
    label2.pack()
    label2.place(relx = 0.38, rely = 0.53, anchor = 'sw')
    self.c1 = Entry(self.search_screen, width=5)
    self.c1.pack()
    self.c1.place(relx = 0.245, rely = 0.57, anchor = 'sw')
    self.e1 = Entry(self.search_screen)
    self.e1.pack()
    self.e1.place(relx = 0.36, rely = 0.57, anchor = 'sw')

    self.c2 = Entry(self.search_screen, width=5)
    self.c2.pack()
    self.c2.place(relx = 0.245, rely = 0.61, anchor = 'sw')
    self.e2 = Entry(self.search_screen)
    self.e2.pack()
    self.e2.place(relx = 0.36, rely = 0.61, anchor = 'sw')
    
    self.c3 = Entry(self.search_screen, width=5)
    self.c3.pack()
    self.c3.place(relx = 0.245, rely = 0.65, anchor = 'sw')
    self.e3 = Entry(self.search_screen)
    self.e3.pack()
    self.e3.place(relx = 0.36, rely = 0.65, anchor = 'sw')

    self.c4 = Entry(self.search_screen, width=5)
    self.c4.pack()
    self.c4.place(relx = 0.245, rely = 0.69, anchor = 'sw')
    self.e4 = Entry(self.search_screen)
    self.e4.pack()
    self.e4.place(relx = 0.36, rely = 0.69, anchor = 'sw')

    self.c5 = Entry(self.search_screen, width=5)
    self.c5.pack()
    self.c5.place(relx = 0.245, rely = 0.73, anchor = 'sw')
    self.e5 = Entry(self.search_screen)
    self.e5.pack()
    self.e5.place(relx = 0.36, rely = 0.73, anchor = 'sw')

    self.c6 = Entry(self.search_screen, width=5)
    self.c6.pack()
    self.c6.place(relx = 0.245, rely = 0.77, anchor = 'sw')
    self.e6 = Entry(self.search_screen)
    self.e6.pack()
    self.e6.place(relx = 0.36, rely = 0.77, anchor = 'sw')

    self.c7 = Entry(self.search_screen, width=5)
    self.c7.pack()
    self.c7.place(relx = 0.245, rely = 0.81, anchor = 'sw')
    self.e7 = Entry(self.search_screen)
    self.e7.pack()
    self.e7.place(relx = 0.36, rely = 0.81, anchor = 'sw')

    self.c8 = Entry(self.search_screen, width=5)
    self.c8.pack()
    self.c8.place(relx = 0.245, rely = 0.85, anchor = 'sw')
    self.e8 = Entry(self.search_screen)
    self.e8.pack()
    self.e8.place(relx = 0.36, rely = 0.85, anchor = 'sw')

    search_button = Button(self.search_screen, text='Search', command=self.search, padx=2, pady=1, bg='#597b45', fg='white')
    search_button.pack()
    search_button.place(relx = 0.37, rely = 0.925, anchor = 'sw')



  def search_screen(self, root):
    self.search_screen = Toplevel(root)
    self.search_screen.geometry("850x600")
    self.search_screen.title("Search For Duplicate")
    self.bring_widgets()
  
            










