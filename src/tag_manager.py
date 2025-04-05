import os

class TagManager:
    """
    Manages saving and loading tags for images.
    Tags are stored in text files with the same name as the image but with a .txt extension.
    """
    
    def __init__(self):
        """Initialize the TagManager."""
        pass
        
    def save_tags(self, image_path, tags):
        """
        Save tags for an image to a corresponding text file.
        
        Args:
            image_path (str): Full path to the image file
            tags (str): String containing tags, space or comma separated
            
        Returns:
            bool: True if tags were saved successfully, False otherwise
        """
        try:
            # Get the directory and filename without extension
            dir_name = os.path.dirname(image_path)
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            
            # Create the path for the tag file
            tag_file_path = os.path.join(dir_name, f"{file_name}.txt")
            
            # Save the tags
            with open(tag_file_path, 'w', encoding='utf-8') as tag_file:
                tag_file.write(tags)
                
            return True
            
        except Exception as e:
            print(f"Error saving tags: {str(e)}")
            return False
            
    def load_tags(self, image_path):
        """
        Load tags for an image from a corresponding text file.
        
        Args:
            image_path (str): Full path to the image file
            
        Returns:
            str: String containing the tags, or empty string if no tags found
        """
        try:
            # Get the directory and filename without extension
            dir_name = os.path.dirname(image_path)
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            
            # Create the path for the tag file
            tag_file_path = os.path.join(dir_name, f"{file_name}.txt")
            
            # Check if the tag file exists
            if not os.path.exists(tag_file_path):
                return ""
                
            # Load the tags
            with open(tag_file_path, 'r', encoding='utf-8') as tag_file:
                return tag_file.read()
                
        except Exception as e:
            print(f"Error loading tags: {str(e)}")
            return ""
            
    def delete_tags(self, image_path):
        """
        Delete tags for an image by removing the corresponding text file.
        
        Args:
            image_path (str): Full path to the image file
            
        Returns:
            bool: True if tags were deleted successfully, False otherwise
        """
        try:
            # Get the directory and filename without extension
            dir_name = os.path.dirname(image_path)
            base_name = os.path.basename(image_path)
            file_name, _ = os.path.splitext(base_name)
            
            # Create the path for the tag file
            tag_file_path = os.path.join(dir_name, f"{file_name}.txt")
            
            # Check if the tag file exists
            if not os.path.exists(tag_file_path):
                return True
                
            # Delete the tag file
            os.remove(tag_file_path)
            return True
            
        except Exception as e:
            print(f"Error deleting tags: {str(e)}")
            return False