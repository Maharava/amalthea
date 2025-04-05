import os
from glob import glob

class ImageLoader:
    def __init__(self, image_folder=None):
        # Default to 'images' folder in project root if no folder is specified
        if image_folder is None:
            # Get the directory where the script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up one level to get to project root, then to images folder
            project_root = os.path.dirname(script_dir)
            self.image_folder = os.path.join(project_root, "images")
        else:
            self.image_folder = image_folder

    def load_images(self):
        """
        Load all image files from the specified folder.
        Returns a list of full paths to the image files.
        """
        image_extensions = ('*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp')
        images = []
        
        # Ensure the image directory exists
        if not os.path.exists(self.image_folder):
            try:
                os.makedirs(self.image_folder)
                print(f"Created image directory: {self.image_folder}")
            except Exception as e:
                print(f"Error creating image directory: {e}")
                return images
        
        # Load all images with supported extensions
        for ext in image_extensions:
            image_paths = glob(os.path.join(self.image_folder, ext))
            images.extend(image_paths)
            
            # Also check for uppercase extensions
            image_paths = glob(os.path.join(self.image_folder, ext.upper()))
            images.extend(image_paths)
        
        # Sort images alphabetically for consistent navigation
        images.sort()
        
        return images

    def get_next_image(self, current_image_path, images):
        """
        Get the next image in the list after the current one.
        Returns the path to the next image.
        """
        if not images:
            return None
            
        try:
            current_index = images.index(current_image_path)
            next_index = (current_index + 1) % len(images)
            return images[next_index]
        except ValueError:
            # If current image is not in the list, return the first image
            return images[0] if images else None

    def get_prev_image(self, current_image_path, images):
        """
        Get the previous image in the list before the current one.
        Returns the path to the previous image.
        """
        if not images:
            return None
            
        try:
            current_index = images.index(current_image_path)
            prev_index = (current_index - 1) % len(images)
            return images[prev_index]
        except ValueError:
            # If current image is not in the list, return the last image
            return images[-1] if images else None