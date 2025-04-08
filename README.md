==================================================
AMALTHEA IMAGE TAGGING SOFTWARE - USER GUIDE
==================================================

Welcome to Amalthea, a powerful yet simple image tagging tool for organizing 
and cataloging your image collections.

--------------------------------------------------
INSTALLATION
--------------------------------------------------

1. REQUIREMENTS:
   - Python 3.6 or higher with tkinter (usually included in standard installation)
   - PIL/Pillow package for image processing

2. INSTALLATION STEPS:
   a) Download or clone the Amalthea repository
   b) Make sure Python is installed and in your system PATH
   c) Run the setup.bat file to install required dependencies
      OR use pip manually: pip install -r requirements.txt

3. FIRST-TIME SETUP:
   a) Run create_shortcut.bat to create a desktop shortcut
      - This will create "Amalthea.lnk" in the root directory
      - You can move this shortcut anywhere on your system
   b) The shortcut uses the app icon and launches without showing command windows
   c) The "images" folder will be created automatically when needed

--------------------------------------------------
LAUNCHING AMALTHEA
--------------------------------------------------

There are three ways to start Amalthea:

1. RECOMMENDED: Use the shortcut created by running create_shortcut.bat
   - This gives the cleanest experience with proper icon in taskbar
   - No command windows will appear in the background

2. Run the run.bat file directly
   - This shows a command window while running
   - Automatically checks and installs dependencies if needed
   - Creates the images folder if it doesn't exist

3. Advanced/manual startup: 
   - Navigate to the amalthea directory in a command prompt
   - Run: python src/main.py

--------------------------------------------------
USING AMALTHEA
--------------------------------------------------

MAIN INTERFACE:

* IMAGE DISPLAY: Shows the current image in your collection
  - When no images are loaded, shows the Amalthea icon

* FILENAME: Displays the name of the current image file

* PNG METADATA: Shows any embedded metadata in PNG files
  - Particularly useful for AI-generated images with embedded prompts

* AUTO-TAG FIELD: Apply the same tag to multiple images
  - Enter a tag and click "Apply to All" to add it to all images in workspace
  - Used with "Tag Folder" to tag external image collections

* TAGS INPUT: Add or edit tags for the current image
  - Enter tags separated by commas
  - Example: landscape, mountains, sunny

BUTTONS:

* NAVIGATION BUTTONS:
  - Previous Image: Move to the previous image in the collection
  - Next Image: Move to the next image in the collection

* TAG MANAGEMENT:
  - Save Tags: Save the current tags to a text file with the same name as the image
  - Delete Tags: Remove all tags from the current image

* FOLDER MANAGEMENT:
  - Add Folder: Import images from an external folder to the workspace
    * Copies images into your workspace
    * Also imports any matching text files with the same filename
  
  - Export Dataset: Export all images and their tags to a new location
    * Creates a "dataset" folder at the selected location
    * Copies all images and tag files
    * Optionally clears the workspace after export
  
  - Tag Folder: Apply tags to images in an external folder
    * Does NOT import the images
    * Creates/updates .txt files in that location
    * Uses the tag entered in the Auto-Tag field
  
  - Clear Folder: Delete all images and tags from the workspace
    * WARNING: This permanently deletes files
    * Export your dataset first if you want to keep the data

--------------------------------------------------
WORKFLOW EXAMPLES
--------------------------------------------------

BASIC IMAGE TAGGING:
1. Add images to the "images" folder or use Add Folder to import them
2. Navigate through images with Previous/Next buttons
3. Enter tags for each image in the Tags field
4. Click Save Tags for each image

BATCH TAGGING:
1. Add images to workspace
2. Enter a common tag in the Auto-Tag field (e.g., "landscape")
3. Click "Apply to All" to add this tag to all images
4. Navigate through images to add individual tags as needed

CREATING A DATASET:
1. Tag all your images
2. Click Export Dataset
3. Choose a destination folder
4. All images and tags will be copied to a new "dataset" folder
5. Optionally clear your workspace to start fresh

TAGGING EXTERNAL COLLECTIONS:
1. Enter a tag in the Auto-Tag field
2. Click "Tag Folder"
3. Select a folder containing images
4. This creates .txt files with tags for each image, without moving them

--------------------------------------------------
TROUBLESHOOTING
--------------------------------------------------

ISSUE: Application won't start
SOLUTION: Make sure Python 3.6+ is installed and in your PATH
          Run: pip install -r requirements.txt

ISSUE: Images don't load
SOLUTION: Check if the images folder exists and contains image files
          Supported formats: PNG, JPG, JPEG, GIF, BMP

ISSUE: Shortcut doesn't work
SOLUTION: Run create_shortcut.bat again to recreate it
          Make sure the pythonw.exe path in the shortcut is correct

--------------------------------------------------
CONTACT & SUPPORT
--------------------------------------------------

If you encounter issues or have suggestions for improvements,
please open an issue on the GitHub repository.

Thank you for using Amalthea!