import os
import tkinter as tk
from tkinter import Label, StringVar, Frame, messagebox, filedialog, Toplevel, Text, Scrollbar
from PIL import Image, ImageTk, PngImagePlugin
import shutil

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
        
        # Set window icon from resources folder
        try:
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.abspath(__file__)))), "resources", "icon.ico")
            self.master.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error setting window icon: {str(e)}")
        
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
        self.app_icon_photo = None  # Store app icon photo
        
        # Load the application icon for display when no images are loaded
        self.load_app_icon()

        # Image display area
        self.image_frame = Frame(self.frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.image_label = Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # File name display
        self.filename_var = StringVar()
        self.filename_label = Label(self.frame, textvariable=self.filename_var, font=("Arial", 10))
        self.filename_label.pack(pady=5)

        # Auto-tag area - Now with more subtle styling
        self.autotag_frame = Frame(self.frame)
        self.autotag_frame.pack(fill=tk.X, pady=5)
        self.autotag_field = AutoTagField(self.autotag_frame, command=self.apply_auto_tag, 
                                         bg="#f0f0f0")  # Now more subtle gray
        self.autotag_field.pack(fill=tk.X, expand=True)
        
        # Tag input area - Now with more eye-catching styling
        self.tag_var = StringVar()
        self.tag_input = TagInputField(self.frame, textvariable=self.tag_var, width=50,
                                      bg="#e8f0ff", bd=2)  # Now more eye-catching blue
        self.tag_input.pack(fill=tk.X, pady=10)  # Increased padding

        # Navigation buttons
        self.button_frame = Frame(self.frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        # Use a grid layout for better control - modified to have 6 columns
        self.button_frame.columnconfigure(0, weight=1)
        self.button_frame.columnconfigure(1, weight=1)
        self.button_frame.columnconfigure(2, weight=1)
        self.button_frame.columnconfigure(3, weight=1)
        self.button_frame.columnconfigure(4, weight=1)
        self.button_frame.columnconfigure(5, weight=1)

        # First row of buttons
        self.previous_button = NavigationButton(self.button_frame, text="Previous Image", command=self.previous_image)
        self.previous_button.grid(row=0, column=0, padx=5, sticky="w")

        self.save_button = SaveButton(self.button_frame, text="Save Tags", command=self.save_tags)
        self.save_button.grid(row=0, column=1, padx=5, sticky="w")

        self.delete_button = NavigationButton(self.button_frame, text="Delete Tags", 
                                             command=self.delete_tags, bg="#f44336", fg="white")
        self.delete_button.grid(row=0, column=2, padx=5, sticky="w")
        
        self.add_folder_button = NavigationButton(self.button_frame, text="Add Folder", 
                                                 command=self.add_folder, bg="#4285F4", fg="white")
        self.add_folder_button.grid(row=0, column=3, padx=5, sticky="w")
        
        self.export_button = NavigationButton(self.button_frame, text="Export Dataset", 
                                             command=self.export_dataset, bg="#0F9D58", fg="white")
        self.export_button.grid(row=0, column=4, padx=5, sticky="w")

        self.next_button = NavigationButton(self.button_frame, text="Next Image", command=self.next_image)
        self.next_button.grid(row=0, column=5, padx=5, sticky="e")
        
        # Add a second row for the Tag Folder button
        self.tag_folder_button = NavigationButton(self.button_frame, text="Tag Folder", 
                                                command=self.tag_folder, bg="#FF9800", fg="white")
        self.tag_folder_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        # Add Clear Folder button - new
        self.clear_folder_button = NavigationButton(self.button_frame, text="Clear Folder", 
                                                  command=self.clear_folder, bg="#C62828", fg="white")
        self.clear_folder_button.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # PNG Info area - new
        self.png_info_frame = Frame(self.frame, bd=1, relief=tk.GROOVE)
        self.png_info_frame.pack(fill=tk.X, pady=5)
        
        # PNG Info header
        self.png_info_label = Label(self.png_info_frame, text="PNG Metadata", 
                                  font=("Arial", 10, "bold"), fg="#333333")
        self.png_info_label.pack(anchor=tk.W, padx=5, pady=3)
        
        # PNG Info content area with scrollbar
        self.info_container = Frame(self.png_info_frame)
        self.info_container.pack(fill=tk.X, expand=True, padx=5, pady=2)
        
        self.png_info_text = Text(self.info_container, height=3, width=50, 
                                font=("Consolas", 9), wrap=tk.WORD, bd=1, relief=tk.SUNKEN)
        self.png_info_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.png_info_scrollbar = Scrollbar(self.info_container, command=self.png_info_text.yview)
        self.png_info_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.png_info_text.config(yscrollcommand=self.png_info_scrollbar.set)
        
        # Make the info text read-only
        self.png_info_text.config(state=tk.DISABLED)

        # Status message
        self.status_var = StringVar()
        self.status_label = Label(self.frame, textvariable=self.status_var, font=("Arial", 9))
        self.status_label.pack(pady=5)

        # Load images and display the first one (or app icon if none)
        self.load_images()

        # After all UI elements are created, update the window size
        self.master.update_idletasks()  # Force geometry calculation
        
        # Calculate and set a more appropriate window size
        required_height = self.frame.winfo_reqheight() + 40  # Add some extra padding
        required_width = self.frame.winfo_reqwidth() + 40    # Add some extra padding
        self.master.geometry(f"{max(required_width, 800)}x{max(required_height, 650)}")

    def load_app_icon(self):
        """Load the application icon for display when no images are present."""
        try:
            # Path to the application icon - adjust as needed for your project structure
            icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                        os.path.abspath(__file__)))), "resources", "icon.png")
            
            # Fallback path if not found in resources folder
            if not os.path.exists(icon_path):
                icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                            os.path.abspath(__file__)))), "icon.png")
            
            # If icon still not found, use a placeholder
            if not os.path.exists(icon_path):
                # Create a placeholder image with proper dimensions
                img = Image.new('RGB', (512, 512), color=(240, 240, 245))
                self.app_icon_photo = ImageTk.PhotoImage(img)
                return
                
            # Load the icon
            icon_img = Image.open(icon_path)
            
            # Calculate dimensions while preserving aspect ratio
            # Target size is 512x512, but maintain aspect ratio
            max_size = 512
            original_width, original_height = icon_img.size
            
            # Calculate new dimensions preserving aspect ratio
            if original_width >= original_height:
                new_width = max_size
                new_height = int(original_height * (max_size / original_width))
            else:
                new_height = max_size
                new_width = int(original_width * (max_size / original_height))
            
            # Resize with proper aspect ratio
            icon_img = icon_img.resize((new_width, new_height), Image.LANCZOS)
            
            # If needed, create a square backdrop for the icon
            if new_width != new_height:
                # Create a square backdrop
                backdrop = Image.new('RGBA', (max_size, max_size), (240, 240, 245, 0))
                # Calculate position to center the icon
                paste_x = (max_size - new_width) // 2
                paste_y = (max_size - new_height) // 2
                # Paste the icon centered on the backdrop
                backdrop.paste(icon_img, (paste_x, paste_y), icon_img if icon_img.mode == 'RGBA' else None)
                icon_img = backdrop
            
            self.app_icon_photo = ImageTk.PhotoImage(icon_img)
            
        except Exception as e:
            print(f"Error loading application icon: {str(e)}")
            # Create a fallback image with proper dimensions
            img = Image.new('RGB', (512, 512), color=(240, 240, 245))
            self.app_icon_photo = ImageTk.PhotoImage(img)

    def load_images(self):
        """Load all images from the images directory."""
        # Store current window size before loading images
        current_width = self.master.winfo_width()
        current_height = self.master.winfo_height()
        
        self.images = self.image_loader.load_images()
        if self.images:
            self.show_image()
        else:
            self.status_var.set("No images found in the images directory")
            self.show_app_icon()  # Show app icon when no images are available
            
            # Clear PNG info area
            self.png_info_text.config(state=tk.NORMAL)
            self.png_info_text.delete(1.0, tk.END)
            self.png_info_text.insert(tk.END, "No image loaded - PNG metadata will appear here")
            self.png_info_text.config(state=tk.DISABLED)
            
        # Ensure window size doesn't change when reloading images
        if current_width > 100 and current_height > 100:  # Only if window was already sized
            self.master.geometry(f"{current_width}x{current_height}")

    def show_app_icon(self):
        """Display the application icon when no images are loaded."""
        if self.app_icon_photo:
            self.image_label.config(image=self.app_icon_photo)
            self.filename_var.set("No images loaded")
        else:
            self.image_label.config(image=None, text="Amalthea Image Tagger")

    def show_image(self):
        """Display the current image and its tags."""
        if not self.images:
            self.show_app_icon()  # Show app icon if no images available
            
            # Clear PNG info area
            self.png_info_text.config(state=tk.NORMAL)
            self.png_info_text.delete(1.0, tk.END)
            self.png_info_text.insert(tk.END, "No image loaded - PNG metadata will appear here")
            self.png_info_text.config(state=tk.DISABLED)
            return
            
        self.current_image_path = self.images[self.current_image_index]
        
        # Update filename display
        self.filename_var.set(os.path.basename(self.current_image_path))
        
        try:
            # Load and resize image to fit display
            pil_image = Image.open(self.current_image_path)
            
            # Extract PNG metadata if it's a PNG file
            self.png_info_text.config(state=tk.NORMAL)
            self.png_info_text.delete(1.0, tk.END)
            
            if self.current_image_path.lower().endswith('.png'):
                # Get PNG metadata
                try:
                    png_info = ""
                    if hasattr(pil_image, 'info') and pil_image.info:
                        for key, value in pil_image.info.items():
                            if key != 'text' and isinstance(value, (str, int, float)):
                                png_info += f"{key}: {value}\n"
                    
                    # Check for text chunks (commonly used for metadata)
                    if 'text' in pil_image.info:
                        png_info += "\nText Chunks:\n"
                        for key, value in pil_image.info['text'].items():
                            png_info += f"{key}: {value}\n"
                            
                    if not png_info:
                        png_info = "No PNG metadata found."
                        
                    self.png_info_text.insert(tk.END, png_info)
                except Exception as e:
                    self.png_info_text.insert(tk.END, f"Error reading PNG metadata: {str(e)}")
            else:
                self.png_info_text.insert(tk.END, "Not a PNG file or no metadata available.")
                
            self.png_info_text.config(state=tk.DISABLED)
            
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
            
            # Clear PNG info on error
            self.png_info_text.config(state=tk.NORMAL)
            self.png_info_text.delete(1.0, tk.END)
            self.png_info_text.insert(tk.END, "Error loading image metadata.")
            self.png_info_text.config(state=tk.DISABLED)

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

    def add_folder(self):
        """Add images from a selected folder to the current workspace."""
        # Ask user to select a folder
        source_folder = filedialog.askdirectory(title="Select Folder with Images")
        
        if not source_folder:
            return  # User cancelled
            
        # Count imported files for status update
        imported_images = 0
        imported_tags = 0
        
        # Get list of valid image extensions
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        
        # Get the destination images folder
        dest_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
                      os.path.abspath(__file__)))), "images")
        
        # Ensure the destination folder exists
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
        
        # Process all files in the source folder
        for filename in os.listdir(source_folder):
            source_path = os.path.join(source_folder, filename)
            
            # Skip directories
            if os.path.isdir(source_path):
                continue
                
            # Get file name and extension
            file_name, file_ext = os.path.splitext(filename)
            file_ext = file_ext.lower()
            
            # Process image files
            if file_ext in valid_extensions:
                dest_path = os.path.join(dest_folder, filename)
                
                # Skip if file already exists in destination
                if os.path.exists(dest_path):
                    continue
                    
                try:
                    # Copy the image file
                    shutil.copy2(source_path, dest_path)
                    imported_images += 1
                    
                    # Look for corresponding tag file
                    tag_file = os.path.join(source_folder, f"{file_name}.txt")
                    if os.path.exists(tag_file):
                        # Copy the tag file
                        shutil.copy2(tag_file, os.path.join(dest_folder, f"{file_name}.txt"))
                        imported_tags += 1
                except Exception as e:
                    messagebox.showerror("Import Error", f"Error importing {filename}: {str(e)}")
        
        # Reload images after import
        self.load_images()
        
        # Show status message
        self.status_var.set(f"Imported {imported_images} images and {imported_tags} tag files")
        
    def export_dataset(self):
        """Export all images and tag files to a dataset folder."""
        # Store current window dimensions
        current_width = self.master.winfo_width()
        current_height = self.master.winfo_height()
        
        if not self.images:
            messagebox.showinfo("Export", "No images to export.")
            return
            
        # Ask for confirmation
        if not messagebox.askyesno("Confirm Export", 
                                 "This will export all images and tags to a new location and clear the current workspace.\n\nContinue?"):
            return
            
        # Ask user to select destination directory
        dest_dir = filedialog.askdirectory(title="Select Export Location")
        
        if not dest_dir:
            return  # User cancelled
            
        # Create dataset directory
        dataset_dir = os.path.join(dest_dir, "dataset")
        try:
            if not os.path.exists(dataset_dir):
                os.makedirs(dataset_dir)
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to create dataset directory: {str(e)}")
            return
        
        # Count exported files for status update
        exported_images = 0
        exported_tags = 0
        
        # Get source images folder
        source_folder = os.path.dirname(self.images[0])
        
        # Export all images and tag files
        for image_path in self.images:
            try:
                # Get file name
                filename = os.path.basename(image_path)
                file_name, file_ext = os.path.splitext(filename)
                
                # Copy image file
                shutil.copy2(image_path, os.path.join(dataset_dir, filename))
                exported_images += 1
                
                # Check for tag file
                tag_file = os.path.join(source_folder, f"{file_name}.txt")
                if os.path.exists(tag_file):
                    shutil.copy2(tag_file, os.path.join(dataset_dir, f"{file_name}.txt"))
                    exported_tags += 1
            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting {filename}: {str(e)}")
                
        # When resetting the UI after clearing workspace
        if messagebox.askyesno("Clear Workspace", 
                             f"Export complete: {exported_images} images and {exported_tags} tag files exported.\n\nClear current workspace?"):
            try:
                # Clear all files from the images folder
                for file_path in os.listdir(source_folder):
                    full_path = os.path.join(source_folder, file_path)
                    if os.path.isfile(full_path) and not file_path == '.gitkeep':
                        os.remove(full_path)
                
                # Reset the UI
                self.images = []
                self.current_image_index = 0
                self.current_image_path = None
                self.tag_var.set("")
                self.image_label.config(image=None)
                self.filename_var.set("")
                self.status_var.set("Workspace cleared. Export complete.")
                
                # Restore window dimensions 
                self.master.geometry(f"{current_width}x{current_height}")
            except Exception as e:
                messagebox.showerror("Clear Error", f"Error clearing workspace: {str(e)}")
        else:
            self.status_var.set(f"Exported {exported_images} images and {exported_tags} tag files")
            
        # Ensure buttons remain visible by maintaining window size
        self.master.geometry(f"{current_width}x{current_height}")

    def tag_folder(self):
        """Apply the auto-tag field tags to all images in a selected folder without importing them."""
        # Get the tag from the auto-tag field
        tag = self.autotag_field.tag_var.get().strip()
        
        if not tag:
            messagebox.showinfo("Tag Folder", "Please enter a tag in the Auto-Tag field first.")
            return
            
        # Ask user to select a folder
        folder_path = filedialog.askdirectory(title="Select Folder to Tag")
        
        if not folder_path:
            return  # User cancelled
            
        # Get list of valid image extensions
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        
        # Count for status update
        tagged_count = 0
        already_tagged = 0
        
        # Process all files in the folder
        for filename in os.listdir(folder_path):
            # Skip directories and non-image files
            file_path = os.path.join(folder_path, filename)
            if os.path.isdir(file_path):
                continue
                
            # Check if it's an image
            file_name, file_ext = os.path.splitext(filename)
            if file_ext.lower() not in valid_extensions:
                continue
                
            # Check for existing tag file
            tag_file_path = os.path.join(folder_path, f"{file_name}.txt")
            
            try:
                existing_tags = ""
                # Read existing tags if the file exists
                if os.path.exists(tag_file_path):
                    with open(tag_file_path, 'r', encoding='utf-8') as f:
                        existing_tags = f.read().strip()
                        
                # Process the tags
                tags_list = [t.strip() for t in existing_tags.split(',') if t.strip()]
                
                # Skip if tag already exists
                if tag in tags_list:
                    already_tagged += 1
                    continue
                    
                # Add the new tag and save
                tags_list.append(tag)
                new_tags = ', '.join(tags_list)
                
                # Write updated tags
                with open(tag_file_path, 'w', encoding='utf-8') as f:
                    f.write(new_tags)
                    
                tagged_count += 1
                    
            except Exception as e:
                messagebox.showerror("Tag Error", f"Error tagging {filename}: {str(e)}")
        
        # Show results
        total_images = tagged_count + already_tagged
        result_message = f"Tagged {tagged_count} images with '{tag}'\n"
        if already_tagged > 0:
            result_message += f"{already_tagged} images already had this tag"
            
        if total_images == 0:
            result_message = f"No images found in the selected folder."
            
        messagebox.showinfo("Tag Folder Results", result_message)
        self.status_var.set(f"Tagged {tagged_count} external images with '{tag}'")

    def clear_folder(self):
        """Clear all images and tags from the images folder."""
        if not self.images:
            messagebox.showinfo("Clear Folder", "No images to clear.")
            return
            
        # Strong warning with recommendation to export first
        if not messagebox.askokcancel("Warning", 
                                    "This will delete ALL images and tags from your workspace.\n\n"
                                    "It is STRONGLY RECOMMENDED to export your dataset first!\n\n"
                                    "Continue with deletion?",
                                    icon="warning"):
            return
            
        # Double-check with a second confirmation
        if not messagebox.askyesno("Confirm Deletion", 
                                 "Are you absolutely sure? This cannot be undone.",
                                 icon="warning"):
            return
        
        # Store current window dimensions
        current_width = self.master.winfo_width()
        current_height = self.master.winfo_height()
        
        # Get source images folder
        source_folder = os.path.dirname(self.images[0])
        
        # Count deleted files
        deleted_count = 0
        
        try:
            # Clear all files from the images folder
            for file_path in os.listdir(source_folder):
                full_path = os.path.join(source_folder, file_path)
                if os.path.isfile(full_path) and not file_path == '.gitkeep':
                    os.remove(full_path)
                    deleted_count += 1
            
            # Reset the UI
            self.images = []
            self.current_image_index = 0
            self.current_image_path = None
            self.tag_var.set("")
            
            # Show app icon instead of empty space
            self.show_app_icon()
            
            # Clear PNG info area
            self.png_info_text.config(state=tk.NORMAL)
            self.png_info_text.delete(1.0, tk.END)
            self.png_info_text.insert(tk.END, "No image loaded - PNG metadata will appear here")
            self.png_info_text.config(state=tk.DISABLED)
            
            self.status_var.set(f"Workspace cleared. {deleted_count} files deleted.")
            
            # Restore window dimensions
            self.master.geometry(f"{current_width}x{current_height}")
        except Exception as e:
            messagebox.showerror("Clear Error", f"Error clearing workspace: {str(e)}")