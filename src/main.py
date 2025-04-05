"""
Amalthea - Image Tagging Software
Main application entry point
"""
import tkinter as tk
from src.ui.main_window import MainWindow

def main():
    """Initialize and run the Amalthea application"""
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Set application icon (optional)
    try:
        root.iconbitmap('icon.ico')  # You can add an icon file later
    except:
        pass  # Ignore if icon file is missing
        
    # Initialize the main application window
    app = MainWindow(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()