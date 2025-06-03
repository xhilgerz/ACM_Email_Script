import csv
import class_professor
import class_prof_manager
import class_course
import script

def check_row(item):
    if item == "":
        item = "N/A"
    return item


def read_data():
    print("What name would you like to have on the email (both first and last name.)")
    userName = input()
    
    with open('Fall_2025_clean.csv','r') as infile:
        reader = csv.reader(infile)
        manager = class_prof_manager.Manager()
        
        next(reader)
        i = 0
        for row in reader:
            prof_name = row[12]
            course_name = check_row(row[5])
            course_time = check_row(row[8])
            course_date = check_row(row[7])
            course_num = check_row(row[2])
            course_campus = check_row(row[10])

            if prof_name == "":
                continue

            if manager.check_professors(prof_name):
                #print("Found " +prof_name)
                professor = manager.grab_remove_prof_obj(prof_name)
                
            else:
                #print("Created " +prof_name)
                professor = class_professor.Professor(prof_name)
                i = i+1
            
            course = class_course.Course(course_name,course_time,course_date,course_num,course_campus)

            professor.add_course(course)
            
            manager.add_prof_obj(professor)

            
        
        
        for professor in manager.professors:
            script.generate_script(professor,userName)

        
    
    





            
        



        
