import csv
import Backend.class_professor as class_professor
import Backend.class_prof_manager as class_prof_manager
import Backend.class_course as class_course
from Backend.script import ACM_Script
import pandas as pd

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
    

class Data():
    def __init__(self):
        self.filename = ""

    def set_filename(self,filename):
        self.filename = filename

    def get_filename(self,filename):
        return self.filename


class ACM_Data(Data,metaclass=Singleton):
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
        return pd.read_csv(filename)
        

    def normalize_df_headers(self,df):
        df.columns = df.columns.str.lower().str.replace(" ", "_")
        return df

    def drop_columns(self,df,column_names):
        try:
            return df.drop(columns=column_names)
        
        except:return df


    def add_columns(self,df,column_names):
        for column in column_names:
            df[column] = ""
        return df

    def df_to_csv(self,df,filename):
        df.to_csv(filename, index=False)


    def clean_df(self,df):
        #Removes Classes that have a time that is TBA
        df.columns = df.columns.str.lower().str.replace(" ","_")

        df = df.copy()
        df = df[df["times"] != "TBA"]

        #Removes all Graduate level classes
        course_numeric = pd.to_numeric(df["course"], errors="coerce")
        df = df[course_numeric <= 5000].copy()
        # Keep course numbers in output without trailing decimals (e.g. 1336 not 1336.0).
        df["course"] = course_numeric.loc[df.index].astype("Int64").astype("string").fillna("")


        #Any classes that don't have confirmed teachers
        df = df[df["instructor"] != "Staff"]


        #Any classes that are a syncrhnous
        df = df[(df["meeting_type"] != "Online only, no set time")]
        df = df[df["times"] != ""]

        #df = df[df["course"].astype(int) < 2000]

        #Any classes that are a syncrhnous
        

        # Any classes that are Independent Study

        df = df[df["title"] != "Independent Study"]
        return df
        

    def df_to_teacher_manager(self,df,notion_import = False):
        manager = class_prof_manager.Manager()
        
        for row in df.itertuples(index = False):
            raw_course_num = row.course
            if pd.isna(raw_course_num):
                course_num = ""
            elif isinstance(raw_course_num, float) and raw_course_num.is_integer():
                course_num = str(int(raw_course_num))
            else:
                course_num = str(raw_course_num)

            course = class_course.Course(
                row.title,
                row.times,
                row.meeting_days,
                course_num,
                row.campus,
            )
            
            if notion_import:
                course.change_presenter(row.presenter)
                course.change_presentation_date(row.presentation_date)

            raw_prof_name = row.instructor
            if pd.isna(raw_prof_name):
                continue
            prof_name = str(raw_prof_name).strip()
            if prof_name == "":
                continue
            #checks to see if the professor has already been created in the manager
            if manager.check_professors(prof_name):
                
                    professor = manager.grab_remove_prof_obj(prof_name)
                        
                
            else:
                professor = class_professor.Professor(prof_name)
                    

            professor.add_course(course)
                    
            manager.add_prof_obj(professor)
        
            
        return manager

    def write_scripts(self,manager,script):
        for professor in manager.professors:
            ACM_Script.generate_script(professor,script)


    SIGN_UP_COLUMNS_TO_ADD = [
        "confirmed",
        "status",
        "presenter",
        "presentation_date",
        "flyer",
    ]
    SIGN_UP_COLUMNS_TO_DROP = [
        "status",
        "section",
        "crn",
        "cred",
        "date",
        "weeks",
        "seats",
        "enrolled",
        "available",
        "wait_list",
        "final_exam",
        "fees",
        "notes",
    ]

    def create_sign_up_df(self,df) -> pd.DataFrame:
        """Pure transform: raw course rows -> the sign-up roster, no file I/O."""
        df = self.normalize_df_headers(df)
        df = self.clean_df(df)
        df = self.add_columns(df,self.SIGN_UP_COLUMNS_TO_ADD)
        df = self.drop_columns(df,self.SIGN_UP_COLUMNS_TO_DROP)
        return df

    def create_sign_up(self,filename):
        df = self.csv_to_df(filename)
        df = self.create_sign_up_df(df)

        output_name = filename + "_output.csv"
        self.df_to_csv(df,output_name)
        return output_name

    def create_email_scripts_df(self,df):
        """Pure transform: roster rows -> a Manager of professors/courses, ready for write_scripts."""
        df = self.normalize_df_headers(df)
        df = self.clean_df(df)
        notion_import = "presenter" in df.columns and "presentation_date" in df.columns
        return self.df_to_teacher_manager(df,notion_import=notion_import)

    def create_email_scripts(self,filename,script):
        df = self.csv_to_df(filename)
        manager = self.create_email_scripts_df(df)
        self.write_scripts(manager,script)

    def create_heatmap_df(self,df):
        from Backend.heat_calendar import build_heatmap_dataframe

        df = self.normalize_df_headers(df)
        df = self.clean_df(df)
        return build_heatmap_dataframe(df)

    def create_heatmap(self,filename):
        df = self.csv_to_df(filename)
        return self.create_heatmap_df(df)
