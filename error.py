import tkinter as tk
from tkinter import messagebox


def check_filename(filename):
    if filename == "":
        messagebox.showinfo(f"No file chosen")


def header_error_print(header,line):

    if header != line:
        error_print(line)
        exit()
    

def error_print(line):
    print(f"Error: Missing {line} column")


def check_header_line(header):

    try:
        header_error_print(header[12], "Instructor")

    except IndexError:
        print(f"Error: Missing 'Instructor' column (file only has {len(header)} columns)")
             
    try:
        header_error_print(header[5],"Title")

    except IndexError:
        print(f"Error: Missing 'Instructor' column (file only has {len(header)} columns)")


    try:
        header_error_print(header[8],"Times")

    except IndexError:
        print(f"Error: Missing 'Instructor' column (file only has {len(header)} columns)")
    
    try:
        header_error_print(header[7],"Meeting Days")

    except IndexError:
        print(f"Error: Missing 'Instructor' column (file only has {len(header)} columns)")
    
    try:
        header_error_print(header[2],"Course")

    except IndexError:
        print(f"Error: Missing 'Instructor' column (file only has {len(header)} columns)")

    try:
        header_error_print(header[10],"Campus")

    except IndexError:
        print(f"Error: Missing 'Instructor' column (file only has {len(header)} columns)")
        


