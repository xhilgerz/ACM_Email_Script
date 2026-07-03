
import os

import pandas as pd
"""
Writes each professor and their corresponding class into .txt file which is then stored in a folder. The name of each file is last_first_middle
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Class_Script:

    def __init__(self):
        self.script = ""
        self.first_name = "Null"
        self.last_name = "Null"
        pass

    def set_name(first_name,last_name):
        pass

    def generate_script():
        pass

    def get_script():
        pass

    def set_script():
        pass

    def get_first_name():
        pass

    def get_last_name():
        pass

    def edit_script(self,script):
        pass
        

class ACM_Script(Class_Script, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.script = f"Greetings!\n\tI hope the start of the semester has been treating you well. My name is {self.first_name} {self.last_name} and I represent the Association for Computing Machinery or ACM. If you haven't heard of ACM before we are a computer science organization that strives to help fellow students learn more about coding and programming through community, workshops, hackathons, and other events. As ACM's Open House approaches, we wanted to see if we could send a representative of ACM to very briefly present what ACM is about and our upcoming events for the semester. If your interested please let us know, and confirm if we have all the correct classes below."
        pass


    def set_name(self,first_name,last_name):
        self.first_name = first_name
        self.last_name = last_name
        pass

    def get_script(self):
        return self.script
    
    def set_script(self,script):
        self.script = script
    
    def get_first_name(self):
        return self.first_name
    
    def get_last_name(self):
        return self.last_name
    
    def generate_script(professor,script):

        output_folder = "teacher_files"

        os.makedirs(output_folder, exist_ok=True)

        raw_name = professor.name
        if raw_name is None:
            safe_name = "unknown_professor"
        elif isinstance(raw_name, float) and raw_name != raw_name:
            safe_name = "unknown_professor"
        else:
            safe_name = str(raw_name).strip() or "unknown_professor"

        name_arr = safe_name.replace('.','').replace(' ','_').replace(',','')
        filename = name_arr +".txt"
        
        file_path = os.path.join(output_folder, filename)
        with open(file_path,'w') as outfile:
            outfile.write(ACM_Script.script+"\n"+"\n")
            for course in professor.courses:
                presenter_missing = pd.isna(course.presenter) or str(course.presenter).strip() == ""
                date_missing = pd.isna(course.presentation_date) or str(course.presentation_date).strip() == ""
                asynchronous = pd.isna(course.date) or str(course.date).strip() =="" and pd.isna(course.time) or str(course.time).strip() ==""

                info = f"CS {course.course_num} {course.name} {course.date} {course.time} {course.campus} presented by {course.presenter} on {course.presentation_date}\n"

                if asynchronous:
                    info = f"Since {course.course_num} {course.name}is an asynchronous class we'd like for you to post the video in canvas.\n"
                elif presenter_missing and date_missing:
                    info = f"While no representatives are signed up for {course.course_num} {course.name} {course.date} {course.time} {course.campus}. It would be a great help if you showed the video in class\n"

                


                info = info + "\n"
                outfile.write(info)



    pass








    #df = df[(df["meeting_type"] != "Online only, no set time")]
     #df = df[df["times"] != ""]