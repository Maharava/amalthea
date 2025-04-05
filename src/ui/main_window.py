import os
import tkinter as tk
from tkinter import Label, StringVar, Frame
from PIL import Image, ImageTk

# Change relative imports to absolute imports
from src.image_loader import ImageLoader
from src.tag_manager import TagManager
from src.ui.components import TagInputField, NavigationButton, SaveButton

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Amalthea - Image Tagging Software")
        self.master.geometry("800x600")
        
        # Main frame
        self.frame = Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Initialize image loader and tag manager
        self.image_loader = ImageLoader()
        self.tag_manager = TagManager()

        # Image tracking variables
        self.current_image_index = 0
        self.images = []
        self.current_image_path = None
        self.photo = None

        # Image display area
        self.image_frame = Frame(self.frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.image_label = Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # File name display
        self.filename_var = StringVar()
        self.filename_label = Label(self.frame, textvariable=self.filename_var, font=("Arial", 10))
        self.filename_label.pack(pady=5)

        # Tag input area - Using our custom TagInputField component
        self.tag_var = StringVar()
        self.tag_input = TagInputField(self.frame, textvariable=self.tag_var, width=50)
        self.tag_input.pack(fill=tk.X, pady=5)

        # Navigation buttons
        self.button_frame = Frame(self.frame)
        self.button_frame.pack(fill=tk.X, pady=10)
        
        self.previous_button = NavigationButton(self.button_frame, text="Previous Image", command=self.previous_image)
        self.previous_button.pack(side=tk.LEFT, padx=5)
        
        self.save_button = SaveButton(self.button_frame, text="Save Tags", command=self.save_tags)
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.next_button = NavigationButton(self.button_frame, text="Next Image", command=self.next_image)
        self.next_button.pack(side=tk.RIGHT, padx=5)  # Changed to RIGHT for better layout

        # Status message
        self.status_var = StringVar()
        self.status_label = Label(self.frame, textvariable=self.status_var, font=("Arial", 9))
        self.status_label.pack(pady=5)

        # Load images and display the first one
        self.load_images()

    def load_images(self):
        """Load all images from the images directory."""
        self.images = self.image_loader.load_images()
        if self.images:
            self.show_image()
        else:
            self.status_var.set("No images found in the images directory")

    def show_image(self):
        """Display the current image and its tags."""
        if not self.images:
            return
            
        self.current_image_path = self.images[self.current_image_index]
        
        # Update filename display
        self.filename_var.set(os.path.basename(self.current_image_path))
        
        try:
            # Load and resize image to fit display
            pil_image = Image.open(self.current_image_path)
            # Calculate resize dimensions to fit in display area (max 700x400)
            width, height = pil_image.size
            max_width, max_height = 700, 400
            
            if width > max_width or height > max_height:
                ratio = min(max_width/width, max_height/height)
                width = int(width * ratio)
                height = int(height * ratio)
                pil_image = pil_image.resize((width, height), Image.LANCZOS)
                
            # Convert PIL image to Tkinter PhotoImage
            self.photo = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.photo)
            
            # Load existing tags for this image
            existing_tags = self.tag_manager.load_tags(self.current_image_path)
            self.tag_var.set(existing_tags)
            
            self.status_var.set(f"Image {self.current_image_index + 1} of {len(self.images)}")
            
        except Exception as e:
            self.status_var.set(f"Error loading image: {str(e)}")
            self.image_label.config(image=None, text="Cannot display image")

    def next_image(self):
        """Navigate to the next image."""
        if self.images:
            self.current_image_index = (self.current_image_index + 1) % len(self.images)
            self.show_image()

    def previous_image(self):
        """Navigate to the previous image."""
        if self.images:
            self.current_image_index = (self.current_image_index - 1) % len(self.images)
            self.show_image()

    def save_tags(self):
        """Save the current tags for the displayed image."""
        if self.images and self.current_image_path:
            # Use get_tags to handle placeholder text properly
            tags = self.tag_input.get_tags()
            success = self.tag_manager.save_tags(self.current_image_path, tags)
            if success:
                self.status_var.set(f"Tags saved for {os.path.basename(self.current_image_path)}")
            else:
                self.status_var.set("Error saving tags")