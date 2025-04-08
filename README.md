# Amalthea Image Tagging Software

![Amalthea Icon](icon.ico)

Amalthea is a user-friendly image tagging software that allows you to effortlessly organize and manage your image collections. With Amalthea, you can load images from a specified directory, view them, and add custom tags to each image. These tags are saved in a separate text file associated with each image, making it easy to search, filter, and retrieve images based on their metadata.

## Features

*   **Image Loading:** Load images from a specified directory. The default directory is the `/images` folder in the project root.
*   **Image Navigation:** Easily navigate between images using the "Previous Image" and "Next Image" buttons.
*   **Tagging:** Add custom tags to each image using a simple text input field. Tags can be comma-separated or space-separated.
*   **Tag Saving:** Save tags to a `.txt` file with the same name as the image file.
*   **Supported Image Formats:** Amalthea supports a wide range of image formats, including PNG, JPG, JPEG, GIF, and BMP.
*   **Automatic Image Directory Creation:** If the `/images` directory does not exist, Amalthea will automatically create it.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    ```
2.  **Navigate to the project directory:**

    ```bash
    cd amalthea
    ```
3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Windows Users

Simply double-click the `run.bat` file to start Amalthea. The batch file will automatically check for and install required dependencies if needed.

### Manual Start

1.  **Place your images in the `/images` folder.** This folder is created automatically on the first run if it doesn't exist.
2.  **Run the application:**

    ```bash
    python src/main.py
    ```
3.  **Use the "Previous Image" and "Next Image" buttons to navigate between images.**
4.  **Enter tags in the text input field (comma or space separated).**
5.  **Click the "Save Tags" button to store the tags.**

## Directory Structure

```
amalthea/
├── .git/                # Git repository
├── images/             # Store your images here
│   └── .gitkeep        # Keeps the images directory in version control
├── src/                # Source code
│   ├── __init__.py     # Initializes the src directory as a Python package
│   ├── image_loader.py # Handles loading images from the directory
│   ├── main.py         # Main application entry point
│   ├── tag_manager.py  # Manages saving and loading tags for images
│   └── ui/             # User interface components
│       ├── __init__.py # Initializes the ui directory as a Python package
│   ├── components.py # Reusable UI components
│       └── main_window.py # Main GUI window setup
├── .gitignore          # Specifies intentionally untracked files that Git should ignore
├── README.md           # Project documentation (this file)
├── requirements.txt    # Lists project dependencies
└── run.bat             # Windows batch file for easy startup
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.