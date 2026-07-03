from abc import ABC, abstractmethod
import pandas as pd
from Interface.Data_User_Interface import DataUserInterface
from Backend.script import ACM_Script
from Backend.data import ACM_Data


class ACM_User_Interface(DataUserInterface):
    
    def get_heatmap_df(self,file_name) -> pd.DataFrame:
        #implement
        ACM_Data.set_filename = file_name
        return ACM_Data.create_heatmap(file_name)
    
    def get_script(self) -> str:
        return ACM_Script.get_script

    def post_script(self,script:str):
        ACM_Script.set_script(script)
        pass
    
    def post_csv(self,file_name):
        ACM_Data.set_filename = file_name

        pass
        #implement

    def post_scripts_csv(self,file_name):
        ACM_Data.set_filename = file_name
        ACM_Data.create_email_scripts()

        pass

    def post_sign_up_csv(self,file_name):
        ACM_Data.set_filename = file_name
        ACM_Data.create_sign_up(file_name)


        pass


