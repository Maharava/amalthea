# Amalthea Image Tagging Software

Amalthea is an image tagging software that allows users to load images from a specified directory, view them, and tag them with custom labels. The tags are saved in a text file corresponding to each image, making it easy to manage and retrieve image metadata.

## Features

- Load and display images from the `/images` folder
- Navigate between images using intuitive Previous/Next buttons
- Enter and save tags for each image with a user-friendly interface
- Tags are stored in a `.txt` file with the same name as the image
- Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP)
- Automatic image resizing to fit the display area
- Visual indicators showing current image position in the collection

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd amalthea
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Windows Users
Simply double-click the `run.bat` file to start Amalthea. The batch file will automatically check for and install required dependencies if needed.

### Manual Start
1. Place your images in the `/images` folder (created automatically on first run if it doesn't exist)
2. Run the application:
   ```
   python src/main.py
   ```
3. Use the "Previous Image" and "Next Image" buttons to navigate between images
4. Enter tags in the text input field (comma or space separated)
5. Click the "Save Tags" button to store the tags

## Directory Structure

```
amalthea
├── src
│   ├── main.py           # Entry point of the application
│   ├── image_loader.py   # Handles loading images
│   ├── tag_manager.py    # Manages saving and loading tags
│   └── ui
│       ├── __init__.py   # Initializes the UI package
│       ├── main_window.py # Main GUI window setup
│       └── components.py  # Reusable UI components
├── images                # Store your images here
│   └── .gitkeep          # Keeps the images directory in version control
├── run.bat               # Windows batch file for easy startup
├── requirements.txt      # Lists project dependencies
├── README.md             # Project documentation
└── .gitignore            # Specifies files to ignore in version control
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.