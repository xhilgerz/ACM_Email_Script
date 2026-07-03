import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from Backend.data import create_sign_up,create_email_scripts
from Backend.data import read_data

import sys
import os
from Backend.heat_calendar import load_csv

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
        self.dark_mode = tk.BooleanVar(value=False)
        self.style = ttk.Style(self.root)
        
        self.setup_ui()
        self.apply_theme()
        
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

        self.main_frame = ttk.Frame(self.root, style="App.TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Presenting the image
        self.logo = ttk.Label(self.main_frame, image=self.tk_image, style="App.TLabel")
        self.logo.pack()

        # Add a label
        self.label = ttk.Label(self.main_frame, text="Welcome to ACM Email Generator", style="App.TLabel")
        self.label.pack(pady=10)

        


        
        # File selection button
        self.choose_file = ttk.Button(self.main_frame, text="Open File", command=self.open_file, style="App.TButton")
        self.choose_file.pack(pady=10)

        # Entry box 
        self.prefix_entry = ttk.Entry(self.main_frame, width=30)
        
        # Action buttons (initially disabled)
        self.clean_button = ttk.Button(self.main_frame, text="Create Sign Up Form", 
                                    command=self.on_clean_button_click,
                                    state=tk.DISABLED,
                                    style="App.TButton")
        self.clean_button.pack(pady=10)
        
        self.script_button = ttk.Button(self.main_frame, text="Write teacher scripts", 
                                     command=self.on_script_button_click,
                                     state=tk.DISABLED,
                                     style="App.TButton")
        self.script_button.pack(pady=10)

        self.edit_script_button = ttk.Button(self.main_frame, text="Edit Script", 
                                     command=self.edit_script_button_click,
                                     style="App.TButton")
        self.edit_script_button.pack(pady=10)

        self.create_calendar = ttk.Button(self.main_frame, text="Create Week Calendar", 
                                    command=self.on_create_calendar_click,
                                    state=tk.DISABLED,
                                    style="App.TButton")
        self.create_calendar.pack(pady=10)

        # Status label
        self.status_label = ttk.Label(self.main_frame, text="No file selected", style="App.TLabel")
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
            create_sign_up(self.filename)
        
        except Exception as e:
            messagebox.showerror("Error", str(e))


        # try:
        #     filename = clean_data(self.filename)
        #     print(filename)
        #     end_name= filename.split('/')
            
        #     end_name = end_name[-1]
        #     print(end_name)
        #     messagebox.showinfo("Success", f"Copy created successfully: {end_name}")
        # except Exception as e:
        #     messagebox.showerror("Error", str(e))
        
    """
    The cleaned csv ideally is parsed and .txt files are produced in a teacher-files folder
    """
    
    def on_script_button_click(self):
        try:
            print(self.filename)
            
            #read_data(self.filename,self.script)

            create_email_scripts(self.filename,self.script)
            
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
            editor_frame = ttk.Frame(self.script_window, style="App.TFrame")
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
            button_frame = ttk.Frame(editor_frame, style="App.TFrame")
            button_frame.pack(fill=tk.X, pady=5)
                
            ttk.Button(
                button_frame, 
                text="Save",
                command=self.save_script,
                style="Success.TButton"
            ).pack(side=tk.LEFT, padx=5)
                
            ttk.Button(
                button_frame,
                text="Clear",
                command=lambda: self.script_editor.delete(1.0, tk.END),
                style="Danger.TButton"
            ).pack(side=tk.LEFT, padx=5)

            ttk.Button(
                button_frame,
                text="Default",
                command=lambda: self.restore_default_script(),
                style="Neutral.TButton"
            ).pack(side=tk.LEFT, padx=5)

            self.apply_theme()
            
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

    def toggle_theme(self):
        self.apply_theme()

    def apply_theme(self):
        colors = {
            "bg": "#1E1E1E",
            "fg": "#F5F5F5",
            "entry_bg": "#2C2C2C",
            "entry_fg": "#F5F5F5",
            "button_bg": "#3A3A3A",
            "button_fg": "#F5F5F5",
            "button_active": "#525252",
            "success_bg": "#2E7D32",
            "danger_bg": "#B71C1C",
            "neutral_bg": "#616161"
        } if self.dark_mode.get() else {
            "bg": "#F0F0F0",
            "fg": "#111111",
            "entry_bg": "#FFFFFF",
            "entry_fg": "#111111",
            "button_bg": "#E6E6E6",
            "button_fg": "#111111",
            "button_active": "#DADADA",
            "success_bg": "#4CAF50",
            "danger_bg": "#f44336",
            "neutral_bg": "#757575"
        }

        self.style.theme_use("clam")
        self.root.configure(bg=colors["bg"])
        self.style.configure("App.TFrame", background=colors["bg"])
        self.style.configure("App.TLabel", background=colors["bg"], foreground=colors["fg"])
        self.style.configure(
            "App.TButton",
            background=colors["button_bg"],
            foreground=colors["button_fg"],
            borderwidth=0,
            padding=6
        )
        self.style.map(
            "App.TButton",
            background=[("active", colors["button_active"]), ("pressed", colors["button_bg"])],
            foreground=[("disabled", "#8A8A8A"), ("active", colors["button_fg"])]
        )
        self.style.configure(
            "App.TCheckbutton",
            background=colors["bg"],
            foreground=colors["fg"]
        )
        self.style.map(
            "App.TCheckbutton",
            background=[("active", colors["bg"])],
            foreground=[("active", colors["fg"])]
        )
        self.style.configure(
            "TEntry",
            fieldbackground=colors["entry_bg"],
            foreground=colors["entry_fg"]
        )
        self.style.configure(
            "Success.TButton",
            background=colors["success_bg"],
            foreground="#FFFFFF",
            borderwidth=0
        )
        self.style.map("Success.TButton", background=[("active", colors["success_bg"])])
        self.style.configure(
            "Danger.TButton",
            background=colors["danger_bg"],
            foreground="#FFFFFF",
            borderwidth=0
        )
        self.style.map("Danger.TButton", background=[("active", colors["danger_bg"])])
        self.style.configure(
            "Neutral.TButton",
            background=colors["neutral_bg"],
            foreground="#FFFFFF",
            borderwidth=0
        )
        self.style.map("Neutral.TButton", background=[("active", colors["neutral_bg"])])

        if hasattr(self, "script_window") and self.script_window.winfo_exists():
            self.script_window.configure(bg=colors["bg"])
        if hasattr(self, "script_editor") and self.script_editor.winfo_exists():
            self._safe_config(
                self.script_editor,
                bg=colors["entry_bg"],
                fg=colors["entry_fg"],
                insertbackground=colors["entry_fg"],
                selectbackground=colors["button_bg"],
                relief=tk.FLAT,
                borderwidth=0,
                highlightthickness=0
            )

    def _safe_config(self, widget, **kwargs):
        for key, value in kwargs.items():
            try:
                widget.configure(**{key: value})
            except tk.TclError:
                continue

    
    
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
        
        ttk.Label(self.popup, text=prompt).pack(pady=10)
        
        self.entry = ttk.Entry(self.popup, width=30)
        self.entry.pack(pady=5)
        self.entry.focus_set()
        
        self.value = None
        
        ttk.Button(self.popup, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=10)
        ttk.Button(self.popup, text="Cancel", command=self.popup.destroy).pack(side=tk.RIGHT, padx=10)
        
        self.popup.transient(parent)  # Set to be on top of parent
        self.popup.grab_set()  # Modal dialog
        parent.wait_window(self.popup)  # Wait for popup to close
    
    def on_ok(self):
        self.value = self.entry.get()
        self.popup.destroy()

    
