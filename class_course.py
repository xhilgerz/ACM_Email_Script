"""
Course object that represents a course and its corresponding info
"""
class Course:
    def __init__(self,name,time,date,course_num,campus):

        self.name = name
        self.time = time
        self.date = date
        self.course_num = course_num
        self.campus = campus

    
    def change_name(self,name):
        self.name = name
    
    def change_time(self,time):
        self.time = time
    
    def change_date(self,meeting):
        self.date = meeting

    def change_course_num(self,course_num):
        self.course_num = course_num

    def change_course_type(self,campus):
        self.campus = campus
    
