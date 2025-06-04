import csv
import os
"""
Writes each professor and their corresponding class into .txt file which is then stored in a folder. The name of each file is last_first_middle
"""
def generate_script(professor,name):

    output_folder = "teacher_files"

    os.makedirs(output_folder, exist_ok=True)
    
    name_arr = professor.name.replace('.','').replace(' ','_').replace(',','')
    filename = name_arr +".txt"
    
    file_path = os.path.join(output_folder, filename)
    with open(file_path,'w') as outfile:
        script = f"Greetings!\n\tI hope the start of the semester has been treating you well. My name is Zander Brysch and I am the membership officer of the Association of Computer Machinery or ACM. If you haven't heard of ACM before we are a computer science organization that strives to help fellow students learn more about coding and programming through community, workshops, hackathons, and other events. As ACM's Open House approaches, we wanted to see if we could send a representative of ACM to very briefly present what ACM is about and our upcoming events for the semester. If your interested please let us know, and confirm if we have all the correct classes below."
        outfile.write(script+"\n"+"\n")
        for course in professor.courses:
            info ="CS " +course.course_num +" " +course.name +" "+ course.date + " "+course.time+ " " +course.campus+"\n"
            outfile.write(info)

