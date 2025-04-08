"""
Amalthea - Image Tagging Software
Main application entry point
"""
import os
import tkinter as tk
import sys
import ctypes
from src.ui.main_window import MainWindow

def main():
    """Initialize and run the Amalthea application"""
    # Create the main Tkinter window
    root = tk.Tk()
    
    # Set application icon properly
    try:
        # Use the same path resolution approach as in MainWindow
        icon_path = os.path.join(os.path.dirname(os.path.dirname(
                    os.path.abspath(__file__))), "resources", "icon.ico")
        
        # Set the window icon
        root.iconbitmap(icon_path)
        
        # Set the taskbar icon (Windows-specific)
        if sys.platform == 'win32':
            # Get the application ID
            app_id = 'amalthea.imagetagger.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            
            # Force the taskbar icon to be the same as the window icon
            root.after(10, lambda: root.iconbitmap(icon_path))
    except Exception as e:
        print(f"Error setting application icon: {str(e)}")
        
    # Initialize the main application window
    app = MainWindow(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()