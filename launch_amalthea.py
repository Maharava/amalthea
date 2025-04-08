import os
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