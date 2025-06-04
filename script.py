import csv
import os
"""
Writes each professor and their corresponding class into .txt file which is then stored in a folder. The name of each file is last_first_middle
"""
def generate_script(professor,name,script):

    output_folder = "teacher_files"

    os.makedirs(output_folder, exist_ok=True)
    
    name_arr = professor.name.replace('.','').replace(' ','_').replace(',','')
    filename = name_arr +".txt"
    
    file_path = os.path.join(output_folder, filename)
    with open(file_path,'w') as outfile:
        outfile.write(script+"\n"+"\n")
        for course in professor.courses:
            info ="CS " +course.course_num +" " +course.name +" "+ course.date + " "+course.time+ " " +course.campus+"\n"
            outfile.write(info)

