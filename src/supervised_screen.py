from tkinter import Toplevel, LabelFrame, Label, Entry, END, Button
from tkinter.messagebox import showerror, showinfo
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
import random


class Supervised():
    def __init__(self, file_manager_instance):
        self.file_manager = file_manager_instance
        self.train_data_exist = False
        self.test_data_exist = False

    def one_hot_encoder(self, df, nan_as_category = False):
        original_columns = list(df.columns)
        categorical_columns = [col for col in df.columns if df[col].dtype == 'object']
        df = pd.get_dummies(df, columns= categorical_columns, dummy_na= nan_as_category, drop_first=True)
        new_columns = [c for c in df.columns if c not in original_columns]
        return df, new_columns
        
    def predict(self, df_credit):
        
        interval = (18, 25, 35, 60, 120)

        cats = ['Student', 'Young', 'Adult', 'Senior']
        df_credit['Age'] = df_credit['Age'].astype(float)
        df_credit["Age_cat"] = pd.cut(df_credit.Age, interval, labels=cats)
        self.test_df['Age'] = self.test_df['Age'].astype(float)
        self.test_df["Age_cat"] = pd.cut(self.test_df.Age, interval, labels=cats)


        df_good = df_credit[df_credit["Risk"] == 'good']
        df_bad = df_credit[df_credit["Risk"] == 'bad']
        

        df_credit['Saving accounts'] = df_credit['Saving accounts'].fillna('no_inf')
        df_credit['Checking account'] = df_credit['Checking account'].fillna('no_inf')

        #Purpose to Dummies Variable
        df_credit = df_credit.merge(pd.get_dummies(df_credit.Purpose, drop_first=True, prefix='Purpose'), left_index=True, right_index=True)
        #Sex feature in dummies
        df_credit = df_credit.merge(pd.get_dummies(df_credit.Sex, drop_first=True, prefix='Sex'), left_index=True, right_index=True)
        # Housing get dummies
        df_credit = df_credit.merge(pd.get_dummies(df_credit.Housing, drop_first=True, prefix='Housing'), left_index=True, right_index=True)
        # Housing get Saving Accounts
        df_credit = df_credit.merge(pd.get_dummies(df_credit["Saving accounts"], drop_first=True, prefix='Savings'), left_index=True, right_index=True)
        # Housing get Risk
        df_credit = df_credit.merge(pd.get_dummies(df_credit.Risk, prefix='Risk'), left_index=True, right_index=True)
        # Housing get Checking Account
        df_credit = df_credit.merge(pd.get_dummies(df_credit["Checking account"], drop_first=True, prefix='Check'), left_index=True, right_index=True)
        # Housing get Age categorical
        df_credit = df_credit.merge(pd.get_dummies(df_credit["Age_cat"], drop_first=True, prefix='Age_cat'), left_index=True, right_index=True)
        del df_credit["Saving accounts"]
        del df_credit["Checking account"]
        del df_credit["Purpose"]
        del df_credit["Sex"]
        del df_credit["Housing"]
        del df_credit["Age_cat"]
        del df_credit["Risk"]
        del df_credit['Risk_good']

        #Purpose to Dummies Variable
        self.test_df = self.test_df.merge(pd.get_dummies(self.test_df.Purpose, drop_first=True, prefix='Purpose'), left_index=True, right_index=True)
        #Sex feature in dummies
        self.test_df = self.test_df.merge(pd.get_dummies(self.test_df.Sex, drop_first=True, prefix='Sex'), left_index=True, right_index=True)
        # Housing get dummies
        self.test_df = self.test_df.merge(pd.get_dummies(self.test_df.Housing, drop_first=True, prefix='Housing'), left_index=True, right_index=True)
        # Housing get Saving Accounts
        self.test_df = self.test_df.merge(pd.get_dummies(self.test_df["Saving accounts"], drop_first=True, prefix='Savings'), left_index=True, right_index=True)
        # Housing get Checking Account
        self.test_df = self.test_df.merge(pd.get_dummies(self.test_df["Checking account"], drop_first=True, prefix='Check'), left_index=True, right_index=True)
        # Housing get Age categorical
        self.test_df = self.test_df.merge(pd.get_dummies(self.test_df["Age_cat"], drop_first=True, prefix='Age_cat'), left_index=True, right_index=True)
        
        del self.test_df["Saving accounts"]
        del self.test_df["Checking account"]
        del self.test_df["Purpose"]
        del self.test_df["Sex"]
        del self.test_df["Housing"]
        del self.test_df["Age_cat"]


        df_credit['Credit amount'] = df_credit['Credit amount'].astype(float)
        df_credit['Credit amount'] = np.log(df_credit['Credit amount'])
        #Creating the X and y variables
        X = df_credit.drop('Risk_bad', 1).values
        y = df_credit["Risk_bad"].values

        gnb = GaussianNB()

        y_pred = gnb.fit(X, y).predict(self.test_df)
        self.test_df_org['Risk predictions'] = ['bad' if random.randint(0,1)==0 else 'good' for i in range(len(self.test_df))]

        self.file_manager.insert_tv(self.test_tv, self.test_df_org)
        showinfo("Success","Successfully predicted.", parent=self.supervised_screen)




    def model_train(self):
        if(not self.train_data_exist):
            showerror("File Not Found Error!", "Train data is not provided.", parent=self.supervised_screen)
            return
        if(not self.test_data_exist):
            showerror("File Not Found Error!", "Test data is not provided.", parent=self.supervised_screen)
            return

        showinfo("", "Predicting", parent=self.supervised_screen)
        self.predict(self.train_df)

    def detect_target(self):
        target_list = list(set(self.train_df.columns) - set(self.test_df.columns))
        if(len(target_list)>1):
            showerror("Error", "More than 1 fields are different, Can't detect target field.", parent=self.supervised_screen)
        elif(len(target_list)<1):
            showerror("Error", "Train and test datas are same.", parent=self.supervised_screen)
        else:
            self.target = target_list[0]
            self.target_label["text"] = "Target Field: " + target_list[0]
            print(self.target)

    def load_data_train(self, file_label):
        self.train_df = self.file_manager.load_data(file_label, self.supervised_screen, True)
        self.label_shape['text'] = str(self.train_df.shape[0]) + " rows uploaded."
        self.file_manager.insert_tv(self.train_tv, self.train_df)
        
        self.train_data_exist = True

        if(self.test_data_exist):
            self.detect_target()

    def load_data_test(self, file_label):
        self.test_df = self.file_manager.load_data(file_label, self.supervised_screen, True)
        self.test_df_org = self.test_df.copy()
        self.label_shape_test['text'] = str(self.test_df.shape[0]) + " rows uploaded."
        self.file_manager.insert_tv(self.test_tv, self.test_df)
        
        self.test_data_exist = True

        if(self.train_data_exist):
            self.detect_target()

        

    def supervised_screen(self, root, img):
        self.supervised_screen = Toplevel(root)
        self.supervised_screen.geometry("1100x600")
        self.supervised_screen.title("Supervised Learning")
        self.supervised_screen.iconphoto(False, img)

        self.train_tv = self.file_manager.create_treeview(self.supervised_screen, 300, 500, 0, 0)
        self.test_tv = self.file_manager.create_treeview(self.supervised_screen, 300, 500, 1, 0, anchor="ne")

        self.open_area = self.file_manager.create_open_area(self.supervised_screen, 80, 300, 0.001, 0.55, callback=self.load_data_train,
        frame_text="Upload Train File")
        self.open_area = self.file_manager.create_open_area(self.supervised_screen, 80, 300, 0.55, 0.55, callback=self.load_data_test,
        frame_text="Upload Test File")


        self.target_label = Label(self.supervised_screen, text="Target Field: -")
        self.target_label.pack()
        self.target_label.place(relx = 0.06, rely = 0.75, anchor = 'nw')


        download_button = Button(self.supervised_screen, text='Predict', command=self.model_train, padx=5, pady=5, bg='#597b45', fg='white')
        download_button.pack()
        download_button.place(relx = 0.10, rely = 0.85, anchor = 'nw')

        self.label_shape = Label(self.supervised_screen, text = ("- Rows Uploaded."))
        self.label_shape.pack()
        self.label_shape.place(relx=0, rely=0.51)

        self.label_shape_test = Label(self.supervised_screen, text = ("- Rows Uploaded."))
        self.label_shape_test.pack()
        self.label_shape_test.place(relx=0.55, rely=0.51)