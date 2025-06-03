class Professor:
    def __init__(self,name):
        self.name = name
        self.courses = []

    


    def add_course(self, class_obj):
        if not hasattr(class_obj, 'course_num'):
            raise ValueError("Expects Class Object")
        self.courses.append(class_obj)

    
    def change_name(self,name):
        self.name = name
    
    def remove_course_at(self, index):
        self.courses.pop(index)

    

    

    




