import csv
import class_professor
import class_prof_manager
import class_course
from script import generate_script
import error

"""
Cleans the data by removing any rows or classes that are TBA or have unknown teachers (Staff)
"""

def clean_data(filename):
    arr = filename.split(".")
    newfile = arr[0]+"_clean.csv"
    #print(newfile)
    with open(filename,'r') as infile,open(newfile, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        header = next(reader)

        error.check_header_line(header)

        infile.seek(0)  # Rewind file pointer
        reader = csv.reader(infile) 

        for row in reader:


            try:
                if row[8] != "TBA" and row[12] != "Staff":
                    #print(row[5])
                    writer.writerow(row)
            except IndexError as e:
                    print(f"Error: Missing column in row - {e}")
                    continue  # Skip to next row
            except ValueError as e:
                    print(f"Invalid data format: {e}")
                    continue
            except Exception as e:
                    print(f"Unexpected error processing row: {e}")
                    continue

        return newfile
    
"""
Checks the inserted row item and if it has nothing in it. It will fill the empty space with Not Listed. 
"""

def check_item(item):
    if item == "":
        item = ""
    return item 

"""
Read reads each row of the csv and creates a corresponding Professor Object and adds their correspoding corse objects
"""
    

def read_data(filename,script):
    
    
    with open(filename,'r') as infile:
        reader = csv.reader(infile)

        manager = class_prof_manager.Manager()
        
        error.check_header_line(next(reader))
        i = 0

        for row in reader:
                
                try:
                    prof_name = check_item(row[12])
                    course_name = check_item(row[5])
                    course_time = check_item(row[8])
                    course_date = check_item(row[7])
                    course_num = check_item(row[2])
                    course_campus = check_item(row[10])
                    
                except IndexError as e:
                    print(f"Error: Missing column in row - {e}")
                    continue  # Skip to next row
                except ValueError as e:
                    print(f"Invalid data format: {e}")
                    continue
                except Exception as e:
                    print(f"Unexpected error processing row: {e}")
                    continue


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
            generate_script(professor,script)

   
     

            