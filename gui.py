import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import Tk, Label
from data import clean_data
from data import read_data

from PIL import Image, ImageTk

class ACMEmailGenerator:
    def __init__(self):
        self.filename = ""
        self.root = tk.Tk()
        self.root.geometry("400x300")
        self.root.title("ACM Email Generator")
        self.image_url ="ACM.png"
        self.tk_image = ""
        
        
        self.setup_ui()
        
    def setup_ui(self):
        # resizing the image
        image = Image.open(self.image_url)
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
        
        # Status label
        self.status_label = tk.Label(self.root, text="No file selected")
        self.status_label.pack(pady=10)
    
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
        if file_path:
            self.filename = file_path
            self.status_label.config(text=f"Selected: {file_path}")
            self.clean_button.config(state=tk.NORMAL)
            self.script_button.config(state=tk.NORMAL)
    
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
    
    def on_script_button_click(self):
        try:
            print(self.filename)
            popup = InputPopup(self.root, "", "Enter First and Last Name to be put into default Script")
            read_data(self.filename,popup.value)
            
            messagebox.showinfo("Success", f"Scripts created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def run(self):
        self.root.mainloop()
    
    
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

    