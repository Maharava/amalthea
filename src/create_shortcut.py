import os
import sys
import subprocess

def create_shortcut():
    """Create a Windows shortcut for Amalthea with the proper icon"""
    try:
        # First, try to import win32com.client
        try:
            import win32com.client
        except ImportError:
            print("Installing required module (pywin32)...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
            import win32com.client
            print("Module installed successfully.")
            
        # Get the path to the project root directory (absolute path)
        # Note: We're now in src/ so we need to go up one level
        root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
        
        # Path to the launcher script (absolute path)
        launcher_py = os.path.abspath(os.path.join(root_dir, "launch_amalthea.py"))
        
        # Check if the launcher script exists, if not create it
        if not os.path.exists(launcher_py):
            print("Creating launcher script...")
            with open(launcher_py, 'w') as f:
                f.write('''import os
import sys
import runpy

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Change to the project root directory
os.chdir(project_root)

# Run the main module
if __name__ == "__main__":
    runpy.run_module("src.main", run_name="__main__")
''')
            print("Launcher script created.")
        
        # Path to the icon (absolute path)
        icon_path = os.path.abspath(os.path.join(root_dir, "resources", "icon.ico"))
        
        # Verify the icon exists
        if not os.path.exists(icon_path):
            print(f"WARNING: Could not find icon at {icon_path}")
            print("Shortcut will use default icon.")
        
        # Path to the pythonw executable (windowless python)
        pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
        if not os.path.exists(pythonw_path):
            print(f"Warning: Could not find pythonw.exe at {pythonw_path}")
            print("Using regular python.exe instead.")
            pythonw_path = sys.executable
        
        # Path for the shortcut
        shortcut_path = os.path.join(root_dir, "Amalthea.lnk")
        
        print("Creating shortcut with following properties:")
        print(f"Target: {pythonw_path}")
        print(f"Arguments: \"{launcher_py}\"")
        print(f"Working Directory: {root_dir}")
        print(f"Icon: {icon_path}")
        print(f"Shortcut Location: {shortcut_path}")
        
        # Create the shortcut
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = pythonw_path
        shortcut.Arguments = f'"{launcher_py}"'
        shortcut.WorkingDirectory = root_dir
        shortcut.IconLocation = icon_path
        shortcut.save()
        
        print("\nShortcut created successfully!")
        print(f"You can find it at: {shortcut_path}")
        print("You can now move this shortcut anywhere you want (desktop, Start menu, etc.)")
        
    except Exception as e:
        print(f"Error creating shortcut: {str(e)}")

if __name__ == "__main__":
    create_shortcut()
    input("\nPress Enter to exit...")