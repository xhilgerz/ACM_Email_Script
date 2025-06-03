
from cleanData import cleanData
from read_data import read_data

def main():
    print("1: Clean Data")
    print("2: Write teacher scripts")

    choice = input()

    if choice == "1":
        print("This function removes all classes that have times with TBA within this dataset as well as professors labeled as STAFF. Do you want to continue Y /N")

        inputs = input()

        if(inputs =="Y" or inputs == "y"):
            cleanData()
            print("Copy created Succesfully ")  
            exit()
        
        else:
            exit()

    
    if choice == "2":
        read_data()
        print("Scripts created succesfully.")


main()