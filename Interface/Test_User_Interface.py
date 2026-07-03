from Interface.Data_User_Interface import DataUserInterface
from Backend.Test_data import Test_Data
import pandas as pd
class Test_User_Interface(DataUserInterface):
    @staticmethod
    def get_heatmap_df(file_name) -> pd.DataFrame:
        #implement
        print("heatmap df interface")
        data = Test_Data()
        data.set_filename(file_name)
        df = data.create_heatmap(file_name)
        return df
     
    def get_script(self) -> str:
        return Test_Data.get_script

    def post_script(self,script:str):
        Test_Data.set_script(script)
        pass
    
    def post_csv(self,file_name):
        Test_Data.set_filename = file_name

        pass
        #implement

    def post_scripts_csv(self,file_name):
        Test_Data.set_filename = file_name
        Test_Data.create_email_scripts()

        pass
    @staticmethod
    def post_sign_up_csv(file_name):
        data = Test_Data()
        print("Sign up Interface")
        data.set_filename = file_name
        print("set filename")
        data.create_sign_up(file_name)


        pass