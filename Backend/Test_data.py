import csv
import Backend.class_professor as class_professor
import Backend.class_prof_manager as class_prof_manager
import Backend.class_course as class_course
from Backend.script import ACM_Script
from Backend.data import Data,Singleton

import pandas as pd




class Test_Data(Data,metaclass=Singleton):

    filename = None
    def __init__(self):
        super().__init__()
    


    def check_item(self,item):
        if item == "":
            item = ""
        return item 

    """
    Read reads each row of the csv and creates a corresponding Professor Object and adds their correspoding corse objects
    """ 
                
    def csv_to_df(self,filename,):
        print("Csv to df")
        

    def normalize_df_headers(self,df):
        print("Normalizes df headers")

    def drop_columns(self,df,column_names):
        print("Drop columns")


    def add_columns(self,df,column_names):
        print("Added columns")
        return None

    def df_to_csv(self,df,filename):
        print("df to csv")


    def clean_df(self,df):
        #Removes Classes that have a time that is TBA
        df = None
        print("cleans Dataframe")
        return df
        

    def df_to_teacher_manager(self,df,notion_import = False):
        #manager = class_prof_manager.Manager()
        manager = None
        print("created df from teacher manager")
        
            
        return manager

    def write_scripts(self,manager,script):
        print("Write scripts")

    
    def create_sign_up(self,filename):
        print("created sign up")

    


        
    def create_email_scripts(self,filename,script):
        df = self.csv_to_df(filename)
        print("writes the scripts")


        
    def create_heatmap(self,filename):
        print("creates heatmap")
        df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
        )
        return self.create_df_heatmap(df)

        

    def create_df_heatmap(self,df):
        
        print("heatmap hit")
        print(df)
        return df
        

        
    