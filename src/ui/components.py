import tkinter as tk
from tkinter import Button, Entry, Frame, Label

class TagInputField(Frame):
    """Enhanced tag input field with better styling and functionality"""
    
    def __init__(self, master=None, textvariable=None, width=50, **kwargs):
        super().__init__(master, **kwargs)
        
        # Container for the entry and label
        self.inner_frame = Frame(self)
        self.inner_frame.pack(fill=tk.X, expand=True)
        
        # Label
        self.label = Label(self.inner_frame, text="Tags:", padx=5)
        self.label.pack(side=tk.LEFT)
        
        # Entry field
        self.tag_var = textvariable if textvariable else tk.StringVar()
        self.entry = Entry(self.inner_frame, textvariable=self.tag_var, 
                          width=width, font=("Arial", 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Add placeholder text and bindings for better UX
        self.placeholder = "Enter tags separated by commas or spaces"
        if not self.tag_var.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="gray")
        
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        
        # Button frame for potential additional controls
        self.button_frame = Frame(self)
        self.button_frame.pack(fill=tk.X, expand=True, pady=2)
        
        # Help text
        self.help_label = Label(self.button_frame, 
                              text="Example: landscape, nature, mountains", 
                              font=("Arial", 8), fg="gray")
        self.help_label.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        self.clear_button = Button(self.button_frame, text="Clear", 
                                 command=self.clear_tags,
                                 font=("Arial", 8), padx=5)
        self.clear_button.pack(side=tk.RIGHT, padx=5)

    def _on_focus_in(self, event):
        """Handle focus in event to remove placeholder text"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(fg="black")

    def _on_focus_out(self, event):
        """Handle focus out event to add placeholder text if empty"""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(fg="gray")

    def get_tags(self):
        """Get the current tags, handling the placeholder text case"""
        current_text = self.tag_var.get()
        return "" if current_text == self.placeholder else current_text
    
    def clear_tags(self):
        """Clear all tags"""
        self.tag_var.set("")
        self.entry.focus_set()  # Set focus to trigger the focus_in event
        self.entry.delete(0, tk.END)  # Clear any placeholder text
        self.entry.insert(0, self.placeholder)
        self.entry.config(fg="gray")


class NavigationButton(Button):
    """Enhanced navigation button with styling"""
    
    def __init__(self, master=None, text="", command=None, **kwargs):
        # Default styling
        self.button_style = {
            "font": ("Arial", 10, "bold"),
            "borderwidth": 2,
            "relief": tk.RAISED,
            "padx": 10,
            "pady": 5,
            "bg": "#e1e1e1",
            "activebackground": "#d1d1d1"
        }
        # Update with any user-provided styling
        self.button_style.update(kwargs)
        
        super().__init__(master, text=text, command=command, **self.button_style)
        
        # Add hover effect
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Mouse enter effect"""
        self.config(bg="#d1d1d1")
    
    def _on_leave(self, event):
        """Mouse leave effect"""
        self.config(bg="#e1e1e1")


class SaveButton(Button):
    """Enhanced save button with styling"""
    
    def __init__(self, master=None, text="Save Tags", command=None, **kwargs):
        # Default styling for save button - make it stand out
        self.button_style = {
            "font": ("Arial", 10, "bold"),
            "borderwidth": 2,
            "relief": tk.RAISED,
            "padx": 15,
            "pady": 5,
            "bg": "#4CAF50",  # Green color
            "fg": "white",
            "activebackground": "#45a049",
            "activeforeground": "white"
        }
        # Update with any user-provided styling
        self.button_style.update(kwargs)
        
        super().__init__(master, text=text, command=command, **self.button_style)
        
        # Add hover effect
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_enter(self, event):
        """Mouse enter effect"""
        self.config(bg="#45a049")
    
    def _on_leave(self, event):
        """Mouse leave effect"""
        self.config(bg="#4CAF50")