import tkinter as tk
from tkinter import filedialog, messagebox,scrolledtext
from tkinter import Tk, Label
from data import clean_data
from data import read_data
import sys
import os
from heat_calendar import load_csv

from PIL import Image, ImageTk

class ACMEmailGenerator:
    def __init__(self):
        self.filename = ""
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.root.title("ACM Email Generator")
        self.image_url ="images/ACM.png"
        self.tk_image = ""
        self.username = "FIRST_NAME LAST_NAME"
        self.script = f"Greetings!\n\tI hope the start of the semester has been treating you well. My name is {self.username} and I am the membership officer of the Association of Computer Machinery or ACM. If you haven't heard of ACM before we are a computer science organization that strives to help fellow students learn more about coding and programming through community, workshops, hackathons, and other events. As ACM's Open House approaches, we wanted to see if we could send a representative of ACM to very briefly present what ACM is about and our upcoming events for the semester. If your interested please let us know, and confirm if we have all the correct classes below."
        self.default_script = f"Greetings!\n\tI hope the start of the semester has been treating you well. My name is {self.username} and I am the membership officer of the Association of Computer Machinery or ACM. If you haven't heard of ACM before we are a computer science organization that strives to help fellow students learn more about coding and programming through community, workshops, hackathons, and other events. As ACM's Open House approaches, we wanted to see if we could send a representative of ACM to very briefly present what ACM is about and our upcoming events for the semester. If your interested please let us know, and confirm if we have all the correct classes below."
        
        
        self.setup_ui()
        
    """
    Sets up the starting window UI for user interaction
    """
    
    def setup_ui(self):
        # resizing the image
        img_path =  self.resource_path(self.image_url)
        image = Image.open(img_path)
        new_width = 100
        new_height = 100
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Convert to Tkinter format
        self.tk_image = ImageTk.PhotoImage(image)  # Store as instance variable

        # Presenting the image
        logo = Label(self.root, image=self.tk_image)
        logo.pack()

        # Add a label
        label = tk.Label(self.root, text="Welcome to ACM Email Generator")
        label.pack(pady=10)
        
        # File selection button
        choose_file = tk.Button(self.root, text="Open File", command=self.open_file)
        choose_file.pack(pady=10)

        # Entry box 
        self.prefix_entry = tk.Entry(self.root, width=30)
        
        # Action buttons (initially disabled)
        self.clean_button = tk.Button(self.root, text="Clean Data", 
                                    command=self.on_clean_button_click,
                                    state=tk.DISABLED)
        self.clean_button.pack(pady=10)
        
        self.script_button = tk.Button(self.root, text="Write teacher scripts", 
                                     command=self.on_script_button_click,
                                     state=tk.DISABLED)
        self.script_button.pack(pady=10)

        self.edit_script_button = tk.Button(self.root, text="Edit Script", 
                                     command=self.edit_script_button_click)
        self.edit_script_button.pack(pady=10)

        self.create_calendar = tk.Button(self.root, text="Create Week Calendar", 
                                    command=self.on_create_calendar_click,
                                    state=tk.DISABLED)
        self.create_calendar.pack(pady=10)
        
        self.clean_button.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(self.root, text="No file selected")
        self.status_label.pack(pady=10)

    """
    Checks if it is being run as an executable or as a script and adapts accordingly so the program can still find the ACM Image
    """
    
    def resource_path(self,relative_path):

        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    """
    Opens the file directory for the user to find the desired csv file
    """
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if file_path:
            self.filename = file_path
            self.status_label.config(text=f"Selected: {file_path}")
            self.clean_button.config(state=tk.NORMAL)
            self.script_button.config(state=tk.NORMAL)
            self.create_calendar.config(state=tk.NORMAL)
    
    """
    When the button is clicked the chosen csv file is cleaned removing any unnecessary data from the csv 
    """
    def on_clean_button_click(self):
        try:
            filename = clean_data(self.filename)
            print(filename)
            end_name= filename.split('/')
            
            end_name = end_name[-1]
            print(end_name)
            messagebox.showinfo("Success", f"Copy created successfully: {end_name}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    """
    The cleaned csv ideally is parsed and .txt files are produced in a teacher-files folder
    """
    
    def on_script_button_click(self):
        try:
            print(self.filename)
            
            read_data(self.filename,self.script)
            
            messagebox.showinfo("Success", f"Scripts created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    """
    Allows the user to edit the script that is utilized for the script function
    """
    def edit_script_button_click(self):
        try:
            #name = InputPopup(self.root, "", "Enter First and Last Name to be put into default Script")
            #self.name = name.value


            # Create a new top-level window for editing
            self.script_window = tk.Toplevel(self.root)
            self.script_window.title("Edit Script")
            self.script_window.geometry("800x600")
                
            # Create frame to hold text widget and buttons
            editor_frame = tk.Frame(self.script_window)
            editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                
            # Create scrollable text box
            self.script_editor = scrolledtext.ScrolledText(
                editor_frame,
                wrap=tk.WORD,
                font=('Consolas', 11),  # Monospace font for scripts
                undo=True,  # Enable undo/redo
                padx=10,
                pady=10
            )
            self.script_editor.pack(fill=tk.BOTH, expand=True)
                
            # Load existing script content if available
            if hasattr(self, 'script'):
                self.script_editor.insert(tk.END, self.script)
                
            # Add control buttons
            button_frame = tk.Frame(editor_frame)
            button_frame.pack(fill=tk.X, pady=5)
                
            tk.Button(
                button_frame, 
                text="Save",
                command=self.save_script,
                bg="#4CAF50",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)
                
            tk.Button(
                button_frame,
                text="Clear",
                command=lambda: self.script_editor.delete(1.0, tk.END),
                bg="#f44336",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame,
                text="Default",
                command=lambda: self.restore_default_script(),
                bg="Grey",
                fg="white"
            ).pack(side=tk.LEFT, padx=5)
            
            #messagebox.showinfo("Editor Ready", "You can now edit the script.")
            
        except Exception as e:
            messagebox.showerror("Editor Error", f"Failed to open editor:\n{str(e)}")
    
    """
    Saves the script to be used in the script function
    """
    def save_script(self):
        """Saves the content of the script editor"""
        if hasattr(self, 'script_editor'):
            self.script = self.script_editor.get(1.0, tk.END)
            messagebox.showinfo("Saved", "Script content saved successfully!")
        else:
            messagebox.showwarning("No Editor", "No active editor window found")


    def on_create_calendar_click(self):
        try:
            print(self.filename)
            
            #function to create a calendar
            load_csv(self.filename)
            
            messagebox.showinfo("Success", f"Week Schedule created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    """
    Restores the script to the original default script 
    """
    def restore_default_script(self):
        self.script_editor.delete(1.0, tk.END)
        self.script_editor.insert(tk.END, self.default_script)

    
    
    def run(self):
        self.root.mainloop()


    def update_default_script(self,username):
        self.username = username
        self.script = f"Greetings!\n\tI hope the start of the semester has been treating you well. My name is {self.username} and I am the membership officer of the Association of Computer Machinery or ACM. If you haven't heard of ACM before we are a computer science organization that strives to help fellow students learn more about coding and programming through community, workshops, hackathons, and other events. As ACM's Open House approaches, we wanted to see if we could send a representative of ACM to very briefly present what ACM is about and our upcoming events for the semester. If your interested please let us know, and confirm if we have all the correct classes below."

        
    
    """
    an inputPopup object that can be used to create multiple inputPopups if necessary
    """
class InputPopup:
    def __init__(self, parent, title, prompt):
        self.popup = tk.Toplevel(parent)
        self.popup.title(title)
        
        tk.Label(self.popup, text=prompt).pack(pady=10)
        
        self.entry = tk.Entry(self.popup, width=30)
        self.entry.pack(pady=5)
        self.entry.focus_set()
        
        self.value = None
        
        tk.Button(self.popup, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=10)
        tk.Button(self.popup, text="Cancel", command=self.popup.destroy).pack(side=tk.RIGHT, padx=10)
        
        self.popup.transient(parent)  # Set to be on top of parent
        self.popup.grab_set()  # Modal dialog
        parent.wait_window(self.popup)  # Wait for popup to close
    
    def on_ok(self):
        self.value = self.entry.get()
        self.popup.destroy()

    