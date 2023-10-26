# Import necessary modules for image validation.
from PIL import Image
from django.core.exceptions import ValidationError
import os


# Custom validation function to check the size of an image.
def validate_icon_image_size(image):
    # Check if an image file is provided.
    if image:
        # Open the image using PIL (Pillow).
        with Image.open(image) as img:
            # Check if the image dimensions exceed 70x70 pixels.
            if img.width > 70 or img.height > 70:
                # Raise a ValidationError if the image size is too large.
                raise ValidationError(
                    f"the maximum allowed dimensions for the image are 70x70 - size of image you uploaded: {img.size}"
                )


# Custom validation function to check the file extension of an image.
def validate_image_file_extension(value):
    # Extract the file extension from the provided file's name.
    ext = os.path.splitext(value.name)[1]
    # Define a list of valid image file extensions (lowercase).
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    # Check if the extracted extension is not in the list of valid extensions.
    if not ext.lower() in valid_extensions:
        # Raise a ValidationError if the extension is not supported.
        raise ValidationError("Unsupported file extension")
