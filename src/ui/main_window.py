import os
import tkinter as tk
from tkinter import Label, StringVar, Frame, messagebox
from PIL import Image, ImageTk

# Change relative imports to absolute imports
from src.image_loader import ImageLoader
from src.tag_manager import TagManager
from src.ui.components import TagInputField, NavigationButton, SaveButton, AutoTagField

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Amalthea - Image Tagging Software")
        self.master.geometry("900x700")  # Increased window size
        self.master.minsize(800, 650)    # Set minimum window size
        
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

        # Auto-tag area - New component
        self.autotag_frame = Frame(self.frame)
        self.autotag_frame.pack(fill=tk.X, pady=5)
        self.autotag_field = AutoTagField(self.autotag_frame, command=self.apply_auto_tag)
        self.autotag_field.pack(fill=tk.X, expand=True)

        # Navigation buttons
        self.button_frame = Frame(self.frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # Use a grid layout for better control
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)

        self.previous_button = NavigationButton(self.button_frame, text="Previous Image", command=self.previous_image)
        self.previous_button.grid(row=0, column=0, padx=5, sticky="w")

        self.save_button = SaveButton(self.button_frame, text="Save Tags", command=self.save_tags)
        self.save_button.grid(row=0, column=1, padx=5, sticky="w")

        self.delete_button = NavigationButton(self.button_frame, text="Delete Tags", 
                                             command=self.delete_tags, bg="#f44336", fg="white")
        self.delete_button.grid(row=0, column=2, padx=5, sticky="w")

        self.next_button = NavigationButton(self.button_frame, text="Next Image", command=self.next_image)
        self.next_button.grid(row=0, column=3, padx=5, sticky="e")

        # Status message
        self.status_var = StringVar()
        self.status_label = Label(self.frame, textvariable=self.status_var, font=("Arial", 9))
        self.status_label.pack(pady=5)

        # Load images and display the first one
        self.load_images()

        # After all UI elements are created, update the window size
        self.master.update_idletasks()  # Force geometry calculation
        
        # Calculate and set a more appropriate window size
        required_height = self.frame.winfo_reqheight() + 40  # Add some extra padding
        required_width = self.frame.winfo_reqwidth() + 40    # Add some extra padding
        self.master.geometry(f"{max(required_width, 800)}x{max(required_height, 650)}")

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
        if not self.images:
            return
        
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.show_image()

    def previous_image(self):
        """Navigate to the previous image."""
        if not self.images:
            return
        
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

    def delete_tags(self):
        """Delete the tags for the current image."""
        if self.images and self.current_image_path:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the tags for this image?"):
                success = self.tag_manager.delete_tags(self.current_image_path)
                if success:
                    self.tag_var.set("")  # Clear the tag input field
                    self.status_var.set(f"Tags deleted for {os.path.basename(self.current_image_path)}")
                else:
                    self.status_var.set("Error deleting tags")
    
    def apply_auto_tag(self, tag):
        """Apply the specified tag to all images."""
        if not self.images or not tag:
            self.status_var.set("No images to tag or no tag specified")
            return False
        
        success_count = 0
        current_image_tags = None  # Store tags for current image to update UI
        
        for image_path in self.images:
            # Get existing tags
            existing_tags = self.tag_manager.load_tags(image_path)
            
            # Add the new tag if it's not already present
            tags_list = [t.strip() for t in existing_tags.split(',') if t.strip()]
            if tag not in tags_list:
                tags_list.append(tag)
                
                # Save the updated tags
                new_tags = ', '.join(tags_list)
                if self.tag_manager.save_tags(image_path, new_tags):
                    success_count += 1
                    
                    # If this is the current image, store its tags
                    if image_path == self.current_image_path:
                        current_image_tags = new_tags
        
        # Update the current image's tags in the UI without disturbing navigation state
        if current_image_tags is not None:
            self.tag_var.set(current_image_tags)
        
        self.status_var.set(f"Tag '{tag}' applied to {success_count} of {len(self.images)} images")
        return success_count > 0