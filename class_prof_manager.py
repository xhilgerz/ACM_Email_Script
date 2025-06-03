class Manager:

    def __init__(self):
        self.professors = []


    def check_professors(self,name):
        for professor in self.professors:
            if(professor.name == name):
                return True 
        return False   
            
    def grab_prof_obj(self,name):
        for professor in self.professors:
            if(professor.name == name):
                
                return professor
        
        return None
    def add_prof_obj(self,professor):
        self.professors.append(professor)

    def remove_prof_at(self, index):
        self.professors.pop(index)

    def grab_remove_prof_obj(self,name):
        for i,professor in enumerate(self.professors):
            if(professor.name == name):
                self.professors.pop(i)
                return professor
        
            
